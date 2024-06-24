import requests
import csv
import os

# Base URL for fetching ability data
base_url = "https://pokeapi.co/api/v2/ability/"

# Directory to save CSV files
output_dir = "csv_files"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to fetch ability data
def fetch_ability_data(ability_id):
    url = base_url + str(ability_id)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to extract relevant data from the ability JSON
def extract_ability_data(ability_json):
    id = ability_json['id']
    effect_entries = ability_json['effect_entries']
    extracted_data = []

    for entry in effect_entries:
        effect = entry['effect']
        language = entry['language']['name']
        short_effect = entry['short_effect']
        extracted_data.append([id, effect, language, short_effect])

    return extracted_data

# Function to write data to CSV
def write_to_csv(start_id, end_id, data):
    file_name = f"abilities_{start_id}_to_{end_id}.csv"
    file_path = os.path.join(output_dir, file_name)
    header = ['pokemon_ability_id', 'effect', 'language', 'short_effect']

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header
        if data:
            writer.writerows(data)  # Write the data if it exists

# Main script to fetch and save data in batches of 100
batch_size = 100
for start_id in range(1, 1000, batch_size):
    end_id = start_id + batch_size - 1
    batch_data = []

    for ability_id in range(start_id, end_id + 1):
        ability_data = fetch_ability_data(ability_id)
        if ability_data:
            batch_data.extend(extract_ability_data(ability_data))

    write_to_csv(start_id, end_id, batch_data)
    print(f"Saved abilities {start_id} to {end_id} to CSV.")
