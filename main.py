from citycoordinates import get_coordinates
from overpass_search import get_businesses_in_radius

def main():
    print("========================================")
    print("   Minijob Mailer - Konsolen-Modus      ")
    print("========================================")
    
    # 1. Ort abfragen
    ort = input("\nGib einen Ortsnamen ein (z. B. Lübbecke oder Stuttgart): ").strip()
    if not ort:
        print("Kein Ort eingegeben. Programm wird beendet.")
        return

    print(f"Suche Koordinaten für '{ort}'...")
    lat, lon = get_coordinates(ort)

    if lat is None or lon is None:
        print(f"Fehler: Konnte keine Koordinaten für '{ort}' finden.")
        return

    print(f"-> Gefunden! Lat: {lat}, Lon: {lon}")

    # 2. Umkreis abfragen
    try:
        radius_input = input("Gewünschter Umkreis in km (Standard: 2): ").strip()
        radius = float(radius_input) if radius_input else 2.0
    except ValueError:
        radius = 2.0
        print("Ungültige Eingabe, verwende Standardwert von 2 km.")

    # 3. Betriebe abfragen
    print(f"Suche Betriebe im Umkreis von {radius} km...")
    betriebe = get_businesses_in_radius(lat, lon, radius_km=radius)

    print(f"\n--- Gefundene Betriebe ({len(betriebe)}) ---")
    if not betriebe:
        print("Keine Betriebe in diesem Bereich gefunden.")
        return

    for index, b in enumerate(betriebe, start=1):
        print(f"\n{index}. Betrieb: {b['name']}")
        print(f"   Adresse: {b['address']}")
        print(f"   E-Mail:  {b['email'] if b['email'] else '❌ Keine Mail gefunden'}")
        print(f"   Website: {b['website'] if b['website'] else '❌ Keine Website'}")

    print("\n----------------------------------------")
    print("Konsolen-Test erfolgreich abgeschlossen!")

if __name__ == "__main__":
    main()