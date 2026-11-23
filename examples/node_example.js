// Run ai-brand-visibility-tracker on Apify and print the results. npm install apify-client
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const input = {
  "helloWorld": 123
};
const run = await client.actor('kamerozkan/ai-brand-visibility-tracker').call(input);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
