import requests

def get_businesses_in_radius(lat, lon, radius_km=1.5):
    # Liste von alternativen Overpass-Servern (Failover-Kette)
    endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.private.coffee/api/interpreter",
        "https://ovp.dresel.systems/api/interpreter"
    ]
    
    radius_meters = int(radius_km * 1000)
    
    query = f"""
    [out:json][timeout:30];
    (
      node(around:{radius_meters},{lat},{lon})[shop];
      way(around:{radius_meters},{lat},{lon})[shop];
      node(around:{radius_meters},{lat},{lon})[amenity];
      way(around:{radius_meters},{lat},{lon})[amenity];
    );
    out body center;
    """
    
    headers = {
        'User-Agent': 'MinijobMailer/1.0 (Schulprojekt)'
    }
    
    # Schleife für das automatische Failover
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
                
                if name and name not in seen_names:
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
                    
            print(f"Erfolgreich Daten von {url} geladen!")
            return businesses

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Server {url} fehlgeschlagen ({e}). Wechsle zum nächsten Mirror...")
            continue
            
    print("❌ Alle Overpass-Server sind aktuell nicht erreichbar oder im Timeout.")
    return []