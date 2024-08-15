import streamlit as st
from datetime import datetime, timedelta

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

receiver_email = st.text_input("Ton Email")
st.write("The current movie title is", receiver_email)

# Initialiser le nombre de champs dans session_state
if 'input_count' not in st.session_state:
    st.session_state.input_count = 3  # Par défaut, on commence avec 3 champs

# Fonction pour ajouter un nouveau champ d'input
def add_input():
    st.session_state.input_count += 1


race_1_hour = st.number_input("Heures", min_value=0, max_value=23, key="race_1_hour")
race_1_min = st.number_input("Minutes", min_value=0, max_value=59, key="race_1_min")
race_1_sec = st.number_input("Secondes", min_value=0, max_value=59, key="race_1_sec")

st.write("Heures", race_1_hour)
st.write("Minutes", race_1_min)
st.write("Secondes", race_1_sec)

race_2_hour = st.number_input("Heures", min_value=0, max_value=23, key="race_2_hour")
race_2_min = st.number_input("Minutes", min_value=0, max_value=59, key="race_2_min")
race_2_sec = st.number_input("Secondes", min_value=0, max_value=59, key="race_2_sec")



### TEST

if 'input_count' not in st.session_state:
    st.session_state.input_count = 3  # Par défaut, on commence avec 3 champs

# Fonction pour ajouter un nouveau champ d'input
def add_input():
    st.session_state.input_count += 1

# Afficher les champs d'input
st.write("Entrez les valeurs :")
for i in range(st.session_state.input_count):
    st.text_input(f'Input {i + 1}', key=f'input_{i}')

# Bouton pour ajouter un nouveau champ d'input
if st.button('Ajouter un champ'):
    add_input()

# Afficher les valeurs saisies
st.write("Les valeurs saisies :")
for i in range(st.session_state.input_count):
    st.write(f"Input {i + 1}: {st.session_state[f'input_{i}']}")




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
