import streamlit as st
from datetime import datetime, timedelta

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

receiver_email = st.text_input("Ton Email")
st.write("The current movie title is", receiver_email)





### TEST


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Fonction pour afficher les inputs pour une course
def course_input_block(course_name):
    st.write(f"## {course_name}")

    # Distance en mètres dans les inputs
    distance = st.number_input(f"Distance de la {course_name} (en mètres)", min_value=0, value=0)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        heures = st.number_input(f"Heures", min_value=0, max_value=23, value=0, key=f"{course_name}_heures")
    with col2:
        minutes = st.number_input(f"Minutes", min_value=0, max_value=59, value=0, key=f"{course_name}_minutes")
    with col3:
        secondes = st.number_input(f"Secondes", min_value=0, max_value=59, value=0, key=f"{course_name}_secondes")
    
    return distance, heures, minutes, secondes

# Affichage des deux blocs d'input
st.write("# Informations sur les courses")

st.write("### Course 1")
distance_1, heures_1, minutes_1, secondes_1 = course_input_block("Course 1")

st.write("### Course 2")
distance_2, heures_2, minutes_2, secondes_2 = course_input_block("Course 2")

# Calcul du temps total



### Partie Mail
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "An email with attachment from Python"
body = "This is an email with attachment sent from Python"
sender_email = "maximebataille95@gmail.com"
password = "upqm tezg vljv zhuh"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

filename = "document.pdf"  # In same directory as script


# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()


### Provisoire
'''
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)

'''
