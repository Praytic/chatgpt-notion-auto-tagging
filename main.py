import os

import openai
from notion_client import Client

# Set up the Notion client
notion = Client(auth=os.environ.get("NOTION_API_KEY"))

# Set up the OpenAI API client
openai.api_key = os.environ.get("OPENAI_API_KEY")


def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=100,
            n=1,
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error from ChatGPT: {e}")
        return None


def choose_tags(options, gem_url):
    prompt_tags = f"Choose the most relevant tags for this webpage {gem_url}. The must use only single-worded tags, abbrevations, common nouns. Use only comma separator to list the tags."
    print("ChatGPT tags prompt:", prompt_tags)

    # Get the response from the ChatGPT API
    chatgpt_answer = get_chatgpt_response(prompt_tags)
    print("ChatGPT selected tags:", chatgpt_answer)

    # Select Notion tags that were suggested by ChatGPT
    tokens = chatgpt_answer.lower().rstrip(" ,.!/").split(", ")

    return [{"name": token} for token in tokens if options]


def choose_categories(options, gem_url):
    categories = [option["name"] for option in options]

    prompt_categories = f"Choose the most relevant tags for this webpage {gem_url} from the following list: {', '.join(categories)}. You are not allowed to use any other tags. Use only comma separator to list the tags."
    print("ChatGPT categories prompt:", prompt_categories)

    # Get the response from the ChatGPT API
    chatgpt_answer = get_chatgpt_response(prompt_categories)
    print("ChatGPT selected categories:", chatgpt_answer)

    # Select Notion categories that were selected by ChatGPT
    tokens = chatgpt_answer.lower().rstrip(" ,.!/").split(", ")
    chat_gpt_options = [option for option in options if option["name"].lower() in tokens]

    return chat_gpt_options


def describe_url(webhook):
    request_json = webhook.get_json()
    print("JSON Payload:", request_json)

    # Validate Notion API key
    if not notion:
        return "Missing Notion API key", 400

    # Validate OpenAI API key
    if not openai.api_key:
        return "Missing OpenAI API key", 400

    # Get the website URL which ChatGPT has to parse
    gem_url = request_json["gem_url"]
    new_page_id = request_json["new_page_id"]

    # Get the new entry's properties
    new_page = notion.pages.retrieve(new_page_id)
    database_id = new_page["parent"]["database_id"]
    database = notion.databases.retrieve(database_id)

    category = database["properties"]["Category"]
    tags = database["properties"]["Tags"]

    chosen_categories = choose_categories(category["multi_select"]["options"], gem_url)
    chosen_tags = choose_tags(tags["multi_select"]["options"], gem_url)

    # Create missing unique tags in the database
    if not tags["multi_select"]["options"]:
        tags["multi_select"]["options"] = []
    tags["multi_select"]["options"].extend(chosen_tags)
    request_payload = {
        "properties": {
            "Tags": tags
        }
    }

    print("Update Notion database with new tags:", chosen_tags)
    notion.databases.update(
        database["id"],
        **request_payload
    )

    # Form a PATCH request payload to update Notion page with selected categories
    request_payload = {
        "properties": {
            "Category": {
                "multi_select": chosen_categories
            },
            "Tags": {
                "multi_select": chosen_tags
            }
        }
    }
    request_payload["properties"]["Category"]["multi_select"] = chosen_categories
    request_payload["properties"]["Tags"]["multi_select"] = chosen_tags

    # Update the Notion database with the ChatGPT answer
    print("Update Notion page with new categories:", chosen_categories)
    print("Update Notion page with new tags:", chosen_tags)
    notion.pages.update(
        new_page["id"],
        **request_payload
    )

    return "Success", 200
