import json
import random
import tkinter as tk
from tkinter import ttk, messagebox

# Read the JSON file
with open('user_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Get player data from _userData
players = data["_userData"]

# IDs to exclude
excluded_ids = ['76561198089766116', '76561198394871655']

# Minimum required playtime (in seconds)
min_playtime = 36000

def draw_player():
    # Clear previous results
    results_text.config(state=tk.NORMAL)
    results_text.delete('1.0', tk.END)
    
    # Run the draw logic
    run_draw()
    
    # Display results
    results_text.config(state=tk.DISABLED)

def run_draw():
    # Filter players with playtime + afkTime greater than min_playtime and exclude specific IDs
    filtered_players = {k: v for k, v in players.items() if v['playtime'] + v['afkTime'] > min_playtime and k not in excluded_ids}

    # Calculate tickets for each player (1 ticket per hour)
    for player_info in filtered_players.values():
        total_time = player_info['playtime'] + player_info['afkTime']
        player_info['tickets'] = max(1, int(total_time // 3600))  # Ensure at least 1 ticket

    # Create ticket pool
    all_tickets = []
    for steam_id, player_info in filtered_players.items():
        all_tickets.extend([steam_id] * player_info['tickets'])
    results_text.insert(tk.END, f"Total tickets: {len(all_tickets)}\n")

    # List all players that meet the criteria
    results_text.insert(tk.END, "Players in the draw:\n")
    for steam_id, player_info in filtered_players.items():
        total_time = player_info['playtime'] + player_info['afkTime']
        results_text.insert(tk.END, f"Display Name: {player_info['displayName']}, Total Time: {total_time}, Tickets: {player_info['tickets']}\n")

    # Count the number of players meeting the criteria
    player_count = len(filtered_players)
    results_text.insert(tk.END, f"\nTotal number of players in the draw: {player_count}\n")

    # Randomly select one player based on tickets
    if all_tickets:
        random_player_id = random.choice(all_tickets)
        random_player_info = filtered_players[random_player_id]
        total_time = random_player_info['playtime'] + random_player_info['afkTime']

        results_text.insert(tk.END, "\nRandomly selected player:\n")
        results_text.insert(tk.END, f"Display Name: {random_player_info['displayName']}, Total Time: {total_time}, Tickets: {random_player_info['tickets']}\n")
    else:
        results_text.insert(tk.END, "\nNo players found for the draw.\n")

# Create the main window
root = tk.Tk()
root.title("Player Draw")
root.geometry("600x400")

# Create and pack widgets
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Draw button
draw_button = ttk.Button(frame, text="Draw Player", command=draw_player)
draw_button.grid(column=0, row=0, columnspan=2, pady=10)

# Results display
results_text = tk.Text(frame, wrap=tk.WORD, width=60, height=15)
results_text.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
results_text.config(state=tk.DISABLED)

# Scrollbar for results
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=results_text.yview)
scrollbar.grid(column=2, row=1, sticky=(tk.N, tk.S))
results_text.configure(yscrollcommand=scrollbar.set)

# Configure grid weights
frame.columnconfigure(1, weight=1)
frame.rowconfigure(1, weight=1)

# Start the GUI event loop
root.mainloop()
