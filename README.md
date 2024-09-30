# JAZZEE
# Resume Filter and Interview Scheduler

This project is a Streamlit application that allows recruiters to filter resumes based on a given job description and schedule interviews with top candidates via email.

## Features

- **Resume Filtering**: Utilizes cosine similarity to rank candidate resumes against a specified job description using TF-IDF vectorization.
- **Email Notification**: Sends an email to the selected candidate to schedule an interview.
- **User-Friendly Interface**: Built with Streamlit for easy interaction and use.

## Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- SMTP for email notifications

## Requirements

To run this application, ensure you have the following Python packages installed:

```bash
pip install streamlit pandas scikit-learn
