from google import genai
from PIL import Image

class AiHandler:
    def __init__(self):
        with open("./login.env", "r") as f:
            data = f.read().splitlines()
            API_KEY = data[2]

        self.client = genai.Client(api_key=API_KEY)

    def askQuestion(self, screenshotPath, text: str):
        image = Image.open(screenshotPath)

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[image, text]
        )

        return response
