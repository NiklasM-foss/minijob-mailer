import requests

def get_businesses_in_radius(lat, lon, radius_km=5):
    # Stabilen Mirror verwenden, um 502 Bad Gateway zu vermeiden
    url = "https://overpass.kumi.systems/api/interpreter"
    
    radius_meters = int(radius_km * 1000)
    
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
                
        return businesses

    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der Overpass-Abfrage: {e}")
        return []