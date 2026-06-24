import os
import mimetypes
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class INException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{self.message}"

def getConfigPath():
    allFiles = list()
    for i in os.listdir():
        if (i.endswith(".json")):
            allFiles.append(i)
    if len(allFiles) == 1:
        return allFiles[0]

    print("multiple configuration files were found in this directory:")
    for i in allFiles:
        print(f" ({allFiles.index(i) + 1}) {i}")
    print(f"which configuration would you like to use?")

    userInput = ""
    while True:
        try:
            userInput = input(f"(1-{len(allFiles)}): ")
            userInput = int(userInput)
            if userInput < 1 or userInput > len(allFiles):
                raise INException("Invalid Number!")
            break
        except ValueError:
            print("Invalid input!")
        except INException as e:
            print(e)
    
    return allFiles[userInput - 1]

def sendMail(data):
    ### init ###
    sender = data["sender-address"]
    pw = data["sender-pw"]
    files = data["file-attachments"]

    ### create mail and send ###
    for recipient in data["recipients"]:

        ### fill ###
        message = MIMEMultipart()
        message["From"] = sender 
        message["To"] = recipient
        message["Subject"] = "Auto Mail"

        body = f"""Hallo {recipient.split("@")[0]}!
    Diese E-Mail wird automatisiert versendet!
    Es sollte auch ein Anhang dabei sein...

    Hoffe es funktioniert!

    LG
    {sender.split("@")[0]}
    """
        message.attach(MIMEText(body, "plain"))

        ### add files ###
        for path in files:
            filename = os.path.basename(path)
            ctype, encoding = mimetypes.guess_type(path)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            with open(path, "rb") as f:
                part = MIMEBase(maintype, subtype)
                part.set_payload(f.read())

                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
                message.attach(part)

        ### send ###
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.ehlo()
            server.login(sender, pw)
            server.ehlo()
            server.sendmail(sender, recipient, message.as_string())

def dataIsValid(data):
    ### check validity of json ###
    try:
        data["sender-address"]
        data["sender-pw"]
        data["recipients"]
        data["file-attachments"]
        return True
    except KeyError:
        return False