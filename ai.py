import os
from google import genai
from google.genai import types

# The fast model goes first. If a model is busy, slow or gives an error, the next one is tried.
MODEL_NAMES = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]
WAIT_SECONDS = 30  # stop waiting for a model after 30 seconds


def analyze_stock(stock, headlines):
    # The prompt is the instruction we send to Gemini
    prompt = (
        "You are a stock research assistant for beginners.\n"
        "Stock data: " + str(stock) + "\n"
        "Recent news headlines: " + str(headlines) + "\n"
        "Write a short research report in plain text only. "
        "Do not use markdown, bullet symbols or special characters.\n"
        "Use exactly these headings, each on its own line and ending with a colon: "
        "Summary:, Strengths:, Risks:, News Impact:, Final View:\n"
        "Keep each section to 2 or 3 short sentences. "
        "Do not give financial advice."
    )

    # Try each model in the list until one works
    for model_name in MODEL_NAMES:
        try:
            # The timeout is in milliseconds, so we multiply the seconds by 1000
            options = types.HttpOptions(timeout=WAIT_SECONDS * 1000)
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"), http_options=options)
            response = client.models.generate_content(model=model_name, contents=prompt)
            if response.text:
                return response.text
        except Exception as error:
            print("Gemini problem with", model_name + ":", error)

    return "AI analysis is not available right now."