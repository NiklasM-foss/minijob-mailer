import json
import os

import requests
from dotenv import load_dotenv

# settings
load_dotenv()
API_KEY = os.getenv("NVIDIA_API_KEY")
URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODELL = "nvidia/nemotron-3-ultra-550b-a55b"

# über dich
with open("haupttext.txt", encoding="utf-8") as datei:
    haupttext = datei.read().strip()

# Info über firma(Beispiel)
firma = "Café Sonnenschein in Köln. Kleines Familiencafé mit selbstgebackenem Kuchen. Sucht Aushilfe am Wochenende."

# main rules
regeln = """Du schreibst kurze Bewerbungs-E-Mails für Minijobs auf Deutsch.
Schreibe NUR:
- einen Betreff
- eine Einleitung: "Sehr geehrte Damen und Herren," + 1-2 Sätze über die Firma
- einen Schluss: 1-2 Sätze (z. B. Angebot zum Probearbeiten)
Erfinde nichts. Wiederhole nichts aus dem Text des Bewerbers.
Antworte nur mit JSON: {"betreff": "...", "einleitung": "...", "schluss": "..."}"""

aufgabe = "Firma:\n" + firma + "\n\nText des Bewerbers:\n" + haupttext

# senden an ki
antwort = requests.post(
    URL,
    headers={"Authorization": "Bearer " + API_KEY},
    json={
        "model": MODELL,
        "messages": [
            {"role": "system", "content": regeln},
            {"role": "user", "content": aufgabe},
        ],
    },
    timeout=120,
)

# antwort von KI bekommen
ki_text = antwort.json()["choices"][0]["message"]["content"]
print("Antwort der KI:")
print(ki_text)
print()

teile = json.loads(ki_text)

# email erstellen
mail = (
    teile["einleitung"] + "\n\n"
    + haupttext + "\n\n"
    + teile["schluss"] + "\n\n"
    + "Mit freundlichen Grüßen"
)

print("Betreff:", teile["betreff"])
print("-" * 40)
print(mail)
