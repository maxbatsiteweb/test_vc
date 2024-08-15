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

    distance = st.number_input(f"Distance de la {course_name} (en km)", min_value=0, value=0)

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

# Calcul du temps total pour chaque course en secondes
total_seconds_course_1 = heures_1 * 3600 + minutes_1 * 60 + secondes_1
total_seconds_course_2 = heures_2 * 3600 + minutes_2 * 60 + secondes_2

# Calcul des vitesses en m/s (Distance en mètres / Temps en secondes)
vitesse_1 = (distance_1 * 1000) / total_seconds_course_1
vitesse_2 = (distance_2 * 1000) / total_seconds_course_2

# Affichage des résultats
st.write("## Résultats des courses")
st.write(f"Temps total de la Course 1 : {heures_1} heures, {minutes_1} minutes et {secondes_1} secondes.")
st.write(f"Vitesse moyenne de la Course 1 : {vitesse_1:.2f} m/s")
st.write(f"Temps total de la Course 2 : {heures_2} heures, {minutes_2} minutes et {secondes_2} secondes.")
st.write(f"Vitesse moyenne de la Course 2 : {vitesse_2:.2f} m/s")

# Nuage de points (Temps vs Vitesse)
times = np.array([total_seconds_course_1, total_seconds_course_2])
speeds = np.array([vitesse_1, vitesse_2])

plt.figure(figsize=(10, 6))
plt.scatter(times, speeds, color='blue', label='Données')

# Définir la relation ln(v) = (E-1)ln(T) + ln(S)
def model(T, E, S):
    return np.exp((E-1) * np.log(T) + np.log(S))

# Ajuster le modèle aux données pour déterminer les constantes E et S
popt, _ = curve_fit(model, times, speeds)
E_opt, S_opt = popt

# Tracer la régression linéaire
T_fit = np.arange(0, 15001, 100)
v_fit = model(T_fit, E_opt, S_opt)

# Distances en mètres
distances_km = [5, 10, 21.1, 42.2]
distances_m = np.array(distances_km) * 1000

# Calcul du temps pour chaque distance avec les vitesses issues de la régression
T_points = distances_m / v_fit[-1]  # Utiliser la vitesse correspondant à la fin de la courbe de régression
v_points = model(T_points, E_opt, S_opt)

# Tracer les points spécifiques sur la courbe de régression
plt.scatter(T_points, v_points, color='green', label='Points spécifiques', zorder=5)
for i, dist in enumerate(distances_km):
    plt.text(T_points[i], v_points[i], f'{dist} km', fontsize=9, verticalalignment='bottom')

plt.plot(T_fit, v_fit, color='red', label='Régression linéaire')
plt.xlabel('Temps (s)')
plt.ylabel('Vitesse (m/s)')
plt.title('Nuage de points et régression linéaire')
plt.legend()
st.pyplot(plt)

# Afficher les constantes optimisées E et S
st.write(f"Constante E optimisée : {E_opt:.4f}")
st.write(f"Constante S optimisée : {S_opt:.4f}")

# Ajout d'un deuxième graphique : Distance en mètres vs Temps en secondes basé sur la courbe de régression
plt.figure(figsize=(10, 6))

# Relation distance (m) vs temps (s) basé sur la courbe de régression
distances_range = np.linspace(0, 45000, 1000)  # Intervalle de 0 à 45 km
times_range = distances_range / v_fit[-1]      # Temps calculé à partir de la vitesse issue de la régression

# Tracer la courbe distance vs temps
plt.plot(distances_range, times_range, color='orange', label='Courbe régression Distance-Temps')

# Tracer les points spécifiques (5km, 10km, semi-marathon, marathon)
plt.scatter(distances_m, T_points, color='purple', label='Points spécifiques')
for i, dist in enumerate(distances_km):
    plt.text(distances_m[i], T_points[i], f'{dist} km', fontsize=9, verticalalignment='bottom')

plt.xlabel('Distance (m)')
plt.ylabel('Temps (s)')
plt.title('Relation entre la Distance et le Temps')
plt.legend()
st.pyplot(plt)



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
