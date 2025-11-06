import streamlit as st
import pandas as pd
import os
from autogen import AssistantAgent
from dotenv import load_dotenv
import io

# ------------------------------------------------------------
# Page Config
# ------------------------------------------------------------
st.set_page_config(page_title="Candidate Background Verification", layout="wide")
st.title("Candidate Background Verification System")
st.markdown("Upload `candidates.csv` or use the default dataset. Select a candidate to run full verification.")

# ------------------------------------------------------------
# Load API keys
# ------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    st.error(" OPENROUTER_API_KEY missing in `.env` file!")
    st.stop()

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
# Agents Definition
# ------------------------------------------------------------
@st.cache_resource
def get_agents():
    resume_agent = AssistantAgent(
        name="ResumeVerificationAgent",
        llm_config=llm_config,
        system_message="You are the Resume Verification Agent. Verify if resume has skills, experience, and projects. Respond: 'Verified' or 'Incomplete'."
    )
    education_agent = AssistantAgent(
        name="EducationVerificationAgent",
        llm_config=llm_config,
        system_message="You are the Education Verification Agent. Validate institution legitimacy. Respond: 'Education Verified' or 'Education Not Verified'."
    )
    employment_agent = AssistantAgent(
        name="EmploymentVerificationAgent",
        llm_config=llm_config,
        system_message="You are the Employment Verification Agent. Confirm employer, title, duration. Respond: 'Employment Verified' or 'Employment Not Verified'."
    )
    identity_agent = AssistantAgent(
        name="IdentityVerificationAgent",
        llm_config=llm_config,
        system_message="You are the Identity Verification Agent. Check name, email, phone consistency. Respond: 'Identity Verified' or 'Identity Not Verified'."
    )
    address_agent = AssistantAgent(
        name="AddressVerificationAgent",
        llm_config=llm_config,
        system_message="You are the Address Verification Agent. Validate address format and location. Respond: 'Address Verified' or 'Address Not Verified'."
    )
    criminal_agent = AssistantAgent(
        name="CriminalRecordCheckAgent",
        llm_config=llm_config,
        system_message="You are the Criminal Record Check Agent. Check for public criminal records. Respond: 'No Criminal Record Found' or 'Criminal Record Found'."
    )
    background_agent = AssistantAgent(
        name="BackgroundAgent",
        llm_config=llm_config,
        system_message="You are the Background Check Coordinator. Summarize all checks. If all pass: 'Background Verification successfully done'. Else: 'Verification failed' + list failures."
    )
    return {
        "resume": resume_agent,
        "education": education_agent,
        "employment": employment_agent,
        "identity": identity_agent,
        "address": address_agent,
        "criminal": criminal_agent,
        "background": background_agent
    }

agents = get_agents()

# ------------------------------------------------------------
# Load CSV Data
# ------------------------------------------------------------
default_csv = """name,email,phone,linkedin,github,skills,experience_years,education,previous_employer,address,govt_id,criminal_record
Rajesh Verma,rajesh.verma@gmail.com,9876543210,linkedin.com/in/rajesh-verma,github.com/rajeshverma,Python,2,University of Delhi (DU),TCS,New Delhi,AADHAR1234,No
Kabir Singh,kabir.singh@gmail.com,9876500000,linkedin.com/in/kabir-singh,github.com/kabirsingh,Java,1.5,Birla Institute of Technology and Science (BITS Pilani),Infosys,Mumbai,AADHAR5678,No
Meera Menon,meera.menon@gmail.com,9876511111,linkedin.com/in/meera-menon,github.com/meeramenon,Python,0.8,Manipal University,Intern at Wipro,Bangalore,AADHAR4321,No
Nisha Joshi,nisha.joshi@gmail.com,9876522222,linkedin.com/in/nisha-joshi,github.com/nishajoshi,Data Science,3,Indian Institute of Technology Delhi (IIT Delhi),Google,Gurgaon,AADHAR9876,No
Anita Rao,anita.rao@gmail.com,9876533333,linkedin.com/in/anita-rao,github.com/anitarao,Web Development,1.2,Christ University Bangalore,Zoho,Chennai,AADHAR3456,No
Arjun Kumar,arjun.kumar@gmail.com,9876544444,linkedin.com/in/arjun-kumar,github.com/arjunkumar,AI/ML,0.5,University of Petroleum and Energy Studies (UPES Dehradun),Intern at TCS,Dehradun,AADHAR2468,No
Sara Ali,sara.ali@gmail.com,9876555555,linkedin.com/in/sara-ali,github.com/saraali,Cloud Computing,2,SRM Institute of Science and Technology,Amazon,Hyderabad,AADHAR1357,No"""

# File uploader
uploaded_file = st.file_uploader("Upload candidates.csv", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        df = pd.read_csv(io.StringIO(default_csv))
else:
    df = pd.read_csv(io.StringIO(default_csv))

# Validate columns
required_cols = ["name", "email", "phone", "skills", "experience_years", "education", "previous_employer", "address", "govt_id", "criminal_record"]
if not all(col in df.columns for col in required_cols):
    st.error(f"CSV must contain columns: {', '.join(required_cols)}")
    st.stop()

# ------------------------------------------------------------
# Candidate Selection
# ------------------------------------------------------------
candidate_name = st.selectbox("Select Candidate", options=df["name"].tolist())

if st.button(" Run Background Verification", type="primary"):
    candidate = df[df["name"] == candidate_name].iloc[0]

    with st.spinner("Running verification checks..."):
        # Prepare candidate details string
        details = f"""
        Name: {candidate['name']}
        Email: {candidate['email']}
        Phone: {candidate['phone']}
        LinkedIn: {candidate['linkedin']}
        GitHub: {candidate['github']}
        Skills: {candidate['skills']}
        Experience: {candidate['experience_years']} years
        Education: {candidate['education']}
        Previous Employer: {candidate['previous_employer']}
        Address: {candidate['address']}
        Govt ID: {candidate['govt_id']}
        Criminal Record (Self): {candidate['criminal_record']}
        """

        # Run all agent checks
        resume_response = agents["resume"].generate_reply(
            messages=[{"role": "user", "content": f"Verify resume for {candidate_name}. Details:\n{details}"}]
        )
        education_response = agents["education"].generate_reply(
            messages=[{"role": "user", "content": f"Verify education for {candidate_name}. Details:\n{details}"}]
        )
        employment_response = agents["employment"].generate_reply(
            messages=[{"role": "user", "content": f"Verify employment for {candidate_name}. Details:\n{details}"}]
        )
        identity_response = agents["identity"].generate_reply(
            messages=[{"role": "user", "content": f"Verify identity for {candidate_name}. Details:\n{details}"}]
        )
        address_response = agents["address"].generate_reply(
            messages=[{"role": "user", "content": f"Verify address for {candidate_name}. Details:\n{details}"}]
        )
        criminal_response = agents["criminal"].generate_reply(
            messages=[{"role": "user", "content": f"Check criminal record for {candidate_name}. Details:\n{details}"}]
        )

        # Final summary
        summary_input = f"""
        Candidate: {candidate_name}

        Resume Check: {resume_response}
        Education Check: {education_response}
        Employment Check: {employment_response}
        Identity Check: {identity_response}
        Address Check: {address_response}
        Criminal Record Check: {criminal_response}

        Summarize and conclude the background verification.
        """
        final_response = agents["background"].generate_reply(
            messages=[{"role": "user", "content": summary_input}]
        )

    # ------------------------------------------------------------
    # Display Results
    # ------------------------------------------------------------
    st.success("Verification Complete!")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Candidate Profile")
        st.json(candidate.to_dict(), expanded=False)

    with col2:
        st.subheader("Verification Summary")
        st.markdown(f"**Final Result:** `{final_response.split('.')[0]}`")

    st.markdown("---")
    st.subheader("Detailed Verification Reports")

    checks = [
        ("Resume", resume_response),
        ("Education", education_response),
        ("Employment", employment_response),
        ("Identity", identity_response),
        ("Address", address_response),
        ("Criminal Record", criminal_response),
    ]

    for check_name, result in checks:
        status = "✅" if "Verified" in result or "No Criminal" in result or "successfully done" in result else "❌"
        st.markdown(f"**{status} {check_name}:** {result}")

    st.markdown("---")
    st.caption("Powered by AutoGen + OpenRouter + Streamlit")


#streamlit run app.py
