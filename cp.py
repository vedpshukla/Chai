import smtplib
import random
import datetime

def send_email(sender_email, sender_password, recipient_email, cc_emails, subject, message):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        headers = f"From: {sender_email}\r\nTo: {recipient_email}\r\nCC: {','.join(cc_emails)}\r\nSubject: {subject}\r\n\r\n"
        email_message = headers + message
        server.sendmail(sender_email, [recipient_email] + cc_emails, email_message)

def select_random_member(members):
    return random.choice(members)

# Set the email credentials and details
sender_email = "vedshuklasln@gmail.com"
sender_password = "abc"
subject = "Chai Treat Reminder"

team_members = [
    {"email": "abc", "name": ""},
    {"email": "abc@mail.com", "name": ""},
    {"email": "", "name": ""},
    {"email": "", "name": ""},
    {"email": "", "name": ""},
    {"email": "", "name": ""},
    {"email": "", "name": ""},
    {"email": "', "name": ""},
    # Add more members 
]


today = datetime.datetime.now().date()
if today.weekday() >= 5:  # 5 and 6 represent Saturday and Sunday
    print("It's a weekend. No chai treat today.")
    exit()

recipient_member = None
cc_members = [member for member in team_members]  # Create a copy of team_members initially
while recipient_member is None:
    selected_member = select_random_member(cc_members)
    if selected_member != recipient_member:
        recipient_member = selected_member
        cc_members.remove(selected_member)

recipient_name = recipient_member["name"]
message = f"Hello {recipient_name}! It's your turn for the chai treat today. Enjoy your day!"
print(message)


#send_email(sender_email, sender_password, recipient_member["email"], [member["email"] for member in cc_members], subject, message)
