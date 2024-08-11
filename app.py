import os
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load the environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Application Tracking System 💻", page_icon=":robot:")

# Sidebar
with st.sidebar:
    st.title("Resume Analyzer Info 📄")
    st.write("""
        Welcome to the Application Tracking System (ATS) Resume Analyzer! 🎉
        
        **Instructions:**
        1. **Enter Job Description:** Paste the job description in the provided text area 📝.
        2. **Upload Resume:** Upload your resume in PDF format 📤.
        3. **Submit:** Click the 'Submit' button to analyze your resume 🚀.
        
        **Note:** Make sure your resume is well-formatted for the best results ⚙️.
    """)
    st.write("""
        **Features:**
        - Evaluates resume based on the provided job description 🔍.
        - Provides a percentage match 📊.
        - Highlights missing keywords 🔑.
        - Offers a profile summary 📋.
             
        - Suggests improvements to enhance your resume 🛠️.
        
        Improve your resume and increase your chances of getting the job! 💼
    """)

# Prompt Template
input_prompt = """
You are a skilled and very experienced ATS (Application Tracking System) with a deep understanding of the tech field, software engineering,
data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive, and you should provide the best assistance for improving the resumes.
Assign the percentage Matching based on Job description and the missing keywords with high accuracy.
Resume:
Description:

I want the only response in 4 sectors as follows:
* Job Description Match: \n
* Missing Keywords: \n
* Profile Summary: \n
* Suggestions for Improvement: \n
"""

# Streamlit app
st.header("APPLICATION TRACKING SYSTEM 🤖")
st.text("Improve Your Resume ATS Score 💪")
jd = st.text_area("Job Description 📝")
uploaded_file = st.file_uploader("Upload Your Resume 📤", type="pdf", help="Please upload the PDF")

submit = st.button("Submit 🚀")    

if submit:
    if uploaded_file is not None:
        reader = pdf.PdfReader(uploaded_file)
        extracted_text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            extracted_text += str(page.extract_text())
        response = model.generate_content(input_prompt + f"Resume: {extracted_text}\nDescription: {jd}")
        st.write(response.text)
