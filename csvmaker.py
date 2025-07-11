import requests
import time
import csv

# Define generation ranges based on Pokémon species ID
GEN_RANGES = [
    (1, 151, 1),
    (152, 251, 2),
    (252, 386, 3),
    (387, 493, 4),
    (494, 649, 5),
    (650, 721, 6),
    (722, 809, 7),
    (810, 898, 8),
    (899, 1025, 9)  # Current maximum species ID
]

def get_generation(species_id):
    """Determine generation based on species ID"""
    for start, end, gen in GEN_RANGES:
        if start <= species_id <= end:
            return gen
    return 9  # Default to latest generation if unknown

def main():
    # Step 1: Fetch species data (for generation mapping)
    species_data = {}
    species_url = "https://pokeapi.co/api/v2/pokemon-species?limit=2000"
    species_response = requests.get(species_url).json()
    
    for species in species_response['results']:
        species_id = int(species['url'].split('/')[-2])
        species_data[species['name']] = species_id

    # Step 2: Fetch all Pokémon forms
    all_forms = []
    pokemon_url = "https://pokeapi.co/api/v2/pokemon?limit=1300"
    pokemon_response = requests.get(pokemon_url).json()
    
    # Step 3: Process each form with rate limiting
    for idx, pokemon in enumerate(pokemon_response['results']):
        time.sleep(0.05)  # Respect API rate limits (100 requests/min)
        data = requests.get(pokemon['url']).json()
        
        # Extract species information
        species_name = data['species']['name']
        species_id = species_data.get(species_name, 0)
        generation = get_generation(species_id)
        
        # Extract types
        types = [t['type']['name'] for t in data['types']]
        type1 = types[0] if types else ''
        type2 = types[1] if len(types) > 1 else ''
        
        # Extract physical characteristics
        height = data['height']  # In decimeters
        weight = data['weight']  # In hectograms
        
        all_forms.append({
            'name': data['name'],
            'generation': generation,
            'type1': type1,
            'type2': type2,
            'height': height,
            'weight': weight
        })
        
        print(f"Processed {idx+1}/{len(pokemon_response['results'])}: {data['name']}")

    # Step 4: Write to CSV
    with open('pokemon_forms.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Name', 'Generation', 'Type1', 'Type2', 'Height', 'Weight'])
        writer.writeheader()
        for form in all_forms:
            writer.writerow({
                'Name': form['name'],
                'Generation': form['generation'],
                'Type1': form['type1'],
                'Type2': form['type2'],
                'Height': form['height'],
                'Weight': form['weight']
            })

    print("CSV generated with", len(all_forms), "Pokémon forms")

if __name__ == '__main__':
    main()