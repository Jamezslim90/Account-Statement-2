import requests
from datetime import datetime, timedelta
from fpdf import FPDF
from jinja2 import Template
import os

# Constants
BACKEND_API_URL = "https://api.example.com/customers/active-accounts"  # Placeholder for the backend API
EMAIL_API_URL = "https://api.emailservice.com/send-email"              # Placeholder for the email service API
API_KEY = "your_email_api_key"                                         # Placeholder for API key
STATEMENT_PERIOD_DAYS = 30                                             # Set to 30 days for a month

# Fetch all active customer bank account data
def fetch_customer_data():
    response = requests.get(BACKEND_API_URL)
    response.raise_for_status()
    return response.json()  # Assuming response is in JSON format

# Generate PDF statement for each account
def generate_pdf(account, transactions):
    pdf = FPDF()
    pdf.add_page()

    # Add a title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Bank Statement for {account['account_holder']}", ln=True, align='C')

    # Account details
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Account Number: {account['account_number']}", ln=True)
    pdf.cell(200, 10, f"Email: {account['email']}", ln=True)
    pdf.cell(200, 10, f"Statement Period: Last {STATEMENT_PERIOD_DAYS} Days", ln=True)
    pdf.cell(200, 10, "", ln=True)

    # Transactions table header
    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 10, "Date", border=1)
    pdf.cell(40, 10, "Branch", border=1)
    pdf.cell(50, 10, "Details", border=1)
    pdf.cell(30, 10, "Withdrawals", border=1)
    pdf.cell(30, 10, "Deposits", border=1)
    pdf.cell(0, 10, "Balance", border=1, ln=True)

    # Transactions data
    pdf.set_font("Arial", "", 10)
    for txn in transactions:
        pdf.cell(40, 10, txn["date"], border=1)
        pdf.cell(40, 10, txn["branch"], border=1)
        pdf.cell(50, 10, txn["details"], border=1)
        pdf.cell(30, 10, str(txn["withdrawal"]), border=1)
        pdf.cell(30, 10, str(txn["deposit"]), border=1)
        pdf.cell(0, 10, str(txn["balance"]), border=1, ln=True)

    # Save PDF
    file_name = f"{account['account_number']}_statement.pdf"
    pdf.output(file_name)
    return file_name

# Prepare email template with Jinja2
def prepare_email_template(account_holder):
    template = Template("""
    <html>
    <body>
        <h2>Dear {{ account_holder }},</h2>
        <p>Please find attached your bank statement for the last {{ days }} days.</p>
        <p>Thank you for banking with us!</p>
        <p>Best regards,<br>Your Bank</p>
    </body>
    </html>
    """)
    return template.render(account_holder=account_holder, days=STATEMENT_PERIOD_DAYS)

# Send the email with the PDF attached
def send_email(account, pdf_file):
    with open(pdf_file, "rb") as file:
        payload = {
            "to": account["email"],
            "subject": "Your Monthly Bank Statement",
            "html_body": prepare_email_template(account["account_holder"]),
            "attachments": {
                "file_name": pdf_file,
                "file_data": file.read(),
                "mime_type": "application/pdf"
            }
        }
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.post(EMAIL_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Email sent to {account['email']}")

# Main processing function
def process_statements():
    customer_data = fetch_customer_data()
    for account in customer_data:
        transactions = account["transactions"]
        filtered_transactions = [
            txn for txn in transactions if datetime.strptime(txn["date"], "%Y-%m-%d") >= datetime.now() - timedelta(days=STATEMENT_PERIOD_DAYS)
        ]
        pdf_file = generate_pdf(account, filtered_transactions)
        send_email(account, pdf_file)
        os.remove(pdf_file)  # Clean up the PDF files 

if __name__ == "__main__":
    process_statements()
