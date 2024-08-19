
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

import os

from email.mime.image import MIMEImage

import base64

from streamlit_javascript import st_javascript

# CSS pour masquer le lien GitHub et le footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.image("logo.png", width=150)

st.title("Estimation des temps par la loi de Puissance")
st.write(
    "[Source](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10858092/)."
)
st.write("Jonah P. Drake, Axel Finke, and Richard A. Ferguson (2023) Modelling human endurance: power laws vs critical power")

st.write("Indique au moins deux courses durant lesquelles tu as donné ton maximum et durant lesquelles les conditions étaient bonnes. Les performances doivent de préférence être récentes.")

st.write("Tu recevras par e-mail les estimations de performance sur 5km, 10km, semi-marathon et marathon. Vérifie tes spams.")




# Données des courses : distances en mètres et temps en secondes
distances_options = {
    "5 km": 5000,
    "10 km": 10000,
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

# Créer les cases à cocher
races = list(distances_options.keys())
col1, col2, col3, col4 = st.columns(len(races))

# Dictionnaire pour stocker l'état des cases à cocher
selected_courses = {}

# Afficher les cases à cocher dans les colonnes
with col1:
    selected_courses[races[0]] = st.checkbox(races[0])
with col2:
    selected_courses[races[1]] = st.checkbox(races[1])
with col3:
    selected_courses[races[2]] = st.checkbox(races[2])
with col4:
    selected_courses[races[3]] = st.checkbox(races[3])

# Vérification avant de calculer les vitesses
def calculate_speed_safe(distance, hours, minutes, seconds):
    total_seconds = hours * 3600 + minutes * 60 + seconds
    if total_seconds > 0:
        speed = distance / total_seconds
    else:
        speed = 0
    return speed, total_seconds

# Obtenir la liste des courses sélectionnées
selected_courses_list = [course for course, selected in selected_courses.items() if selected]

if len(selected_courses_list) < 2:
    st.error("Veuillez sélectionner au moins deux courses.")
else:
    results = {}
    total_seconds = []
    speeds = []
    for course in selected_courses_list:
        st.write(f"**{course}**")
        
        # Entrée des heures, minutes, secondes
        distance = distances_options[course]
        hours = st.number_input(f"Heures", max_value=23, value=0, key=f"{course}_hours")
        minutes = st.number_input(f"Minutes", min_value=0, max_value=59, value=0, key=f"{course}_minutes")
        seconds = st.number_input(f"Secondes", min_value=0, max_value=59, value=0, key=f"{course}_seconds")

        results[course] = (hours, minutes, seconds)
        seconds, speed = calculate_speed_safe(distance, hours, minutes, seconds)
        total_seconds.append(seconds)
        speeds.append(speed)        

        





if 0 in total_seconds:
    # Réaliser la régression linéaire avec Scikit-learn
    X = np.log(np.array(total_seconds)).reshape(-1, 1)
    y = np.log(np.array(speeds))
    
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


    # Afficher les résultats dans les colonnes
    with col1:
            st.header("Ligne 1")
            for course, speed, total_second in zip(selected_courses_list[:2], speeds[:2], total_seconds[:2]):  # Les deux premiers résultats

                st.write(f"{course}")
                st.write(f"Vitesse : {speed:.2f} m/s, {(speed * 3.6):.2f} km/h")
                st.write(f"Allure : {calculate_pace(total_seconds, distances_options[course])}")
                st.write("---")  # Séparateur pour les résultats

    with col2:
            st.header("Ligne 2")
            for course, speed, total_second in zip(selected_courses_list[2:], speeds[2:], total_seconds[2:]):  # Les deux derniers résultats
                st.write(f"{course}")
                st.write(f"Vitesse : {speed:.2f} m/s, {(speed * 3.6):.2f} km/h")
                st.write(f"Allure : {calculate_pace(total_seconds, distances_options[course])}")
                st.write("---")  # Séparateur pour les résultats
    

    # Affichage du texte centré sous les résultats des courses
    st.write("\n\n")  # Ajoute des espaces pour créer un peu de marge avant le texte
    st.markdown("<h3 style='text-align: center;'>Recevoir mes estimations de performance</h3>", unsafe_allow_html=True)

    # Formulaire
    col1, col2, col3 = st.columns([1, 2, 1])
    mail_to_be_sent = False
    with col2:
        receiver_name = st.text_input("Prénom", value=None)
        receiver_email = st.text_input("Email", value=None)

        # Créer une case à cocher
        checkbox = st.checkbox("J’accepte de recevoir par email mes estimations de temps de course et des newletters")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:    
                    if st.button('Valider', use_container_width=True):
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
                            mail_to_be_sent = True
                            st.session_state.button_clicked = False
                            st.session_state.receiver_email = None
                            st.session_state.receiver_name = None
                
    if mail_to_be_sent:   
        predictions = {}
        predictions_secondes = {}
        for dist_name, dist_value in distances_options.items():
            # Temps prédit en utilisant la relation: ln(T) = (1/E) * (ln(S) + ln(D)) + (1/E) * ln(T)
            pred_time = np.exp((1/E_opt) * (np.log(dist_value) - np.log(S_opt)))
            hours, remainder = divmod(pred_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            predictions[dist_name] = f"{int(hours)} heures, {int(minutes)} minutes, {int(seconds)} secondes"
            predictions_secondes[dist_name] = pred_time
    

        # graphique
        def power_law(time, S, E):
            return S * (time**(E-1))   
        time = np.arange(0, predictions_secondes["Marathon"] + 4000, 100)
        speed = np.array([power_law(t, S_opt, E_opt) for t in time])

        speed_races = np.array([power_law(t, S_opt, E_opt) for t in predictions_secondes.values()])

        time_in_minutes = [t/60 for t in time]
        predictions_in_minutes = [t/60 for t in predictions_secondes.values()]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_in_minutes, y=speed, mode='lines', line=dict(color='#0B1F52')))
        
        
        fig.add_trace(go.Scatter(x=predictions_in_minutes,
                                 y=speed_races,
                                 mode='markers+text',
                                 marker_color='#83FFC0',
                                 marker_size=12,
                                 text=list(distances_options.keys()),
                                 textposition='top right',
                                 textfont=dict(color='#0B1F52', size=12)))
                

        # Mise en page pour personnaliser les axes
        fig.update_layout(
            xaxis=dict(
                title='Temps (minutes)',
                range=[0, max(time_in_minutes)],  # Limites de l'axe x
                tick0=0,  # Début des ticks
                dtick=20,  # Granularité des ticks
                zeroline=True,  # Ligne zéro
                showline=True,  # Afficher la ligne de l'axe
                zerolinewidth=2,  # Largeur de la ligne zéro
                zerolinecolor='black',  # Couleur de la ligne zéro
                tickformat='%d',  # Format des ticks en entier
            ),
            yaxis=dict(
                title='Vitesse (m/s)',
                range=[min(speed) - 0.5, max(speed) + 1],  # Limites de l'axe y
                tick0=0,  # Début des ticks
                dtick=0.25,  # Granularité des ticks
                zeroline=True,  # Ligne zéro
                zerolinewidth=2,  # Largeur de la ligne zéro
                zerolinecolor='black'  # Couleur de la ligne zéro
            ),
            showlegend=False,
            plot_bgcolor='white',  # Couleur de fond du graphique
            paper_bgcolor='white',  # Couleur de fond du papier (zone autour du graphique)
            xaxis_showgrid=False,  # Désactiver la grille des abscisses
            yaxis_showgrid=False,   # Désactiver la grille des ordonnées,
            margin=dict(l=50, r=20, t=40, b=40)  # Marges : gauche, droite, haut, bas
        )
                

        # Sauvegarder le graphique en tant qu'image PNG
        fig.write_image("power_law.png", format='png')


        # Lire l'image et la convertir en base64
        with open("power_law.png", "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        ### Partie Mail pour utilisateur

        # Créer le corps du mail avec des éléments HTML
        body = f"""
        <html>
        <head></head>
        <body>
           
            <p>Hello, tes estimations de temps du 5km au marathon sont là.<br><br>

            Ces estimations sont basées sur la loi de Puissance.<br><br>
            
            C'est une très bonne estimation objective de ton potentiel et de ce que tu peux viser sur tes prochaines courses.<br><br>
            
            Une question ? répond directement à ce mail.
            </p>

            <!-- Estimations de Temps -->
            <h4>Tes estimations:</h4>
            <ul>
                <li>5km : {predictions["5 km"]}</li>
                <li>10km : {predictions["10 km"]}</li>
                <li>Semi-marathon : {predictions["Semi-marathon"]}</li>
                <li>Marathon : {predictions["Marathon"]}</li>
            </ul>

            <br>

            <p>L'une des prévisions te semble anormale ? C'est certainement car tu as sous-performé sur l'une des courses.</p>

            <!-- Profil -->
            <h4>Ton profil de Vitesse</h4>

            <img src="cid:Mailtrapimage", alt="Graphique", style="width: auto; height: 450px">

            <br>

            <p><div style="margin: 0; padding: 0;">Maxime</div>
            <div style="margin: 0; padding: 0;"><i>Entraineur de trail-running, Data Scientist</i></div></p>

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
        sender_email = "maximebataille.trailrunning@gmail.com"
        password = "upqm tezg vljv zhuh" #95
        password = "rkvn fkyc yljb ihew" #trailrunning
        
        # Create a multipart message and set headers
        message = MIMEMultipart('alternative')
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails
    
        # Add body to email
        message.attach(MIMEText(body, "html"))

        fp = open('power_law.png', 'rb')
        image = MIMEImage(fp.read())
        fp.close()
        
        # Specify the  ID according to the img src in the HTML part
        
        image.add_header('Content-ID', '<Mailtrapimage>')
        image.add_header('Content-Disposition', 'attachment', filename='powerlaw.png')  # Nom de la pièce jointe
        message.attach(image)

        
        # Add attachment to message and convert message to string
        text = message.as_string()
                
        # Log in to server using secure context and send email
        context = ssl.create_default_context()
            

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

        html_code = """
            <div style="text-align: center;">
                <p>Vérifie ta boîte mail</p>
            </div>
            """
        st.markdown(html_code, unsafe_allow_html=True)
 

        #ouvrir la page du site web
        def nav_to(url):
                js = f'window.open("{url}", "_blank").then(r => window.parent.location.href);'
                st_javascript(js)
                    
        nav_to("https://maximebataille-trailrunning.fr/")

                                 
else:
    st.warning("Veuillez entrer des valeurs valides pour les deux courses (temps non nul).")
