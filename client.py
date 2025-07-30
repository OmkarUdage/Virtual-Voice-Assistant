# Cohere AI API integration 
import cohere

co = cohere.ClientV2("")

response = co.chat(
    model="command-a-03-2025", 
    messages=[
        {"role": "system", "content": "You are a virtual voice assistant named Nova, skilled in general tasks like Alexa and Siri"},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming"}
    ]
)

print(response.message.content.strip())
