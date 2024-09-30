import pandas as pd
import nltk
import smtplib
from email.mime.text import MIMEText
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import datetime

# Load the dataset
candidate_df = pd.read_csv('sample_candidate_data.csv')

# Extract resumes and emails
resumes = candidate_df['resume'].tolist()
emails = candidate_df['email'].tolist()
job_description = "Looking for a software engineer with knowledge in Python and AI."

def filter_resumes(resumes, job_description):
    tfidf_vectorizer = TfidfVectorizer()
    vectors = tfidf_vectorizer.fit_transform([job_description] + resumes)
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    ranked_resumes = sorted(zip(cosine_similarities, resumes), reverse=True, key=lambda x: x[0])
    return ranked_resumes

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

def book_interview(candidate_email):
    interview_time = datetime.datetime.now() + datetime.timedelta(days=7)
    subject = "Interview Scheduled"
    body = f"Dear Candidate,\n\nYour interview has been scheduled for {interview_time}.\n\nBest,\nRecruitment Team"
    send_email(candidate_email, subject, body)

if _name_ == "_main_":  # Corrected here
    print("Filtering Resumes:")
    ranked_resumes = filter_resumes(resumes, job_description)
    for score, resume in ranked_resumes:
        print(f"Score: {score:.2f} - Resume: {resume}")

    candidate_email = emails[0]  # For demonstration, sending the interview invitation to the first candidate
    print(f"\nSending interview invitation to {candidate_email}...")
    book_interview(candidate_email)