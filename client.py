from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="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")

# Create a chat completion
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
    ]
)

# Print the output
print(response.choices[0].message.content)
