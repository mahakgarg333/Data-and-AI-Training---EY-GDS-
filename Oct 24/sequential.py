import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------------------------------------------------
# 1. Load environment variables
# ----------------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# ----------------------------------------------------------
# 2. Initialize model (Mistral via OpenRouter)
# ----------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)

# ----------------------------------------------------------
# 3. Define a dynamic ChatPromptTemplate
# ----------------------------------------------------------
prompt = ChatPromptTemplate.from_template(
    "<s>[INST] You are a summarizer and Quiz Generator. Summarize {topic} within 60 words and generate 3-4 quiz questions on {topic}. [/INST]"
)

# Output parser converts model output to plain string
parser = StrOutputParser()


# --------------------------------
# 4. Create a reusable chain (prompt -> model -> output)
# ---------------------------------------------------------
def generate_explanation(topic):
    try:
        # Invoke the chain and get the response
        chain = prompt | llm | parser
        response = chain.invoke({"topic": topic})

        return response
    except Exception as e:
        print(f"Error during API call: {e}")
        return None


# -------------------------------------------------
# 5. Run dynamically for any topic
# ------------------------------------------------------
user_topic = input("Enter topic: ").strip()

# Check if the user entered a topic
if not user_topic:
    print("No topic entered. Please provide a valid topic.")
else:
    response = generate_explanation(user_topic)

    # Check if the response is valid
    if response:
        print("\n ----Mistral Response----")
        print(response)

        # --------------------
        # 6. Log the prompt and output
        # -----------------------------------------
        os.makedirs("logs", exist_ok=True)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "topic": user_topic,
            "response": response
        }

        log_filename = "logs/summarizer_quiz_generator_log.jsonl"

        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

        print(f"\nResponses logged to {log_filename}")
    else:
        print("No response generated from the model.")
