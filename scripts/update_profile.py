import requests
from datetime import datetime, timedelta
import os

username = 'sirjan255'
token = os.getenv('GH_TOKEN')  # Retrieve the token from environment variables

def get_commits():
    url = f'https://api.github.com/users/{username}/events'
    headers = {'Authorization': f'token {token}'}
    
    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Check for a successful response
    if response.status_code != 200:
        print(f"Error fetching events: {response.status_code} - {response.text}")
        return []

    events = response.json()
    commits = []
    
    # Process the events
    for event in events:
        if event['type'] == 'PushEvent':
            for commit in event['payload']['commits']:
                commit_time = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                if commit_time > datetime.now() - timedelta(days=1):
                    commits.append(commit['message'])

    return commits

def update_activity():
    commits = get_commits()
    
    # Check if there are any commits
    if not commits:
        print("No commits found in the last 24 hours.")
        return

    with open('activity.md', 'w') as file:
        file.write('# Daily GitHub Activity\n\n')
        file.write('## Commits\n')
        for commit in commits:
            file.write(f'- {commit}\n')

if __name__ == "__main__":
    if token is None:
        print("Error: GH_TOKEN environment variable is not set.")
    else:
        update_activity()
