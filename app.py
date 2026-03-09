import streamlit as st
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import PyPDF2
import re
import uuid

st.set_page_config(page_title="personalized Cover Letter Generator", layout="wide")

# ---------------- SESSION STATE ----------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title(" Chat History")

    if st.button(" New Chat"):
        new_chat_id = str(uuid.uuid4())
        st.session_state.current_chat = new_chat_id
        st.session_state.chats[new_chat_id] = []

    for i, chat_id in enumerate(st.session_state.chats.keys()):
        if st.button(f"Chat {i+1}", key=chat_id):
            st.session_state.current_chat = chat_id

# ---------------- LOAD OCR ----------------
@st.cache_resource
def load_ocr():
    return PaddleOCR(use_angle_cls=True, lang="en")

ocr = load_ocr()

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_pdf_text(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text

# ---------------- IMAGE OCR ----------------
def extract_image_text(uploaded_image):
    image = Image.open(uploaded_image).convert("RGB")
    image_np = np.array(image)
    result = ocr.ocr(image_np)

    extracted_text = ""
    if result and result[0]:
        for line in result[0]:
            extracted_text += line[1][0] + " "

    return extracted_text

# ---------------- NAME EXTRACTION ----------------
def extract_name_from_resume(resume_text):
    lines = resume_text.split("\n")

    for line in lines[:5]:  # Check first few lines
        line = line.strip()

        # Match proper name pattern
        if re.match(r'^[A-Z][a-zA-Z\s]{2,40}$', line):
            return line

    return "Applicant"

# ---------------- MATCHING FUNCTION ----------------
def calculate_match(resume_text, jd_text):
    resume_words = set(re.findall(r'\w+', resume_text.lower()))
    jd_words = set(re.findall(r'\w+', jd_text.lower()))

    common_words = resume_words.intersection(jd_words)
    match_percentage = (len(common_words) / len(jd_words)) * 100 if jd_words else 0

    return round(match_percentage, 2), common_words

# ---------------- COVER LETTER GENERATOR ----------------
def generate_cover_letter(resume_text, jd_text, match_score, common_words):

    candidate_name = extract_name_from_resume(resume_text)

    important_skills = [word for word in common_words if len(word) > 3][:8]
    skills_text = ", ".join(important_skills) if important_skills else "relevant technical skills"

    cover_letter = f"""
Dear Hiring Manager,

My name is {candidate_name}, and I am writing to express my strong interest in the position outlined in your job description.

After reviewing the job requirements, I believe my technical background and project experience align well with your expectations.

Based on resume and job description analysis, I have demonstrated experience in:
{skills_text}.

The overall resume-to-job match score is {match_score}%, indicating strong compatibility with the role.

I am highly motivated, adaptable, and eager to contribute effectively to your organization while continuously enhancing my professional skills.

Thank you for your time and consideration. I look forward to the opportunity to discuss how I can add value to your team.

Sincerely,  
{candidate_name}
"""
    return cover_letter

# ---------------- MAIN UI ----------------
st.title("personalized Cover Letter Generator")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_image = st.file_uploader("Upload Job Description Screenshot (Image)", type=["png", "jpg", "jpeg"])

if resume_file and jd_image:
    st.info("Processing... Please wait ")

    resume_text = extract_pdf_text(resume_file)
    jd_text = extract_image_text(jd_image)

    match_score, common_words = calculate_match(resume_text, jd_text)
    cover_letter = generate_cover_letter(resume_text, jd_text, match_score, common_words)

    st.session_state.chats[st.session_state.current_chat].append({
        "match_score": match_score,
        "resume_text": resume_text,
        "jd_text": jd_text,
        "cover_letter": cover_letter
    })

# ---------------- DISPLAY CURRENT CHAT ----------------
current_chat_data = st.session_state.chats[st.session_state.current_chat]

for idx, chat in enumerate(current_chat_data):
    st.success(f" Match Score: {chat['match_score']}%")

    with st.expander(f" View Resume Text - Analysis {idx+1}"):
        st.write(chat["resume_text"])

    with st.expander(f" View Job Description Text - Analysis {idx+1}"):
        st.write(chat["jd_text"])

    with st.expander(f"✉ Generated Cover Letter - Analysis {idx+1}"):
        st.text_area("Cover Letter", chat["cover_letter"], height=400)