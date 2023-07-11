import argparse
import os
import subprocess
import sys

import openai

parser = argparse.ArgumentParser(prog="chatgpt-commit", description="ChatGPT Commit Message Generator")
parser.add_argument(
    "-t",
    "--temperature",
    type=float,
    default=1.0,
    help="set the temperature for the openai model",
)


def main():
    args = parser.parse_args()
    openai.organization = os.getenv("OPENAI_ORG_ID")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    process = subprocess.run(["git", "diff"], check=True, capture_output=True)
    git_diff_output = process.stdout.decode()

    content = "\n\n".join(
        [
            "Based on the following Git diff output, could you help me to create an appropriate Git commit message in one line?",
            git_diff_output,
        ]
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            temperature=args.temperature,
        )
    except openai.error.AuthenticationError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    for choice in response.choices:
        print(choice.message.content)


if __name__ == "__main__":
    main()
