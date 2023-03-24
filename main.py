import os

import openai
from notion_client import Client
from notion_client.helpers import pick

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
    options = category["multi_select"]["options"]
    categories = [option["name"] for option in options]

    # Generate the prompt
    prompt = f"Describe this webpage ({gem_url}) using only the following tags: {', '.join(categories)}"
    print("ChatGPT prompt:", prompt)

    # Get the response from the ChatGPT API
    chatgpt_answer = get_chatgpt_response(prompt)

    # Select Notion categories that were selected by ChatGPT
    tokens = chatgpt_answer.lower().rstrip(" ,.!/").split(", ")
    chat_gpt_options = [option for option in options if option["name"].lower() in tokens]

    # Form a PATCH request payload to update Notion page with selected categories
    request_payload = new_page["properties"]["Category"]
    request_payload["multi_select"] = chat_gpt_options
    request_payload = { "properties": { "Category": request_payload } }

    # Update the Notion database with the ChatGPT answer
    print("Notion request payload:", pick(request_payload, "properties"))
    notion.pages.update(
        new_page_id,
        **request_payload
    )

    return "Success", 200
