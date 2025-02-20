from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": "你現在是一個電影售票員"
        },
        {
            "role": "user",
            "content": "請問現在還有復仇者聯盟1的票嗎?"
        }
    ]
)

print(completion.choices[0].message)