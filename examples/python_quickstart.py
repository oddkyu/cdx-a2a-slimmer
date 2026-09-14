from openai import OpenAI

# Direct your requests through the local CDX Sidecar Proxy
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="YOUR_OPENAI_API_KEY"  # Your existing OpenAI API key
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Analyze the quarterly earnings report and invoke calculation tools."}
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "calculate_ebitda",
                "description": "Calculates EBITDA based on operating profit and depreciation allowances.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operating_profit": {"type": "number"},
                        "depreciation": {"type": "number"}
                    },
                    "required": ["operating_profit", "depreciation"]
                }
            }
        }
    ]
)

print("Response:", response.choices[0].message.content)
