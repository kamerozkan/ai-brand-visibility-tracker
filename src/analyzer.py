from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse


POSITIVE_KEYWORDS = {
    "best", "top", "leading", "popular", "excellent", "recommended", "powerful",
    "intuitive", "fast", "great", "favorite", "efficient", "modern", "standout",
    "superior", "trusted", "preferred", "clean", "reliable", "seamless", "innovative"
}

NEGATIVE_KEYWORDS = {
    "expensive", "slow", "clunky", "steep learning curve", "lacks", "limited",
    "buggy", "outdated", "complex", "confusing", "poor", "frustrating", "drawback",
    "complaint", "hard to use"
}


def extract_domain(url: str) -> str:
    if not url:
        return ""
    try:
        raw = url.strip()
        if "://" not in raw:
            raw = "https://" + raw
        parsed = urlparse(raw)
        netloc = parsed.netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc
    except Exception:
        return ""


def clean_brand(b: str) -> str:
    return b.strip()


class VisibilityAnalyzer:
    @staticmethod
    def analyze(
        text: str,
        citations: list[str],
        brand_name: str,
        brand_domain: str | None = None,
        brand_aliases: list[str] | None = None,
        competitors: list[str] | None = None,
    ) -> dict[str, Any]:
        """Analyze an AI response for brand presence, GEO ranking, sentiment, and citations."""
        aliases = [clean_brand(brand_name)] + [clean_brand(a) for a in (brand_aliases or []) if a]
        comp_list = [clean_brand(c) for c in (competitors or []) if c]

        text_lower = text.lower()

        # 1. Check brand mentions
        brand_match_spans: list[tuple[int, int]] = []
        for alias in aliases:
            pattern = re.compile(rf"\b{re.escape(alias.lower())}\b")
            for m in pattern.finditer(text_lower):
                brand_match_spans.append(m.span())

        is_mentioned = len(brand_match_spans) > 0
        mention_count = len(brand_match_spans)

        # 2. Check competitor mentions
        comp_mentions: dict[str, int] = {}
        comp_spans: dict[str, list[tuple[int, int]]] = {}
        for comp in comp_list:
            c_pattern = re.compile(rf"\b{re.escape(comp.lower())}\b")
            spans = [m.span() for m in c_pattern.finditer(text_lower)]
            if spans:
                comp_mentions[comp] = len(spans)
                comp_spans[comp] = spans

        competitors_mentioned = list(comp_mentions.keys())

        # 3. Detect Ordered List Ranking (1. Brand, 2. Brand...)
        # Match lines like: "1. **Brand**", "1. Brand:", "#1 Brand", "* **Brand**"
        list_items = re.findall(
            r"(?:^|\n)\s*(?:(?:\d+\.|\*|-|#\d+)\s+)?(?:\*\*)?([A-Za-z0-9\.\s\-_/]+?)(?:\*\*)?(?:\s*[-:\u2014]|\s+\()",
            text,
            flags=re.MULTILINE,
        )

        detected_order: list[str] = []
        for raw_item in list_items:
            clean_item = raw_item.strip().lower()
            if len(clean_item) < 2 or len(clean_item) > 40:
                continue
            detected_order.append(clean_item)

        # Compute rank for brand
        brand_rank: int | None = None
        for idx, item in enumerate(detected_order, start=1):
            if any(alias.lower() in item for alias in aliases):
                brand_rank = idx
                break

        # Fallback ranking by first character appearance if list parsing was ambiguous
        if is_mentioned and brand_rank is None:
            first_brand_idx = min(s[0] for s in brand_match_spans)
            # Compare first appearance against competitor appearances
            all_first_spans = [(first_brand_idx, "brand")]
            for comp, spans in comp_spans.items():
                all_first_spans.append((min(s[0] for s in spans), comp))
            all_first_spans.sort(key=lambda x: x[0])
            for idx, (_, entity) in enumerate(all_first_spans, start=1):
                if entity == "brand":
                    brand_rank = idx
                    break

        # Compute competitor ranks
        competitor_ranks: dict[str, int] = {}
        for comp in competitors_mentioned:
            c_rank = None
            for idx, item in enumerate(detected_order, start=1):
                if comp.lower() in item:
                    c_rank = idx
                    break
            if c_rank is None and comp in comp_spans:
                comp_first_idx = min(s[0] for s in comp_spans[comp])
                all_spans = [(comp_first_idx, comp)]
                if is_mentioned:
                    all_spans.append((min(s[0] for s in brand_match_spans), "brand"))
                for other_c, spans in comp_spans.items():
                    if other_c != comp:
                        all_spans.append((min(s[0] for s in spans), other_c))
                all_spans.sort(key=lambda x: x[0])
                for idx, (_, entity) in enumerate(all_spans, start=1):
                    if entity == comp:
                        c_rank = idx
                        break
            competitor_ranks[comp] = c_rank or 99

        # 4. Share of Voice (SOV)
        total_market_mentions = mention_count + sum(comp_mentions.values())
        share_of_voice_pct = (
            round((mention_count / total_market_mentions) * 100, 1)
            if total_market_mentions > 0
            else 0.0
        )

        # 5. Prominence Score (0 to 100)
        if not is_mentioned:
            prominence_score = 0
        elif brand_rank == 1:
            prominence_score = 100
        elif brand_rank == 2:
            prominence_score = 85
        elif brand_rank == 3:
            prominence_score = 75
        elif brand_rank and brand_rank <= 5:
            prominence_score = 60
        elif brand_rank and brand_rank <= 10:
            prominence_score = 45
        else:
            prominence_score = 30

        # 6. Recommendation Snippet & Sentiment
        snippet = ""
        sentiment = "NEUTRAL"
        sentiment_score = 0.5

        if is_mentioned:
            first_span = min(brand_match_spans, key=lambda s: s[0])
            start_ctx = max(0, first_span[0] - 120)
            end_ctx = min(len(text), first_span[1] + 250)
            ctx = text[start_ctx:end_ctx].strip()
            # Clean up snippet boundaries
            snippet = re.sub(r"\s+", " ", ctx)

            # Sentiment calculation on context
            ctx_lower = ctx.lower()
            pos_hits = sum(1 for w in POSITIVE_KEYWORDS if re.search(rf"\b{re.escape(w)}\b", ctx_lower))
            neg_hits = sum(1 for w in NEGATIVE_KEYWORDS if re.search(rf"\b{re.escape(w)}\b", ctx_lower))

            if pos_hits > neg_hits:
                sentiment = "POSITIVE"
                sentiment_score = min(0.95, round(0.6 + (pos_hits * 0.1), 2))
            elif neg_hits > pos_hits:
                sentiment = "NEGATIVE"
                sentiment_score = max(0.1, round(0.4 - (neg_hits * 0.1), 2))
            else:
                sentiment = "NEUTRAL"
                sentiment_score = 0.5

        # 7. Citation Intelligence
        cited_domains_set: set[str] = set()
        clean_citations: list[str] = []
        is_brand_cited = False
        target_domain_clean = extract_domain(brand_domain) if brand_domain else ""

        for u in citations:
            if not u or not isinstance(u, str):
                continue
            clean_u = u.strip()
            clean_citations.append(clean_u)
            dom = extract_domain(clean_u)
            if dom:
                cited_domains_set.add(dom)
                if target_domain_clean and (target_domain_clean in dom or dom in target_domain_clean):
                    is_brand_cited = True

        # Check in text if domain was explicitly cited in markdown links [text](url)
        markdown_links = re.findall(r"\[([^\]]+)\]\((https?://[^\)]+)\)", text)
        for _, link in markdown_links:
            clean_citations.append(link)
            dom = extract_domain(link)
            if dom:
                cited_domains_set.add(dom)
                if target_domain_clean and (target_domain_clean in dom or dom in target_domain_clean):
                    is_brand_cited = True

        cited_domains = sorted(list(cited_domains_set))

        return {
            "isMentioned": is_mentioned,
            "rank": brand_rank,
            "mentionCount": mention_count,
            "prominenceScore": prominence_score,
            "shareOfVoicePercentage": share_of_voice_pct,
            "sentiment": sentiment,
            "sentimentScore": sentiment_score,
            "competitorsMentioned": competitors_mentioned,
            "competitorRanks": competitor_ranks,
            "isBrandCited": is_brand_cited,
            "citations": clean_citations[:30],
            "citedDomains": cited_domains[:20],
            "recommendationSnippet": snippet,
        }
