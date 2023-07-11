import os
import subprocess

import openai


def main():
    openai.organization = os.getenv("OPENAI_ORG_ID")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    process = subprocess.run(["git", "diff"], check=True, capture_output=True)
    git_diff_output = process.stdout.decode()

    content = "\n\n".join(
        [
            "Based on the following Git diff output, could you help me to create an appropriate Git commit message?",
            git_diff_output,
        ]
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        temperature=0.6,
    )

    for choice in response.choices:
        print(choice.message["content"])


if __name__ == "__main__":
    main()
