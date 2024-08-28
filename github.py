import requests
from datetime import datetime, timedelta
import sys

def get_contributors(repo, token):
    # Calculate the date 90 days ago from today
    date_90_days_ago = datetime.now() - timedelta(days=90)
    date_90_days_ago = date_90_days_ago.strftime('%Y-%m-%d')

    # GitHub API endpoint to fetch commits from a repository
    url = f"https://api.github.com/repos/{repo}/commits"
    
    # Headers for the HTTP requests including the access token
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    params = {
        'since': date_90_days_ago,
        'sha': 'main'  # Default branch assumed as 'main'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        commits = response.json()

        contributors = set()
        for commit in commits:
            # Extract the author's username from commit data
            if commit['author']:  # Check if the author field is not None
                author = commit['author']['login']
                contributors.add(author)

        return list(contributors)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def save_contributors_to_file(contributors, filename="contributors.txt"):
    # Write the list of contributors to a text file
    with open(filename, 'w') as file:
        for contributor in contributors:
            file.write(f"{contributor}\n")
    print(f"Contributors list saved to {filename}")

def read_config(filename="config.txt"):
    # Read the repository name and token from a configuration file
    try:
        with open(filename, 'r') as file:
            repo = file.readline().strip()
            token = file.readline().strip()
        return repo, token
    except FileNotFoundError:
        print("Configuration file not found.")
        sys.exit(1)

def main():
    repo, token = read_config()  # Read repo and token from config.txt
    contributors = get_contributors(repo, token)
    save_contributors_to_file(contributors)

if __name__ == "__main__":
    main()
