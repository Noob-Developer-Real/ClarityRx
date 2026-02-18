from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.GROQ_API_TOKEN,
    base_url="https://api.groq.com/openai/v1"
)
def simplify_prescription(text: str) -> str:
    if not text.strip():
        return "No readable text found."
    text = text[:3000]
    prompt = f"""
You are a medical text simplification assistant.

Rewrite the prescription text below in simple, patient-friendly language.

Rules:
- Do NOT add or infer information
- Do NOT give medical advice
- Keep medicine names and dosages unchanged
- Expand abbreviations
- Use bullet points
- Limit the response to a maximum of 8 bullet points
- If unclear, say "Not clearly specified in the prescription."

Prescription text:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You simplify medical text."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=800,
    )
    choice = response.choices[0]
    print("Finish reason:", choice.finish_reason)
    return response.choices[0].message.content.strip()
