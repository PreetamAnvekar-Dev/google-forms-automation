
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# =====================================================
# CONFIGURATION
# =====================================================

SCOPES = [
    "https://www.googleapis.com/auth/forms.body"
]

# Leave empty to create a new form.
# Provide an existing Form ID to update a form.
FORM_ID = ""

# Customize these values.
FORM_TITLE = "My Automated Google Form"

FORM_DESCRIPTION = """
Welcome!

Thank you for your interest.

Please complete this form with the requested information.
All required fields must be completed before submission.

Thank you!
"""

# =====================================================
# FORM QUESTIONS
# =====================================================

QUESTIONS = [
    {
        "title": "Full Name",
        "type": "TEXT",
        "required": True
    },
    {
        "title": "Email Address",
        "type": "TEXT",
        "required": True
    },
    {
        "title": "Phone Number",
        "type": "TEXT",
        "required": False
    },
    {
        "title": "Organization",
        "type": "TEXT",
        "required": False
    },
    {
        "title": "Select Your Category",
        "type": "RADIO",
        "options": [
            "Student",
            "Working Professional",
            "Business Owner",
            "Other"
        ],
        "required": True
    },
    {
        "title": "Areas of Interest",
        "type": "CHECKBOX",
        "options": [
            "Technology",
            "Programming",
            "Artificial Intelligence",
            "Data Science",
            "Cloud Computing",
            "Other"
        ],
        "required": True
    },
    {
        "title": "Additional Comments",
        "type": "PARAGRAPH",
        "required": False
    }
]


# =====================================================
# AUTHENTICATION
# =====================================================

def authenticate():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


# =====================================================
# QUESTION VALIDATION
# =====================================================

def validate_questions():

    allowed_types = [
        "TEXT",
        "PARAGRAPH",
        "RADIO",
        "CHECKBOX"
    ]

    for question in QUESTIONS:

        if not question.get("title"):
            raise ValueError("Question title cannot be empty.")

        question_type = question.get("type")

        if question_type not in allowed_types:
            raise ValueError(
                f"Unsupported question type: {question_type}"
            )

        if question_type in ["RADIO", "CHECKBOX"]:

            options = question.get("options", [])

            if not options:
                raise ValueError(
                    f"Options are required for: {question['title']}"
                )


# =====================================================
# CREATE QUESTION ITEM
# =====================================================

def make_item(data):

    question = {
        "required": data.get("required", False)
    }

    question_type = data["type"]

    if question_type == "TEXT":

        question["textQuestion"] = {
            "paragraph": False
        }

    elif question_type == "PARAGRAPH":

        question["textQuestion"] = {
            "paragraph": True
        }

    elif question_type in ["RADIO", "CHECKBOX"]:

        question["choiceQuestion"] = {
            "type": question_type,
            "options": [
                {"value": option}
                for option in data["options"]
            ],
            "shuffle": False
        }

    return {
        "title": data["title"],
        "questionItem": {
            "question": question
        }
    }


# =====================================================
# CREATE OR UPDATE FORM
# =====================================================

def create_or_update_form(service):

    global FORM_ID

    if FORM_ID:

        form = service.forms().get(
            formId=FORM_ID
        ).execute()

        print("Updating existing form:", form["info"]["title"])

    else:

        form = service.forms().create(
            body={
                "info": {
                    "title": FORM_TITLE
                }
            }
        ).execute()

        FORM_ID = form["formId"]

        print("Created new form:", FORM_ID)

    existing_items = form.get("items", [])

    existing_titles = {
        item.get("title", "").strip().lower()
        for item in existing_items
    }

    requests = [
        {
            "updateFormInfo": {
                "info": {
                    "description": FORM_DESCRIPTION
                },
                "updateMask": "description"
            }
        }
    ]

    next_index = len(existing_items)

    added = 0
    skipped = 0

    for data in QUESTIONS:

        title = data["title"].strip().lower()

        if title in existing_titles:

            print("Skipping existing question:", data["title"])
            skipped += 1
            continue

        requests.append({
            "createItem": {
                "item": make_item(data),
                "location": {
                    "index": next_index
                }
            }
        })

        next_index += 1
        added += 1

    service.forms().batchUpdate(
        formId=FORM_ID,
        body={
            "requests": requests
        }
    ).execute()

    print("\n========== FORM SUMMARY ==========")

    print("Form ID:", FORM_ID)
    print("New questions added:", added)
    print("Existing questions skipped:", skipped)

    print(
        "\nEdit URL:",
        f"https://docs.google.com/forms/d/{FORM_ID}/edit"
    )

    print(
        "\nRegistration URL:",
        f"https://docs.google.com/forms/d/{FORM_ID}/viewform"
    )


# =====================================================
# MAIN FUNCTION
# =====================================================

def main():

    validate_questions()

    if not os.path.exists("credentials.json"):
        raise FileNotFoundError(
            "credentials.json not found. "
            "Configure Google OAuth credentials first."
        )

    credentials = authenticate()

    service = build(
        "forms",
        "v1",
        credentials=credentials
    )

    create_or_update_form(service)


if __name__ == "__main__":
    main()
