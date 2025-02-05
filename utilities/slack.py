import requests
import os

SLACK_API_URL = "https://slack.com/api"

def get_headers():
    bot_access_token = os.environ['SLACK_APP_TOKEN']
    return {
        "Authorization": f"Bearer {bot_access_token}",
        "Content-Type": "application/json"
    }

def complete_workflow(function_execution_id):
    # Complete the Slack workflow
    url = f"{SLACK_API_URL}/functions.completeSuccess"
    headers = get_headers()
    payload = {
        "function_execution_id": function_execution_id,
        "outputs": {"result": "Workflow steps in progress!"}
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def get_message(channel_id, message_timestamp):
    # Get message text using message_ts and channel_id
    url = f"{SLACK_API_URL}/conversations.history"
    headers = get_headers()
    params = {
        "channel": channel_id,
        "latest": message_timestamp,
        "inclusive": True,
        "limit": 1
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_user_info(user_id):
    # Get user information using user_id
    url = f"{SLACK_API_URL}/users.info"
    headers = get_headers()
    params = {"user": user_id}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
