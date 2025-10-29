import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage

# ------------------------------------------------------------
# 1. Load environment variables
# ------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# ------------------------------------------------------------
# 2. Initialize the Mistral model
# ------------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# ------------------------------------------------------------
# 3. Define tool functions
# ------------------------------------------------------------
def summarize(phrase):
    response = llm.invoke(f"Summarize the following in 60 words:\n{phrase}")
    return response.content

def classify_task(phrase):
    response = llm.invoke(
        f"Classify the task as HIGH, MEDIUM, or LOW priority: {phrase}. "
        f"Give only one word as output."
    )
    return response.content

# ------------------------------------------------------------
# 4. Initialize memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
note_memory = ConversationBufferMemory(memory_key="note_history", return_messages=True)

# ------------------------------------------------------------
# 5. Conversational loop
# ------------------------------------------------------------
print("\n=== Start chatting with your Agent ===")
print("Commands: summarize, analyze, note, get notes, improve, priority")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    # --- Summarizer ---
    if user_input.lower().startswith("summarize"):
        try:
            sent = user_input.replace("summarize", "", 1).strip()
            response = summarize(sent)
            print(f"Agent: {response}")
            memory.save_context({"input": user_input}, {"output": response})
            continue
        except Exception as e:
            print(f"Agent: Summary error: {e}")
            continue

    # --- Sentiment Analyzer ---
    if user_input.lower().startswith("analyze"):
        try:
            sent = user_input.replace("analyze", "", 1).strip()
            response = llm.invoke(
                f"""
Classify the sentiment of this phrase as Positive, Negative, or Neutral.
Also explain briefly why.

Phrase: "{sent}"

Respond in this format:
Sentiment: <Positive/Negative/Neutral>
Explanation: <reason>
"""
            )
            print(f"Agent: {response.content}")
            memory.save_context({"input": user_input}, {"output": response.content})
            continue
        except Exception as e:
            print(f"Agent: Sentiment error: {e}")
            continue

    # --- Note Maker ---
    if user_input.lower().startswith("note"):
        try:
            note = user_input.replace("note", "", 1).strip()
            if not note:
                print("Agent: Please specify what to note.")
                continue
            response = llm.invoke(f"Create a reminder note: {note}")
            print(f"Agent: Noted — {response.content}")
            note_memory.save_context({"input": user_input}, {"output": note})
            continue
        except Exception as e:
            print(f"Agent: Note error: {e}")
            continue

    # --- Get Notes ---
    if user_input.lower() == "get notes":
        try:
            messages = note_memory.load_memory_variables({}).get("note_history", [])
            note_messages = [msg for msg in messages if isinstance(msg, AIMessage)]
            if note_messages:
                print(f"Agent: You have {len(note_messages)} notes:")
                for i, msg in enumerate(note_messages):
                    print(f"  Note {i+1}: {msg.content}")
            else:
                print("Agent: No notes found.")
            continue
        except Exception as e:
            print(f"Agent: Notes retrieval error: {e}")
            continue

    # --- Text Improver ---
    if user_input.lower().startswith("improve"):
        try:
            sent = user_input.replace("improve", "", 1).strip()
            response = llm.invoke(f"Rewrite this text to make it clearer and more professional:\n{sent}")
            print(f"Agent: {response.content}")
            memory.save_context({"input": user_input}, {"output": response.content})
            continue
        except Exception as e:
            print(f"Agent: Text improvement error: {e}")
            continue

    # --- Task Priority ---
    if user_input.lower().startswith("priority"):
        try:
            task = user_input.replace("priority", "", 1).strip()
            response = classify_task(task)
            result = response.lower()
            if "high" in result:
                print(f"Agent: Task '{task}' marked as HIGH Priority.")
            elif "medium" in result:
                print(f"Agent: Task '{task}' marked as MEDIUM Priority.")
            elif "low" in result:
                print(f"Agent: Task '{task}' marked as LOW Priority.")
            else:
                print(f"Agent: Could not classify priority. Raw response: {response}")
            memory.save_context({"input": user_input}, {"output": response})
            continue
        except Exception as e:
            print(f"Agent: Task classification error: {e}")
            continue

    # --- Default Chat Mode (the missing part!) ---
    try:
        response = llm.invoke(user_input)
        print(f"Agent: {response.content}")
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print(f"Agent: Error generating response: {e}")
