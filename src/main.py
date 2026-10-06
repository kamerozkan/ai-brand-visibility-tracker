from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from apify import Actor
from .analyzer import VisibilityAnalyzer
from .engines import AIEngineClient


class ChargeLimitReached(Exception):
    pass


async def main() -> None:
    async with Actor:
        inp: dict[str, Any] = await Actor.get_input() or {}

        brand_name = str(inp.get("brandName") or "").strip()
        brand_domain = str(inp.get("brandDomain") or "").strip() or None
        brand_aliases = [str(a).strip() for a in (inp.get("brandAliases") or []) if str(a).strip()]
        competitors = [str(c).strip() for c in (inp.get("competitors") or []) if str(c).strip()]
        industry = str(inp.get("industry") or "").strip()

        # Fallback to demo mode if no brand specified
        if not brand_name:
            brand_name = "Linear"
            brand_domain = "linear.app"
            competitors = ["Jira", "Asana", "Monday.com", "ClickUp"]
            industry = "project management software"
            Actor.log.info("No brandName provided. Running in Demo Mode for 'Linear'.")

        platforms = [str(p).lower().strip() for p in (inp.get("platforms") or ["perplexity", "chatgpt", "gemini"])]
        max_queries = max(1, min(int(inp.get("maxQueriesPerPlatform") or 3), 20))

        # Build list of queries
        queries: list[str] = []
        raw_custom = inp.get("customQueries") or inp.get("queries") or []
        for q in raw_custom:
            clean_q = str(q).strip()
            if clean_q and clean_q not in queries:
                queries.append(clean_q)

        # Generate template queries if explicitly requested or if no custom queries were provided
        user_specified_templates = inp.get("queryTemplates")
        if user_specified_templates is not None:
            templates = user_specified_templates
        elif not queries:
            templates = ["best_tools", "alternatives", "recommendations"]
        else:
            templates = []

        ind_label = industry or "software"
        if "best_tools" in templates:
            q_best = f"What are the best {ind_label} tools in 2026?"
            if q_best not in queries:
                queries.append(q_best)
        if "alternatives" in templates and competitors:
            q_alt = f"Top alternatives to {competitors[0]} for {ind_label}"
            if q_alt not in queries:
                queries.append(q_alt)
        if "recommendations" in templates:
            q_rec = f"Recommend top {ind_label} solutions for modern teams"
            if q_rec not in queries:
                queries.append(q_rec)

        target_queries = queries[:max_queries]

        engine_client = AIEngineClient(
            openai_key=inp.get("openaiApiKey"),
            perplexity_key=inp.get("perplexityApiKey"),
            gemini_key=inp.get("geminiApiKey"),
            anthropic_key=inp.get("anthropicApiKey"),
            log=Actor.log,
        )

        total_checks = len(platforms) * len(target_queries)
        Actor.log.info(
            f"Starting AI Brand Visibility Tracker: Brand='{brand_name}', "
            f"{len(platforms)} platform(s), {len(target_queries)} query/queries ({total_checks} total checks)"
        )
        await Actor.set_status_message(f"Auditing AI search visibility for {brand_name} across {len(platforms)} engines...")

        pushed_records: list[dict[str, Any]] = []
        stop_processing = False

        for platform in platforms:
            if stop_processing:
                break

            for query in target_queries:
                if stop_processing:
                    break

                # Charge Pay-per-event for brand-query-checked
                try:
                    await Actor.charge(event_name="brand-query-checked")
                except Exception as err:
                    err_msg = str(err).lower()
                    if "budget" in err_msg or "limit" in err_msg or "charge" in err_msg:
                        Actor.log.warning(f"Spending budget reached: {err}. Halting audit.")
                        stop_processing = True
                        break
                    Actor.log.debug(f"Non-fatal charge notice: {err}")

                Actor.log.info(f"Querying [{platform.upper()}]: \"{query}\"")

                # Fetch AI response
                try:
                    if platform == "perplexity":
                        text, citations = await engine_client.query_perplexity(query)
                    elif platform == "chatgpt":
                        text, citations = await engine_client.query_chatgpt(query)
                    elif platform == "gemini":
                        text, citations = await engine_client.query_gemini(query)
                    elif platform == "claude":
                        text, citations = await engine_client.query_claude(query)
                    else:
                        text, citations = await engine_client.query_perplexity(query)
                except Exception as err:
                    Actor.log.warning(f"Error querying {platform} for '{query}': {err}")
                    text, citations = f"Unable to fetch response for {query}", []

                # Analyze visibility and citations
                analysis = VisibilityAnalyzer.analyze(
                    text=text,
                    citations=citations,
                    brand_name=brand_name,
                    brand_domain=brand_domain,
                    brand_aliases=brand_aliases,
                    competitors=competitors,
                )

                record: dict[str, Any] = {
                    "brandName": brand_name,
                    "brandDomain": brand_domain,
                    "platform": platform,
                    "query": query,
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    **analysis,
                    "aiResponseExcerpt": text[:1500],
                }

                await Actor.push_data(record)
                pushed_records.append(record)

        # Aggregate Run Summary
        mentioned_count = sum(1 for r in pushed_records if r.get("isMentioned"))
        ranks = [r["rank"] for r in pushed_records if r.get("rank")]
        avg_rank = round(sum(ranks) / len(ranks), 1) if ranks else None
        sovs = [r.get("shareOfVoicePercentage", 0) for r in pushed_records]
        avg_sov = round(sum(sovs) / len(sovs), 1) if sovs else 0.0

        all_cited_domains: dict[str, int] = {}
        for r in pushed_records:
            for d in r.get("citedDomains", []):
                all_cited_domains[d] = all_cited_domains.get(d, 0) + 1

        top_domains = sorted(all_cited_domains.items(), key=lambda x: x[1], reverse=True)[:10]

        summary = {
            "brandName": brand_name,
            "totalChecks": len(pushed_records),
            "mentionCount": mentioned_count,
            "mentionRatePercentage": round((mentioned_count / len(pushed_records)) * 100, 1) if pushed_records else 0,
            "averageRank": avg_rank,
            "averageShareOfVoicePercentage": avg_sov,
            "topCitedDomains": [{"domain": d, "citationsCount": c} for d, c in top_domains],
        }
        await Actor.set_value("RUN_SUMMARY", summary)

        msg = (
            f"Completed: {len(pushed_records)} checks, Mention Rate: {summary['mentionRatePercentage']}%, "
            f"Avg SOV: {summary['averageShareOfVoicePercentage']}%"
        )
        Actor.log.info(msg)
        await Actor.set_status_message(msg)


if __name__ == "__main__":
    asyncio.run(main())
