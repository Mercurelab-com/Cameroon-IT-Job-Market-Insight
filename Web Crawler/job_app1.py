import pandas as pd
import streamlit as st
import plotly.express as px
import datetime

# Load cleaned data


@st.cache_data
def load_data():
    return pd.read_csv("jobinfocamer_informatique_cleaned.csv", parse_dates=["Date"])


# Add ML-ready job category labeling
df = load_data()
today = pd.Timestamp.today()
six_months_ago = today - pd.DateOffset(months=6)
df_recent = df[df["Date"] >= six_months_ago]

# --- ML-READY LABELING ---


def label_category(job_title):
    title = job_title.lower()
    if any(word in title for word in ["développeur", "developer", "software engineer", "fullstack", "backend", "frontend", "java", "php", "node", "react", "angular", "windev", "odoo", "sap"]):
        return "Developer"
    elif any(word in title for word in ["data analyst", "data engineer", "data scientist", "analyste", "intelligence artificielle", "nlp"]):
        return "Data Analyst"
    elif any(word in title for word in ["network", "réseau", "system", "it support", "technicien", "infrastructure", "maintenance"]):
        return "Network/IT"
    elif any(word in title for word in ["manager", "product owner", "chef de projet", "responsable", "lead", "supervisor"]):
        return "IT Manager"
    elif any(word in title for word in ["designer", "ui", "ux", "webdesigner", "graphique"]):
        return "UI/UX Designer"
    elif any(word in title for word in ["test", "qa", "quality"]):
        return "QA/Test"
    elif any(word in title for word in ["consultant", "trainer", "formateur", "enseignant"]):
        return "Consultant/Trainer"
    else:
        return "Full Stack"


df["Category"] = df["Job Title"].astype(str).apply(label_category)
# --- IGNORE ---
st.set_page_config(page_title="Cameroon IT Jobs Dashboard", layout="wide")

st.title("📊 Cameroon IT Job Insights Dashboard")
st.markdown(
    "Search, explore and analyze tech job opportunities scraped from JobInfoCamer.")

# --- Sidebar filters
st.sidebar.header("🔍 Filter Jobs")
job_types = st.sidebar.multiselect(
    "Job Type", options=df["Job Type"].unique(), default=df["Job Type"].unique())

# "select all" option for locations
location_options = ["Select All"] + list(df["Location"].unique())
selected_locations = st.sidebar.multiselect(
    "Location", options=location_options, default=location_options
)

# selecl all logic

if "Select All" in selected_locations:
    filtered_locations = df["Location"].unique()
else:
    filtered_locations = selected_locations

# locations = st.sidebar.multiselect("Location", options=df["Location"].unique(), default=df["Location"].unique())
search_text = st.sidebar.text_input(
    "🔎 Search Job Title ( 'developer', 'network')")

# --- Apply filters
filtered_df = df[
    (df["Job Type"].isin(job_types)) &
    (df["Location"].isin(filtered_locations)) &
    (df["Job Title"].str.lower().str.contains(search_text.lower()))
]


st.markdown(f"### 🗂️ {len(filtered_df)} Jobs Found")
st.dataframe(filtered_df, width="stretch")

# --- 🥧 JOB TYPE DISTRIBUTION ---
st.subheader("🥧 Job Type Distribution")
job_type_counts = filtered_df["Job Type"].value_counts(
    normalize=False).reset_index()
job_type_counts.columns = ["Job Type", "Count"]
job_type_counts["Percent"] = (
    job_type_counts["Count"] / job_type_counts["Count"].sum() * 100).round(1)
fig_jobtype = px.pie(job_type_counts, names="Job Type", values="Count", title="Job Type Distribution",
                     hover_data=["Percent"], labels={"Percent": "%"})
st.plotly_chart(fig_jobtype, width="stretch")

st.dataframe(job_type_counts, width="stretch")

# --- 📅 TEMPORAL POSTING TRENDS BY WEEKDAY ---
st.subheader("📅 Job Postings by Day of the Week")
filtered_df["Weekday"] = filtered_df["Date"].dt.day_name()
weekday_counts = filtered_df["Weekday"].value_counts().reindex([
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]).reset_index()
weekday_counts.columns = ["Weekday", "Count"]
fig_weekday = px.line(weekday_counts, x="Weekday", y="Count",
                      markers=True, title="Job Postings by Day of the Week")
st.plotly_chart(fig_weekday, width="stretch")
st.dataframe(weekday_counts, width="stretch")


# --- 📈 SKILL FREQUENCY ANALYSIS ---
st.subheader("🔥 Top In-Demand Skills")

# Key word list for skills extraction
skill_keywords = [
    "developer", "engineer", "network", "security", "analyst", "IT Support",
    "software", "hardware", "cloud computing", "AI", "machine learning", "Network Administrator",
    "data analyst", "data scientist", "cybersecurity", "DevOps", "database administrator",
    "web development", "mobile development", "full stack developer", "frontend", "backend",
    "Java", "Python", "JavaScript", "C#", "PHP", "SQL", "Vue", "React", "Angular", "Node.js",
    "C++", "C", "Android", "iOS", "Swift", "Kotlin", "Ruby", "Go", "Rust",
    "Django", "Flask", "Spring", "ASP.NET", "MySQL",
    "HTML", "CSS", "Linux", "Windows", "Agile", "Scrum", "Git", "Docker", "Kubernetes",
    "API", "REST", "GraphQL", "Big Data", "IoT", "IT Support", "technical support",
    "system administrator", "network engineer", "cloud engineer", "data engineer", "IT Manager",
    "project manager", "business analyst", "QA", "quality assurance", "testing", "SEO Specialist",
    "digital marketing", "content management", "UI/UX designer", "graphic designer", ".NET", "CSS", "HTML",
    "web developer", "full stack",
    # Added skills below
    "INGENIEUR BUREAU TECHNIQUE",
    "Angular graphic designer",
    "Full stack developper",
    "Enseignant en Informatique",
    "Analyste programmeur",
    "Stage pre-emploi",
    "IT Volunteer",
    "Web Developer needed",
    "Administrateur Réseaux",
    "PHP Software Engineer",
    "DEVELOPPEURS JAVA",
    "ADMINISTRATEUR SYSTEME ET SECURITE INFORMATIQUE",
    "Développeur JEE/Oracle",
    "Stage développeur web",
    "Developpeur H/F",
    "Ingénieur Système et Réseau (H/F)",
    "Certified MICROSOFT, Oracle and CISCO Instructors",
    "LECTURERS FOR UNDERGRADUATE AND POST GRADUATE PROGRAMS",
    "Formateur Linux",
    "Assistant terrain en charge des bases de données",
    "Recrutement  de 2 stagiaires en web développement",
    "Formateur Bureautique",
    "Administrateur Réseaux",
    "Développeur Web et Mobile Dev",
    "ICT Assistant",
    "Registration Associate",
    "Développeur Front-End Javascript/ JQUERY",
    "LECTURERS",
    "Stage pré-emploi Graphiste/Designer",
    "C# Software Engineer",
    "Ingénieur informaticien",
    "C++ Software Engineer",
    "iOS Mobile Apps Developer",
    "Android Mobile Apps Developer",
    "Java Software Engineer",
    "IT Engineer",
    "TESTEUR DES APPLICATIONS",
    "IT Operations Associate",
    "Développeur web / Web Developer",
    "Développeur web",
    "Web Developer/Designer",
    "Infrastructure Engineer",
    "IOS Developer",
    "Développeur web",
    "Developpement d'application web et mobile",
    "Développeur Dot NET, C Sharp",
    "Biostatistician",
    "PROGRAMMEUR/DATA MANAGER",
    "FRONT-END WEB DEVELOPER",
    "Chef d'Unité de Gestion Informatique des Stocks",
    "Stage(s) developpeur informatique - 6 mois",
    "Développeur Web et SQL",
    "1 développeur Android & 1 développeur web",
    "Technicien systèmes et réseaux",
    "Business Development Manager",
    "Ingénieur",
    "Responsable Solution IT",
    "Analyste Programmeur",
    "CONSULTANT STAGIAIRE",
    "INFORMATICIENS RESEAUX ET DEVELOPPEURS",
    "Recherche de Formateur en Bureutique et comptabilite informatisee",
    "DEVELOPPEUR WEB",
    "Web designer / Infographe / Intégrateur qualifié",
    "Gestionnaire de flotte automobile",
    "Développeur Symfony Confirmé",
    "Développeur mobile Windev",
    "Développeur JAVA/J2EE",
    "IT Operations Officer",
    "Maintenance et Réseaux informatiques",
    "Développeur Symfony Confirmé (H/F)",
    "INGENIEUR SYSTEMES",
    "IT ASSISTANT",
    "Développeur / Intégrateur web",
    "Web Développeur",
    "Développeur",
    "Informaticien(ne)",
    "Administrateur de site Web(Webmaster)",
    "Informaticien Stagiaire",
    "Ingénieurs informaticiens",
    "Data and ICT Officer",
    "Stage en Administration de base de données Oracle",
    "Professeur de TECHNOLOGIE INFORMATIQUE",
    "Webmaster Expérimenté",
    "Infographe/Graphiste 3D",
    "INFORMATICIEN ASSISTANT",
    "Senior Web Developer",
    "Systems Engineer/Software Developer",
    "Informaticien",
    "Programmeurs, Analystes et Ingénieurs Informaticiens",
    "DEVELOPPEUR  APPLICATIONS WEB ET MOBILES",
    "Stagiaire en Informatique de Gestion",
    "DEVELOPPEUR QLIEKVIEW",
    "DEVELOPPEUR/PROGRAMMEUR  en J2EE",
    "INSTRUCTORS FOR CERTIFICATION AND DIPLOMA PROGRAMS",
    "Graphic Designer and IT Specialist",
    "Stage Professionnel RÉSEAUX ET SÉCURITÉ INFORMATIQUE",
    "Stagiaire",
    "INFOGRAPHE",
    "Recrutement Ingénieurs télécoms et informatique",
    "Spécialiste SIG",
    "Infographiste Web Designer",
    "Designer Graphique",
    "VNU ICT ASSISTANT",
    "Data Manager",
    "Designer/Intégrateur qualifié",
    "Analyste/Developpeur Java / JEE",
    "Informaticien",
    "Information Technology Assistant",
    "ICT Assistant",
    "ICT Assistant",
    "Information \\& Technology Assistant",
    "Associé à la Base de données réfugiés",
    "Gerante Cyber",
    "Part Time Information Technology Assistant",
    "Analyste/Développeur nouvelles technologies et Business Intelligence",
    "Gestionnaire des données",
    "CHEFS DE PROJET MOA",
    "INGENIEUR STREAM SERVE ET BUSINESS OBJET",
    "IT Assistant/Network and System Support",
    "IT System Manager",
    "IT Coordinator",
    "IT Assistant",
    "STAGE PROFESSIONNEL EN INFORMATIQUE ET GENIE LOGICIEL",
    "Stagiaire en Informatique",
    "DEVELOPPEUR D APPLICATION WEB SENIOR",
    "INGENIEUR SYSTEMES MICROSOFT",
    "Développeur PHP / prestashop",
    "Mobile App Developer Needed",
    "Senior Web Developer",
    "Cadre Supérieur",
    "Stagiaire professionnel",
    "Infographe",
    "ASSISTANT INFORMATIQUE",
    "Technicien ICT",
    "Technicien Support Anglophone (H/F)",
    "Développeur Sénior PHP (H/F)",
    "Développeur SDK Android (H/F)",
    "Développeur Web Front End (H/F)",
    "Développeur OS X (H/F)",
    "INGENIEURS / MATHEMATICIENS",
    "TECHNICIEN SUPERIEUR EN MAINTENANCE INFORMATIQUE",
    "INTEGRATEUR SOLUTIONS INFORMATIQUES- ERP",
    "Information Technology Intern",
    "M&E Officer",
    "Technicien en Maintenance Informatique",
    "Ingénieur d'Affaires Grands Comptes",
    "Ingénieur Avant Vente",
    "Développeur JEE expérimenté/Architecte Technique JEE",
    "Ingénieur Développeur JAVA/JEE Web Expérimeté",
    "INFOGRAPHISTE",
    "RECRUTEMENT 02 DEVELOPPEURS(INFORMATIQUE)",
    "Informaticien stagiaire",
    "SUPERVISEURS",
    "CHARGE DES OPERATIONS",
    "Ingenieur Technico commercial",
    "Senior Information Technology Assistant",
    "Assistant Principal en Gestion des données",
    "[Stage] Rédacteurs web",
    "Stagiaires en Informatique",
    "Web designer qualifié",
    "Analyste Programmeur",
    "Infographiste",
    "Formateurs et consultants expérimentés",
    "Enseignant / Formateur",
    "Ingénieurs en TIC",
    "Développeurs Web Dashboard",
    "Développeur BI",
    "IT Manager",
    "Product Manager",
    "OFFRE DE STAGE",
    "Développeur Web Junior",
    "Infographe numérique flasheur expérimenté",
    "IT OFFICER",
    "Chargé de déploiement Maximo",
    "Technicien maintenance informatique et électronique",
    "Network Security Specialist",
    "Axxentis Scholaris EPM/CL Integration \\& Support Analyst",
    "[Urgent] Graphiste Web",
    "Axxentis Scholaris EPM/CL Application Developer",
    "Unified Communications Support Analyst",
    "System \\& Virtualization Support Analyst",
    "Network \\& Security Support Analyst",
    "Web Designer \\& Integrator",
    "Recrutement de 05 INFORMATICIENS à la POLICE",
    "Web Content Administrator",
    "Business Development Officer",
    "Web Designers/Developers",
    "Informaticien Bilingue",
    "DEVELOPPEURS PRESTASHOP",
    "INFOGRAPHE - WEB DESIGNER",
    "HEALTH INFORMATION ASSISTANT",
    "COORDONNATEUR DES TIC",
    "Infographiste,Web Designer",
    "Information and Communication Technology Coordinator",
    "Chef de service exploitation",
    "INFOGRAPHISTE",
    "DEVELOPPEUR STAGIAIRE",
    "DEVELOPPEUR PHP",
    "FORMATEURS EN LIGNE",
    "Développeur Web"
]


def extract_skills(job_title):
    found = []
    for skill in skill_keywords:
        if skill in job_title.lower():
            found.append(skill)
    return found


filtered_df["Skills"] = filtered_df["Job Title"].apply(extract_skills)
all_skills = [skill for sublist in filtered_df["Skills"] for skill in sublist]
skill_df = pd.Series(all_skills).value_counts().reset_index()
skill_df.columns = ["Skill", "Count"]

fig1 = px.bar(skill_df, x="Skill", y="Count", color="Skill",
              title="Most Mentioned Skills in Job Titles")
st.plotly_chart(fig1, width="stretch")


# --- 📊 JOB CATEGORY DISTRIBUTION ---
st.subheader("🧩 Job Category Distribution (ML-Ready Labels)")
category_counts = filtered_df["Category"].value_counts().reset_index()
category_counts.columns = ["Category", "Count"]
fig_cat = px.bar(category_counts, x="Category", y="Count",
                 color="Category", title="Distribution of Job Categories")
st.plotly_chart(fig_cat, width="stretch")

# --- 📈 JOB TRENDS OVER TIME ---
st.subheader("📆 Job Type Trend Over Time")

time_df = filtered_df[filtered_df["Date"] >= six_months_ago].copy()
time_df["Month"] = pd.to_datetime(
    time_df["Date"]).dt.to_period("M").astype(str)

trend = time_df.groupby(["Month", "Job Type"]).size().reset_index(name="Count")
fig2 = px.bar(trend, x="Month", y="Count", color="Job Type",
              title="Job Types Trend Over Time")
st.plotly_chart(fig2, width="stretch")

# --- 📍 JOB DISTRIBUTION BY CITY ---
st.subheader("🌍 Job Opportunities by City")

location_df = filtered_df[filtered_df["Date"] >=
                          six_months_ago]["Location"].value_counts().reset_index()
location_df.columns = ["City", "Count"]

fig3 = px.pie(location_df, names="City", values="Count",
              title="Job Distribution by City Past 6 Months")
st.plotly_chart(fig3, width="stretch")
