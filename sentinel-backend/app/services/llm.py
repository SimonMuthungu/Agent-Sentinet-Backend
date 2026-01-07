import google.generativeai as genai
from app.config.settings import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

async def synthesize(context: str, vendor_name: str) -> str:
    prompt = f"""
    Assess vendor risk.

    Vendor: {vendor_name}
    Context:
    {context}

    Return a concise compliance risk summary.
    """
    response = model.generate_content(prompt)
    return response.text
