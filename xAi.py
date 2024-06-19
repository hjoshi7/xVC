import asyncio
import sys

import xai_sdk

import os
os.environ['XAI_API_KEY'] = "Eh97MbeIZ4p4UjhF4D8JVyTRAZm7oErMkdePDVi1jWzNYWPq47XPUFWgqcBd0Ysa7bfaAwrHZCVxK+pzGSVBaXUvHmKzZ8F34vsqwtDpI3hKBCf3rhIz/Obwir0obKZ9PQ"

message = []
text = "Clerk - What they do: Complete user management. Add sign up, sign in, and profile management to your application in minutes"

async def main():
    client = xai_sdk.Client()
    sampler = client.sampler

    PREAMBLE = """\
This is a conversation between a human user and a highly intelligent AI. The AI's name is Grok and it makes every effort to truthfully answer a user's questions. It always responds politely but is not shy to use its vast knowledge in order to solve even the most difficult problems. The conversation begins.

Human: I want you to tell me about this startup objectively given its twitter bio and top tweets. DO not be biased towards the startup.

Please format your answer in the style of a Crunchbase description. 
Here is an example of a good description: Yubo, the social platform where Generation Z creates communities of friends around the world. Yubo lets users create live video discussion spaces where both streamers and viewers interact through a live chat. Relying on cutting-edge technology and tools specifically designed to protect the app users, Yubo provides a secure discussion platform builtto widen their circle of friends. The social network favors sociability, sharing, and authenticity rather than the approval mechanisms and influencers systems of traditional social networks.

Assistant: Understood! Please provide the description of the startup."""

    #text = input("Give me details about a startup: ")
    temps = {
        "warm": 0.7,
        "hot": 0.9,
        "lukewarm": 0.5,
        "cold": 0.3,
        "frigid": 0.1
    }
    prompt = PREAMBLE + f"<|separator|>\n\nHuman: {text}<|separator|>\n\nAssistant: " + "{\n"
    print(prompt)
    async for token in sampler.sample(
        prompt=prompt,
        max_len=1024,
        stop_tokens=["<|separator|>"],
        temperature=temps['lukewarm'],
        nucleus_p=0.95):
        message.append(token.token_str)

asyncio.run(main())

print("Message: " + "".join(message))