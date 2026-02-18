import requests
from django.conf import settings

OCR_SPACE_URL = "https://api.ocr.space/parse/image"

def extract_text_from_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        response = requests.post(
            OCR_SPACE_URL,
            files={"file": image_file},
            data={
                "apikey": settings.OCR_SPACE_API_KEY,
                "language": "eng",
                "OCREngine": 2,
            },
            timeout=30,
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
