import smtplib, ssl
from email.message import EmailMessage
from datetime import datetime, timedelta
from fpdf import FPDF
from jinja2 import Template
import os
import random

# Email configuration
EMAIL_HOST = "smtp.office365.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "jamezslim90@gmail.com"       
EMAIL_HOST_PASSWORD = "boiyhaxzidarokpp"       
DEFAULT_FROM_EMAIL = "TajBank <statement@gmail.com>"

# Mock data for customer accounts and transactions
MOCK_CUSTOMER_DATA = [
    {
        "account_holder": "James Inaz",
        "account_number": "1234567890",
        "email": "iamsundayjames@gmail.com",
        "transactions": [
            {
                "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                "branch": "Main Branch",
                "details": "Payment",
                "withdrawal": round(random.uniform(20, 500), 2),
                "deposit": 0,
                "balance": round(random.uniform(1000, 5000), 2)
            }
            for i in range(45)
        ]
    },
    {
        "account_holder": "Abdul Umar",
        "account_number": "9876543210",
        "email": "james.inalegwu@tajbank.com",
        "transactions": [
            {
                "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                "branch": "Downtown Branch",
                "details": "Deposit",
                "withdrawal": 0,
                "deposit": round(random.uniform(50, 1000), 2),
                "balance": round(random.uniform(2000, 6000), 2)
            }
            for i in range(45)
        ]
    }
]

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
    pdf.cell(200, 10, "Statement Period: Last 30 Days", ln=True)
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
# def prepare_email_template(account_holder):
#     template = Template("""
#     <html>
#     <body>
#         <h2>Dear {{ account_holder }},</h2>
#         <p>Please find attached your bank statement for the last 30 days.</p>
#         <p>Thank you for banking with us!</p>
#         <p>Best regards,<br>Your Bank</p>
#     </body>
#     </html>
#     """)
#     return template.render(account_holder=account_holder)

# Prepare email template with Jinja2 and inline CSS
def prepare_email_template(account_holder):
    template = Template("""
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            .email-container {
                max-width: 600px;
                margin: auto;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .header {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                text-align: center;
                font-size: 1.5em;
            }
            .content {
                padding: 20px;
            }
            h2 {
                color: #333;
                font-size: 1.4em;
            }
            p {
                line-height: 1.6;
                margin: 8px 0;
            }
            .footer {
                padding: 10px;
                text-align: center;
                font-size: 0.9em;
                color: #777;
                border-top: 1px solid #e0e0e0;
            }
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                Monthly Bank Statement
            </div>
            <div class="content">
                <h2>Dear {{ account_holder }},</h2>
                <p>Please find attached your bank statement for the last 30 days.</p>
                <p>Thank you for banking with us!</p>
                <p>Best regards,<br>Your Bank</p>
            </div>
            <div class="footer">
                &copy; {{ current_year }} TajBank - All Rights Reserved
            </div>
        </div>
    </body>
    </html>
    """)
    return template.render(account_holder=account_holder, current_year=datetime.now().year)



# Send email with Gmail SMTP
def send_email(account, pdf_file):
    email_content = prepare_email_template(account["account_holder"])

    # Configure email message
    msg = EmailMessage()
    msg["Subject"] = "Your Monthly Bank Statement"
    msg["From"] = DEFAULT_FROM_EMAIL
    msg["To"] = account["email"]
    msg.set_content("Please see the attached PDF for your monthly statement.", subtype="plain")
    msg.add_alternative(email_content, subtype="html")

    # Attach PDF
    with open(pdf_file, "rb") as file:
        msg.add_attachment(
            file.read(),
            maintype="application",
            subtype="pdf",
            filename=pdf_file
        )

    # Send email via Gmail SMTP
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.ehlo()
            server.starttls()  # Secure the connection
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(msg)
            print(f"Email sent to {account['email']}")

    except Exception as e:
        print(f"Failed to send email to {account['email']}: {e}")


# Main processing function
def process_statements():
    for account in MOCK_CUSTOMER_DATA:
        # Filter transactions for the last 30 days
        filtered_transactions = [
            txn for txn in account["transactions"] if datetime.strptime(txn["date"], "%Y-%m-%d") >= datetime.now() - timedelta(days=30)
        ]
        # Generate PDF
        pdf_file = generate_pdf(account, filtered_transactions)
        # Send email
        send_email(account, pdf_file)
        # Clean up the PDF file
        os.remove(pdf_file)

if __name__ == "__main__":
    process_statements()
