"""Run ai-brand-visibility-tracker on Apify and print the results. pip install apify-client"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run_input = {'helloWorld': 123}
run = client.actor("kamerozkan/ai-brand-visibility-tracker").call(run_input=run_input)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
