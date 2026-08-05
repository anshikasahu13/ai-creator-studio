from groq import Groq

# Initialize the client
client = Groq(api_key="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")

# Ask Groq for the list of all active models
print("--- ACTIVE GROQ MODELS ---")
models = client.models.list()
for m in models.data:
    print(m.id)