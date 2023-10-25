import requests

# Define the DataDragon API endpoints for champion data and versions
data_dragon_base_url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"


# Function to fetch the list of skins from a champion
def get_champion_skins(version, champion_name):
    champion_url = data_dragon_base_url.format(version=version)
    response = requests.get(champion_url)
    if response.status_code == 200:
        data = response.json()
        champion_data = data.get("data", {}).get(champion_name, {})
        return champion_data.get("skins", [])
    else:
        print(f"Failed to fetch data for {champion_name}. Error: {response.status_code}")
        return []


# Function to fetch all champions in a version
def get_all_champions(version):
    champion_url = data_dragon_base_url.format(version=version)
    response = requests.get(champion_url)
    if response.status_code == 200:
        data = response.json()
        return list(data.get("data", {}).keys())
    else:
        print(f"Failed to fetch champion data for version {version}. Error: {response.status_code}")
        return []


# Function to compare and list new skins for a given champion between two versions
def compare_and_list_new_skins(champion_name, latest_version, previous_version):
    latest_champion_data = get_champion_skins(latest_version, champion_name)
    previous_champion_data = get_champion_skins(previous_version, champion_name)

    new_skins = [skin["name"] for skin in latest_champion_data if skin not in previous_champion_data]

    if new_skins:
        print(f"New skins for {champion_name} in version {latest_version}:")
        for skin in new_skins:
            print(skin)
    else:
        print(f"No new skins found for {champion_name} in version {latest_version}")


# Fetch the latest and previous versions
response = requests.get(versions_url)
if response.status_code == 200:
    versions = response.json()
    if len(versions) >= 2:
        latest_version = versions[0]
        previous_version = versions[1]

        # Get the list of all champions
        champion_names = get_all_champions(latest_version)

        for champion_name in champion_names:
            compare_and_list_new_skins(champion_name, latest_version, previous_version)
    else:
        print("Insufficient versions for comparison.")
else:
    print(f"Failed to fetch version data. Error: {response.status_code}")
