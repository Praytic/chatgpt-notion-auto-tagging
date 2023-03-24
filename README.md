# ChatGPT-Notion-Auto-Tagging

Integration between [ChatGPT](https://chat.openai.com/) and [Notion](https://www.notion.so/). 
The main idea of this repo is to enhance [Notion Clipper plugin](https://www.notion.so/web-clipper)
with auto-tagging based on the web page summary.

**Steps:**

1. User saves URL via [Notion Clipper plugin](https://www.notion.so/web-clipper).
1. Entry is created in the user's Notion database.
1. [Zapier](https://www.notion.so/integrations/zapier-ffdbc66b-ab6b-4366-9ce3-c22dc258b201) webhook (on database entry created) is triggered.
1. [Zapier](https://www.notion.so/integrations/zapier-ffdbc66b-ab6b-4366-9ce3-c22dc258b201) sends webhook payload to the Google function.
1. Google function sends prompts to [ChatGPT](https://chat.openai.com/).
1. [ChatGPT](https://chat.openai.com/) generates tags.
1. Google function updates the database entry with auto-generated tags.

## Getting Started

### Prerequisites

- Python 3.10, `pip`
- A Notion account and API key
- An OpenAI API key
- Google Cloud project with billing account

### Installation

0. Make sure your Notion database has these properties: **Tags** and **Category**. Category is a predefined set of tags, Tags is a dynamic set of tags created for each web page by GPT model. Example:

1. Connect https://cloud.google.com/functions and https://cloud.google.com/build to your project
2. Place you API keys for OpenAI and Notion into https://cloud.google.com/secret-manager
3. Download and setup `gcloud` for you project
4. Run ` gcloud builds submit --config cloudbuild.yaml` to deploy this function to Cloud
5. Install Notion database poller (e.g. [Zapier](https://www.notion.so/integrations/zapier-ffdbc66b-ab6b-4366-9ce3-c22dc258b201)) and connect it to your google function trigger.

