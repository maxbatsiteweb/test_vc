import streamlit as st
from datetime import datetime, timedelta

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

receiver_email = st.text_input("Ton Email")
st.write("The current movie title is", receiver_email)


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Options de distance en mètres
distances_options = {
    "5 km": 5000,
    "10 km": 10000,
    "20 km": 20000,
    "Semi-marathon": 21097.5,
    "Marathon": 42195
}

# Fonction pour afficher les inputs pour une course
def course_input_block(course_name, exclude=None):
    st.write(f"## {course_name}")

    # Sélectionner la distance
    distance = st.selectbox(
        f"Choisissez la distance de la {course_name}", 
        options=[dist for dist in distances_options.keys() if dist != exclude]
    )
    
    # Inputs pour le temps
    col1, col2, col3 = st.columns(3)
    with col1:
        heures = st.number_input(f"Heures", min_value=0, max_value=23, value=0, key=f"{course_name}_heures")
    with col2:
        minutes = st.number_input(f"Minutes", min_value=0, max_value=59, value=0, key=f"{course_name}_minutes")
    with col3:
        secondes = st.number_input(f"Secondes", min_value=0, max_value=59, value=0, key=f"{course_name}_secondes")

    return distances_options[distance], heures, minutes, secondes

# Affichage des deux blocs d'input
st.write("# Informations sur les courses")

st.write("### Course 1")
distance_1, heures_1, minutes_1, secondes_1 = course_input_block("Course 1")

st.write("### Course 2")
distance_2, heures_2, minutes_2, secondes_2 = course_input_block("Course 2", exclude=distance_1)

# Calcul du temps total pour chaque course en secondes
total_seconds_course_1 = heures_1 * 3600 + minutes_1 * 60 + secondes_1
total_seconds_course_2 = heures_2 * 3600 + minutes_2 * 60 + secondes_2

# Calcul des vitesses en m/s (Distance en mètres / Temps en secondes)
vitesse_1 = distance_1 / total_seconds_course_1
vitesse_2 = distance_2 / total_seconds_course_2

# Affichage des résultats
st.write("## Résultats des courses")
st.write(f"Course 1 : {distance_1 / 1000} km en {heures_1} heures, {minutes_1} minutes et {secondes_1} secondes.")
st.write(f"Vitesse moyenne de la Course 1 : {vitesse_1:.2f} m/s")
st.write(f"Course 2 : {distance_2 / 1000} km en {heures_2} heures, {minutes_2} minutes et {secondes_2} secondes.")
st.write(f"Vitesse moyenne de la Course 2 : {vitesse_2:.2f} m/s")

# Réaliser la régression linéaire avec Scikit-learn
X = np.log(np.array([total_seconds_course_1, total_seconds_course_2])).reshape(-1, 1)
y = np.log(np.array([vitesse_1, vitesse_2]))

model = LinearRegression()
model.fit(X, y)

# Extraire les coefficients
E_opt = model.coef_[0] + 1
S_opt = np.exp(model.intercept_)

# Tracer la courbe de régression
T_fit = np.linspace(0.01, 15000, 1000)  # Eviter log(0) en utilisant une petite valeur minimale
v_fit = np.exp(model.predict(np.log(T_fit).reshape(-1, 1)))

# Points pour 5 km, 10 km, 20 km, semi-marathon, marathon
distances_m = [5000, 10000, 20000, 21097.5, 42195]
T_points = np.array(distances_m) / v_fit[-1]
v_points = model.predict(np.log(T_points).reshape(-1, 1))

# Graphique : Temps vs Vitesse
plt.figure(figsize=(10, 6))
plt.scatter([total_seconds_course_1, total_seconds_course_2], [vitesse_1, vitesse_2], color='blue', label='Données')
plt.plot(T_fit, v_fit, color='red', label='Régression linéaire')
plt.scatter(T_points, np.exp(v_points), color='green', label='Points spécifiques', zorder=5)
for i, dist in enumerate(distances_m):
    plt.text(T_points[i], np.exp(v_points[i]), f'{dist/1000:.1f} km', fontsize=9, verticalalignment='bottom')

plt.xlabel('Temps (s)')
plt.ylabel('Vitesse (m/s)')
plt.title('Nuage de points et régression linéaire')
plt.legend()
st.pyplot(plt)

# Graphique : Distance vs Temps
plt.figure(figsize=(10, 6))
plt.plot(distances_m, T_points, color='orange', label='Courbe régression Distance-Temps')
plt.scatter(distances_m, T_points, color='purple', label='Points spécifiques')
for i, dist in enumerate(distances_m):
    plt.text(distances_m[i], T_points[i], f'{dist/1000:.1f} km', fontsize=9, verticalalignment='bottom')

plt.xlabel('Distance (m)')
plt.ylabel('Temps (s)')
plt.title('Relation entre la Distance et le Temps')
plt.legend()
st.pyplot(plt)

# Afficher les temps probables selon la régression pour 5 km, 10 km, 20 km, semi-marathon, et marathon
st.write("## Temps probables selon la régression")
for i, dist in enumerate(distances_m):
    hours, remainder = divmod(T_points[i], 3600)
    minutes, seconds = divmod(remainder, 60)
    st.write(f"Pour {dist/1000:.1f} km : {int(hours)} heures, {int(minutes)} minutes, {int(seconds)} secondes")

# Afficher les constantes optimisées E et S
st.write(f"Constante E optimisée : {E_opt:.4f}")
st.write(f"Constante S optimisée : {S_opt:.4f}")





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
