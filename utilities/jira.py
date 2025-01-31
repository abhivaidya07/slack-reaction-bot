from jira import JIRA
import os

JIRA_AUTH = (os.environ['JIRA_USERNAME'], os.environ['JIRA_API_TOKEN'])  # Replace with actual credentials

def get_jira_client():
    return JIRA(server=os.environ['JIRA_SERVER'], basic_auth=JIRA_AUTH)

def get_issue(ticket_id):
    jira = get_jira_client()
    return jira.issue(ticket_id)

def transition_issue(issue, transition_id):
    jira = get_jira_client()
    jira.transition_issue(issue, transition=transition_id)

def add_comment(issue_key, comment):
    jira = get_jira_client()
    jira.add_comment(issue_key, comment)

def assign_issue(issue_key, assignee):
    jira = get_jira_client()
    jira.assign_issue(issue_key, assignee)
