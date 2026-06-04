import pandas as pd
import html
import dateparser
import re
from deep_translator import GoogleTranslator

# --- Fix encoding issues and HTML entities ---
def super_fix(text):
    if isinstance(text, str):
        # Remove non-printable characters
        text = re.sub(r'[^\x00-\x7F\u00C0-\u017F]+', ' ', text)
        text = html.unescape(text.strip())  # Decode HTML entities
    return text

# --- Parse French date to YYYY-MM-DD ---
def parse_date(date_str):
    try:
        date = dateparser.parse(date_str, languages=['fr'])
        return date.strftime('%Y-%m-%d') if date else None
    except:
        return None

# --- Translate French job titles to English ---
def translate_safe(text):
    try:
        return GoogleTranslator(source='fr', target='en').translate(text)
    except Exception as e:
        print(f"[!] Translation failed for: {text} | {e}")
        return text  # Keep original if fails

# --- Load original CSV ---
try:
    df = pd.read_csv("jobinfocamer_informatique.csv", encoding="utf-8", on_bad_lines="skip")
except FileNotFoundError:
    print("File not found: jobinfocamer_informatique.csv")
    exit()

# --- Clean text ---
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].apply(super_fix)

# --- Translate Job Titles ---
df["Job Title"] = df["Job Title"].apply(translate_safe) 

# --- Translate Job Type from French to English ---
job_type_map = {
    "CDI": "Full-time",
    "CDD": "Part-time",
    "STAGE": "Internship"
}
df["Job Type"] = df["Job Type"].map(job_type_map).fillna(df["Job Type"])

# --- Parse dates ---
df['Date'] = df['Date'].apply(parse_date)

# --- Final cleanup ---
df.drop_duplicates(inplace=True)
df = df.dropna(subset=['Date', 'Job Title', 'Company', 'Location'])
df.sort_values(by='Date', ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

# --- Save cleaned CSV ---
df.to_csv("jobinfocamer_informatique_cleaned1.csv", index=False, encoding='utf-8-sig')
print(" Text, encoding, translation & date fully cleaned and saved successfully!")
