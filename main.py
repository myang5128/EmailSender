# import libraries
import smtplib
from email.message import EmailMessage
import random as rand
import pandas as pd
import os

# credentials
my_email = "automatedsender2@gmail.com"
test_email = ["automatedsendee2@gmail.com"]
password = "sozd znqf fxrn myqp"

# grab quotes
def grab_quotes():
    quote_data = pd.read_csv('data\insparation.csv')
    random_index = rand.randrange(0, len(quote_data))
    currentQuote = quote_data.iloc[random_index]
    return currentQuote.Quote

# grab facts
def grab_facts():
    fact_data = pd.read_csv(r'data\animal-fun-facts-dataset.csv')
    random_index = rand.randrange(0, len(fact_data))
    currentFact = fact_data.iloc[random_index]
    fact = currentFact.text 
    if fact[0] == '"':
        fact = fact[1:-2]
    return fact

# grab emails
def grab_emails():
    file_path = 'data\email_list.txt'
    email_list = []
    with open(file_path, 'r') as file:
        contents = file.readlines()
        for content in contents:
            if content[0] != '#':
                content = content.replace(" ", "")
                content = content.replace("\n", "")
                email_list.append(content)
    return email_list

# grab poems
def grab_poems():
    folder_path = 'poem_file'
    
    subfolders = next(os.walk(folder_path))[1]
    num_subfolders = len(subfolders)
    random_folder = rand.randrange(0, num_subfolders)
    subfolder = subfolders[random_folder]
    subfolder_path = 'poem_file/' + subfolder + '/'
    file_list = os.listdir(subfolder_path)
    random_file = rand.randrange(0, len(file_list))
    random_file = file_list[random_file]
    file_path = os.path.join(subfolder_path, random_file)
    print(file_path)
    
    with open(file_path, 'r') as file:
        # Read the file line by line and preserve line breaks
        # check to see if file is valid, if not, redo
        try:
            contents = file.read()
            # Replace newline characters with HTML line breaks
            contents_html = contents.replace('\n', '<br>')
            return contents_html
        except:
            grab_poems()
    
# send email
def send_email(quote_content, poem_content, fact_content, email_list):
    # change email_list to test_email for testing
    for email in email_list:
        # html styling
        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    line-height: 1.5;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                .quote {{
                    margin-bottom: 20px;
                }}
                .message {{
                    font-style: italic;
                    color: #555555;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="quote">
                    <h2>{'Your Daily Quote:'}</h2>
                    <p>{quote_content}</p>
                </div>
                <div class="fact">
                    <h2>{'Your Daily Animal Fact:'}</h2>
                    <p>{fact_content}</p>
                </div>
                <div class="poem">
                    <h2>{'Your Daily Poem:'}</h2>
                    <p>{poem_content}</p>
                </div>
                <div class="message">
                    <p>Here's your reminder! Good luck and and enjoy life!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # generate email content
        msg = EmailMessage()
        msg.set_content(html_content, subtype='html')
        msg['Subject'] = 'Daily Inspirational Quote'
        msg['From'] = 'Daily Inspirations <' + my_email + '>'
        msg['To'] = email

        # establish connection
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.send_message(msg)
            print()
            print(f"Finished sending email to {email}!")
            print()

def main():
    quote = grab_quotes()
    poem = grab_poems()
    facts = grab_facts()
    email = grab_emails()
    send_email(quote, poem, facts, email)
    
main()