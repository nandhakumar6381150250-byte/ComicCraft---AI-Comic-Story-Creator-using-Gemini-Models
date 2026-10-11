import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from config import GEMINI_API_KEY, TEXT_MODEL

class ComicPanel(BaseModel):
    panel_number: int = Field(description="The sequential number of the comic panel.")
    visual_description: int = Field(description="Detailed visual prompt describing characters, action, and setting for image generation.")
    caption: str = Field(description="Narrator text or setting description box for the top of the panel.")
    dialogue: str = Field(description="Character speech bubble dialogue, formatted like 'Character: Spoken text'.")

class ComicScript(BaseModel):
    title: str = Field(description="Catchy title for the comic book.")
    panels: list[ComicPanel] = Field(description="List of 4 to 6 comic panels outlining the story.")

def generate_comic_script(user_prompt: str) -> dict:
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    Create a compelling comic book script based on the following user concept:
    "{user_prompt}"
    
    Break the story down into 4 sequential panels. Ensure each panel has vivid visual descriptions that can be passed to an image generator, clear narration captions, and engaging character dialogue.
    """
    
    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicScript,
            temperature=0.7,
        ),
    )
    
    return json.loads(response.text)