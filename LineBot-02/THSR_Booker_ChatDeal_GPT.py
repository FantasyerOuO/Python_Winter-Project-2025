from openai import OpenAI
client = OpenAI()

def ChatGPT(System_Prompt, User_Message, Completion_model="gpt-4o-mini") :
    completion = client.chat.completions.create(
        model=Completion_model,
        messages=[
            {
                "role": "system", 
                "content": "{System_Prompt}".format(System_Prompt=System_Prompt)
            },
            {
                "role": "user",
                "content": "{User_Message}".format(User_Message=User_Message)
            }
        ]
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    System_Prompt, User_Message = input("設定一個和你對話的身分:"), input("你想對這個身分說的話:")
    ChatGPT(System_Prompt=System_Prompt, User_Message=User_Message)
