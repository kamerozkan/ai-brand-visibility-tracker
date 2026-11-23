#!/usr/bin/env bash
# Run ai-brand-visibility-tracker synchronously and get the dataset items back. Needs APIFY_TOKEN.
curl -s -X POST "https://api.apify.com/v2/acts/kamerozkan~ai-brand-visibility-tracker/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"helloWorld": 123}'
