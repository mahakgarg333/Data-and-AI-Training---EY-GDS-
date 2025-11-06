from autogen import AssistantAgent
import os
from dotenv import load_dotenv

# ------------------------------------------------------------
# Load API keys
# ------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# ------------------------------------------------------------
# LLM Configuration
# ------------------------------------------------------------
llm_config = {
    "model": "meta-llama/llama-3-8b-instruct",
    "api_key": api_key,
    "base_url": base_url,
    "temperature": 0.7,
    "max_tokens": 500,
}

# ------------------------------------------------------------
# Agents for Candidate Background Verification
# ------------------------------------------------------------

resume_agent = AssistantAgent(
    name="ResumeVerificationAgent",
    llm_config=llm_config,
    system_message=(
        "You are the Resume Verification Agent. "
        "Your job is to verify that the candidate's resume includes necessary details like skills, experience, and projects. "
        "If resume information is sufficient, mark resume as 'Verified'. Otherwise, mark as 'Incomplete'."
    )
)

education_agent = AssistantAgent(
    name="EducationVerificationAgent",
    llm_config=llm_config,
    system_message=(
        "You are the Education Verification Agent. "
        "Validate the authenticity of the candidate's education background, ensuring the institution (university/college) is legitimate "
        "and degree completion appears valid. Respond briefly with 'Education Verified' or 'Education Not Verified'."
    )
)

employment_agent = AssistantAgent(
    name="EmploymentVerificationAgent",
    llm_config=llm_config,
    system_message=(
        "You are the Employment Verification Agent. "
        "Confirm the candidate’s previous employer details, job titles, and duration of employment. "
        "If all details seem authentic, respond 'Employment Verified', else 'Employment Not Verified'."
    )
)

identity_agent = AssistantAgent(
    name="IdentityVerificationAgent",
    llm_config=llm_config,
    system_message=(
        "You are the Identity Verification Agent. "
        "Verify personal identity based on provided details such as name, email, and phone number consistency. "
        "Respond with 'Identity Verified' or 'Identity Not Verified'."
    )
)

address_agent = AssistantAgent(
    name="AddressVerificationAgent",
    llm_config=llm_config,
    system_message=(
        "You are the Address Verification Agent. "
        "Confirm that the candidate's address information (current or permanent) appears valid based on common patterns or known locations. "
        "Respond with 'Address Verified' or 'Address Not Verified'."
    )
)

criminal_agent = AssistantAgent(
    name="CriminalRecordCheckAgent",
    llm_config=llm_config,
    system_message=(
        "You are the Criminal Record Check Agent. "
        "Search public data references conceptually to ensure there is no criminal background associated with the candidate. "
        "Respond with 'No Criminal Record Found' or 'Criminal Record Found'."
    )
)

background_agent = AssistantAgent(
    name="BackgroundAgent",
    llm_config=llm_config,
    system_message=(
        "You are the Background Check Coordinator Agent. "
        "Your role is to review all verification reports from other agents and provide a final summarized result. "
        "If all checks are verified, respond 'Background Verification successfully done'. "
        "If any verification fails, respond 'Verification failed' and summarize the failed checks."
    )
)

# ------------------------------------------------------------
# Custom user input for candidate name
# ------------------------------------------------------------
candidate_name = input("Enter candidate name for verification: ")

# ------------------------------------------------------------
# Simulate agent conversation
# ------------------------------------------------------------
resume_response = resume_agent.generate_reply(
    messages=[{"role": "user", "content": f"Verify resume details for {candidate_name}."}]
)

education_response = education_agent.generate_reply(
    messages=[{"role": "user", "content": f"Verify education details for {candidate_name}."}]
)

employment_response = employment_agent.generate_reply(
    messages=[{"role": "user", "content": f"Verify employment history for {candidate_name}."}]
)

identity_response = identity_agent.generate_reply(
    messages=[{"role": "user", "content": f"Verify identity details for {candidate_name}."}]
)

address_response = address_agent.generate_reply(
    messages=[{"role": "user", "content": f"Verify address details for {candidate_name}."}]
)

criminal_response = criminal_agent.generate_reply(
    messages=[{"role": "user", "content": f"Check for any criminal record for {candidate_name}."}]
)

# ------------------------------------------------------------
# Final background verification summary
# ------------------------------------------------------------
final_response = background_agent.generate_reply(
    messages=[
        {
            "role": "user",
            "content": (
                f"Candidate: {candidate_name}\n\n"
                f"Resume Check: {resume_response}\n"
                f"Education Check: {education_response}\n"
                f"Employment Check: {employment_response}\n"
                f"Identity Check: {identity_response}\n"
                f"Address Check: {address_response}\n"
                f"Criminal Record Check: {criminal_response}\n\n"
                "Summarize and conclude the overall background verification process."
            )
        }
    ]
)

# ------------------------------------------------------------
# Print Final Outputs
# ------------------------------------------------------------
print("\n Resume Verification:\n", resume_response, "\n")
print(" Education Verification:\n", education_response, "\n")
print(" Employment Verification:\n", employment_response, "\n")
print(" Identity Verification:\n", identity_response, "\n")
print(" Address Verification:\n", address_response, "\n")
print(" Criminal Record Check:\n", criminal_response, "\n")
print(" Final Background Verification Result:\n", final_response)
