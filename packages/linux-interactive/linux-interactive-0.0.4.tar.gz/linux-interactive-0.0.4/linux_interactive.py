import openai
import sys
import os

def main():
    # Check if the OpenAI API key is set
    if "OPENAI_API_KEY" not in os.environ:
        print("ERROR: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key in your Bash profile using the following command:")
        print("echo 'export OPENAI_API_KEY=YOUR_API_KEY' >> ~/.bashrc")
        print("Then, run 'source ~/.bashrc' to apply the changes.")
        sys.exit(1)

    # Get the API key from the environment
    api_key = os.environ["OPENAI_API_KEY"]

    openai.api_key = api_key

    def get_chat_completion(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a utility for Linux users. Your single role is to respond with Linux commands. The commands must do what the user asks. Do not argue or instruct the user about what you can't do for them. Only respond with Linux, and if you can't, then respond with the Linux that you can."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        print(response.choices[0].message.content)

    # Check if the script was called with one argument (the prompt)
    if len(sys.argv) == 2:
        prompt = sys.argv[1]
        get_chat_completion(prompt)
    else:
        print("Usage: li 'your_prompt_here'")

if __name__ == "__main__":
    main()

