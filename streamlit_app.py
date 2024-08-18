import streamlit as st
from datetime import datetime, timedelta
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression

import re

import plotly.express as px
import plotly.graph_objects as go

st.image("logo.png", width=150)

st.title("Estimation des temps par la loi de Puissance")
st.write(
    "[Source](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10858092/)."
)
st.write("Jonah P. Drake, Axel Finke, and Richard A. Ferguson (2023) Modelling human endurance: power laws vs critical power")

st.write("Indique au moins deux courses durant lesquelles tu as donné ton maximum et durant lesquelles les conditions étaient bonnes. Les performances doivent de préférence être récentes.")

st.write("Tu recevras par e-mail les estimations de performance sur 5km, 10km, 20km, semi-marathon et marathon.")




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
    # Affichage des temps, vitesses et allures pour les deux courses

    def format_time(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)} heures, {int(minutes)} minutes, {int(seconds)} secondes"
    
    def calculate_pace(total_seconds, distance_meters):
        pace_seconds_per_km = total_seconds / (distance_meters / 1000)
        minutes, seconds = divmod(pace_seconds_per_km, 60)
        return f"{int(minutes)} min {int(seconds):02d} s / km"

    # Utilisation des colonnes pour afficher les résultats côte à côte
    # Utilisation des colonnes pour afficher les résultats côte à côte
    col1, col2 = st.columns(2)
    
    # Course 1
    with col1:
        st.write(f"### Course 1 ({distance_1})")
        st.write(f"Temps : {format_time(total_seconds_1)}")
        st.write(f"Vitesse : {speed_1:.2f} m/s, {(speed_1 * 3.6):.2f} km/h")
        st.write(f"Allure : {calculate_pace(total_seconds_1, distances_options[distance_1])}")
    
    # Course 2
    with col2:
        st.write(f"### Course 2 ({distance_2})")
        st.write(f"Temps : {format_time(total_seconds_2)}")
        st.write(f"Vitesse : {speed_2:.2f} m/s, {(speed_2 * 3.6):.2f} km/h")
        st.write(f"Allure : {calculate_pace(total_seconds_2, distances_options[distance_2])}")

    # Affichage du texte centré sous les résultats des courses
    st.write("\n\n")  # Ajoute des espaces pour créer un peu de marge avant le texte
    st.markdown("<h3 style='text-align: center;'>Recevoir mes estimations de performance</h3>", unsafe_allow_html=True)

    # Formulaire
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        receiver_name = st.text_input("Prénom", value=None)
        receiver_email = st.text_input("Email", value=None)

        # Créer une case à cocher
        checkbox = st.checkbox("J’accepte de recevoir par email mes estimations de temps de course et des newletters")

        if st.button('Valider'):
            st.session_state.button_clicked = True

            # Vérifier si la case est cochée
            if not checkbox:
                # Afficher un message d'avertissement si la case n'est pas cochée
                st.warning("Veuillez cocher la case pour continuer.")
            elif receiver_email is None:
                    st.warning("Veuillez remplir le mail.")
            elif receiver_name is None:
                    st.warning("Veuillez remplir le prénom.")
            else:
                st.write(receiver_name)
                st.write("Envoyé")
                st.session_state.button_clicked = False
                st.session_state.receiver_email = None
                st.session_state.receiver_name = None
                
       
                # Prédictions pour les distances spécifiées
                st.write("## Prédictions pour d'autres distances")
                predictions = {}
                predictions_secondes = {}
                for dist_name, dist_value in distances_options.items():
                    # Temps prédit en utilisant la relation: ln(T) = (1/E) * (ln(S) + ln(D)) + (1/E) * ln(T)
                    pred_time = np.exp((1/E_opt) * (np.log(dist_value) - np.log(S_opt)))
                    hours, remainder = divmod(pred_time, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    predictions[dist_name] = f"{int(hours)} heures, {int(minutes)} minutes, {int(seconds)} secondes"
                    predictions_secondes[dist_name] = pred_time
                    st.write(f"{dist_name} : {predictions[dist_name]}")
        
                # Affichage des résultats
                st.write("## Résultats de la régression linéaire")
                st.write(f"Constante E : {E_opt:.4f}")
                st.write(f"Constante S : {S_opt:.4f}")

                # graphique
                def power_law(time, S, E):
                    return S * (time**(E-1))   
                time = np.arange(0, predictions_secondes["Marathon"] + 1000, 100)
                speed = np.array([power_law(t, S_opt, E_opt) for t in time])

                speed_races = np.array([power_law(t, S_opt, E_opt) for t in predictions_secondes.values()])

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=time, y=speed, mode='lines', line=dict(color='#0B1F52')))
                
                
                fig.add_trace(go.Scatter(x=list(predictions_secondes.values()),
                                         y=speed_races,
                                         mode='markers',
                                         marker_color='#83FFC0',
                                         marker_size=12))
                

                # Mise en page pour personnaliser les axes
                fig.update_layout(
                    title='Loi de Puissance',
                    xaxis=dict(
                        title='Temps (minutes)',
                        range=[0, max(time)],  # Limites de l'axe x
                        tick0=0,  # Début des ticks
                        dtick=1200,  # Granularité des ticks
                        zeroline=True,  # Ligne zéro
                        zerolinewidth=2,  # Largeur de la ligne zéro
                        zerolinecolor='black',  # Couleur de la ligne zéro
                        tickformat='%d',  # Format des ticks en entier
                        ticktext=[f'{int(val / 60)}' for val in np.arange(0, max(time) + 1, 1200)]  # Labels divisés par 60
                    ),
                    yaxis=dict(
                        title='Vitesse (m/s)',
                        range=[0, max(speed) + 1],  # Limites de l'axe y
                        tick0=0,  # Début des ticks
                        dtick=0.25,  # Granularité des ticks
                        zeroline=True,  # Ligne zéro
                        zerolinewidth=2,  # Largeur de la ligne zéro
                        zerolinecolor='black'  # Couleur de la ligne zéro
                    ),
                    showlegend=False
                )
                

                st.plotly_chart(fig)
    
                ### Partie Mail

                # Créer le corps du mail avec des éléments HTML
                body = f"""
                <html>
                <head></head>
                <body>
                   
                    <p>Hello, tes estimations de temps du 5km au marathon sont là.<br><br>

                    Ces estimations sont basées sur la loi de Puissance.<br><br>
                    
                    C'est une très bonne estimation objective de ton potentiel et de ce que tu peux viser sur tes prochaines courses</p>

                    <!-- Estimations de Temps -->
                    <h4>Tes estimations:</h4>
                    <ul>
                        <li>5km : {predictions["5 km"]}</li>
                        <li>10km : {predictions["10 km"]}</li>
                        <li>20km : {predictions["20 km"]}</li>
                        <li>Semi-marathon : {predictions["Semi-marathon"]}</li>
                        <li>Marathon : {predictions["Marathon"]}</li>
                    </ul>

                    <p><div style="margin: 0; padding: 0;">Maxime</div>
                    <div style="margin: 0; padding: 0;"><i>Entraineur de trail-running indépendant, Data Scientist</i></div></p>

                    <br>

                    <p><i>PS: Profite du <a href="https://maximebataille-trailrunning.fr/">premier mois offert</a> sur la programmation et le suivi de ton entrainement</i></p>
                
                    <!-- Liens vers les réseaux sociaux -->
                    <p><div style="margin: 0; padding: 0;">Retrouve-moi sur :</div>
                   <div style="margin: 0; padding: 0;">
                        <a href="https://www.linkedin.com/in/maxime-bataille-data/?originalSubdomain=fr">LinkedIn</a> |
                        <a href="https://www.instagram.com/maxbataille.coachtrailrunning/">Instagram</a> |
                        <a href="https://maximebataille-trailrunning.fr/">Site Web</a></div>
                    </p>
                </body>
                </html>
                """
    
                subject = "Tes estimations de temps du 5km au Marathon avec la loi de Puissance"
                sender_email = "maximebataille95@gmail.com"
                password = "upqm tezg vljv zhuh"
                
                # Create a multipart message and set headers
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject
                message["Bcc"] = receiver_email  # Recommended for mass emails
            
                # Add body to email
                message.attach(MIMEText(body, "html"))
                
                
                
                # Add attachment to message and convert message to string
                text = message.as_string()
                
                # Log in to server using secure context and send email
                context = ssl.create_default_context()
                    
                
                ### Provisoire
               
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, text)
                           
else:
    st.warning("Veuillez entrer des valeurs valides pour les deux courses (temps non nul).")
