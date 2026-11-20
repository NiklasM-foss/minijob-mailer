import requests

def get_businesses_in_radius(lat, lon, radius_km=1.5):
    endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.private.coffee/api/interpreter",
        "https://ovp.dresel.systems/api/interpreter"
    ]
    
    radius_meters = int(radius_km * 1000)
    
    # Gezieltere Abfrage: Nur echte Shops, Supermärkte, Gastronomie und Dienstleister
    query = f"""
    [out:json][timeout:30];
    (
      node(around:{radius_meters},{lat},{lon})[shop];
      way(around:{radius_meters},{lat},{lon})[shop];
      node(around:{radius_meters},{lat},{lon})[amenity~"restaurant|cafe|fast_food|bar|pub|supermarket|bakery|pharmacy"];
      way(around:{radius_meters},{lat},{lon})[amenity~"restaurant|cafe|fast_food|bar|pub|supermarket|bakery|pharmacy"];
    );
    out body center;
    """
    
    headers = {
        'User-Agent': 'MinijobMailer/1.0 (Schulprojekt)'
    }
    
    for url in endpoints:
        try:
            print(f"Versuche Overpass-Server: {url} ...")
            response = requests.post(url, data={'data': query}, headers=headers, timeout=25)
            response.raise_for_status()
            data = response.json()
            
            businesses = []
            seen_names = set()
            
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                name = tags.get('name')
                
                # Filter: Ignoriere Einträge, die nach Straße/Haltestelle klingen
                if name and name not in seen_names:
                    if any(keyword in name.lower() for keyword in ["straße", "weg", "allee", "platz"]):
                        continue # Überspringen, wenn es reine Straßennamen sind
                        
                    seen_names.add(name)
                    
                    street = tags.get('addr:street', '')
                    housenumber = tags.get('addr:housenumber', '')
                    postcode = tags.get('addr:postcode', '')
                    city = tags.get('addr:city', '')
                    
                    if street or housenumber:
                        address = f"{street} {housenumber}".strip()
                        if postcode or city:
                            address += f", {postcode} {city}".strip()
                    else:
                        address = "Adresse nicht hinterlegt"
                    
                    email = tags.get('email', tags.get('contact:email', None))
                    website = tags.get('website', tags.get('contact:website', None))
                    
                    businesses.append({
                        'name': name,
                        'address': address,
                        'email': email,
                        'website': website
                    })
                    
            print(f"Erfolgreich gefilterte Daten von {url} geladen!")
            return businesses

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Server {url} fehlgeschlagen ({e}). Wechsle zum nächsten Mirror...")
            continue
            
    print("❌ Alle Overpass-Server sind aktuell nicht erreichbar.")
    return []