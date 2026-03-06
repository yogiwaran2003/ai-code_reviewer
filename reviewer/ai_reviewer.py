import anthropic


class AIReviewer:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)

    def review(self, filename, patch):
        prompt = f"""You are a senior software engineer doing a code review.

File: {filename}
Changes:
{patch}

Review this code for:
1. Bugs or logical errors
2. Security issues
3. Performance problems
4. Code quality and readability

Be concise. Use bullet points. Label issues as [BUG], [SECURITY], [PERFORMANCE], or [SUGGESTION].
If the code looks good, say so."""

        message = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
