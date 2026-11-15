# 🚀 Google Forms Automation Using Python

Automate Google Forms creation and management using Python, Google Forms API, and OAuth 2.0.

 Python 3.9+ Google Forms API OAuth 2.0 MIT License

## 📌 About

A reusable Python application to create and update Google Forms programmatically. Customize form titles, descriptions, questions, and answer options through simple configurations.

## ✨ Features

- Automatic Google Form creation.
- Update existing forms.
- Support multiple question types.
- Prevent duplicate questions.
- Google OAuth 2.0 authentication.
- Automatic form URL generation.

## 🛠️ Tech Stack

- Python
- Google Forms API
- Google OAuth 2.0
- Google Auth
- Google API Client

## 📂 Project Structure

```
google-forms-automation/

│ ├── main.py ├── requirements.txt ├── README.md ├── index.html ├── LICENSE └── .gitignore
```

## ⚙️ Installation

```
git clone https://github.com/PreetamAnvekar-Dev/google-forms-automation.git

cd google-forms-automation

python -m venv venv

pip install -r requirements.txt

python main.py
```

## 📦 Dependencies

```
google-auth

google-auth-oauthlib google-api-python-client
```

## ☁️ Google Cloud Setup

1. Create a project in Google Cloud Console.
2. Enable Google Forms API.
3. Configure the OAuth consent screen.
4. Create Desktop App OAuth credentials.
5. Download and save as credentials.json.

 [Google Cloud Console](https://console.cloud.google.com/)

## 📋 Supported Question Types

- TEXT – Short answers
- PARAGRAPH – Long answers
- RADIO – Single choice
- CHECKBOX – Multiple choice
