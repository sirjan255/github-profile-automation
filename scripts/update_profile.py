import requests
from datetime import datetime, timedelta
import os

username = 'sirjan255'
token = os.getenv('GH_TOKEN')  # Retrieve the token from environment variables

def get_commits():
    url = f'https://api.github.com/users/{username}/events'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    events = response.json()

    commits = []
    for event in events:
        if event['type'] == 'PushEvent':
            for commit in event['payload']['commits']:
                commit_time = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                if commit_time > datetime.now() - timedelta(days=1):
                    commits.append(commit['message'])

    return commits

def update_activity():
    commits = get_commits()
    with open('activity.md', 'w') as file:
        file.write('# Daily GitHub Activity\n\n')
        file.write('## Commits\n')
        for commit in commits:
            file.write(f'- {commit}\n')

if __name__ == "__main__":
    update_activity()

