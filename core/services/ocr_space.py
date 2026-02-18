import requests
from django.conf import settings

OCR_SPACE_URL = "https://api.ocr.space/parse/image"

def extract_text_from_image(image_url: str) -> str:
    response = requests.post(
        OCR_SPACE_URL,
        data={
            "apikey": settings.OCR_SPACE_API_KEY,
            "url": image_url,
            "language": "eng",
            "OCREngine": 2,
        },
        timeout=90,
    )

    try:
        result = response.json()
    except ValueError:
        raise Exception(f"OCR API returned non-JSON response: {response.text}")

    if result.get("IsErroredOnProcessing"):
        error = result.get("ErrorMessage", "Unknown OCR error")
        raise Exception(error)

    parsed_results = result.get("ParsedResults")
    if not parsed_results:
        return ""

    return parsed_results[0].get("ParsedText", "").strip()
