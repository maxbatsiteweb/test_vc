import streamlit as st
from datetime import datetime, timedelta

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

receiver_email = st.text_input("Ton Email")
st.write("The current movie title is", receiver_email)

import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression

# Données des courses : distances en mètres et temps en secondes
distances_options = {
    "5 km": 5000,
    "10 km": 10000,
    "20 km": 20000,
    "Semi-marathon": 21097.5,
    "Marathon": 42195
}

# Fonction pour calculer la vitesse en m/s
def calculate_speed(distance, hours, minutes, seconds):
    total_seconds = hours * 3600 + minutes * 60 + seconds
    speed = distance / total_seconds
    return speed, total_seconds

# Sélection des distances
st.write("# Choix des courses")

# Utilisation des colonnes pour afficher les inputs côte à côte

st.write("# Choix des courses")

# Course 1
col1, col2, col3, col4 = st.columns(4)
with col1:
    distance_1 = st.selectbox("Distance de la course 1", list(distances_options.keys()))
with col2:
    hours_1 = st.number_input("Heures", min_value=0, max_value=23, value=0, key="heures_1")
with col3:
    minutes_1 = st.number_input("Minutes", min_value=0, max_value=59, value=0, key="minutes_1")
with col4:
    seconds_1 = st.number_input("Secondes", min_value=0, max_value=59, value=0, key="secondes_1")

# Course 2
col1, col2, col3, col4 = st.columns(4)
with col1:
    distance_2 = st.selectbox("Distance de la course 2", [dist for dist in distances_options.keys() if dist != distance_1])
with col2:
    hours_2 = st.number_input("Heures", min_value=0, max_value=23, value=0, key="heures_2")
with col3:
    minutes_2 = st.number_input("Minutes", min_value=0, max_value=59, value=0, key="minutes_2")
with col4:
    seconds_2 = st.number_input("Secondes", min_value=0, max_value=59, value=0, key="secondes_2")

# Vérification avant de calculer les vitesses
def calculate_speed_safe(distance, hours, minutes, seconds):
    total_seconds = hours * 3600 + minutes * 60 + seconds
    if total_seconds > 0:
        speed = distance / total_seconds
    else:
        speed = 0
    return speed, total_seconds

# Calcul des vitesses et temps avec vérification
speed_1, total_seconds_1 = calculate_speed_safe(distances_options[distance_1], hours_1, minutes_1, seconds_1)
speed_2, total_seconds_2 = calculate_speed_safe(distances_options[distance_2], hours_2, minutes_2, seconds_2)

# Affichage ou utilisation des vitesses et temps uniquement si les valeurs sont valides
if total_seconds_1 > 0 and total_seconds_2 > 0:
    # Continuez avec la régression linéaire et les autres calculs ici
    pass
else:
    st.write("Veuillez entrer des valeurs valides pour le temps de chaque course.")

if total_seconds_1 > 0 and total_seconds_2 > 0:
    # Réaliser la régression linéaire avec Scikit-learn
    X = np.log(np.array([total_seconds_1, total_seconds_2])).reshape(-1, 1)
    y = np.log(np.array([speed_1, speed_2]))
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Extraction des coefficients
    a = model.coef_[0]
    b = model.intercept_
    
    # Calcul des paramètres E et S
    E_opt = a + 1
    S_opt = np.exp(b)
    
    # Affichage des résultats
    st.write("## Résultats de la régression linéaire")
    st.write(f"Constante E : {E_opt:.4f}")
    st.write(f"Constante S : {S_opt:.4f}")
    
    # Prédictions pour les distances spécifiées
    st.write("## Prédictions pour d'autres distances")
    predictions = {}
    for dist_name, dist_value in distances_options.items():
        # Temps prédit en utilisant la relation: ln(T) = (1/E) * (ln(S) + ln(D)) + (1/E) * ln(T)
        pred_time = np.exp((1/E_opt) * (np.log(dist_value) - np.log(S_opt)))
        hours, remainder = divmod(pred_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        predictions[dist_name] = pred_time
        st.write(f"{dist_name} : {predictions[dist_name]}")
    
    # Affichage des temps et vitesses
    st.write("## Détails des courses")
    st.write(f"Course 1 : {distances_options[distance_1] / 1000:.1f} km en {hours_1} heures, {minutes_1} minutes, {seconds_1} secondes.")
    st.write(f"Vitesse moyenne de la Course 1 : {speed_1:.2f} m/s")
    st.write(f"Course 2 : {distances_options[distance_2] / 1000:.1f} km en {hours_2} heures, {minutes_2} minutes, {seconds_2} secondes.")
    st.write(f"Vitesse moyenne de la Course 2 : {speed_2:.2f} m/s")

else:
    st.write("Veuillez entrer des valeurs valides pour les deux courses (temps non nul).")



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
