from dotenv import load_dotenv
import os
def initialize_llm(app):
    load_dotenv()
    app.state.API_KEY = os.getenv("GEMINI_API_KEY")
    app.state.llm_cache = dict()
    print("Finished loading API KEY")