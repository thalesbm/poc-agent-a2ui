from llm.client.openai import OpenAIClient
from llm.client.openai_key import OpenAIKey

def main():
    """
    Main function to run the agent.
    """
    openai_client = OpenAIClient(api_key=OpenAIKey().get_openai_key())
    response = openai_client.invoke()
    
    if response:
        print(response)
    else:
        print("No response from OpenAI")


if __name__ == "__main__":
    main()