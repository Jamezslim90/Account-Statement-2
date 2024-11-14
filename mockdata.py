from datetime import datetime, timedelta
from fpdf import FPDF
from jinja2 import Template
import os
import random

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
            for i in range(45)  # 45 days of mock transactions
        ]
    },
    {
        "account_holder": "Jane Smith",
        "account_number": "987654321",
        "email": "jane.smith@example.com",
        "transactions": [
            {
                "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                "branch": "Downtown Branch",
                "details": "Deposit",
                "withdrawal": 0,
                "deposit": round(random.uniform(50, 1000), 2),
                "balance": round(random.uniform(2000, 6000), 2)
            }
            for i in range(45)  # 45 days of mock transactions
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
def prepare_email_template(account_holder):
    template = Template("""
    <html>
    <body>
        <h2>Dear {{ account_holder }},</h2>
        <p>Please find attached your bank statement for the last 30 days.</p>
        <p>Thank you for banking with us!</p>
        <p>Best regards,<br>Your Bank</p>
    </body>
    </html>
    """)
    return template.render(account_holder=account_holder)

# Mock email sending function
def send_email(account, pdf_file):
    email_content = prepare_email_template(account["account_holder"])
    print(f"Mock sending email to {account['email']}")
    print(f"Email Subject: Your Monthly Bank Statement")
    print(f"Email Body:\n{email_content}")
    print(f"PDF Attachment: {pdf_file} (not actually attached in mock)")

# Main processing function
def process_statements():
    
    # Make API Calls to retrieve Account details
    # Loop through each data

    for account in MOCK_CUSTOMER_DATA:
        # Filter transactions for the last 30 days
        filtered_transactions = [
            txn for txn in account["transactions"] if datetime.strptime(txn["date"], "%Y-%m-%d") >= datetime.now() - timedelta(days=30)
        ]
        # Generate PDF
        pdf_file = generate_pdf(account, filtered_transactions)
        # Mock email sending
        send_email(account, pdf_file)
        # Clean up the PDF file
        os.remove(pdf_file)

if __name__ == "__main__":
    process_statements()
