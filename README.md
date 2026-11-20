# Minijob Mailer

Schulprojekt am Berufskolleg Lübbecke (FOS Informatik, freies Projekt im Zweierteam).

Der Minijob Mailer soll bei der Suche nach einem Minijob helfen: Man gibt einen Ort und einen Umkreis ein, das Tool sucht über OpenStreetMap Betriebe in der Nähe und erstellt aus einer eigenen Vorlage für jeden Betrieb eine Bewerbungsanfrage. Jede Mail wird einzeln freigegeben und danach mit Pause über das eigene Mail-Konto verschickt.

## Team

| Person | Schwerpunkt |
|---|---|
| Niklas Metzger | Betriebssuche über OpenStreetMap, Weboberfläche |
| Mykhailo Panchenko | Mail-Versand über SMTP, Vorlage, Versand-Warteschlange |

## Stand

Das Projekt ist in Arbeit. Bisher gibt es zwei einzelne Bausteine, die noch nicht miteinander verbunden sind.

| Datei | Was sie macht |
|---|---|
| `citycoordinates.py` | Funktion `get_coordinates(city)`: fragt Nominatim (OpenStreetMap) ab und gibt Breitengrad und Längengrad eines Ortes zurück |
| `test.py` | Verschickt eine Testmail per SMTP an die eigene Adresse |

Geplant (siehe Projektplan):

- [ ] Betriebe im Umkreis über die Overpass-API suchen
- [ ] Mail-Vorlage mit Platzhaltern und Vorschau pro Betrieb
- [ ] Versand-Warteschlange mit Pause, Tageslimit und Sperrliste
- [ ] Weboberfläche mit Flask: suchen, freigeben, senden, Status sehen

## Installation

Voraussetzung ist Python 3 und Git.

```bash
git clone https://github.com/NiklasM-foss/minijob-mailer.git
cd minijob-mailer
python -m venv .venv
```

Virtuelle Umgebung aktivieren:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Pakete installieren:

```bash
pip install -r requirements.txt
pip install requests
```

`requests` steht noch nicht in der `requirements.txt` und muss deshalb im Moment extra installiert werden.

## Konfiguration

Zugangsdaten stehen nur in einer lokalen Datei `.env` im Projektordner. Diese Datei wird nicht ins Repository hochgeladen.

```bash
cp .env.example .env
```

Inhalt der `.env`:

```
DEBUG=false
SMTP_USER=deine.adresse@gmail.com
SMTP_PASS=dein-app-passwort
```

| Variable | Bedeutung |
|---|---|
| `DEBUG` | Bei `true` fragt `get_coordinates` den Ort in der Konsole ab und gibt die Antwort von Nominatim aus |
| `SMTP_USER` | Mail-Adresse, mit der gesendet wird. Die Testmail geht an dieselbe Adresse |
| `SMTP_PASS` | Passwort für den SMTP-Login |

`test.py` ist fest auf Gmail eingestellt (`smtp.gmail.com`, Port 465, SSL). Gmail braucht dafür ein App-Passwort, das normale Konto-Passwort funktioniert nicht.

## Starten

Testmail verschicken:

```bash
python test.py
```

Bei Erfolg erscheint `Gesendet`, sonst `Fehler:` mit der Fehlermeldung.

Koordinaten eines Ortes abfragen:

```bash
python -c "from citycoordinates import get_coordinates; print(get_coordinates('Lübbecke'))"
```

## Bekannte Probleme

- `get_coordinates` bricht mit einem Fehler ab, wenn kein Ort gefunden wird oder die Anfrage fehlschlägt, weil dann kein Rückgabewert vorhanden ist.
- `.env.example` enthält bisher nur `debug`, die SMTP-Variablen fehlen dort noch.

## Hinweise zur Nutzung

- Getestet wird nur mit eigenen Mail-Adressen. Im Rahmen des Projekts gehen keine Mails an fremde Betriebe.
- Nominatim erlaubt höchstens eine Anfrage pro Sekunde und verlangt einen eigenen User-Agent. Beides bitte einhalten.
- Kartendaten © OpenStreetMap-Mitwirkende, Lizenz ODbL.
