import os
import sys
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

def categorize_image(image_path, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    image = Image.open(image_path)
    
    prompt = """You are an expert real estate inspector. Please categorize this image into exactly ONE of the following categories. Respond with only the category name:

1. Facades / Windows / Exterior doors
2. Flat roof / Pitched roof
3. Ancillary rooms (Basement / Attic / Stairwell)
4. Electrical systems
5. Plumbing and heating systems
6. Elevators
7. Living / Bedrooms
8. Kitchen / Wet rooms (Bathroom / separate WC)

Category:"""
    
    response = model.generate_content([prompt, image])
    return response.text.strip()

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: python process-image.py <image_path>")
        sys.exit(1)
    
    load_dotenv()
    
    image_path = sys.argv[1]
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    
    result = categorize_image(image_path, api_key)
    print(f"Category: {result}")
