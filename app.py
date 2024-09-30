import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import datetime
import smtplib
from email.mime.text import MIMEText

# Function to filter resumes based on job description using cosine similarity
def filter_resumes(resumes, job_description):
    tfidf_vectorizer = TfidfVectorizer()
    vectors = tfidf_vectorizer.fit_transform([job_description] + resumes)
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    ranked_resumes = sorted(zip(cosine_similarities, resumes), reverse=True, key=lambda x: x[0])
    return ranked_resumes

# Function to send email (you can disable this if not testing emails)
def send_email(to_email, subject, body):
    from_email = "your_email@example.com"
    password = "your_password"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

# Function to book an interview and send an email to a candidate
def book_interview(candidate_email):
    interview_time = datetime.datetime.now() + datetime.timedelta(days=7)
    subject = "Interview Scheduled"
    body = f"Dear Candidate,\n\nYour interview has been scheduled for {interview_time}.\n\nBest,\nRecruitment Team"
    send_email(candidate_email, subject, body)

# Streamlit app
st.title("Resume Filter and Interview Scheduler")

# File upload option
uploaded_file = st.file_uploader("Upload CSV file with candidate data", type=["csv"])

# Text area to input job description
job_description = st.text_area("Job Description", "Looking for a software engineer with knowledge in Python and AI.")

# If file is uploaded, process the data
if uploaded_file is not None:
    # Load the dataset
    candidate_df = pd.read_csv(uploaded_file)

    # Extract resumes and emails
    resumes = candidate_df['resume'].tolist()
    emails = candidate_df['email'].tolist()

    # Filter resumes based on job description
    ranked_resumes = filter_resumes(resumes, job_description)

    st.subheader("Ranked Resumes:")
    for score, resume in ranked_resumes:
        st.write(f"Score: {score:.2f}")
        st.write(f"Resume: {resume}")
        st.write("---")

    # Email sending option for top-ranked candidate
    if st.button(f"Send Interview Invitation to {emails[0]}"):
        book_interview(emails[0])
        st.success(f"Interview invitation sent to {emails[0]}!")

# To run locally, in terminal, type:
# streamlit run app.py