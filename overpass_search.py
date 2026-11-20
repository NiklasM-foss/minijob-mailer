import requests

def get_businesses_in_radius(lat, lon, radius_km=5):
    """
    Sucht Betriebe (Geschäfte, Gastronomie, Dienstleister) im angegebenen Umkreis 
    über die Overpass-API von OpenStreetMap.
    
    :param lat: Breitengrad (float)
    :param lon: Längengrad (float)
    :param radius_km: Suchradius in Kilometern (int/float)
    :return: Liste von Dictionaries mit Name, Adresse, E-Mail und Website
    """
    url = "https://overpass-api.de/api/interpreter"
    
    # Radius in Meter umrechnen (Overpass erwartet Meter bei 'around')
    radius_meters = int(radius_km * 1000)
    
    # Overpass QL Query: Sucht nach Shops, Gastronomie (amenity) und Büros im Umkreis
    query = f"""
    [out:json][timeout:25];
    (
      node(around:{radius_meters},{lat},{lon})[shop];
      way(around:{radius_meters},{lat},{lon})[shop];
      node(around:{radius_meters},{lat},{lon})[amenity];
      way(around:{radius_meters},{lat},{lon})[amenity];
    );
    out body;
    >;
    out skel qt;
    """
    
    # Wichtig: Immer einen aussagekräftigen User-Agent mitschicken (OpenStreetMap-Richtlinie)
    headers = {
        'User-Agent': 'MinijobMailer/1.0 (Schulprojekt)'
    }
    
    try:
        response = requests.post(url, data={'data': query}, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        businesses = []
        seen_names = set()
        
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            name = tags.get('name')
            
            # Nur Elemente berücksichtigen, die auch einen Namen haben
            if name and name not in seen_names:
                seen_names.add(name)
                
                # Adresse zusammenbauen
                street = tags.get('addr:street', '')
                housenumber = tags.get('addr:housenumber', '')
                postcode = tags.get('addr:postcode', '')
                city = tags.get('addr:city', '')
                
                # Formatierte Adresse erstellen
                if street or housenumber:
                    address = f"{street} {housenumber}".strip()
                    if postcode or city:
                        address += f", {postcode} {city}".strip()
                else:
                    address = "Adresse nicht hinterlegt"
                
                # Kontaktdaten auslesen (manchmal unter 'email' oder 'contact:email')
                email = tags.get('email', tags.get('contact:email', None))
                website = tags.get('website', tags.get('contact:website', None))
                
                businesses.append({
                    'name': name,
                    'address': address,
                    'email': email,
                    'website': website
                })
                
        return businesses

    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der Overpass-Abfrage: {e}")
        return []

# Test-Block direkt zum Ausführen
if __name__ == "__main__":
    # Beispielkoordinaten (z. B. Stuttgart Mitte als Test)
    test_lat = 48.7758
    test_lon = 9.1829
    
    print("Suche Betriebe im Umkreis...")
    ergebnisse = get_businesses_in_radius(test_lat, test_lon, radius_km=2)
    
    print(f"Gefunden: {len(ergebnisse)} Betriebe")
    for b in ergebnisse[:5]:  # Zeige die ersten 5
        print(f"- {b['name']} | {b['address']} | Mail: {b['email']} | Web: {b['website']}")