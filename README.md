# AI Brand Visibility & GEO Rank Tracker (ChatGPT, Perplexity, Gemini & Claude)

[![Run on Apify](https://apify.com/actor-badge?actor=kamerozkan/ai-brand-visibility-tracker)](https://apify.com/kamerozkan/ai-brand-visibility-tracker)
[![Pricing](https://img.shields.io/badge/Pricing-Pay--Per--Event%20($0.04)-blue)](https://apify.com/kamerozkan/ai-brand-visibility-tracker)
[![Category](https://img.shields.io/badge/Discipline-Generative%20Engine%20Optimization%20(GEO)-purple)](https://apify.com/kamerozkan/ai-brand-visibility-tracker)
[![Engines](https://img.shields.io/badge/Supported%20Engines-Perplexity%20|%20ChatGPT%20|%20Gemini%20|%20Claude-success)](https://apify.com/kamerozkan/ai-brand-visibility-tracker)

Track how major AI answer engines (**Perplexity, ChatGPT, Google Gemini, and Claude**) recommend your brand, software, or e-commerce products in response to real buyer queries.

Audit brand presence, calculate **Share of Voice (SOV)** against competitors, track **ranking prominence (#1, #2, #3)**, classify **recommendation sentiment**, and uncover the **exact citation URLs and media domains** the AI uses to source its answers.

---

## Why Generative Engine Optimization (GEO)?

Buyers no longer just browse Google search links: they ask AI engines: *"What is the best CRM for B2B startups?"*, *"Top alternatives to Salesforce"*, or *"Recommend accounting software for small businesses"*.

If your brand is not recommended in these AI answers, you are losing high-intent buyers to competitors before they ever visit your website.

| Feature | This Actor (kamerozkan) | Legacy AI Rank Trackers | Enterprise GEO SaaS ($499+/mo) |
| :--- | :--- | :--- | :--- |
| **Pricing Model** | **$0.04 / check (Pay-Per-Event)** | $0.08 / check (2x higher) | $299 - $999 / mo fixed lock-in |
| **Citation Intelligence**| **Full URL list + Root Domains** | Basic text check only | Gated behind enterprise tier |
| **Share of Voice (SOV)**| **Automated % vs Competitors** | Manual calculation | Included |
| **Supported Engines** | **Perplexity, ChatGPT, Gemini, Claude** | Usually 1 or 2 engines | 3 engines |
| **Setup & Maintenance** | **Zero Setup (Run with 1 Click)** | Requires complex setup | Sales call required |
| **BYOK Support** | **Yes (Use your own keys or default)**| Key required | Proprietary black box |

---

## Core Use Cases

- **GEO (Generative Engine Optimization) Audits:** Measure your brand's AI search visibility before and after PR releases, product updates, and content marketing campaigns.
- **Citation & PR Backlink Strategy:** Discover which third-party review sites (G2, Capterra, Forbes, TechRadar) AI engines cite most frequently when answering category queries. Focus your PR and backlink acquisition on these exact domains.
- **Competitor Share of Voice (SOV) Benchmarking:** Track how often competitors (e.g. Jira, Asana, Monday) are co-recommended alongside your brand and calculate your market share percentage.
- **Brand Sentiment & Risk Monitoring:** Catch negative AI summaries, hallucinated drawbacks, or outdated pricing claims before prospective buyers see them.
- **Agency Client Reporting:** Generate weekly, automated AI visibility and prominence score reports for marketing and enterprise clients.

---

## Key Metrics Extracted per Check

Every run generates structured records containing:

1. **`isMentioned` (Boolean):** Indicates whether your brand name or any alias appeared in the AI response.
2. **`rank` (Integer):** 1-based recommendation position (e.g. `1` if you are the #1 recommended tool).
3. **`prominenceScore` (0 to 100):** Weighted score reflecting position, list order, and context prominence.
4. **`shareOfVoicePercentage` (Float):** Ratio of your brand mentions versus configured competitors (`Brand / (Brand + Competitors) * 100`).
5. **`sentiment` & `sentimentScore`:** Automatic classification (`POSITIVE`, `NEUTRAL`, `NEGATIVE`) with numeric confidence score.
6. **`competitorsMentioned` & `competitorRanks`:** Full list of competitors detected in the answer and their relative rank.
7. **`isBrandCited` (Boolean):** Flags whether the AI directly linked to your brand's primary domain.
8. **`citations` & `citedDomains`:** Complete array of cited source URLs and deduplicated root domains (e.g. `["forbes.com", "g2.com", "techradar.com"]`).
9. **`recommendationSnippet`:** Extracted contextual excerpt describing how the AI characterized your product.

---

## Input Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `brandName` | String | **Yes** | `"Linear"` | Primary brand, product, or company name to monitor. |
| `brandDomain` | String | No | `"linear.app"` | Primary website domain to track direct citation backlinks. |
| `brandAliases` | Array of Strings | No | `["Linear App"]` | Alternative names or spelling variations. |
| `competitors` | Array of Strings | No | `["Jira", "Asana"]` | Competitor brand names to benchmark against for SOV. |
| `industry` | String | No | `"project management"` | Product category used for automated prompt generation. |
| `platforms` | Array of Strings | No | `["perplexity", "chatgpt", "gemini"]` | AI engines to query: Perplexity, ChatGPT, Gemini, Claude. |
| `customQueries` | Array of Strings | No | `[]` | Specific buyer prompts or search queries to test. |
| `queryTemplates` | Array of Strings | No | `["best_tools", ...]` | Automated prompt categories: `best_tools`, `alternatives`, `recommendations`. |
| `maxQueriesPerPlatform` | Integer | No | `3` | Maximum queries to run per engine (1 to 20). |
| `openaiApiKey` | String (Secret) | No | `null` | Optional BYOK OpenAI API key. |
| `perplexityApiKey` | String (Secret) | No | `null` | Optional BYOK Perplexity Sonar API key. |
| `geminiApiKey` | String (Secret) | No | `null` | Optional BYOK Google Gemini API key. |
| `anthropicApiKey` | String (Secret) | No | `null` | Optional BYOK Anthropic Claude API key. |

---

## Example JSON Output

```json
{
  "brandName": "Linear",
  "brandDomain": "linear.app",
  "platform": "perplexity",
  "query": "What are the best project management software for startups in 2026?",
  "timestamp": "2026-10-06T20:45:00+00:00",
  "isMentioned": true,
  "rank": 1,
  "mentionCount": 2,
  "prominenceScore": 100,
  "shareOfVoicePercentage": 50.0,
  "sentiment": "POSITIVE",
  "sentimentScore": 0.95,
  "isBrandCited": true,
  "competitorsMentioned": ["Jira", "Asana"],
  "competitorRanks": {
    "Jira": 2,
    "Asana": 3
  },
  "citations": [
    "https://linear.app/features",
    "https://www.g2.com/categories/project-management",
    "https://techradar.com/best-project-management"
  ],
  "citedDomains": [
    "g2.com",
    "linear.app",
    "techradar.com"
  ],
  "recommendationSnippet": "Linear is widely considered the best and fastest issue tracker for software startups. Its keyboard-first design, speed, and Git integrations make it a standout choice...",
  "aiResponseExcerpt": "Based on real-time web intelligence for 'best project management software for startups'..."
}
```

---

## Code Examples

### Python (apify-client)

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_API_TOKEN")

run_input = {
    "brandName": "HubSpot",
    "brandDomain": "hubspot.com",
    "competitors": ["Salesforce", "Zoho CRM", "Pipedrive"],
    "industry": "CRM software for small business",
    "platforms": ["perplexity", "chatgpt", "gemini"],
    "customQueries": [
        "What is the best CRM software for small businesses in 2026?",
        "Top alternatives to Salesforce for growing teams"
    ],
}

# Run the audit on Apify
run = client.actor("kamerozkan/ai-brand-visibility-tracker").call(run_input=run_input)

# Print results
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"[{item['platform'].upper()}] Mentioned: {item['isMentioned']} | Rank: #{item['rank']} | SOV: {item['shareOfVoicePercentage']}%")
    print(f"  Cited Domains: {', '.join(item['citedDomains'][:4])}")
```

### JavaScript / Node.js (apify-client)

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({
    token: 'YOUR_APIFY_API_TOKEN',
});

const runInput = {
    brandName: 'Stripe',
    brandDomain: 'stripe.com',
    competitors: ['Adyen', 'PayPal', 'Square'],
    platforms: ['perplexity', 'chatgpt'],
    customQueries: ['Best payment gateways for global SaaS platforms in 2026'],
};

const run = await client.actor('kamerozkan/ai-brand-visibility-tracker').call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();

console.log('GEO Audit Report:', items);
```

### cURL

```bash
curl --request POST \
  --url "https://api.apify.com/v2/acts/kamerozkan~ai-brand-visibility-tracker/runs?token=YOUR_APIFY_API_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "brandName": "Shopify",
    "brandDomain": "shopify.com",
    "competitors": ["WooCommerce", "BigCommerce"],
    "platforms": ["perplexity", "chatgpt"],
    "industry": "ecommerce platform"
  }'
```

---

## Pricing Details

This Actor operates under **Pay-Per-Event (PPE)**:
- **Per Brand Query Checked ($0.04):** Charged per individual brand × query × platform check.
- 50% cheaper than legacy AI brand monitoring scrapers ($0.08 / check).
- Compute usage is fully included in the event fee. Set spending limits in your Apify Console to keep your runs within budget.
