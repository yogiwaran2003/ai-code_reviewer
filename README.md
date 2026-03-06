# AI Code Reviewer

An automated code review bot that integrates with GitHub Actions and uses Claude AI to review pull requests. On every PR, it analyzes the diff, detects bugs, security vulnerabilities, and code quality issues, and posts structured feedback as a comment automatically.

---

## Demo

![AI Code Review comment on a pull request showing detected SQL injection, unclosed file handles, and path traversal vulnerabilities]

> The bot reviews every PR and posts findings labeled as `[BUG]`, `[SECURITY]`, `[PERFORMANCE]`, or `[SUGGESTION]`.

---

## Features

- Triggers automatically on every pull request (opened or updated)
- Reviews changed files using Claude AI (claude-sonnet-4-6)
- Labels issues by severity: `[BUG]`, `[SECURITY]`, `[PERFORMANCE]`, `[SUGGESTION]`
- Posts a summary: "X issues found across Y files"
- Skips non-reviewable files (lock files, images, `.env`)
- Zero setup for reviewers — works entirely through GitHub Actions

---

## How It Works

```
PR opened/updated
      │
      ▼
GitHub Actions triggers workflow
      │
      ▼
Fetch changed files + diffs from GitHub API
      │
      ▼
Send each file's diff to Claude AI for review
      │
      ▼
Post structured review comment on the PR
```

---

## Project Structure

```
ai-code-reviewer/
├── .github/
│   └── workflows/
│       └── code-review.yml   # GitHub Actions pipeline
├── reviewer/
│   ├── __init__.py
│   ├── github_client.py      # GitHub API (fetch diff, post comment)
│   ├── ai_reviewer.py        # Claude API integration
│   └── main.py               # Entry point, orchestrates the review
├── requirements.txt
└── .env                      # Local development keys (never committed)
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yogiwaran2003/ai-code_reviewer.git
cd ai-code_reviewer
```

### 2. Install dependencies

```bash
pip install anthropic requests python-dotenv
```

### 3. Add your API key to GitHub Secrets

Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret Name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Claude API key from [console.anthropic.com](https://console.anthropic.com) |

> `GITHUB_TOKEN` is automatically provided by GitHub — no action needed.

### 4. That's it

Open a pull request in your repo. The bot will trigger automatically and post a review comment within ~30 seconds.

---

## Local Development

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_pat_here
ANTHROPIC_API_KEY=your_claude_api_key_here
GITHUB_REPOSITORY=yogiwaran2003/ai-code_reviewer
PR_NUMBER=1
```

Run manually:

```bash
python reviewer/main.py
```

---

## Example Review Output

```
## AI Code Review

**9 issue(s) found across 2 file(s).**

### `sample_code.py`

[SECURITY] SQL injection vulnerability — string interpolation in query allows
attackers to bypass auth. Use parameterized queries.

[BUG] Database connection is never closed. Use a context manager or conn.close().

[SECURITY] Passwords stored and compared in plaintext. Use bcrypt.

[BUG] File handle is never closed, risking resource leaks.
```

---

## Tech Stack

- **Claude AI** (claude-sonnet-4-6) — code analysis and review
- **GitHub Actions** — CI/CD pipeline trigger
- **GitHub REST API** — fetch PR diffs and post comments
- **Python 3.11+**

---

## Getting Your API Keys

- **Claude API key**: [console.anthropic.com](https://console.anthropic.com) → API Keys → Create Key
- **GitHub PAT** (for local dev): GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic) → scopes: `repo`
