import fireworks.client

# Example usage:

# Configure the client
#   fireworks.client.api_key = 'your-key'
# or pass it in FIREWORKS_API_KEY environment variable

# Create a prompt
response = fireworks.client.Completion.create(model="accounts/fireworks/models/llama-v2-7b", prompt="once upon a time", max_tokens=16)

# Print the completion
print(response.choices[0].text)
