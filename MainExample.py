# imports
from pprint import pprint


# Created class for the emails
class Email:
    def __init__(self, email_sender, email_subject, email_content):
        self.email_sender = email_sender
        self.email_subject = email_subject
        self.email_content = email_content

# Create received email list
emails = [
    Email("bigNews@bignews.corp.org", "Zuckeberg to fight Musk", "Drama heats up as Mark and Elon snap back at eachother..."),
    Email("tomgo@gmail.com", "About that game", "Hey that game that you told me about..."),
    Email("JakeWork@gmail.com", "You broke the database again", "You did it again, the whole app is down.."),
    Email("tomgo@gmail.com", "When is our next meetup", "Hey we said we would meet up soon, when would that be..."),
    Email("JakeWork@gmail.com", "How many times, I Swear", "How many gosh darn times do I need to tell you not to push to the main branch go...")
]

# Create ditionary per sender
emails_by_sender = {}

# Sort based on sender
for email in emails:
    email_sender = email.email_sender
    if email_sender not in emails_by_sender:
        emails_by_sender[email_sender] = []
    emails_by_sender[email_sender].append(email)
        
# Printing
for email_sender, sender_email in emails_by_sender.items():
    print("")
    print(f"Sent by: {email_sender}")
    print("")
    for email in sender_email:
        obj_vars = vars(email)
        pprint(obj_vars, sort_dicts=False)
        print("")
    