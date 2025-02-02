import json, re, os
from utilities.slack import complete_workflow, get_message, get_user_info
from utilities.jira import get_issue, transition_issue, add_comment, assign_issue

def lambda_handler(event, context):
    slack_event = json.loads(event["body"])
    print(slack_event)
    # Verfiy lambda function with challenge parameter
    if slack_event.get("type") == "url_verification":
        challenge_token = slack_event.get("challenge")
        return {
            'statusCode': 200,
            'body': challenge_token
        }
    # Retrieve all required information from slack_event
    event_data = slack_event.get("event", {})
    callback_id = event_data.get("function", {}).get("callback_id")
    channel_id = event_data.get("inputs", {}).get("channel_id")
    reacted_user_id = event_data.get("inputs", {}).get("user_id")
    message_timestamp = event_data.get("inputs", {}).get("message_ts")
    function_execution_id = event_data.get("function_execution_id")

    if not (channel_id and message_timestamp and function_execution_id and reacted_user_id and callback_id):
        return {"statusCode": 400, "body": "Missing parameters in the event payload."}

    try:
        # Complete the Slack workflow
        # Mark workflow completed within 3 sec, Refer https://api.slack.com/apis/events-api#responding for more info
        complete_workflow(function_execution_id)

        # Get the Slack message and user info
        message_data = get_message(channel_id, message_timestamp)
        user_info = get_user_info(reacted_user_id)

        if message_data.get("ok") and user_info.get("ok"):
            messages = message_data.get("messages", [])
            # Ensure that only the ticket associated with the reacted message is updated.
            if messages and messages[0].get("ts") == message_timestamp:
                message_text = messages[0].get("text", "")
                print(message_text)
                # Get ticket ID assuming ticket message is "DO-2050 Test Ticket"
                ticket_id = re.search(r"\bDO-\d+\b", message_text)
                print(ticket_id[0])
                if ticket_id:
                    issue = get_issue(ticket_id[0])
                    current_status = issue.fields.status.name.lower()
                    # Get email address from slack user ID
                    user_email = user_info["user"]["profile"].get("email", "No email found")
                    print(user_email)

                    # update ticket status based on "callback_id" specified in slack workflow steps
                    if callback_id == "update_done":
                        if current_status == "done":
                            print(f"Issue {ticket_id[0]} is already updated as 'Done'. No action taken.")
                        else:
                            # Update JIRA ticket status based on transition ID
                            transition_issue(issue, os.environ['DONE_TRANSITION_ID'])
                            # Add comment if the ticket is marked as done
                            add_comment(ticket_id[0], f"Issue updated as done by {user_email} using Slack reaction.")
                    elif callback_id == "update_in_prog":
                        if current_status == "in progress":
                              print(f"Issue {ticket_id[0]} is already updated as 'In Progress'. No action taken.")
                        else:  
                            # Update JIRA ticket status based on transition ID 
                            transition_issue(issue, os.environ['IN_PROGRESS_TRANSITION_ID'])
                            # Assign the ticket to the user who reacted
                            assign_issue(ticket_id[0], user_email)
                else:
                    print("No ticket ID found in the message.")
            else:
                print("No messages found for the given timestamp.")
    except Exception as e:
        print(f"Error while processing event: {e}")
        return {"statusCode": 500, "body": "Internal server error."}

    return {"statusCode": 200, "body": "Event processed successfully."}
