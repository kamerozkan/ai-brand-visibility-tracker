# AI Brand Visibility & GEO Rank Tracker

Monitor brand mentions, Share of Voice (SOV), competitor recommendations, sentiment, and citation sources across AI search engines (Perplexity, ChatGPT, Gemini, Claude). Uses your own API keys. Essential for Generative Engine Optimization (GEO).

**[Run it on Apify Store](https://apify.com/kamerozkan/ai-brand-visibility-tracker)**: no servers, no proxies to manage, results as JSON, CSV or Excel, or straight into your app through the API.

## Why use it

- Runs in the cloud on [Apify](https://apify.com/kamerozkan/ai-brand-visibility-tracker); start it from the browser, the API, a schedule, or tools like Make, n8n and Zapier.
- Pay only for results. The current price and plan discounts are always on the [Store page](https://apify.com/kamerozkan/ai-brand-visibility-tracker).
- Cap the cost of any run with the maximum cost per run setting.

## Quick start

1. Open the [Actor page](https://apify.com/kamerozkan/ai-brand-visibility-tracker) and click **Try for free**.
2. Paste an input like the one below and click **Start**.
3. Download the dataset or read it over the API.

```json
{
  "helloWorld": 123
}
```

## Use it from code

Python ([examples/python_example.py](examples/python_example.py)), Node.js ([examples/node_example.js](examples/node_example.js)) and cURL ([examples/curl.sh](examples/curl.sh)) examples are in the `examples` folder. All of them need an [Apify API token](https://console.apify.com/settings/integrations).

## Use in n8n & Make

- **n8n:** Import [integrations/n8n-workflow.json](integrations/n8n-workflow.json) directly into your n8n workspace, set your `APIFY_TOKEN` environment variable (or Bearer token header), and click **Execute Workflow**.
- **Make / Zapier:** Call the Apify **Run an Actor** module with Actor ID `kamerozkan/ai-brand-visibility-tracker` and the JSON input above, or POST to `https://api.apify.com/v2/acts/kamerozkan~ai-brand-visibility-tracker/run-sync-get-dataset-items`.

## Use with AI Agents (Apify MCP)

This Actor works with Claude Desktop, Cursor, Windsurf and any MCP-compatible AI agent through the official [Apify MCP Server](https://mcp.apify.com). Copy [integrations/mcp-config.json](integrations/mcp-config.json) into your MCP client configuration and replace `YOUR_APIFY_TOKEN` with your token.

## Sample output

Real rows from a recent run, with any contact details masked. Full sample: [sample-output.json](sample-output.json).

```json
[
  {
    "brandName": "Linear",
    "brandDomain": "linear.app",
    "platform": "web-search",
    "query": "What are the best project management software for engineering startups in 2026?",
    "timestamp": "2026-11-23T10:22:50+00:00",
    "answerSource": "none",
    "isAiAnswer": false,
    "isMentioned": false,
    "rank": null,
    "mentionCount": 0,
    "prominenceScore": 0,
    "shareOfVoicePercentage": 0,
    "sentiment": "NEUTRAL",
    "sentimentScore": 0.5,
    "competitorsMentioned": [],
    "competitorRanks": {},
    "isBrandCited": false,
    "citations": [],
    "citedDomains": [],
    "recommendationSnippet": "",
    "aiResponseExcerpt": null,
    "webSearchExcerpt": null,
    "note": "Not an AI answer. No API key was given for perplexity, chatgpt, gemini, so this row shows DuckDuckGo search results and is free. Add your own API key to get real answers from that engine. The web search also failed: DuckDuckGo answered HTTP 202"
  }
]
```

## Support

Found a problem or need a field? Open an issue on the [Actor's Issues tab](https://apify.com/kamerozkan/ai-brand-visibility-tracker/issues) and include your run link.

---
This repository holds usage examples and sample data. The Actor itself runs on Apify.
