import json
import random

# Read the JSON file
with open('user_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Get player data from _userData
players = data["_userData"]

# IDs to exclude
excluded_ids = ['76561198089766116', '76561198394871655']

# Filter players with playtime + afkTime greater than 36000 and exclude specific IDs
filtered_players = {k: v for k, v in players.items() if v['playtime'] + v['afkTime'] > 36000 and k not in excluded_ids}

# Calculate tickets for each player (1 ticket per hour)
for player_info in filtered_players.values():
    total_time = player_info['playtime'] + player_info['afkTime']
    player_info['tickets'] =  int(total_time // 3600)  # 3600 seconds = 1 hour

# Create a list of tickets
all_tickets = []
for steam_id, player_info in filtered_players.items():
    all_tickets.extend([steam_id] * player_info['tickets'])

# List all players that meet the criteria
print("Players with playtime + afkTime greater than 36000:")
for steam_id, player_info in filtered_players.items():
    total_time = player_info['playtime'] + player_info['afkTime']
    print(f"Display Name: {player_info['displayName']}, Total Time: {total_time}, Tickets: {player_info['tickets']}")

# Count the number of players meeting the criteria
player_count = len(filtered_players)
print(f"\nTotal number of players meeting the criteria: {player_count}")

# Randomly select one player based on tickets
if all_tickets:
    random_player_id = random.choice(all_tickets)
    random_player_info = filtered_players[random_player_id]
    total_time = random_player_info['playtime'] + random_player_info['afkTime']

    print("\nRandomly selected player:")
    print(f"Display Name: {random_player_info['displayName']}, Total Time: {total_time}, Tickets: {random_player_info['tickets']}")
else:
    print("\nNo players with playtime + afkTime greater than 36000 found.")