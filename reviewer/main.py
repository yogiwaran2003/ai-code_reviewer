import os
import sys
from dotenv import load_dotenv
from github_client import GitHubClient
from ai_reviewer import AIReviewer

load_dotenv()

SKIP_FILES = {
    "package-lock.json", "yarn.lock", "poetry.lock",
    ".env", ".env.example"
}
SKIP_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".woff", ".woff2"}


def should_skip(filename):
    if filename in SKIP_FILES:
        return True
    ext = "." + filename.rsplit(".", 1)[-1] if "." in filename else ""
    return ext in SKIP_EXTENSIONS


def run():
    github = GitHubClient(os.environ["GITHUB_TOKEN"])
    reviewer = AIReviewer(os.environ["ANTHROPIC_API_KEY"])

    repo = os.environ["GITHUB_REPOSITORY"]
    pr_number = int(os.environ["PR_NUMBER"])

    print(f"Fetching diff for PR #{pr_number} in {repo}...")
    files = github.get_pr_diff(repo, pr_number)

    full_review = []
    issues_count = 0

    for file in files:
        filename = file["filename"]
        patch = file.get("patch", "")

        if not patch or should_skip(filename):
            print(f"Skipping {filename}")
            continue

        print(f"Reviewing {filename}...")
        review = reviewer.review(filename, patch)
        full_review.append(f"### `{filename}`\n{review}")

        for label in ["[BUG]", "[SECURITY]", "[PERFORMANCE]"]:
            issues_count += review.count(label)

    if not full_review:
        print("No reviewable files found.")
        sys.exit(0)

    summary = f"**{issues_count} issue(s) found across {len(full_review)} file(s).**"
    comment = f"## AI Code Review\n\n{summary}\n\n---\n\n" + "\n\n---\n\n".join(full_review)

    github.post_comment(repo, pr_number, comment)
    print("Review posted successfully.")


if __name__ == "__main__":
    run()
