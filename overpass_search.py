import concurrent.futures
import requests

def _fetch_from_endpoint(url, query, headers, timeout):
    """Hilfsfunktion für einen einzelnen Server-Request."""
    response = requests.post(url, data={'data': query}, headers=headers, timeout=timeout)
    response.raise_for_status()
    return url, response.json()

def get_businesses_in_radius(lat, lon, radius_km=1.5):
    endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.private.coffee/api/interpreter",
        "https://ovp.dresel.systems/api/interpreter"
    ]
    
    radius_meters = int(radius_km * 1000)
    
    # Timeout in der Query auf 60 Sekunden erhöht
    query = f"""
    [out:json][timeout:60];
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
    
    print("Sende parallele Anfrage an alle 3 Overpass-Server...")
    
    data = None
    success_url = None

    # Alle Requests gleichzeitig (parallel) starten
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(endpoints)) as executor:
        future_to_url = {
            executor.submit(_fetch_from_endpoint, url, query, headers, 60): url 
            for url in endpoints
        }
        
        # Auf den ersten Server warten, der erfolgreich antwortet
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result_url, result_data = future.result()
                success_url = result_url
                data = result_data
                print(f"🚀 Erster erfolgreicher Server: {success_url}")
                break  # Wir haben unser Ergebnis, abbrechen und weiterverarbeiten!
            except Exception as e:
                print(f"⚠️ Server {url} hat zu lange gebraucht oder Fehler: {e}")

    if not data:
        print("❌ Alle Overpass-Server sind aktuell nicht erreichbar.")
        return []

    # Daten verarbeiten
    businesses = []
    seen_names = set()
    
    for element in data.get('elements', []):
        tags = element.get('tags', {})
        name = tags.get('name')
        
        if name and name not in seen_names:
            if any(keyword in name.lower() for keyword in ["straße", "weg", "allee", "platz"]):
                continue
                
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
            
    return businesses