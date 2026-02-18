from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.GROQ_API_TOKEN,
    base_url="https://api.groq.com/openai/v1"
)

def simplify_prescription(text: str) -> str:
    if not text.strip():
        return "No readable text found."

    prompt = (
        "Simplify the following medical prescription text into clear, "
        "patient-friendly language. Do NOT give medical advice.\n\n"
        f"{text}"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You simplify medical text."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=200,
    )

    return response.choices[0].message.content.strip()
