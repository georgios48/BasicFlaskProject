# Here all the validity functions can be stored
# I will be using just for email

import re

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# function to check if the email is in valid format
def email_check(email):
    if re.fullmatch(email_regex, email):
        return email
