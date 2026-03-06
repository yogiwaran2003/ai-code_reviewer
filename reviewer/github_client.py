import requests


class GitHubClient:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_pr_diff(self, repo, pr_number):
        url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post_comment(self, repo, pr_number, body):
        url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
        payload = {"body": body}
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
