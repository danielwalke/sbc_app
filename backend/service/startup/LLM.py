from dotenv import load_dotenv
import os
def initialize_llm(app):
    load_dotenv()
    app.state.API_KEY = os.getenv("GEMINI_API_KEY")
    print("Finished loading API KEY")