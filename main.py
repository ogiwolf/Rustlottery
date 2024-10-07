import json
import random

# Read the JSON file
with open('user_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Get player data from _userData
players = data["_userData"]

# IDs to exclude
excluded_ids = ['76561198089766116', '76561198394871655']

# Blackbox feature - specify a single player (or leave empty for normal draw)
blackbox_player_id = '76561198813057096'  # Set this to a player ID to use blackbox mode, or leave empty for normal draw

# Minimum required playtime (in seconds)
min_playtime = 36000

# Filter players with playtime + afkTime greater than min_playtime and exclude specific IDs
filtered_players = {k: v for k, v in players.items() if v['playtime'] + v['afkTime'] > min_playtime and k not in excluded_ids}

# Add blackbox player to filtered_players if not already present
if blackbox_player_id and blackbox_player_id not in filtered_players:
    if blackbox_player_id in players:
        blackbox_player = players[blackbox_player_id]
        total_time = blackbox_player['playtime'] + blackbox_player['afkTime']
        if total_time <= min_playtime:
            blackbox_player['playtime'] = min_playtime - blackbox_player['afkTime'] + 1
            print(f"Blackbox player {blackbox_player_id} playtime adjusted to meet minimum requirement.")
        filtered_players[blackbox_player_id] = blackbox_player
        print(f"Blackbox player {blackbox_player_id} added to filtered_players.")
    else:
        print(f"Blackbox player {blackbox_player_id} not found in original player list.")

# Calculate tickets for each player (1 ticket per hour)
for player_info in filtered_players.values():
    total_time = player_info['playtime'] + player_info['afkTime']
    player_info['tickets'] = max(1, int(total_time // 3600))  # Ensure at least 1 ticket

# Create ticket pool based on blackbox mode or normal mode
all_tickets = []
if blackbox_player_id and blackbox_player_id in filtered_players:
    all_tickets = [blackbox_player_id] * filtered_players[blackbox_player_id]['tickets']
    print(f"Blackbox mode: {len(all_tickets)} tickets for player {blackbox_player_id}")
else:
    for steam_id, player_info in filtered_players.items():
        all_tickets.extend([steam_id] * player_info['tickets'])
    print(f"Normal mode: {len(all_tickets)} total tickets")

# List all players that meet the criteria
print("Players in the draw:")
for steam_id, player_info in filtered_players.items():
    total_time = player_info['playtime'] + player_info['afkTime']
    print(f"Display Name: {player_info['displayName']}, Total Time: {total_time}, Tickets: {player_info['tickets']}")

# Count the number of players meeting the criteria
player_count = len(filtered_players)
print(f"\nTotal number of players in the draw: {player_count}")

# Randomly select one player based on tickets
if all_tickets:
    random_player_id = random.choice(all_tickets)
    random_player_info = filtered_players[random_player_id]
    total_time = random_player_info['playtime'] + random_player_info['afkTime']

    print("\nRandomly selected player:")
    if blackbox_player_id:
        print("(Blackbox mode)")
    print(f"Display Name: {random_player_info['displayName']}, Total Time: {total_time}, Tickets: {random_player_info['tickets']}")
else:
    print("\nNo players found for the draw.")