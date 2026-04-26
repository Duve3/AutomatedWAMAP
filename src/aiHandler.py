from google import genai
from google.genai import errors
import time
from PIL import Image


class AiHandler:
    def __init__(self):
        with open("./login.env", "r") as f:
            data = f.read().splitlines()
            API_KEY = data[2]

        self.client = genai.Client(api_key=API_KEY)

    def askQuestion(self, screenshotPath, text: str):
        image = Image.open(screenshotPath)

        # really love python and its amazing "do while" implementation :heart:
        highDemand = True

        while highDemand:
            try:
                print("Sending gemini request...")

                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image, text]
                )
                highDemand = False
            except errors.APIError as err:
                highDemand = True
                print("High demand, waiting 30-60s and retrying...")

                # debug
                print(err.message)
                time.sleep(60)

        return response
