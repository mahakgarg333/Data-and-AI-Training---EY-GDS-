import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
 
 
load_dotenv()
 
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
 
if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")
 
llm = LLM(
    model="openrouter/mistralai/mistral-7b-instruct",
    temperature=0.3,
    max_tokens=300,
    api_key=api_key,
    base_url=base_url,
)
 
 
party_planner = Agent(
    role="Party Planner",
    goal="Create the overall party plan including theme, schedule, and guest list.",
    backstory="You are an expert in organizing successful parties.",
    llm=llm,
    verbose=True
)
 
food_coordinator = Agent(
    role="Food Coordinator",
    goal="Plan the food and beverage menu.",
    backstory="You specialize in creating balanced menus for large gatherings.",
    llm=llm,
    verbose=True
)
 
decorator = Agent(
    role="Decorator",
    goal="Design the party decoration and visual theme.",
    backstory="You bring creativity to life through decoration and design.",
    llm=llm,
    verbose=True
)
 
 
party_plan_task = Task(
    description="Create a party plan including theme, schedule, and guest list.",
    expected_output="Detailed party plan document.",
    agent=party_planner
)
 
food_task = Task(
    description="Plan the food and drinks for the event.",
    expected_output="Food and beverage menu plan.",
    agent=food_coordinator
)
 
decor_task = Task(
    description="Design decorations based on the party theme.",
    expected_output="Decoration layout and theme guide.",
    agent=decorator
)
 

party_crew = Crew(
    agents=[party_planner, food_coordinator, decorator],
    tasks=[party_plan_task, food_task, decor_task],
    verbose=True
)
 
result = party_crew.kickoff()
print("\n===== FINAL OUTPUT =====\n")
print(result)
