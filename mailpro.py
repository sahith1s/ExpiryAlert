import mysql.connector
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Database credentials and SMTP settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'expiry'
}

smtp_server = 'smtp.gmail.com'
smtp_port = 587  # typically 587 for TLS
smtp_user = 'expiryrem@gmail.com'
smtp_password = 'ouqd afvt qikr nzds'

# Connect to the database
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

# Today's date in the same format as the database expiry dates
today = datetime.now()
# Add ten days to the current date
future_date = today + timedelta(days=10)
# Convert the future date to the desired format
today = future_date.strftime('%Y-%m-%d')

# SQL query to fetch relevant columns
query = "SELECT email, product_names, expire_dates FROM invoice"
cursor.execute(query)

# Function to send emails
def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    text = msg.as_string()
    server.sendmail(smtp_user, recipient, text)
    server.quit()

# Process each record
for (email, product_names, expiry_dates) in cursor:
    # Parse the expiry dates string and check if any dates match today
    products = expiry_dates.split(',')
    print('expiry dates ', expiry_dates)
    for product in products:
        print('pro', product)
        # Split the product name and expiry date
        parts = product.split(':')
        if len(parts) == 2:
            name, expiry = parts
            name = name.strip()
            expiry = expiry.strip()
            if expiry == today:
                # Send email if the expiry date matches today
                subject = f"Expiration Notice for {name}"
                body = f"Dear Customer, \n\nYour product {name} will expire today on {expiry}. Please consider renewing your product. \n\nBest regards,\nYour Company"
                send_email(email, subject, body)

# Close the database connection
cursor.close()
db.close()
