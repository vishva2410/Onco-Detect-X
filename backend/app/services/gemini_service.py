import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import json
import re

# Load environment variables
load_dotenv()

# Configure Google Gemini
API_KEY = os.getenv("gemini_API_KEY")
if not API_KEY:
    print("Warning: Gemini API Key not found in environment variables.")

# Initialize Gemini if API key is present
if API_KEY:
    genai.configure(api_key=API_KEY)

# Generation Configs
generation_config = {
    "temperature": 0.4,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 4096,
}

# Safety Settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Initialize Models
# Note: Using the same model for both as in the original code, but could be different.
model_flash = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config, safety_settings=safety_settings)
model_pro = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config, safety_settings=safety_settings)

async def check_relevance(content_parts):
    """
    Checks if the input content is related to cancer/oncology/medical analysis.
    Returns: (bool, str) -> (is_relevant, reason)
    """
    if not API_KEY:
        return False, "API Key missing"

    prompt = """
    You are a content filter for a specialized Oncologist AI application.
    Analyze the provided input (text and/or image).
    Determine if the content is related to:
    1. Cancer or Oncology (reports, scans, symptoms, questions).
    2. General medical issues that might require a doctor's review.
    3. Biological research related to diseases.

    If it is completely unrelated (e.g., a picture of a cat, a car, a generic coding question), answer NO.
    If it is possibly related, answer YES.

    Output format JSON:
    {
        "is_relevant": true/false,
        "reason": "Brief explanation why."
    }
    """
    
    try:
        # Gemini python lib supports async generate_content now, or we can run in threadpool if needed.
        # For simplicity in this port, we'll keep it synchronous but wrap in async def or use async_generate_content if available.
        # The library's async support is `generate_content_async`.
        response = await model_flash.generate_content_async([prompt, *content_parts])
        
        # Clean up JSON
        text = response.text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
            return data.get("is_relevant", False), data.get("reason", "Unknown")
        else:
            return True, "Could not strict parse check, defaulting to proceed."
    except Exception as e:
        print(f"Error in guardrail: {e}")
        return True, "Guardrail error, proceeding with caution."

async def analyze_oncology(content_parts):
    """
    Main Oncologist Analysis.
    Returns: (str, dict) -> (analysis_text, chart_data)
    """
    if not API_KEY:
        return "API Key missing cannot analyze.", None

    system_prompt = """
    You are an expert Oncologist and Cancer Researcher with decades of experience. 
    Your role is to analyze medical inputs (text, patient reports, imaging scans, histology slides) and provide a professional assessment.

    **YOUR TASKS:**
    1.  **Detailed Analysis**: Explain what you see in the image or text. Use medical terminology but explain it clearly. Format this part as Markdown.
    2.  **Probability Assessment**: Estimate the probability of malignancy/cancer based *only* on the provided evidence. 
        *Disclaimer: You must state this is an AI assessment and not a confirmed diagnosis.*
    3.  **Recommendations**: Suggest next steps (biopsy, MRI, CT, blood work, etc.).
    4.  **Charts Data**: You MUST provide data for visual charts at the end of your response in a strict JSON block.

    **JSON OUTPUT FORMAT (Must be at the very end):**
    ```json
    {
        "cancer_types_probability": {
            "Benign/Normal": 0.0 to 1.0,
            "Malignant (General)": 0.0 to 1.0,
            "Specific Type A (if applicable)": 0.0 to 1.0,
            "Specific Type B (if applicable)": 0.0 to 1.0
        },
        "risk_factors": {
            "Age": 0-10,
            "Family History": 0-10,
            "Lifestyle": 0-10,
            "Visual Evidence": 0-10
        }
    }
    ```
    """
    
    try:
        response = await model_pro.generate_content_async([system_prompt, *content_parts])
        full_text = response.text
        
        # Extract JSON
        chart_data = None
        match = re.search(r'```json\n(.*?)\n```', full_text, re.DOTALL)
        if match:
            json_str = match.group(1)
            try:
                chart_data = json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        return full_text, chart_data

    except Exception as e:
        return f"Error during analysis: {str(e)}", None
