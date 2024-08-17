import streamlit as st
from datetime import datetime, timedelta
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import numpy as np
from sklearn.linear_model import LinearRegression
import re

# Logo en haut à gauche
st.image("logo.png", width=150)

# Titre et description
st.title("Estimation des temps par la loi de Puissance")
st.write("[Source](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10858092/).")
st.write("Jonah P. Drake, Axel Finke, and Richard A. Ferguson (2023) Modelling human endurance: power laws vs critical power")
st.write("Indique au moins deux courses durant lesquelles tu as donné ton maximum et durant lesquelles les conditions étaient bonnes. Les performances doivent de préférence être récentes.")
st.write("Tu recevras par e-mail les estimations de performance sur 5km, 10km, 20km, semi-marathon et marathon.")

# Initialisation de st.session_state si nécessaire
if 'distance_1' not in st.session_state:
    st.session_state.distance_1 = "5 km"
if 'hours_1' not in st.session_state:
    st.session_state.hours_1 = 0
if 'minutes_1' not in st.session_state:
    st.session_state.minutes_1 = 0
if 'seconds_1' not in st.session_state:
    st.session_state.seconds_1 = 0
if 'distance_2' not in st.session_state:
    st.session_state.distance_2 = "10 km"
if 'hours_2' not in st.session_state:
    st.session_state.hours_2 = 0
if 'minutes_2' not in st.session_state:
    st.session_state.minutes_2 = 0
if 'seconds_2' not in st.session_state:
    st.session_state.seconds_2 = 0
if 'receiver_name' not in st.session_state:
    st.session_state.receiver_name = ""
if 'receiver_email' not in st.session_state:
    st.session_state.receiver_email = ""
if 'checkbox' not in st.session_state:
    st.session_state.checkbox = False

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

# Fonction pour calculer la vitesse en m/s en toute sécurité
def calculate_speed_safe(distance, hours, minutes, seconds):
    total_seconds = hours * 3600 + minutes * 60 + seconds
    if total_seconds > 0:
        speed = distance / total_seconds
    else:
        speed = 0
    return speed, total_seconds

# Sélection des distances
st.write("# Choix des courses")

# Utilisation des colonnes pour afficher les inputs côte à côte
# Course 1
col1, col2, col3, col4 = st.columns(4)



st.write(st.session_state.distance_1)
st.write(index(st.session_state.distance_1))
with col1:
    st.session_state.distance_1 = st.selectbox("Distance de la course 1", list(distances_options.keys()), index=list(distances_options.keys()).index(st.session_state.distance_1))
with col2:
    st.session_state.hours_1 = st.number_input("Heures", min_value=0, max_value=23, value=st.session_state.hours_1, key="heures_1")
with col3:
    st.session_state.minutes_1 = st.number_input("Minutes", min_value=0, max_value=59, value=st.session_state.minutes_1, key="minutes_1")
with col4:
    st.session_state.seconds_1 = st.number_input("Secondes", min_value=0, max_value=59, value=st.session_state.seconds_1, key="secondes_1")

# Course 2
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.session_state.distance_2 = st.selectbox("Distance de la course 2", [dist for dist in distances_options.keys() if dist != st.session_state.distance_1], index=[dist for dist in distances_options.keys() if dist != st.session_state.distance_1].index(st.session_state.distance_2))
with col2:
    st.session_state.hours_2 = st.number_input("Heures", min_value=0, max_value=23, value=st.session_state.hours_2, key="heures_2")
with col3:
    st.session_state.minutes_2 = st.number_input("Minutes", min_value=0, max_value=59, value=st.session_state.minutes_2, key="minutes_2")
with col4:
    st.session_state.seconds_2 = st.number_input("Secondes", min_value=0, max_value=59, value=st.session_state.seconds_2, key="secondes_2")

# Calcul des vitesses et temps avec vérification
speed_1, total_seconds_1 = calculate_speed_safe(distances_options[st.session_state.distance_1], st.session_state.hours_1, st.session_state.minutes_1, st.session_state.seconds_1)
speed_2, total_seconds_2 = calculate_speed_safe(distances_options[st.session_state.distance_2], st.session_state.hours_2, st.session_state.minutes_2, st.session_state.seconds_2)

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

    # Affichage des temps et vitesses
    def format_time(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)} heures, {int(minutes)} minutes, {int(seconds)} secondes"
    
    def calculate_pace(total_seconds, distance_meters):
        pace_seconds_per_km = total_seconds / (distance_meters / 1000)
        minutes, seconds = divmod(pace_seconds_per_km, 60)
        return f"{int(minutes)} min {int(seconds):02d} s / km"

    # Utilisation des colonnes pour afficher les résultats côte à côte
    col1, col2 = st.columns(2)
    
    # Course 1
    with col1:
        st.write(f"### Course 1 ({st.session_state.distance_1})")
        st.write(f"Temps : {format_time(total_seconds_1)}")
        st.write(f"Vitesse : {speed_1:.2f} m/s, {(speed_1 * 3.6):.2f} km/h")
        st.write(f"Allure : {calculate_pace(total_seconds_1, distances_options[st.session_state.distance_1])}")
    
    # Course 2
    with col2:
        st.write(f"### Course 2 ({st.session_state.distance_2})")
        st.write(f"Temps : {format_time(total_seconds_2)}")
        st.write(f"Vitesse : {speed_2:.2f} m/s, {(speed_2 * 3.6):.2f} km/h")
        st.write(f"Allure : {calculate_pace(total_seconds_2, distances_options[st.session_state.distance_2])}")

    # Affichage du texte centré sous les résultats des courses
    st.write("\n\n")
    st.markdown("<h3 style='text-align: center;'>Recevoir mes estimations de performance</h3>", unsafe_allow_html=True)

    # Formulaire
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.session_state.receiver_name = st.text_input("Prénom", value=st.session_state.receiver_name)
        st.session_state.receiver_email = st.text_input("Email", value=st.session_state.receiver_email)
        st.session_state.checkbox = st.checkbox("J’accepte de recevoir par email mes estimations de temps de course et des newsletters", value=st.session_state.checkbox)

        if st.button('Valider'):
            validation_status = True

            # Vérifier si adresse mail insérée
            if st.session_state.receiver_name == "":
                st.warning("Veuillez insérer un prénom.")
                validation_status = False

            if st.session_state.receiver_email == "":
                st.warning("Veuillez insérer une adresse mail.")
                validation_status = False
            else:
                # Regex pour vérifier le format string@string.
                email_regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
                if not re.match(email_regex, st.session_state.receiver_email):
                    st.warning("L'adresse mail n'est pas valide.")
                    validation_status = False

            # Vérifier si la case est cochée
            if not st.session_state.checkbox:
                st.warning("Veuillez cocher la case pour continuer.")
                validation_status = False

            if validation_status:
                st.write("Envoyé")

                # Prédictions pour les distances spécifiées
                st.write("## Prédictions pour d'autres distances")
                predictions = {}
                for dist_name, dist_value in distances_options.items():
                    # Temps prédit en utilisant la relation: ln(T) = (1/E) * (ln(S) + ln(D)) + (1/E) * ln(T)
                    pred_time = np.exp((1/E_opt) * (np.log(dist_value) - np.log(S_opt)))
                    hours, remainder = divmod(pred_time, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    predictions[dist_name] = f"{int(hours)} heures, {int(minutes)} minutes, {int(seconds)} secondes"
                    st.write(f"{dist_name} : {predictions[dist_name]}")
            
                # Affichage des résultats
                st.write("## Résultats de la régression linéaire")
                st.write(f"Constante E : {E_opt:.4f}")
                st.write(f"Constante S : {S_opt:.4f}")

                ### Partie Mail

                subject = "An email with attachment from Python"
                body = "This is an email with attachment sent from Python"
                sender_email = "maximebataille95@gmail.com"
                password = "upqm tezg vljv zhuh"
                
                # Create a multipart message and set headers
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = st.session_state.receiver_email
                message["Subject"] = subject
                message["Bcc"] = st.session_state.receiver_email  # Recommended for mass emails
                
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
                
                # Provisoire
                '''
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, st.session_state.receiver_email, text)
                '''
else:
    st.warning("Veuillez entrer des valeurs valides pour les deux courses (temps non nul).")
