from groq import Groq
from app.config.settings import Settings

client = Groq(api_key=Settings.GROQ_API_KEY)

def get_llm_answer(query, context):
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You answer using provided context."},
            {"role": "user", "content": f"Query: {query}\nContext: {context}"}
        ]
    )
    return resp.choices[0].message.content
