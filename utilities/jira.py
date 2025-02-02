from jira import JIRA
import os

JIRA_AUTH = (os.environ['JIRA_USERNAME'], os.environ['JIRA_API_TOKEN'])

def get_jira_client():
    # Authenticate with JIRA client
    return JIRA(server=os.environ['JIRA_SERVER'], basic_auth=JIRA_AUTH)

def get_issue(ticket_id):
    # Get details about the issue 
    jira = get_jira_client()
    return jira.issue(ticket_id)

def transition_issue(issue, transition_id):
    # Update JIRA ticket status based on transition ID
    jira = get_jira_client()
    jira.transition_issue(issue, transition=transition_id)

def add_comment(issue_key, comment):
    # Add comment if the ticket is marked as done
    jira = get_jira_client()
    jira.add_comment(issue_key, comment)

def assign_issue(issue_key, assignee):
    # Assign the ticket to the user who reacted
    jira = get_jira_client()
    jira.assign_issue(issue_key, assignee)
