"""
Borders of Aeon: Battle Arena
============================

A tactical battle simulation game where warriors with different types and abilities face off in 1v1 or 3v3 matches.

Game Features
------------
1. Warrior Management
   - Create, edit, and delete warriors
   - Three warrior types: Tough, Dexterous, and Smart
   - Customizable stats: HP, damage, attack speed, etc.
   - Type advantages create strategic depth

2. Item System
   - Create and manage items
   - Items modify warrior stats
   - Equipment slots for each warrior
   - Strategic item allocation

3. Battle System
   - 1v1 or 3v3 battle modes
   - Real-time battle simulation
   - Type-based combat mechanics
   - Detailed battle logs

Type Advantages
--------------
• Tough vs Dexterous: 20% chance to stun for 1 second
• Smart vs Tough: 20% chance for +50% damage
• Smart vs Dexterous: 20% chance to miss completely

Warrior Stats
------------
• Toughness: Affects HP and HP regeneration
• Dexterity: Affects defense and attack speed
• Intelligence: Affects damage output
• Base Stats: Min/max damage, attack time
• Level-up Stats: Stat growth per level

Item Effects
-----------
• Add Tough: Increases toughness stat
• Add Dex: Increases dexterity stat
• Add Smart: Increases intelligence stat
• Add HP: Increases max health
• Add HP Regen: Increases health regeneration
• Add DMG: Increases damage output
• Add Defense: Reduces damage taken
• Add Attack Speed: Increases attack speed

User Manual
----------
1. Managing Warriors:
   - Click "Add Warrior" to create new warriors
   - Select a warrior and click "Edit" to modify stats
   - Delete unwanted warriors with "Delete"
   - Required fields: name, type, and basic stats

2. Managing Items:
   - Create items using "Add Item"
   - Modify existing items with "Edit"
   - Remove items using "Delete"
   - All stat modifications should be numbers

3. Battle Simulation:
   - Choose 1v1 or 3v3 battle mode
   - Select warriors for each team
   - Optionally equip items
   - Click "Start Battle" to begin
   - Watch the battle unfold in the log window
   - Use "Refresh Lists" to update warrior/item selections

File Structure
-------------
config/
    warriors.csv - Stores warrior data
    items.csv - Stores item data

Dependencies
-----------
- Python 3.x
- tkinter (usually included with Python)
- Standard library modules: csv, random, os

Author
------
John Kenneth Realingo

"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import random
import os

class BattleArenaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Borders of Aeon: Battle Arena")
        self.root.geometry("1024x768")
        
        # Create config directory if it doesn't exist
        self.config_dir = "config"
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        # Tabs for different functionalities
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.warriors_tab = ttk.Frame(self.notebook)
        self.items_tab = ttk.Frame(self.notebook)
        self.simulation_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.warriors_tab, text="Manage Warriors")
        self.notebook.add(self.items_tab, text="Manage Items")
        self.notebook.add(self.simulation_tab, text="Battle Simulation")
        
        # Ensure CSV files exist
        self.create_csv_files()
        
        # Initialize functionalities
        self.init_warrior_management()
        self.init_item_management()
        self.init_simulation()

    # Utility: Read CSV
    def read_csv(self, filename):
        if not os.path.exists(filename):
            return []
        with open(filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            return list(reader)
        
    # Utility: Write CSV
    def write_csv(self, filename, data, fieldnames):
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def create_csv_files(self):
        # Create warriors.csv if it doesn't exist
        warriors_path = os.path.join(self.config_dir, "warriors.csv")
        if not os.path.exists(warriors_path):
            self.write_csv(warriors_path, [], [
                "name", "title", "type", "tough", "inctough", 
                "dex", "incdex", "smart", "incsmart", "min_dmg", 
                "max_dmg", "attack_time"
            ])
            
        # Create items.csv if it doesn't exist
        items_path = os.path.join(self.config_dir, "items.csv")
        if not os.path.exists(items_path):
            self.write_csv(items_path, [], [
                "name", "add_tough", "add_dex", "add_smart", 
                "add_hp", "add_hp_regen", "add_dmg", 
                "add_defense", "add_attack_speed"
            ])

    # 1. Warrior Management Tab
    def init_warrior_management(self):
        ttk.Label(self.warriors_tab, text="Manage Warriors").pack()
        
        # Load warriors from file
        self.warriors = self.read_csv(os.path.join(self.config_dir, "warriors.csv"))
        self.warrior_fieldnames = [
            "name", "title", "type", "tough", "inctough", 
            "dex", "incdex", "smart", "incsmart", "min_dmg", 
            "max_dmg", "attack_time"
        ]
        
        # Warrior List Display
        self.warrior_listbox = tk.Listbox(self.warriors_tab)
        self.warrior_listbox.pack(fill='both', expand=True)
        self.load_warrior_list()

        # Add/Edit Warrior Buttons
        self.warrior_buttons = tk.Frame(self.warriors_tab)
        self.warrior_buttons.pack()

        tk.Button(self.warrior_buttons, text="Add Warrior", command=self.add_warrior).pack(side=tk.LEFT)
        tk.Button(self.warrior_buttons, text="Edit Warrior", command=self.edit_warrior).pack(side=tk.LEFT)
        tk.Button(self.warrior_buttons, text="Delete Warrior", command=self.delete_warrior).pack(side=tk.LEFT)

    def load_warrior_list(self):
        self.warrior_listbox.delete(0, tk.END)
        for warrior in self.warriors:
            self.warrior_listbox.insert(tk.END, f"{warrior['name']} ({warrior['type']})")
        
    def add_warrior(self):
        WarriorEditor(self, mode="add")
        
    def edit_warrior(self):
        selected = self.warrior_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No warrior selected!")
            return
        warrior = self.warriors[selected[0]]
        WarriorEditor(self, mode="edit", warrior=warrior)

    def delete_warrior(self):
        selected = self.warrior_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No warrior selected!")
            return
        self.warriors.pop(selected[0])
        self.write_csv(os.path.join(self.config_dir, "warriors.csv"), self.warriors, self.warrior_fieldnames)
        self.load_warrior_list()

    # 2. Item Management Tab
    def init_item_management(self):
        ttk.Label(self.items_tab, text="Manage Items").pack()
        
        # Load items from file
        self.items = self.read_csv(os.path.join(self.config_dir, "items.csv"))
        self.item_fieldnames = [
            "name", "add_tough", "add_dex", "add_smart", 
            "add_hp", "add_hp_regen", "add_dmg", 
            "add_defense", "add_attack_speed"
        ]
        
        # Item List Display
        self.item_listbox = tk.Listbox(self.items_tab)
        self.item_listbox.pack(fill='both', expand=True)
        self.load_item_list()

        # Add/Edit Item Buttons
        self.item_buttons = tk.Frame(self.items_tab)
        self.item_buttons.pack()

        tk.Button(self.item_buttons, text="Add Item", command=self.add_item).pack(side=tk.LEFT)
        tk.Button(self.item_buttons, text="Edit Item", command=self.edit_item).pack(side=tk.LEFT)
        tk.Button(self.item_buttons, text="Delete Item", command=self.delete_item).pack(side=tk.LEFT)

    def load_item_list(self):
        self.item_listbox.delete(0, tk.END)
        for item in self.items:
            self.item_listbox.insert(tk.END, item['name'])

    def add_item(self):
        ItemEditor(self, mode="add")
        
    def edit_item(self):
        selected = self.item_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No item selected!")
            return
        item = self.items[selected[0]]
        ItemEditor(self, mode="edit", item=item)

    def delete_item(self):
        selected = self.item_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No item selected!")
            return
        self.items.pop(selected[0])
        self.write_csv(os.path.join(self.config_dir, "items.csv"), self.items, self.item_fieldnames)
        self.load_item_list()

    # 3. Simulation Tab
    def init_simulation(self):
        ttk.Label(self.simulation_tab, text="Battle Simulation", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Create main container frame for teams
        teams_frame = ttk.Frame(self.simulation_tab)
        teams_frame.pack(fill='both', expand=True)
        
        # Create frames for team selection and items
        self.team1_frame = ttk.LabelFrame(teams_frame, text="Team 1")
        self.team1_frame.pack(side=tk.LEFT, padx=10, pady=5, fill='both', expand=True)
        
        self.team2_frame = ttk.LabelFrame(teams_frame, text="Team 2")
        self.team2_frame.pack(side=tk.LEFT, padx=10, pady=5, fill='both', expand=True)
        
        # Create dropdown variables and lists
        self.team1_selections = []
        self.team2_selections = []
        self.team1_vars = []
        self.team2_vars = []
        self.team1_dropdowns = []
        self.team2_dropdowns = []
        self.team1_item_vars = []  # New: Item selection variables
        self.team2_item_vars = []
        self.team1_item_dropdowns = []  # New: Item dropdown references
        self.team2_item_dropdowns = []
        
        # Create dropdowns for both teams
        for i in range(3):
            # Team 1 warrior and item selection
            frame1 = ttk.Frame(self.team1_frame)
            frame1.pack(fill='x', pady=5)
            
            # Add labels for warrior and item
            warrior_frame1 = ttk.Frame(frame1)
            warrior_frame1.pack(side=tk.LEFT, fill='x', expand=True)
            ttk.Label(warrior_frame1, text="Warrior:").pack(side=tk.LEFT)
            
            var1 = tk.StringVar()
            self.team1_vars.append(var1)
            dropdown1 = ttk.Combobox(warrior_frame1, textvariable=var1, state="readonly")
            dropdown1.pack(side=tk.LEFT, fill='x', expand=True)
            self.team1_dropdowns.append(dropdown1)
            var1.trace('w', lambda *args, team=1, idx=i: self.on_warrior_select(team, idx))
            
            # Add item frame and label
            item_frame1 = ttk.Frame(frame1)
            item_frame1.pack(side=tk.RIGHT)
            ttk.Label(item_frame1, text="Item:").pack(side=tk.LEFT)
            
            item_var1 = tk.StringVar()
            self.team1_item_vars.append(item_var1)
            item_dropdown1 = ttk.Combobox(item_frame1, textvariable=item_var1, state="readonly", width=15)
            item_dropdown1.pack(side=tk.LEFT)
            self.team1_item_dropdowns.append(item_dropdown1)
            
            # Team 2 warrior and item selection
            frame2 = ttk.Frame(self.team2_frame)
            frame2.pack(fill='x', pady=5)
            
            # Add labels for warrior and item
            warrior_frame2 = ttk.Frame(frame2)
            warrior_frame2.pack(side=tk.LEFT, fill='x', expand=True)
            ttk.Label(warrior_frame2, text="Warrior:").pack(side=tk.LEFT)
            
            var2 = tk.StringVar()
            self.team2_vars.append(var2)
            dropdown2 = ttk.Combobox(warrior_frame2, textvariable=var2, state="readonly")
            dropdown2.pack(side=tk.LEFT, fill='x', expand=True)
            self.team2_dropdowns.append(dropdown2)
            var2.trace('w', lambda *args, team=2, idx=i: self.on_warrior_select(team, idx))
            
            # Add item frame and label
            item_frame2 = ttk.Frame(frame2)
            item_frame2.pack(side=tk.RIGHT)
            ttk.Label(item_frame2, text="Item:").pack(side=tk.LEFT)
            
            item_var2 = tk.StringVar()
            self.team2_item_vars.append(item_var2)
            item_dropdown2 = ttk.Combobox(item_frame2, textvariable=item_var2, state="readonly", width=15)
            item_dropdown2.pack(side=tk.LEFT)
            self.team2_item_dropdowns.append(item_dropdown2)
        
        # Control frame
        control_frame = ttk.Frame(self.simulation_tab)
        control_frame.pack(side=tk.BOTTOM, fill='x', pady=10)
        
        # Battle type selection
        self.battle_type = tk.StringVar(value="1v1")
        ttk.Radiobutton(control_frame, text="1v1 Battle", variable=self.battle_type, 
                        value="1v1", command=self.update_battle_mode).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="3v3 Battle", variable=self.battle_type, 
                        value="3v3", command=self.update_battle_mode).pack(side=tk.LEFT, padx=5)
        
        # Battle button
        ttk.Button(control_frame, text="Start Battle", 
                   command=self.run_simulation).pack(side=tk.RIGHT, padx=5)
        
        # Add refresh button
        ttk.Button(control_frame, text="Refresh Lists", 
                   command=self.load_simulation_warriors).pack(side=tk.LEFT, padx=5)
        
        # Results display - increase height
        self.result_text = tk.Text(self.simulation_tab, height=20, width=80)
        self.result_text.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Add scrollbar to results
        result_scrollbar = ttk.Scrollbar(self.simulation_tab, orient='vertical', command=self.result_text.yview)
        result_scrollbar.pack(side='right', fill='y')
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        
        # Initial load of warriors
        self.load_simulation_warriors()
        
        # Initial battle mode setup
        self.update_battle_mode()

    def update_battle_mode(self):
        mode = self.battle_type.get()
        required_warriors = 3 if mode == "3v3" else 1
        
        # Show/hide dropdowns based on battle mode
        for i in range(3):
            frame1 = self.team1_dropdowns[i].master.master  # Get the parent frame
            frame2 = self.team2_dropdowns[i].master.master  # Get the parent frame
            
            if i < required_warriors:
                self.team1_vars[i].set('')  # Clear selection
                self.team2_vars[i].set('')  # Clear selection
                self.team1_item_vars[i].set('')  # Clear item selection
                self.team2_item_vars[i].set('')  # Clear item selection
                frame1.pack(pady=5, padx=5, fill='x')  # Show warrior frame
                frame2.pack(pady=5, padx=5, fill='x')  # Show warrior frame
            else:
                frame1.pack_forget()  # Hide warrior frame
                frame2.pack_forget()  # Hide warrior frame
        
        # Reset selections
        self.team1_selections = []
        self.team2_selections = []
        
        # Refresh available warriors
        self.update_available_warriors()

    def on_warrior_select(self, team, index):
        # Get the selected warrior
        var = self.team1_vars[index] if team == 1 else self.team2_vars[index]
        selection = var.get()
        
        # Update selections list
        selections = self.team1_selections if team == 1 else self.team2_selections
        
        # Remove old selection at this index if it exists
        if len(selections) > index:
            selections[index] = selection
        else:
            selections.append(selection)
        
        # Update available warriors for all dropdowns
        self.update_available_warriors()

    def update_available_warriors(self):
        # Get all warriors
        all_warriors = [f"{w['name']} ({w['type']})" for w in self.warriors]
        
        # Get currently selected warriors for both teams
        team1_selected = [var.get() for var in self.team1_vars if var.get()]
        team2_selected = [var.get() for var in self.team2_vars if var.get()]
        
        # Update dropdowns for both teams
        for i in range(3):
            # Available warriors are those not selected in any dropdown except current one
            current_selection1 = self.team1_vars[i].get()
            current_selection2 = self.team2_vars[i].get()
            
            # Filter out warriors that are already selected, except for current dropdown
            available1 = [''] + [w for w in all_warriors if w not in team1_selected + team2_selected or w == current_selection1]
            available2 = [''] + [w for w in all_warriors if w not in team1_selected + team2_selected or w == current_selection2]
            
            # Update dropdown values
            self.team1_dropdowns[i]['values'] = available1
            self.team2_dropdowns[i]['values'] = available2

    def load_simulation_warriors(self):
        # Clear battle logs
        self.result_text.delete(1.0, tk.END)
        
        # Reload warriors and items from file
        self.warriors = self.read_csv(os.path.join(self.config_dir, "warriors.csv"))
        self.items = self.read_csv(os.path.join(self.config_dir, "items.csv"))
        
        # Reset selections
        self.team1_selections = []
        self.team2_selections = []
        
        # Clear all dropdowns
        for var in self.team1_vars + self.team2_vars:
            var.set('')
        for var in self.team1_item_vars + self.team2_item_vars:
            var.set('')
        
        # Update available warriors
        self.update_available_warriors()
        
        # Update available items
        item_list = [''] + [item['name'] for item in self.items]
        for dropdown in self.team1_item_dropdowns + self.team2_item_dropdowns:
            dropdown['values'] = item_list

    def run_simulation(self):
        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        
        # Get required number of warriors based on battle type
        required_warriors = 3 if self.battle_type.get() == "3v3" else 1
        
        # Validate selections
        team1_selected = [var.get() for var in self.team1_vars[:required_warriors] if var.get()]
        team2_selected = [var.get() for var in self.team2_vars[:required_warriors] if var.get()]
        
        if len(team1_selected) != required_warriors or len(team2_selected) != required_warriors:
            messagebox.showerror("Error", 
                f"Please select exactly {required_warriors} warrior(s) for each team!")
            return
        
        # Get warrior and item data
        team1 = []
        team2 = []
        
        for i, selection in enumerate(team1_selected):
            name = selection.split(" (")[0]
            warrior = next((w for w in self.warriors if w['name'] == name), None)
            if warrior:
                item_name = self.team1_item_vars[i].get()
                item = next((item for item in self.items if item['name'] == item_name), None)
                team1.append({'warrior': warrior, 'item': item})
        
        for i, selection in enumerate(team2_selected):
            name = selection.split(" (")[0]
            warrior = next((w for w in self.warriors if w['name'] == name), None)
            if warrior:
                item_name = self.team2_item_vars[i].get()
                item = next((item for item in self.items if item['name'] == item_name), None)
                team2.append({'warrior': warrior, 'item': item})
        
        # Simulate battle
        result = self.simulate_battle(team1, team2)
        
        # Display results
        self.result_text.insert(tk.END, result)

    def init_warrior_state(self, warrior_data):
        warrior = warrior_data['warrior']
        item = warrior_data['item']
        
        # Define numeric fields
        numeric_fields = [
            'tough', 'inctough', 'dex', 'incdex', 'smart', 
            'incsmart', 'min_dmg', 'max_dmg', 'attack_time'
        ]
        
        # Convert only numeric stats to float
        stats = {
            k: float(v) if k in numeric_fields else v 
            for k, v in warrior.items()
        }
        
        # Apply item bonuses if an item is equipped
        if item:
            stats['tough'] += float(item['add_tough'])
            stats['dex'] += float(item['add_dex'])
            stats['smart'] += float(item['add_smart'])
        
        # Calculate derived stats
        base_hp = 150
        hp = base_hp + stats['tough'] * 20
        hp_regen = 0.25 + stats['tough'] * 0.05
        defense = stats['dex'] * 2
        attack_speed = stats['dex']
        
        # Apply additional item bonuses
        if item:
            hp += float(item['add_hp'])
            hp_regen += float(item['add_hp_regen'])
            defense += float(item['add_defense'])
            attack_speed += float(item['add_attack_speed'])
        
        # Calculate actual damage range
        min_dmg = stats['min_dmg'] + stats['smart'] * 3
        max_dmg = stats['max_dmg'] + stats['smart'] * 3
        
        if item:
            min_dmg += float(item['add_dmg'])
            max_dmg += float(item['add_dmg'])
        
        # Calculate attack cooldown
        base_cooldown = float(stats['attack_time'])
        actual_cooldown = base_cooldown / (1 + attack_speed/100)
        
        state = {
            'name': warrior['name'],
            'type': warrior['type'],
            'hp': hp,
            'max_hp': hp,
            'hp_regen': hp_regen,
            'defense': defense,
            'min_dmg': min_dmg,
            'max_dmg': max_dmg,
            'cooldown': actual_cooldown,
            'next_attack': actual_cooldown,
            'stun_end': 0,
            'stun_immune': 0,
            'stun_diminish': 1.0
        }
        
        return state

    def simulate_battle(self, team1, team2):
        result_text = "=== Battle Report ===\n\n"
        
        # Initialize battle states
        team1_states = [self.init_warrior_state(w) for w in team1]
        team2_states = [self.init_warrior_state(w) for w in team2]
        
        # Print initial stats
        result_text += "Initial Stats:\n"
        for team_name, team_states in [("Team 1", team1_states), ("Team 2", team2_states)]:
            result_text += f"\n{team_name}:\n"
            for state in team_states:
                result_text += (
                    f"{state['name']} ({state['type']}):\n"
                    f"  HP: {state['hp']:.1f}\n"
                    f"  HP Regen: {state['hp_regen']:.2f}/s\n"
                    f"  Defense: {state['defense']:.1f}\n"
                    f"  Damage: {state['min_dmg']:.1f}-{state['max_dmg']:.1f}\n"
                    f"  Attack Speed: {1/state['cooldown']:.2f}/s\n"
                )
        
        result_text += "\nBattle Begin!\n"
        
        # Battle simulation loop
        time = 0
        max_time = 300  # 5 minute time limit
        events = []
        
        while time < max_time:
            current_events = []
            
            # Process HP regeneration every second
            if time % 1 == 0:
                for warrior in team1_states + team2_states:
                    if warrior['hp'] > 0 and warrior['hp'] < warrior['max_hp']:
                        regen = min(warrior['hp_regen'], warrior['max_hp'] - warrior['hp'])
                        warrior['hp'] += regen
                        current_events.append(f"{warrior['name']} regenerates {regen:.1f} HP")
            
            # Process attacks
            for attacker in team1_states + team2_states:
                if attacker['hp'] <= 0:
                    continue
                    
                # Skip if stunned
                if time < attacker['stun_end']:
                    continue
                    
                # Check if ready to attack
                if time >= attacker['next_attack']:
                    # Choose target from opposite team
                    targets = team2_states if attacker in team1_states else team1_states
                    alive_targets = [t for t in targets if t['hp'] > 0]
                    
                    if not alive_targets:
                        continue
                        
                    target = random.choice(alive_targets)
                    
                    # Process type advantages
                    miss = False
                    bonus_dmg = 1.0
                    stun = False
                    
                    if attacker['type'] == 'Smart' and target['type'] == 'Dexterous':
                        if random.random() < 0.2:  # 20% chance to miss
                            miss = True
                            current_events.append(f"{attacker['name']}'s attack misses {target['name']}!")
                    
                    elif attacker['type'] == 'Smart' and target['type'] == 'Tough':
                        if random.random() < 0.2:  # 20% chance for bonus damage
                            bonus_dmg = 1.5
                            current_events.append(f"{attacker['name']} finds a weak spot on {target['name']}!")
                    
                    elif attacker['type'] == 'Tough' and target['type'] == 'Dexterous':
                        if random.random() < 0.2 and time >= target['stun_immune']:  # 20% chance to stun
                            stun = True
                            stun_duration = target['stun_diminish']
                            target['stun_end'] = time + stun_duration
                            target['stun_immune'] = time + stun_duration + 1
                            target['stun_diminish'] *= 0.5
                            current_events.append(f"{attacker['name']} stuns {target['name']} for {stun_duration:.1f}s!")
                    
                    if not miss:
                        # Calculate damage
                        base_damage = random.uniform(attacker['min_dmg'], attacker['max_dmg'])
                        damage_reduction = (0.06 * target['defense']) / (1 + 0.06 * target['defense'])
                        final_damage = max(1, base_damage * (1 - damage_reduction) * bonus_dmg)
                        
                        target['hp'] -= final_damage
                        current_events.append(
                            f"{attacker['name']} deals {final_damage:.1f} damage to {target['name']} "
                            f"(reduced from {base_damage:.1f})"
                        )
                        
                        if target['hp'] <= 0:
                            current_events.append(f"{target['name']} has been defeated!")
                    
                    # Set next attack time
                    attacker['next_attack'] = time + attacker['cooldown']
            
            # Add events to log if any occurred
            if current_events:
                events.append(f"\nTime {time:.1f}s:")
                events.extend(current_events)
            
            # Check victory conditions
            team1_alive = any(w['hp'] > 0 for w in team1_states)
            team2_alive = any(w['hp'] > 0 for w in team2_states)
            
            if not team1_alive or not team2_alive:
                break
            
            time += 0.1  # Advance time in 0.1 second increments
        
        # Format battle log
        result_text += "\n".join(events)
        
        # Add victory declaration
        result_text += "\n\nBattle Results:\n"
        if not team2_alive:
            result_text += "Team 1 is victorious!\n"
        elif not team1_alive:
            result_text += "Team 2 is victorious!\n"
        else:
            result_text += "Battle ended in a draw (time limit reached)\n"
        
        return result_text

class WarriorEditor:
    def __init__(self, parent, mode, warrior=None):
        self.parent = parent
        self.mode = mode
        self.warrior = warrior or {}
        
        # Create new window
        self.editor = tk.Toplevel()
        self.editor.title("Warrior Editor")
        self.fields = {}

        # Define warrior types
        self.warrior_types = ["Tough", "Dexterous", "Smart"]

        # Create scrollable frame
        canvas = tk.Canvas(self.editor)
        scrollbar = ttk.Scrollbar(self.editor, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create fields for editing/adding
        for field in parent.warrior_fieldnames:
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            ttk.Label(frame, text=field.replace("_", " ").title()).pack(side=tk.LEFT)
            
            # Special handling for type field
            if field == "type":
                type_var = tk.StringVar(value=self.warrior.get(field, self.warrior_types[0]))
                entry = ttk.Combobox(frame, textvariable=type_var, values=self.warrior_types, state="readonly")
                entry.pack(side=tk.RIGHT, expand=True, fill="x")
                self.fields[field] = type_var  # Store the StringVar instead of the Combobox
            else:
                entry = ttk.Entry(frame)
                entry.pack(side=tk.RIGHT, expand=True, fill="x")
                entry.insert(0, self.warrior.get(field, ""))
                self.fields[field] = entry

        # Add type description
        desc_frame = ttk.Frame(scrollable_frame)
        desc_frame.pack(fill="x", padx=5, pady=10)
        
        desc_text = """Warrior Type Effects:
• Tough vs Dexterous: 20% chance to stun for 1 second
• Smart vs Tough: 20% chance for +50% damage
• Smart vs Dexterous: 20% chance to miss completely"""
        
        ttk.Label(desc_frame, text=desc_text, wraplength=300, justify="left").pack()

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Set a reasonable minimum size for the editor window
        self.editor.geometry("500x700")
        self.editor.minsize(400, 600)

        # Save button
        tk.Button(self.editor, text="Save", command=self.save).pack(pady=10)

    def save(self):
        # Validate numeric fields
        numeric_fields = ["tough", "inctough", "dex", "incdex", "smart", 
                         "incsmart", "min_dmg", "max_dmg", "attack_time"]
        
        new_warrior = {}
        for field in self.parent.warrior_fieldnames:
            if field == "type":
                value = self.fields[field].get()  # Get value from StringVar
            else:
                value = self.fields[field].get().strip()
                
            if field in numeric_fields:
                try:
                    value = float(value) if value else 0
                except ValueError:
                    messagebox.showerror("Error", f"{field} must be a number!")
                    return
            new_warrior[field] = str(value)  # Convert back to string for CSV storage
            
        if self.mode == "add":
            self.parent.warriors.append(new_warrior)
        else:  # Edit mode
            index = self.parent.warriors.index(self.warrior)
            self.parent.warriors[index] = new_warrior
        self.parent.write_csv(os.path.join(self.parent.config_dir, "warriors.csv"), self.parent.warriors, self.parent.warrior_fieldnames)
        self.parent.load_warrior_list()
        self.editor.destroy()

class ItemEditor:
    def __init__(self, parent, mode, item=None):
        self.parent = parent
        self.mode = mode
        self.item = item or {}
        
        # Create new window
        self.editor = tk.Toplevel()
        self.editor.title("Item Editor")
        self.editor.geometry("500x700")
        self.editor.minsize(400, 600)
        self.fields = {}

        # Create scrollable frame
        canvas = tk.Canvas(self.editor)
        scrollbar = ttk.Scrollbar(self.editor, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create fields for editing/adding
        for field in parent.item_fieldnames:
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            ttk.Label(frame, text=field.replace("_", " ").title()).pack(side=tk.LEFT)
            
            entry = ttk.Entry(frame)
            entry.pack(side=tk.RIGHT, expand=True, fill="x")
            entry.insert(0, self.item.get(field, ""))
            self.fields[field] = entry

        # Add item effects description
        desc_frame = ttk.Frame(scrollable_frame)
        desc_frame.pack(fill="x", padx=5, pady=10)
        
        desc_text = """Item Effects:
• Add Tough: Increases toughness stat
• Add Dex: Increases dexterity stat
• Add Smart: Increases intelligence stat
• Add HP: Increases max health
• Add HP Regen: Increases health regeneration
• Add DMG: Increases damage output
• Add Defense: Reduces damage taken
• Add Attack Speed: Increases attack speed"""
        
        ttk.Label(desc_frame, text=desc_text, wraplength=300, justify="left").pack()

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Save button
        tk.Button(self.editor, text="Save", command=self.save).pack(pady=10)

    def save(self):
        # Validate numeric fields
        numeric_fields = ["add_tough", "add_dex", "add_smart", "add_hp", 
                         "add_hp_regen", "add_dmg", "add_defense", "add_attack_speed"]
        
        new_item = {}
        for field in self.parent.item_fieldnames:
            value = self.fields[field].get().strip()
            if field in numeric_fields:
                try:
                    value = float(value) if value else 0
                except ValueError:
                    messagebox.showerror("Error", f"{field} must be a number!")
                    return
            new_item[field] = str(value)  # Convert back to string for CSV storage
            
        if self.mode == "add":
            self.parent.items.append(new_item)
        else:  # Edit mode
            index = self.parent.items.index(self.item)
            self.parent.items[index] = new_item
        self.parent.write_csv(os.path.join(self.parent.config_dir, "items.csv"), self.parent.items, self.parent.item_fieldnames)
        self.parent.load_item_list()
        self.editor.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BattleArenaApp(root)
    root.mainloop()
