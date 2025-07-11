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

# Special display name formatting rules
SPECIAL_DISPLAY_NAMES = {
    # Hyphenated base names
    "ho-oh": "Ho-Oh",
    "porygon-z": "Porygon-Z",
    "jangmo-o": "Jangmo-o",
    "hakamo-o": "Hakamo-o",
    "kommo-o": "Kommo-o",
    "type-null": "Type: Null",
    "tapu-koko": "Tapu Koko",
    "tapu-lele": "Tapu Lele",
    "tapu-bulu": "Tapu Bulu",
    "tapu-fini": "Tapu Fini",
    "mr-mime": "Mr. Mime",
    "mr-rime": "Mr. Rime",
    "mime-jr": "Mime Jr.",
    "farfetchd": "Farfetch'd",
    "sirfetchd": "Sirfetch'd",
    
    # Form display names
    "castform-sunny": "Castform (Sunny Form)",
    "castform-rainy": "Castform (Rainy Form)",
    "castform-snowy": "Castform (Snowy Form)",
    "deoxys-normal": "Deoxys (Normal Forme)",
    "deoxys-attack": "Deoxys (Attack Forme)",
    "deoxys-defense": "Deoxys (Defense Forme)",
    "deoxys-speed": "Deoxys (Speed Forme)",
    "wormadam-plant": "Wormadam (Plant Cloak)",
    "wormadam-sandy": "Wormadam (Sandy Cloak)",
    "wormadam-trash": "Wormadam (Trash Cloak)",
    "giratina-altered": "Giratina (Altered Forme)",
    "giratina-origin": "Giratina (Origin Forme)",
    "shaymin-land": "Shaymin (Land Forme)",
    "shaymin-sky": "Shaymin (Sky Forme)",
    "basculin-red-striped": "Basculin (Red Striped)",
    "basculin-blue-striped": "Basculin (Blue Striped)",
    "darmanitan-standard": "Darmanitan (Standard Mode)",
    "darmanitan-zen": "Darmanitan (Zen Mode)",
    "tornadus-incarnate": "Tornadus (Incarnate Forme)",
    "tornadus-therian": "Tornadus (Therian Forme)",
    "thundurus-incarnate": "Thundurus (Incarnate Forme)",
    "thundurus-therian": "Thundurus (Therian Forme)",
    "landorus-incarnate": "Landorus (Incarnate Forme)",
    "landorus-therian": "Landorus (Therian Forme)",
    "keldeo-ordinary": "Keldeo (Ordinary Form)",
    "keldeo-resolute": "Keldeo (Resolute Form)",
    "meloetta-aria": "Meloetta (Aria Forme)",
    "meloetta-pirouette": "Meloetta (Pirouette Forme)",
    "aegislash-shield": "Aegislash (Shield Forme)",
    "aegislash-blade": "Aegislash (Blade Forme)",
    "pumpkaboo-average": "Pumpkaboo (Average Size)",
    "gourgeist-average": "Gourgeist (Average Size)",
    
    # Regional forms
    "rattata-alola": "Alolan Rattata",
    "raticate-alola": "Alolan Raticate",
    "raichu-alola": "Alolan Raichu",
    "sandshrew-alola": "Alolan Sandshrew",
    "sandslash-alola": "Alolan Sandslash",
    "vulpix-alola": "Alolan Vulpix",
    "ninetales-alola": "Alolan Ninetales",
    "diglett-alola": "Alolan Diglett",
    "dugtrio-alola": "Alolan Dugtrio",
    "meowth-alola": "Alolan Meowth",
    "persian-alola": "Alolan Persian",
    "geodude-alola": "Alolan Geodude",
    "graveler-alola": "Alolan Graveler",
    "golem-alola": "Alolan Golem",
    "grimer-alola": "Alolan Grimer",
    "muk-alola": "Alolan Muk",
    "exeggutor-alola": "Alolan Exeggutor",
    "marowak-alola": "Alolan Marowak",
    "meowth-galar": "Galarian Meowth",
    "ponyta-galar": "Galarian Ponyta",
    "rapidash-galar": "Galarian Rapidash",
    "slowpoke-galar": "Galarian Slowpoke",
    "slowbro-galar": "Galarian Slowbro",
    "farfetchd-galar": "Galarian Farfetch'd",
    "weezing-galar": "Galarian Weezing",
    "mr-mime-galar": "Galarian Mr. Mime",
    "articuno-galar": "Galarian Articuno",
    "zapdos-galar": "Galarian Zapdos",
    "moltres-galar": "Galarian Moltres",
    "slowking-galar": "Galarian Slowking",
    "corsola-galar": "Galarian Corsola",
    "zigzagoon-galar": "Galarian Zigzagoon",
    "linoone-galar": "Galarian Linoone",
    "darumaka-galar": "Galarian Darumaka",
    "darmanitan-galar": "Galarian Darmanitan",
    "yamask-galar": "Galarian Yamask",
    "stunfisk-galar": "Galarian Stunfisk",
}

def get_generation(species_id):
    """Determine generation based on species ID"""
    for start, end, gen in GEN_RANGES:
        if start <= species_id <= end:
            return gen
    return 9  # Default to latest generation if unknown

def get_human_readable_name(api_name):
    """Convert API name to human-readable display name"""
    # First check if we have a special display rule
    if api_name in SPECIAL_DISPLAY_NAMES:
        return SPECIAL_DISPLAY_NAMES[api_name]
    
    # Handle standard transformations
    if '-' in api_name:
        parts = api_name.split('-')
        # Capitalize each part and join with space
        display_name = ' '.join(part.capitalize() for part in parts)
        
        # Special handling for Mega forms
        if parts[-1].startswith('mega'):
            base = ' '.join(part.capitalize() for part in parts[:-1])
            return f"Mega {base}"
            
        # Special handling for Primal forms
        if parts[-1] == 'primal':
            base = ' '.join(part.capitalize() for part in parts[:-1])
            return f"Primal {base}"
            
        return display_name
    
    # Simple capitalization for names without hyphens
    return api_name.capitalize()

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
        time.sleep(0.01)  # DISRESPECT API rate limits (100 requests/min)
        data = requests.get(pokemon['url']).json()
        
        # Extract species information
        species_name = data['species']['name']
        species_id = species_data.get(species_name, 0)
        generation = get_generation(species_id)
        
        # Get human-readable display name
        display_name = get_human_readable_name(data['name'])
        
        # Extract types
        types = [t['type']['name'] for t in data['types']]
        type1 = types[0].capitalize() if types else ''
        type2 = types[1].capitalize() if len(types) > 1 else ''
        
        # Extract physical characteristics
        height = data['height']  # In decimeters
        weight = data['weight']  # In hectograms
        
        all_forms.append({
            'name': display_name,
            'generation': generation,
            'type1': type1,
            'type2': type2,
            'height': height,
            'weight': weight
        })
        
        print(f"Processed {idx+1}/{len(pokemon_response['results'])}: {display_name}")

    # Step 4: Write to CSV
    with open('pokemon_forms_human_readable.csv', 'w', newline='', encoding='utf-8') as f:
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

    print(f"CSV generated with {len(all_forms)} Pokémon forms")

if __name__ == '__main__':
    main()