import mysql.connector
from datetime import datetime
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
import time 
while True:
    # Today's date in the same format as the database expiry dates
    today = datetime.now().strftime('%Y-%m-%d')
    from datetime import datetime, timedelta
    # Get the current date
    today = datetime.now()
    # Add ten days to the current date
    future_date = today + timedelta(days=10)
    # Convert the future date to the desired format
    future_date_formatted = future_date.strftime('%Y-%m-%d')
    today = future_date_formatted


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
        #print('expiry dates ', expiry_dates)
        for product in products:
            print('pro', product)
            #  1. Laser Mouse: 2024-04-26, 2. Dual XL Monitors: 2024-04-26, 3. Multi-jet Printer: 2024-04-26
            try:
                name, expiry = product.split(':')
                if expiry.strip() == today:
                    # Send email if the expiry date matches today
                    subject = f"Expiration Notice for {name.strip()}"
                    body = f"Dear Customer, \n\nYour product {name.strip()} will expire today on {expiry.strip()}. Please consider renewing your product. \n\nBest regards,\nYour Company"
                    send_email(email, subject, body)
                    print('mail sent ', email, subject)
                    time.sleep(2)
            except Exception as exp:
                print('issue', exp, product)
    # Close the database connection
    cursor.close()
    db.close()
    print('sleep 5min ', end='')
    time.sleep(300)
