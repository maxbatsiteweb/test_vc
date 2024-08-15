import streamlit as st
from datetime import datetime, timedelta

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

receiver_email = st.text_input("Ton Email")
st.write("The current movie title is", receiver_email)





### TEST

if 'input_count' not in st.session_state:
    st.session_state.input_count = 2  # Par défaut, on commence avec 3 champs

# Initialiser chaque champ d'input dans session_state si ce n'est pas déjà fait
for i in range(st.session_state.input_count):
    key = f'input_{i}'
    if key not in st.session_state:
        st.session_state[key] = ""

# Fonction pour ajouter un nouveau champ d'input
def add_input():
    st.session_state.input_count += 1
    # Initialiser le nouveau champ d'input
    st.session_state[f'input_{st.session_state.input_count - 1}'] = ""

# Afficher les champs d'input
st.write( st.session_state.input_count)
for i in range(st.session_state.input_count):
    st.write(i)
    st.number_input("Heures", key=f'input_hour_{i}')
    st.number_input("Minutes", key=f'input_min_{i}')
    st.number_input("Secondes", key=f'input_sec_{i}')

# Bouton pour ajouter un nouveau champ d'input
if st.button('Ajouter un champ'):
    add_input()

# Afficher les valeurs saisies
st.write("Les valeurs saisies :")
for i in range(st.session_state.input_count):
    st.write(f"Heures: {st.session_state[f'input_hour_{i}']}")
    st.write(f"Minutes: {st.session_state[f'input_min_{i}']}")
    st.write(f"Secondes: {st.session_state[f'input_sec_{i}']}")




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
