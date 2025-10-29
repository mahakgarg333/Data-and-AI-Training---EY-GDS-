# ===============================================================
# mini_language_bot.py — Mini Language Utility Bot (All Tools)
# ===============================================================

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# ---------------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# ---------------------------------------------------------------
# 2. Initialize Mistral model
# ---------------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.4,
    max_tokens=128,
    api_key=api_key,
    base_url=base_url
)

# ---------------------------------------------------------------
# 3. Initialize conversation memory
# ---------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ---------------------------------------------------------------
# 4. Define Tools
# ---------------------------------------------------------------

# Word Counter Tool
def count_words(sentence: str) -> str:
    words = sentence.split()
    return f"Your sentence has {len(words)} words."

# Reverse Text Tool
def reverse_text(sentence: str) -> str:
    words = sentence.split()
    reversed_sentence = " ".join(reversed(words))
    return reversed_sentence

# Vocabulary Helper Tool (Uses LLM)
def define_word(word: str) -> str:
    prompt = f"Provide a short definition or synonym for the word: {word}"
    response = llm.invoke(prompt)
    return response.content.strip()

# Uppercase / Lowercase Tool
def change_case(command: str, text: str) -> str:
    if command == "upper":
        return text.upper()
    elif command == "lower":
        return text.lower()
    return "Invalid command. Use 'upper' or 'lower'."

# Word Repeater Tool
def repeat_word(word: str, count: int) -> str:
    try:
        return " ".join([word] * int(count))
    except Exception:
        return "Invalid format. Use: repeat <word> <count>"

# ---------------------------------------------------------------
# 5. Command-line Chat Loop
# ---------------------------------------------------------------
print("\n=== Mini Language Utility Bot ===")
print("Available Commands:")
print(" count <sentence>")
print(" reverse <sentence>")
print(" define <word>")
print(" upper <text>")
print(" lower <TEXT>")
print(" repeat <word> <count>")
print(" history  → show previous inputs/outputs")
print(" exit     → quit the bot\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Word Counter
    if user_input.lower().startswith("count"):
        sentence = user_input.replace("count", "", 1).strip()
        result = count_words(sentence)
        print("Agent:", result)
        memory.save_context({"input": user_input}, {"output": result})
        continue

    # Reverse Text
    if user_input.lower().startswith("reverse"):
        sentence = user_input.replace("reverse", "", 1).strip()
        result = reverse_text(sentence)
        print("Agent:", result)
        memory.save_context({"input": user_input}, {"output": result})
        continue

    # Vocabulary Helper
    if user_input.lower().startswith("define"):
        word = user_input.replace("define", "", 1).strip()
        result = define_word(word)
        print("Agent:", result)
        memory.save_context({"input": user_input}, {"output": result})
        continue

    # Upper / Lower Case
    if user_input.lower().startswith("upper"):
        text = user_input.replace("upper", "", 1).strip()
        result = change_case("upper", text)
        print("Agent:", result)
        memory.save_context({"input": user_input}, {"output": result})
        continue

    if user_input.lower().startswith("lower"):
        text = user_input.replace("lower", "", 1).strip()
        result = change_case("lower", text)
        print("Agent:", result)
        memory.save_context({"input": user_input}, {"output": result})
        continue

    # Word Repeater
    if user_input.lower().startswith("repeat"):
        parts = user_input.split()
        if len(parts) == 3:
            word, count = parts[1], parts[2]
            result = repeat_word(word, count)
        else:
            result = "Please use the format: repeat <word> <count>"
        print("Agent:", result)
        memory.save_context({"input": user_input}, {"output": result})
        continue

    # History command
    if user_input.lower() == "history":
        chat_history = memory.load_memory_variables({}).get("chat_history", [])
        if chat_history:
            print("\n--- Conversation History ---")
            for msg in chat_history:
                print(f"{msg.type.capitalize()}: {msg.content}")
            print("-----------------------------\n")
        else:
            print("Agent: No history yet.")
        continue

    # Default: fallback chat mode using LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print(f"Agent: Error generating response: {e}")
