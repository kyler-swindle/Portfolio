from __future__ import annotations
from datetime import datetime
import json
from math import comb
import os
import random
import time
from Mon import Mon, Tools, Type, Move, Prestige
from typing import Dict, List, Optional, Tuple, Union

class Player: 
    """A class for storing Player data."""

    def __init__(self, 
                name : Optional[str] = "NAME", 
                health : Optional[int] = 100, 
                level : Optional[int] = 1,
                experience : Optional[int] = 0,
                experience_needed : Optional[int] = 1000,
                checkpoint_needed : Optional[int] = None, 
                mons : Optional[List[Mon]] = None, 
                mon_packs : Optional[int] = 0,
                health_potions : Optional[int] = 0,
                learn_random_moves : Optional[int] = 0,
                learn_specific_moves : Optional[int] = 0,
                weapon  : Optional[Weapon] = None, 
                achievements : Optional[List[Achievement]] = None, 
                encounter_log : Optional[List[str]] = None,
                gamesave : Optional[str] = ""):
        self.name = name
        self.health = health
        self.level = level
        self.experience = experience
        self.experience_needed = experience_needed
        self.checkpoint_needed = checkpoint_needed
        self.mons = mons if mons is not None else []
        self.mon_packs = mon_packs
        self.health_potions = health_potions
        self.learn_random_moves = learn_random_moves
        self.learn_specific_moves = learn_specific_moves
        self.weapon = weapon
        self.achievements = achievements if achievements is not None else []
        self.encounter_log = encounter_log if encounter_log is not None else []
        self.gamesave = gamesave

    def __str__(self):
        mons_str = ""
        for mon in self.mons:
            mons_str += f"{mon}"

        return (
            f"Player name: {self.name}\n"
            f"\tLevel {self.level} ({self.experience} / {self.experience_needed} XP)\n"
            f"\tHP: {self.health}\n"
            f"\tMons: {mons_str}\n"
        )
    
    def player_stats(self):
        return (
            f"Player name: {self.name}\n"
            f"\tLevel {self.level} ({self.experience} / {self.experience_needed} XP)\n"
            f"\tHP: {self.health}\n"
        )

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "level": self.level,
            "experience": self.experience,
            "experience_needed": self.experience_needed,
            "checkpoint_needed": self.checkpoint_needed,
            "mons": [mon.to_dict() for mon in self.mons],  # assumes Mon has .to_dict()
            "mon_packs": self.mon_packs, # [item.to_dict() for item in self.items],  # assumes Item has .to_dict()
            "health_potions": self.health_potions, # [item.to_dict() for item in self.items],  # assumes Item has .to_dict()
            "learn_random_moves" : self.learn_random_moves,
            "learn_specific_moves" : self.learn_specific_moves,
            "weapon": None, # self.weapon.to_dict() if self.weapon else None,
            "achievements": [achv.to_dict() for achv in self.achievements], #[ach.to_dict() for ach in self.achievements]  # assumes Achievement has .to_dict()
            "encounter_log": [str(enc) for enc in self.encounter_log], 
            "gamesave" : self.gamesave
        }

    def level_up(self, recursed_levels : Optional[int] = None): 
        """A method to level-up a Player, if possible, and adjust stats accordingly."""

        # instantiate the recursive count
        if recursed_levels is None:
            recursed_levels = 0

        if self.experience < self.experience_needed: 
            if recursed_levels > 0:
                if recursed_levels == 1:
                    Tools.text(f"You leveled up!\n\n", params=Game.text_effects["System"])
                else:
                    Tools.text(f"You leveled up {recursed_levels} times!\n\n", params=Game.text_effects["System"])
            return
        
        self.level += 1 # increase level
        self.experience -= self.experience_needed # deduct needed experience from the total amount
        self.experience_needed += 1000 # adjust needed experience for next level 

        # update stats
        if random.random() < 0.10:
            self.add_mon_pack() # make random chance for more balanced at higher levels?
        self.add_health_potion()

        # increase recursive level counter for printing
        recursed_levels += 1
        self.level_up(recursed_levels) # recursively call for remaining levels

    def add_experience(self, points : int):
        """A method to add experience points to the Player and automatically check if the Player can level up."""

        self.experience += points
        Tools.text(f"You gained ", params=Game.text_effects["System"])
        Tools.text(f"{points} XP\n\n", params=Game.text_effects["XP"])
        self.level_up()

    def achievements_contains(self, achievement : Achievement) -> bool:
        """Checks if the player already has the given achievement by name."""
        return any(achv.name == achievement.name for achv in self.achievements or [])

    def add_achievements(self, achievements : List[Achievement]): 
        """Grants achievements to the player, skipping duplicates."""
        if self.achievements is None:
            self.achievements = []

        for achv in achievements:
            if not self.achievements_contains(achv):
                self.achievements.append(achv)
                print(f"You earned Achievement: {achv.name}!")
                print(f"{achv}")
                self.add_experience(achv.experience_reward)
            else:
                #print(f"[Info] Achievement '{achv.name}' already earned. Skipping.")
                continue

    def add_mons(self, mons : List[Mon]):
        """Adds Mons to the Player, allowing a chance to name them, then sorts Player's list of Mons."""

        self.mons.extend(mons)
        self.mons.sort(key=lambda mon: (
            mon.type[0].subclass.lower() if mon.type and mon.type[0].subclass
            else mon.type[0].parent_class.lower() if mon.type
            else ""
        ))

    def log_encounter(self, player_won : bool, player_mon : Mon, opponent_mon : Mon): 
        """Adds an encounter to the Player's Encounter Log."""

        if player_mon is None or opponent_mon is None:
            # encounter cannot be recorded
            return

        win_loss_str = "Win" if player_won else "Loss"

        # Format: "<rarity> - <name>" (left-aligned, max 20 chars)
        player_id = f"{player_mon.rarity} - {player_mon.name}"
        opponent_id = f"{opponent_mon.rarity} - {opponent_mon.name}"

        # Format: "Lvl#, ### HP, ## DEF" (fixed layout)
        player_stats = f"Lvl{player_mon.level:<2}, {player_mon.max_health:>3} HP, {player_mon.defense:>2} DEF"
        opponent_stats = f"Lvl{opponent_mon.level:<2}, {opponent_mon.max_health:>3} HP, {opponent_mon.defense:>2} DEF"

        # Build aligned log entry
        log_entry = (
            f"{win_loss_str:<4} | "
            f"{player_id:<20} : {player_stats}  VS  "
            f"{opponent_id:<20} : {opponent_stats}"
        )

        self.encounter_log.append(log_entry)

        self.encounter_log = self.encounter_log[-50:] # limit log size if needed

    def remove_mons(self, mons : List[Mon]): 
        """A method to remove the input Mons from the Player's Mon list."""

        for mon in mons:
            if mon in self.mons:
                self.mons.remove(mon)

    def sort_mons_by_type(self):
        """Sorts Mons by subclass if it exists, otherwise by parent_class."""

        self.mons.sort(key=lambda mon: (
            mon.type[0].subclass.lower() if mon.type and mon.type[0].subclass
            else mon.type[0].parent_class.lower() if mon.type
            else ""
        ))

    def add_mon_pack(self):
        """Increments the Player's number of Mon Packs."""

        Tools.text(f"You earned a ", params=Game.text_effects["System"])
        Tools.text(f"M", params=Game.text_effects["Red"])
        Tools.text(f"o", params=Game.text_effects["Orange"])
        Tools.text(f"n ", params=Game.text_effects["Yellow"])
        Tools.text(f"P", params=Game.text_effects["Green"])
        Tools.text(f"a", params=Game.text_effects["Blue"])
        Tools.text(f"c", params=Game.text_effects["Purple"])
        Tools.text(f"k\n\n", params=Game.text_effects["Pink"])

        self.mon_packs += 1

    def add_health_potion(self, amount: Optional[int] = 1):
        """Gives the Player 'amount' number of Health Potions."""
        
        self.health_potions += amount

    def add_learn_random_move(self, amount: Optional[int] = 1):
        """Gives the Player 'amount' number of Learn Random Moves."""
        
        self.learn_random_moves += amount

    def add_learn_specific_move(self, amount: Optional[int] = 1):
        """Gives the Player 'amount' number of Learn Specific Moves."""
        
        self.learn_specific_moves += amount

    def increment_checkpoint(self, method_number : int): 
        """Increments the Player's checkpoint number if it is still needed."""

        if self.checkpoint_needed == method_number:
            self.checkpoint_needed += 1

    def encounter_rewards(self, mon : Mon, rarity: str):
        """Gives the player item rewards after an encounter based on Mon rarity scaling."""

        max_rolls = Mon.rarities[rarity]

        # Track reward tallies
        learn_random_count = 0
        learn_specific_count = 0
        potion_count = 0

        for _ in range(max_rolls):
            if random.random() < 0.05:  # 5%
                learn_random_count += 1
            if random.random() < 0.01:  # 1%
                learn_specific_count += 1
            if random.random() < 0.10:  # 10%
                potion_count += 1

        # Award all rewards at once, with flavor text
        if learn_random_count:
            self.add_learn_random_move(learn_random_count)
            Tools.text(f"{mon.name} ", params=Mon.rarity_effects[rarity])
            Tools.text(f"found {learn_random_count} ", params=Game.text_effects["Miniaturizer"])
            Tools.text(f"Learn Random Move", params=Game.text_effects["Orange"])
            Tools.text(f" item(s) for you!\n\n", params=Game.text_effects["Miniaturizer"])

        if learn_specific_count:
            self.add_learn_specific_move(learn_specific_count)
            Tools.text(f"{mon.name} ", params=Mon.rarity_effects[rarity])
            Tools.text(f"found {learn_specific_count} ", params=Game.text_effects["Miniaturizer"])
            Tools.text(f"Learn Specific Move", params=Game.text_effects["Purple"])
            Tools.text(f" item(s) for you!\n\n", params=Game.text_effects["Miniaturizer"])

        if potion_count:
            self.add_health_potion(potion_count)
            Tools.text(f"{mon.name} ", params=Mon.rarity_effects[rarity])
            Tools.text(f"found {potion_count} ", params=Game.text_effects["Miniaturizer"])
            Tools.text(f"Health Potion", params=Game.text_effects["Red"])
            Tools.text(f" item(s) for you!\n\n", params=Game.text_effects["Miniaturizer"])

    def tame_mons(self, mons : List[Mon], skip_tame : Optional[bool] = False, skip_name : Optional[bool] = False):
        """Handles taming one or more Mons, naming them if allowed, and awarding experience."""

        kept_mons = []

        for mon in mons:
            keep = self.use_health_potion(mon, skip_tame=skip_tame)
            if not keep:
                continue

            print(f"You tamed {mon.name}!")

            if not skip_name:
                name = input(f"Give your Mon '{mon.name}' a name (or press Enter to keep the default): ").strip()
                if name:
                    mon.name = name

            kept_mons.append(mon)
            self.add_experience(100 * Mon.rarities[mon.rarity])  # 100 XP per mon tamed

        if kept_mons:
            self.add_mons(kept_mons)

    def use_health_potion(self, dead_mon : Optional[Mon] = None, skip_tame : Optional[bool] = False):
        """Allows the Player to restore one of their Mons to max health, if they have any Health Potions. Returns True upon success."""

        if self.health_potions <= 0:
            Tools.text(f"You have no more Health Potions!\n\n", params=Game.text_effects["Miniaturizer"])
            return False

        if dead_mon:
            while self.health_potions > 0:
                Tools.text(f"You have {self.health_potions} Health Potions. Would you like to revive {dead_mon.name}?\n", params=Game.text_effects["Miniaturizer"])
                Tools.text(f"(", params=Game.text_effects["Miniaturizer"])
                Tools.text(f"(WARNING: ", 0, False, True, [255, 0, 0])
                Tools.text(f"This will be your only chance to tame ", params=Game.text_effects["Miniaturizer"])
                Tools.text(f"{dead_mon.name}", params=Mon.rarity_effects[dead_mon.rarity])
                Tools.text(f".)\n", params=Game.text_effects["Miniaturizer"])
                Tools.text(f"1 : Yes\n", params=Game.text_effects["Miniaturizer"])
                Tools.text(f"0 : No\n\n", params=Game.text_effects["Miniaturizer"])

                if skip_tame: 
                    inp = 0
                else:
                    inp = int(input())

                if inp == 1:
                    rarity_int = Mon.rarities[dead_mon.rarity]
                    level = dead_mon.level
                    tame_chance = Game.tame_chance(rarity_int, level)  # Returns float between 0 and 1

                    roll = random.random()
                    print(roll, tame_chance)
                    if roll <= tame_chance:
                        Tools.text(f"You revived and successfully tamed {dead_mon.name}!\n", params=Mon.rarity_effects[dead_mon.rarity])
                        dead_mon.restore_health_via_potion()
                        self.health_potions -= 1
                        self.add_achievements([Achievement("Necromancer", "Bring a Mon back from the dead.", 1000)])
                        return True
                    else:
                        Tools.text(f"{dead_mon.name} resisted the taming attempt!\n", params=Mon.rarity_effects[dead_mon.rarity])
                        self.health_potions -= 1
                        if self.health_potions == 0:
                            Tools.text(f"You’ve run out of Health Potions. {dead_mon.name} fades away...\n", params=Game.text_effects["Miniaturizer"])
                            break
                elif inp == 0:
                    Tools.text(f"You chose to walk away from {dead_mon.name}...\n\n", params=Game.text_effects["Miniaturizer"])
                    break
                else:
                    Tools.text(f"Invalid input. Try again.\n", params=Game.text_effects["Miniaturizer"])
            return False

        else:
            mon_pool = Miniaturizer.mon_list(self, filter_is_dead=True, filter_is_hurt=True)

            if not mon_pool: 
                Tools.text("None of your Mons are dead or injured.\n\n", params=Game.text_effects["Miniaturizer"])
                return False

            Tools.text("Select an above Mon to restore to max health.\n", params=Game.text_effects["Miniaturizer"])

            try:
                inp = int(input()) # "Enter the number of the Mon you wish to restore: "
                if 1 <= inp <= len(mon_pool):
                    selected_mon = mon_pool[inp - 1]
                    selected_mon.restore_health_via_potion()
                    Tools.text(f"{selected_mon.name} ", params=Mon.rarity_effects[selected_mon.rarity])
                    Tools.text(f"has been restored to max health!\n\n", params=Game.text_effects["Miniaturizer"])
                    if selected_mon.health <= 0:
                        self.add_achievements([Achievement("Necromancer", "Bring a Mon back from the dead.", 1000)])
                else:
                    Tools.text("Invalid selection. Please enter a valid number.", params=Game.text_effects["Miniaturizer"])
                    return False
            except (ValueError, IndexError):
                Tools.text("Invalid input. Please enter a number.", params=Game.text_effects["Miniaturizer"])
                return False

        self.health_potions -= 1
        self.add_experience(50) # player earns 50 XP per health potion used
        self.add_achievements([Achievement("Sorcerer", "Use your first health potion.", 500)])

        return True
    
    def use_learn_random_move(self):
        """Allows the Player to teach a random move to one of their Mons."""

        if self.learn_random_moves <= 0:
            Tools.text("You have no Learn Random Moves left!\n", params=Game.text_effects["Miniaturizer"])
            return

        if not self.mons:
            Tools.text("You have no Mons to teach a move to!\n", params=Game.text_effects["Miniaturizer"])
            return

        Tools.text(f"You have {self.learn_random_moves} Learn Random Moves.\n", params=Game.text_effects["Miniaturizer"])
        Tools.text("Which Mon would you like to teach a random move to?\n", params=Game.text_effects["Miniaturizer"])
        
        Miniaturizer.mon_list(self)

        while True:
            Tools.text("Which Mon would you like to teach a random move to? (-1 to cancel)\n", params=Game.text_effects["Miniaturizer"])
            Miniaturizer.mon_list(self)

            try:
                choice = int(input("\nEnter the number of the Mon: "))

                if choice == -1:
                    Tools.text("You decided not to use a Learn Random Moves.\n", params=Game.text_effects["Miniaturizer"])
                    return

                if 0 <= choice < len(self.mons) + 1:
                    selected_mon = self.mons[choice - 1]
                    Tools.text(f"Are you sure you want to use a Learn Random Moves on {selected_mon.name}? (1 = Yes, 0 = No)\n", params=Game.text_effects["Miniaturizer"])
                    confirm = input().strip()

                    if confirm == "1":
                        if len(selected_mon.moves) < selected_mon.moves_limit:
                            Tools.text(f"{selected_mon.name} has space for more moves.\n", params=Game.text_effects["Miniaturizer"])
                            selected_mon.learn_move()
                            self.learn_random_moves -= 1
                            return
                        else:
                            Tools.text(f"{selected_mon.name}'s current moves:\n", params=Game.text_effects["Miniaturizer"])
                            for i, move in enumerate(selected_mon.moves):
                                Tools.text(f"{i + 1} : {move}\n", params=Game.text_effects["Miniaturizer"])

                            while True:
                                Tools.text("Select the number of the move you'd like to replace (-1 to cancel):\n", params=Game.text_effects["Miniaturizer"])
                                try:
                                    move_choice = int(input())

                                    if move_choice == -1:
                                        Tools.text("Cancelled. Returning to Mon selection...\n", params=Game.text_effects["Miniaturizer"])
                                        break

                                    if 0 <= move_choice < len(selected_mon.moves) + 1:
                                        replace_me = selected_mon.moves[move_choice - 1]
                                        selected_mon.replace_move(replace_me)
                                        self.learn_random_moves -= 1
                                        return
                                    else:
                                        Tools.text("Invalid choice. Please select a valid move number.\n", params=Game.text_effects["Miniaturizer"])
                                except ValueError:
                                    Tools.text("Invalid input. Please enter a number.\n", params=Game.text_effects["Miniaturizer"])

                    elif confirm == "0":
                        Tools.text("Cancelled. Returning to Mon selection...\n", params=Game.text_effects["Miniaturizer"])
                    else:
                        Tools.text("Invalid confirmation input. Returning to Mon selection...\n", params=Game.text_effects["Miniaturizer"])
                else:
                    Tools.text("Invalid choice. Please select a valid Mon number.\n", params=Game.text_effects["Miniaturizer"])

            except ValueError:
                Tools.text("Invalid input. Please enter a number.\n", params=Game.text_effects["Miniaturizer"])

    def use_learn_specific_move(self):
        """"""

    def use_mon_pack(self):
        """Allows the Player to use a Mon Pack, if they have any."""

        if self.mon_packs <= 0:
            Tools.text(f"You have no more Mon Packs!\n\n", params=Game.text_effects["Miniaturizer"])
            return

        self.tame_mons(Game.mon_pack())
        self.mon_packs -= 1

    @staticmethod
    def parse(filename: str):
        path = os.path.join(os.path.dirname(__file__), "Game", "data", "gamesaves", filename)
        with open(path, "r") as f:
            data = json.load(f)  

        return Player(
            name=data.get("name"),
            health=data.get("health"),
            level=data.get("level"),
            experience=data.get("experience"),
            experience_needed=data.get("experience_needed"),
            checkpoint_needed=data.get("checkpoint_needed"),
            mons=[Mon.parse(mon_name, mon_data) for mon_dict in data["mons"] for mon_name, mon_data in mon_dict.items()],
            mon_packs=data.get("mon_packs", 0),
            health_potions=data.get("health_potions", 0),
            learn_random_moves=data.get("learn_random_moves", 0),
            learn_specific_moves=data.get("learn_specific_moves", 0),
            weapon=data.get("weapon"),
            achievements=[Achievement.parse(achv_data["name"], achv_data) for achv_data in data["achievements"]],
            encounter_log=data.get("encounter_log", []),
            gamesave=filename # Don't forget the name!
        )

    def export_to_json(self, filename=None, filepath : str = None):
        base_dir = os.path.dirname(__file__)
        if filepath is None:
            save_path = os.path.join(base_dir, "Game", "data", "gamesaves")

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}_{self.name}.json"

        full_path = os.path.join(save_path, filename)

        with open(full_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

        print(f"Player saved to {full_path}")

        self.gamesave = filename

        return self

class Game: 
    """A class to implement Game mechanics."""

    checkpoints = {
        0 : "_0000", 
        1 : "_0001", 
        2 : "_0002", 
        3 : "_0003"
    }

    text_effects = {
        "Miniaturizer" : [0, True, False, [120, 190, 255]], 
        "Player Actions" : [0, False, False, [150, 150, 150]],
        "Player Internal" : [0.05, True, False, [255, 255, 255]], 
        "NPC External" : [0.05, False, True, [200, 200, 200]],
        "Narrator" : [0.05, False, False, [255, 255, 255]], 
        "System" : [0, False, True, [255, 255, 255]],
        "XP" : [0, False, True, [125, 255, 0]], 
        "Red" : [0, False, True, [255, 0, 0]], 
        "Orange" : [0, False, True, [255, 120, 0]], 
        "Yellow" : [0, False, True, [255, 190, 0]], 
        "Green" : [0, False, True, [0, 255, 70]], 
        "Blue" : [0, False, True, [0, 70, 255]], 
        "Purple" : [0, False, True, [70, 0, 255]], 
        "Pink" : [0, False, True, [190, 0, 255]]
    }

    rarity_order = ["Omega", "Ultra", "Legendary", "Epic", "Rare", "Uncommon", "Common"]

    rarity_counts = {
        "Omega": (1, 0.01),
        "Ultra": (3, 0.03),
        "Legendary": (4, 0.1),
        "Epic": (6, 0.12),
        "Rare": (10, 0.50),
        "Uncommon": (13, 0.66),
        # "common" handled by remainder
    }

    def __init__(self):
        self.player = Player()
    
    @staticmethod
    def start():
        """A method to start the Game."""

        inp = int(input(
            f"Welcome to the Game!\n"
            f"\t(Hint: make choices by entering numbers corresponding to your selected choice.)\n"
            f"\tStart Story Mode?\n"
            f"\t1\t:\tYes\n"
            f"\t2\t:\tNo\n"
        ))

        if inp == 1:
            Game.story()
            return
        elif inp == 2:
            return
        elif inp == 0:
            return
        
    @staticmethod
    def story():
        """A method to start the Story."""

        # check for existing gamesaves
        base_dir = os.path.dirname(__file__)
        gamesaves_path = os.path.join(base_dir, "Game", "data", "gamesaves")

        if not os.path.exists(gamesaves_path):
            print("No gamesave directory found.")
            return
        
        save_files = [f for f in os.listdir(gamesaves_path) if os.path.isfile(os.path.join(gamesaves_path, f))]

        if save_files:
            print("Gamesaves found:")
            for i, fname in enumerate(save_files):
                print(f"\t{i+1}. {fname}")

        else:
            inp = int(input(
                f"No gamesaves found.\n"
                f"Create new gamesave?\n"
                f"\t1\t:\tYes\n"
                f"\t2\t:\tNo\n"
            ))

            if inp == 1: 
                inp = input("Please choose a name for your Player.\n")
                player = Player(inp)
                player.checkpoint_needed = 1
                Game._0001(player.export_to_json())

        return
    
    @staticmethod
    def load_checkpoint(player : Player, checkpoint_num : int):
        method_name = Game.checkpoints.get(checkpoint_num)
        if method_name:
            method = getattr(Game, method_name, None)
            if callable(method):
                method(player)
            else:
                print(f"Checkpoint method '{method_name}' is not defined.")
        else:
            print(f"Checkpoint #{checkpoint_num} not found.")
    
    @staticmethod
    def _0001(player : Player, timing : float = 0.5):
        method_number = 1

        Tools.text("\n" * 20, 0.05)
        Tools.text(f"Welcome to the game, {player.name}...\n", params=Game.text_effects["Narrator"])
        Tools.text(f"There is much for you to learn...", params=Game.text_effects["Narrator"])
        time.sleep(1)
        Tools.text(f"but there's no time for that right now.\n\n", params=Game.text_effects["Narrator"])
        time.sleep(1)
        Tools.text(f"Here, take this.\n\n", params=Game.text_effects["Narrator"])
        time.sleep(1)
        Tools.text(f"[You obtained one (1) Miniaturizer 9000]\n\n", params=Game.text_effects["System"])
        time.sleep(1)
        Tools.text(f"Good luck, {player.name}...", params=Game.text_effects["Narrator"])
        time.sleep(2)
        Tools.text(f"you're gonna need it...\n", params=Game.text_effects["Narrator"])

        player.increment_checkpoint(method_number)

        return Game._0002(player.export_to_json(player.gamesave))
    
    @staticmethod
    def _0002(player : Player, timing : float = 0.5):
        method_number = 2

        Tools.text("\n" * 20, 0.05)
        time.sleep(timing * 6)
        Tools.text(f"Huh?\n", 0.05, True)
        time.sleep(timing * 6)
        Tools.text(f"Where am I?\n\n", 0.05, True)
        time.sleep(1)
        Tools.text(f"You awake beneath a tree in a field of tall grass.\n\n", 0, False, False, [150, 150, 150])
        time.sleep(timing * 6)
        Tools.text(f"What's this?\n\n", 0.05, True)
        time.sleep(timing * 2)
        Tools.text(f"You notice a small metallic device wrapped around your wrist, resembling a watch.\n\n", 0, False, False, [150, 150, 150])
        time.sleep(timing * 2)
        Tools.text(f"The device hums resonantly with power", 0, False, False, [150, 150, 150])
        time.sleep(timing * 3)
        Tools.text(f"...", 0.05, False, False, [150, 150, 150])
        time.sleep(timing * 3)
        Tools.text(f"then begins beeping rhythmically.\n\n", 0.05, False, False, [150, 150, 150])
        time.sleep(timing * 3)

        mon = Mon()
        Tools.text(f"A {mon.name} appears!\n\n", 0, True, True)
        Tools.text(f"The {mon.name} jumps toward you!\n\n", 0, True, True)
        time.sleep(0.5)
        Tools.text(f"Beams of scattered, colorful light shoot out from the device onto the Mon, and it disappears", 0.05, True, False, [150, 150, 150])
        Tools.text(f"...\n\n", 0.1, True, False, [150, 150, 150])
        time.sleep(1.5)

        player.tame_mons([mon])

        Tools.text(f"The device beeps twice shortly.\n\n", 0.05, False, False, [150, 150, 150])
        
        print(mon)

        player.add_achievements([Achievement("Tamer", "Tame your first Mon.", 1000)])
        
        player.increment_checkpoint(method_number)

        return Game._0003(player.export_to_json(player.gamesave))
    
    @staticmethod
    def _0003(player : Player, timing : float = 0.5, typewriter : float = 0.05):
        method_number = 3

        typewriter = 0.001
        timing = 0.01

        if typewriter != 0.05:
            for txt_efct in Game.text_effects.values():
                if txt_efct[0] == 0:
                    continue # skip effects without typewriter effect
                else:
                    txt_efct[0] = typewriter

        Tools.text("\n" * 20, params=Game.text_effects["System"])
        time.sleep(timing * 6)
        time.sleep(timing * 2)
        Tools.text(f"What *was* that?\n\n", params=Game.text_effects["Player Internal"])
        time.sleep(timing * 2)
        Tools.text(f"You look at the device on your wrist. 'Miniaturizer 9000' is printed on its side.\n\n", params=Game.text_effects["Player Actions"])
        time.sleep(timing * 2)
        Tools.text(f"What *is* this?\n\n", params=Game.text_effects["Player Internal"])
        time.sleep(timing * 2)
        Tools.text(f"You lift your arm closer to get a better look, and beam of blue light shoots out of the Miniaturizer.\n", params=Game.text_effects["Player Actions"])
        Tools.text(f"You see a hologram display a panel with the text: \n\n", params=Game.text_effects["Player Actions"])
        time.sleep(timing * 3)
        Miniaturizer.home_screen(player)
        time.sleep(timing * 4)
        Tools.text(f"...", params=Game.text_effects["Player Internal"])
        time.sleep(timing)
        Tools.text(f"Oh\n\n", params=Game.text_effects["Player Internal"])
        time.sleep(timing * 4)
        Tools.text("HEY!\n\n", params=Game.text_effects["NPC External"])
        time.sleep(timing * 2)
        Tools.text("...?\n\n", params=Game.text_effects["Player Internal"])
        time.sleep(timing * 2)
        Tools.text("HEY, YOU!\n\n", params=Game.text_effects["NPC External"])
        time.sleep(timing * 3)
        Tools.text("You turn around to look and notice an old man calling out to you from a small village nearby.\n\n", params=Game.text_effects["Player Actions"])
        time.sleep(timing * 4)
        Tools.text("WELL, COME ON UP HERE!\n\n", params=Game.text_effects["NPC External"])
        time.sleep(timing * 3)
        Tools.text("Hesitantly, you stand yourself up and walk through the field to the old man.\n\n", params=Game.text_effects["Player Actions"])

        #Game.mon_encounter(player)
        #Miniaturizer.home_screen(player)

        # player.increment_checkpoint(method_number)

        return Game._0004(player.export_to_json(player.gamesave))
    
    @staticmethod
    def _0004(player : Player):
        method_number = 4

        #Tools.text("\n" * 20, 0.05)
        #time.sleep(1)
        #Tools.text(f"What was that?\n", 0.05, True)
    
        # player.increment_checkpoint(method_number)

        #return Game._0004(player.export_to_json(player.gamesave))
    
    """ default checkpoint method stub: 

    @staticmethod
    def _#### (player : Player):
        method_number = ####

        Tools.text("\n" * 20, 0.05)
        time.sleep(3)
    
        # player.increment_checkpoint(method_number)

        return #Game._####(player.export_to_json(player.gamesave))
    """
    @staticmethod
    def tame_chance(rarity, level, base=0.9999, rarity_decay=1.8, level_decay=0.009):
        """
        Returns a taming probability between 0 and 1.

        :param rarity: int (1 = Common, ..., 7 = Omega)
        :param level: int (1 to 100)
        :param base: base probability multiplier (e.g. 0.95 for high base chance)
        :param rarity_decay: how much harder each rarity step is (exponential factor)
        :param level_decay: per-level penalty (linear or exponential)
        """
        rarity_penalty = rarity_decay ** (rarity - 1)
        level_penalty = 1 - (level_decay * (level - 1))
        level_penalty = max(level_penalty, 0.01)  # avoid zero or negative chances

        chance = base / rarity_penalty * level_penalty
        return max(min(chance, 1.0), 0.0001)  # clamp between 0.0001 and 1.0

    @staticmethod
    def mon_encounter(player : Player, 
                      biome : Optional[str] = None,
                      player_use_mon : Optional[Mon] = None, 
                      skip_tame : Optional[bool] = False, 
                      skip_battle : Optional[bool] = False,
                      rarity : Optional[str] = None, 
                      name : Optional[str] = None, 
                      type : Optional[List["Type"]] = None):
        """Simulates a wild encounter with an optionally random Mon or may specify attributes, then must battle to capture"""

        if biome is not None and biome in Type.type_biomes: 
            type = Type.assign_types_weighted(Type.type_biomes[biome]) 

        mon = Mon(
            name=name,
            rarity=rarity,
            tp=type
        )

        mon.rarity_boost(mon.rarity)

        if Mon.rarities[mon.rarity] >= 5: 
            skip_tame = False
            player_use_mon = None

        Tools.text(f"A ", 0, True, True)
        Tools.text(f"{mon.name} ", params=Mon.rarity_effects[mon.rarity])
        Tools.text(f"appears!\n\n", 0, True, True)
        player_won = False
        p_mon = None

        Tools.text(f"Choose your Mon!\n\n", params=Game.text_effects["Miniaturizer"])
        mon_pool = Miniaturizer.mon_list(player, filter_is_alive=True)
        if mon_pool: 
            if len(mon_pool) > 1 and not player_use_mon:
                inp = int(input())
                p_mon = mon_pool[inp - 1]
            elif len(mon_pool) > 1 and player_use_mon:
                p_mon = player_use_mon
                if p_mon.health <= 0:
                    p_mon.health = p_mon.max_health
            else: 
                p_mon = mon_pool[0]

            if skip_battle:
                player_won, mon_leveled_up = p_mon.battle(mon, attacker_use_move=p_mon.moves[0], typewriter_delay=0, timing=0) # ret
            else:
                player_won, mon_leveled_up = p_mon.battle(mon, is_random=False, typewriter_delay=0, timing=0) # ret
            #print(player_won, mon_leveled_up)
            if mon_leveled_up:
                player.encounter_rewards(p_mon, mon.rarity)
        else:
            Tools.text(f"You have no Mons to battle with...\n\n", params=Game.text_effects["Miniaturizer"])

        if player_won: # player may keep mon if won
            if random.random() < 0.5: 
                player.add_health_potion()
                Tools.text(f"You found a ", params=Game.text_effects["Miniaturizer"])
                Tools.text(f"Health Potion", params=Game.text_effects["Red"])
                Tools.text(f"!\n\n", params=Game.text_effects["Miniaturizer"])
            if player.health_potions > 0: # player may keep mon if they can revive it
                player.tame_mons([mon])
            else:
                Tools.text(f"You have no health potions! You cannot revive ", params=Game.text_effects["Miniaturizer"])
                Tools.text(f"{mon.name} ", params=Mon.rarity_effects[mon.rarity])
                Tools.text(f"for taming...\n\n", params=Game.text_effects["Miniaturizer"])
        else:
            Tools.text(f"{mon.name} got away!\n\n", params=Game.text_effects["Miniaturizer"])

        rarity_multiplier = Mon.rarities[mon.rarity] # rarity XP multipler based on opponent rarity
        player_xp = 250 if not player_won else 500 # 250 XP for the losing, 500 XP for winning the encounter
        player.add_experience(player_xp * rarity_multiplier) 
        
        player.log_encounter(player_won, p_mon, mon)
        
        return player_won # mon # ret

    @staticmethod
    def versus(p1 : Player, p2 : Player, mon_num : int = 3): 
        """A method to simulate a Mon Versus Battle between two Players, each with the specified number of Mons."""

        p1_mons = p1.mons[:mon_num]
        p2_mons = p2.mons[:mon_num]

        player = Player(mons=p1_mons)

        while True: 
            if len(p1_mons) <= 0:
                Tools.text(f"All your Mons died!\n\n")
                break

            if len(p2_mons) <= 0:
                Tools.text(f"You defeated {p2.name}!\n\n")
                break
            
            player_won = False
            p_mon = None

            mon = p2_mons[0]

            Miniaturizer.mon_list(p2, filter_is_alive=True)
            Tools.text(f"Choose your Mon!\n\n", params=Game.text_effects["Miniaturizer"])
            mon_pool = Miniaturizer.mon_list(player, filter_is_alive=True)
            if mon_pool: 
                if len(mon_pool) > 1:
                    inp = int(input())
                    p_mon = mon_pool[inp - 1]
                else: 
                    p_mon = mon_pool[0]

                player_won, mon_leveled_up = p_mon.battle(mon, is_random=False, typewriter_delay=0, timing=0) # ret
                #player_won, mon_leveled_up = p_mon.battle(mon, attacker_use_move=p_mon.moves[0], typewriter_delay=0, timing=0) # ret
                #print(player_won, mon_leveled_up)
                if mon_leveled_up:
                    player.encounter_rewards(p_mon, mon.rarity)
            else:
                Tools.text(f"You have no Mons to battle with...\n\n", params=Game.text_effects["Miniaturizer"])
                break

            if player_won: # player won battle, opponent mon removed
                p2_mons.remove(mon)
                Tools.text(f"{mon.name} ", params=Mon.rarity_effects[mon.rarity])
                Tools.text(f"is out of the battle...\n\n", params=Game.text_effects["Miniaturizer"])
            else: # player lost battle, player mon removed
                Tools.text(f"[DEBUG] {p_mon.name}\n\n", params=Game.text_effects["Red"])
                Tools.text(f"{p_mon.name} ", params=Mon.rarity_effects[p_mon.rarity])
                Tools.text(f"is out of the battle...\n\n", params=Game.text_effects["Miniaturizer"])
                p1_mons.remove(p_mon)

    class pPlayer:
        """Temporary psuedo-Player"""

        def __init__(self, 
                        name : str, balance : int = 20000):
            self.name = name
            self.balance = balance

    class Bet:
        """Represents a bet on a Mon in a dog_fight battle."""
        def __init__(self, player: Union[Player, Game.pPlayer, str], mon_choice: bool, amount: int):
            """
            player: a Player object or a string representing the player's name (for testing)
            mon_choice: True if betting on m1, False if betting on m2
            amount: the wagered amount
            """
            self.player = player
            self.mon_choice = mon_choice
            self.amount = amount

        @property
        def name(self) -> str:
            """Return the player's name (works for Player or string)."""
            return self.player.name if hasattr(self.player, "name") else str(self.player)

        def __repr__(self):
            mon_side = "m1" if self.mon_choice else "m2"
            return f"Bet(player={self.name}, mon={mon_side}, amount={self.amount})"

    @staticmethod
    def dog_fight(m1: 'Mon', m2: 'Mon', bets: List[Bet] = None, odds : Tuple[float, float, float] = None):
        """
        Battle between two Mons, allowing multiple Players to bet on the outcome.
        Each Bet instance in 'bets' indicates which Mon the Player picked and how much they wagered.
        Winning bets share the total pool of losing bets.
        """

        # Precompute battle stats for odds
        if odds == None:
            m1w, m1l, m1d = m1.sim_battle_stats(m2)
        else: 
            m1w, m1l, m1d = odds

        # Conduct the battle
        outcome, _ = m1.battle(m2, typewriter_delay=0, timing=0, use_self_ai=True, use_opp_ai=True)
        winner_mon = m1 if outcome else m2

        if bets is None:
            bets = []

        # Separate winners and losers
        winners = []
        losers = []
        for bet in bets:
            chosen_mon = m1 if bet.mon_choice else m2
            if chosen_mon == winner_mon:
                winners.append(bet)
            else:
                losers.append(bet)

        # Compute total pool from losers
        losing_pool = sum(bet.amount for bet in losers)
        total_winner_bets = sum(bet.amount for bet in winners)
        print(f"\nTotal pool = {losing_pool:,} (Losers) + {total_winner_bets:,} (Winners) = {losing_pool+total_winner_bets:,}")

        # Process winners
        if total_winner_bets > 0 and losing_pool > 0:
            # Compute integer shares
            shares = [(bet.amount * losing_pool) // total_winner_bets for bet in winners]
            remainder = losing_pool - sum(shares)

            # Distribute remainder fairly (1 extra unit to first winners until gone)
            for i in range(remainder):
                shares[i] += 1

            # Print winnings
            for bet, share in zip(winners, shares):
                odds = m1w if bet.mon_choice == 0 else m1l - m1d
                Tools.text(f"DEBUG {m1w, m1l, m1d}\n\n", rgb=[255, 255, 0])
                total_winnings = bet.amount + share
                bet_perc = ""
                if hasattr(bet.player, "balance"):
                    bet_perc = bet.amount / bet.player.balance
                    print(f"{bet.name} won bet: {total_winnings:,}! ({odds:.1%} odds) (Bet: {bet.amount:,} [{bet_perc:.4%}])")
                else: print(f"{bet.name} won bet: {total_winnings:,}! ({odds:.1%} odds) (Bet: {bet.amount:,})")
                if hasattr(bet.player, "balance"):
                    bet.player.balance += total_winnings - bet.amount
        else:
            # No winners or no losing pool, just return original bets
            for bet in winners:
                odds = m1w if bet.mon_choice == 0 else m1l - m1d
                Tools.text(f"DEBUG {m1w, m1l, m1d}\n\n", rgb=[255, 255, 0])
                bet_perc = ""
                if hasattr(bet.player, "balance"):
                    bet_perc = bet.amount / bet.player.balance
                    print(f"{bet.name} won bet: {bet.amount:,}! ({odds:.1%} odds) (Bet: {bet.amount:,} [{bet_perc:.4%}])")
                else: print(f"{bet.name} won bet: {bet.amount:,}! ({odds:.1%} odds) (Bet: {bet.amount:,})")

        # Process losers
        for bet in losers:
            odds = m1w if bet.mon_choice == 0 else m1l - m1d
            Tools.text(f"DEBUG {m1w, m1l, m1d}\n\n", rgb=[255, 255, 0])
            bet_perc = ""
            if hasattr(bet.player, "balance"):
                bet_perc = bet.amount / bet.player.balance
                print(f"{bet.name} lost bet: {bet.amount:,} [{bet_perc:.4%}]... ({odds:.1%} odds)")
            else: print(f"{bet.name} lost bet: {bet.amount:,}... ({odds:.1%} odds)")
            if hasattr(bet.player, "balance"):
                bet.player.balance -= bet.amount

        #return winner_mon

    def legendary_encounter(player : Player, mon_num = 6):
        """Simulates an encounter with a Legendary+ Mon, must battle for capture."""

        burner_mon = Mon()

        leg_mon = Mon(
            rarity=burner_mon.assign_rarity_weighted(minimum_rarity="Omega"), # must use burner for...reasons :/
            level=random.randint(250, 350),  # will be random range of sum of all 6 player mon levels times multipliers for a range of vals
            #tp=Type.assign_types_weighted(weighted_pool=[("Fire", 1)]), 
            tp=[Type("Nature", None)],
            pearl=2
        )
        leg_mon.name = leg_mon.make_name(wild=False)
        leg_mon.assign_moves(leg_mon.type, move_priority=(True, True, True))
        for mv in leg_mon.moves:
            #print(mv.name)
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        Tools.text(f"A ", 0, True, True)
        Mon.pearlize(Mon.pearls[leg_mon.pearl].split()[0], short_hand=True) if leg_mon.pearl else None
        Tools.text(f"{leg_mon.name} ", params=Mon.rarity_effects[leg_mon.rarity])
        Tools.text(f"appears!\n\n", 0, True, True)

        Tools.text(f"[DEBUG] {leg_mon.attack_boost + 1.0:.0%}\n\n", rgb=[255,0,0])

        p_mons = player.mons[:mon_num]

        while True: 
            if len(p_mons) <= 0:
                Tools.text(f"All your Mons died!\n\n")
                break
            
            player_won = False
            p_mon = None

            Tools.text(f"Choose your Mon!\n\n", params=Game.text_effects["Miniaturizer"])
            mon_pool = Miniaturizer.mon_list(player, isolate_mons=p_mons, filter_is_alive=True, attribute_sort=["rarity", "pearl"])
            #mon_pool = Miniaturizer.mon_list(player, isolate_mons=p_mons, filter_is_alive=True)
            if mon_pool: 
                if len(mon_pool) > 1:
                    inp = int(input())
                    p_mon = mon_pool[inp - 1]
                else: 
                    p_mon = mon_pool[0]

                player_won, mon_leveled_up = p_mon.battle(leg_mon, is_random=False, typewriter_delay=0, timing=0) # ret
                #player_won, mon_leveled_up = p_mon.battle(mon, attacker_use_move=p_mon.moves[0], typewriter_delay=0, timing=0) # ret
                #print(player_won, mon_leveled_up)
                if mon_leveled_up:
                    player.encounter_rewards(p_mon, leg_mon.rarity)
            else:
                Tools.text(f"You have no Mons to battle with...\n\n", params=Game.text_effects["Miniaturizer"])
                break

            if player_won is not False: # player won battle (or draw), legendary mon defeated
                Tools.text(f"{leg_mon.name} ", params=Mon.rarity_effects[leg_mon.rarity])
                Tools.text(f"has been defeated!\n\n", params=Game.text_effects["Miniaturizer"])

                catch_mon = Mon(
                    name=leg_mon.name,
                    level=leg_mon.level // 5,
                    pearl=leg_mon.pearl,
                    rarity=leg_mon.rarity, 
                    tp=leg_mon.type,
                    moves=leg_mon.moves,
                )
                catch_mon.health = 0

                if player.health_potions > 0:
                    player.tame_mons([catch_mon])
                else: 
                    Tools.text(f"You have no health potions! You cannot revive ", params=Game.text_effects["Miniaturizer"])
                    Tools.text(f"{catch_mon.name} ", params=Mon.rarity_effects[catch_mon.rarity])
                    Tools.text(f"for taming...\n\n", params=Game.text_effects["Miniaturizer"])
                    return

                return
            else: # player lost battle, player mon removed
                Tools.text(f"[DEBUG] {p_mon.name}\n\n", params=Game.text_effects["Red"])
                Tools.text(f"{p_mon.name} ", params=Mon.rarity_effects[p_mon.rarity])
                Tools.text(f"is out of the battle...\n\n", params=Game.text_effects["Miniaturizer"])
                p_mons.remove(p_mon)

    def overtime(self):
        """A method to loop rounds for overtime for Versus Battles."""
    
    @staticmethod
    def parse_saves() -> List[Player]:
        """Parses all gamesaves and returns a list of Player objects."""
        saves_dir = os.path.join(os.path.dirname(__file__), "data", "gamesaves")
        player_files = [f for f in os.listdir(saves_dir) if f.endswith(".json")]

        players = []

        for file in player_files:
            path = os.path.join(saves_dir, file)
            with open(path, "r") as f:
                data = json.load(f)
                player = Player.from_dict(data)
                players.append(player)

        return players

    def mon_case(case_num: int = 1, 
             mon_num: int = 10, 
             mon_types_weighted: Optional[List[Tuple[str, float]]] = None,
             min_keep_rarity: str = None, 
             case_quality: str = None, 
             god_case_chance: bool = (1 / 4096)
            ):
        """
        A method to open a Mon Case, selecting 20 out of 50 generated Mons. Quality Rating determines 
        rarity bias, increasing the chance of pulling rarer Mons.

        :param mon_types_weighted: A List of Tuples in the form: (Mon Type-string instance or set, weight)
        """

        def calculate_rarity_binomial_stats(rarity_counts, deferred_rolls_per_tier, actual_counts, rarity_order):
            """
            Calculates binomial probabilities of actual counts per rarity, adjusting roll counts for deferred rolls and previous tier actual counts.
            
            Returns dict: rarity -> probability of actual count under binomial model
            """
            results = {}
            rarity_indices = {r: i for i, r in enumerate(rarity_order)}

            for r in rarity_order:
                if r not in rarity_counts:
                    continue

                idx = rarity_indices[r]
                base_rolls, p = rarity_counts[r]
                actual = actual_counts.get(r, 0)

                deferred_from_higher = deferred_rolls_per_tier[rarity_order[idx - 1]] if idx > 0 else 0

                effective_rolls = base_rolls + deferred_from_higher
                effective_rolls = max(effective_rolls, actual)  # Ensure effective rolls ≥ actual count

                if effective_rolls < actual:
                    prob = 0.0
                else:
                    prob = comb(effective_rolls, actual) * (p ** actual) * ((1 - p) ** (effective_rolls - actual))

                results[r] = {
                    "actual_count": actual,
                    "effective_rolls": effective_rolls,
                    "probability": prob,
                    "base_probability": p
                }
            return results

        local_rarity_counts = Game.rarity_counts.copy()
        
        actual_counts = {r: 0 for r in Mon.rarities}
        deferred_rolls_per_tier = {r: 0 for r in Game.rarity_order}

        total = 0
        pool = []

        for i, rarity in enumerate(Game.rarity_order[:-1]):  # Exclude 'Common' for now
            expected_count, chance = local_rarity_counts[rarity]
            count = 0
            for _ in range(expected_count):
                if random.random() < chance:
                    pool.append(Mon(rarity=rarity))
                    actual_counts[rarity] += 1
                    count += 1
                else:
                    deferred_rolls_per_tier[rarity] += 1

            total += count

            # Pass deferred rolls down to next tier
            if i + 1 < len(Game.rarity_order) - 1:
                next_rarity = Game.rarity_order[i + 1]
                base_count, base_prob = local_rarity_counts[next_rarity]
                local_rarity_counts[next_rarity] = (
                    base_count + deferred_rolls_per_tier[rarity],
                    base_prob
                )
                deferred_rolls_per_tier[rarity] = 0

        # Fill remaining with commons
        remaining = 50 - len(pool)
        for _ in range(remaining):
            pool.append(Mon(rarity="Common"))
            actual_counts["Common"] += 1

        assert len(pool) == 50, f"Expected 50 mons, got {len(pool)}"

        ### torture :) ###
        print("Pool:")
        for m in pool:
            print(m.name_str())
        print("-" * 40, "\n")
        ### ---------- ###
        
        # Select 20 random mons equally weighted
        final_selection = random.sample(pool, 20)

        # Print actual counts
        print("Actual rarity counts in pool:")
        for rarity, count in actual_counts.items():
            if rarity == "Any":
                continue
            print(f"{count:>2} - {Mon.rarity_colors(rarity)}")

        # Calculate and print stats
        stats_results = calculate_rarity_binomial_stats(
            rarity_counts=local_rarity_counts,
            deferred_rolls_per_tier=deferred_rolls_per_tier,
            actual_counts=actual_counts,
            rarity_order=Game.rarity_order
        )

        print("\nRarity probabilities based on actual counts and rolls:")
        for rarity, data in stats_results.items():
            print(f"{Mon.rarity_colors(rarity):<10} | Count: {data['actual_count']:>2} | "
                f"Effective Rolls: {data['effective_rolls']:>2} | "
                f"Prob: {data['probability']:.4f} (Base p={data['base_probability']})")

        return final_selection
        
    @staticmethod
    def mon_pack(pack_num : int = 1, 
                 mon_num : int = 10, 
                 mon_types_weighted : Optional[List[Tuple[str, float]]] = None,
                 min_keep_rarity : str = None, 
                 pack_quality : str = None, 
                 god_pack_chance : bool = (1 / 4096)
                 ): # params - plr : Player
        """
        A method to open a Mon Pack of 10 Mons. Quality Rating determines 
        rarity bias, increasing the chance of pulling rarer Mons.

        :param mon_types_weighted: A List of Tuples in the form: (Mon Type-string instance or set, weight)
        """

        if mon_types_weighted is None:
            mon_types_weighted = [(t, 1.0) for t in Type.types]  # even weights by default
        total_weight = sum(weight for _, weight in mon_types_weighted)
        if total_weight <= 0 or any(weight < 0 for _, weight in mon_types_weighted):
            raise ValueError("All weights must be non-negative, and total must be > 0.")

        if min_keep_rarity is not None and min_keep_rarity not in Mon.rarities:
            raise ValueError(f"[ERROR] Invalid value for 'min_keep_rarity': {min_keep_rarity}.")


        pack_qualities = {
            "Normal" : None, 
            "Enhanced" : [
                ("Common", 0.5), # 50%
                ("Uncommon", 0.25), # 25%
                ("Rare", 0.15), # 15%
                ("Epic", 0.06), # 6%
                ("Legendary", 0.0345), # 3.45%
                ("Ultra", 0.005), # 0.5%
                ("Omega", 0.0005) # 0.05%
            ], 
            "Amplified" : [
                ("Common", 0.30), # 30%
                ("Uncommon", 0.23), # 23%
                ("Rare", 0.20), # 20%
                ("Epic", 0.13), # 13%
                ("Legendary", 0.085), # 8.5%
                ("Ultra", 0.035), # 3.5%
                ("Omega", 0.02) # 2%
            ]
        }

        if pack_quality not in pack_qualities:
            if pack_quality is None:
                pack_quality = "Normal"
            else:
                print("Invalid Quality Rating.")
                return
            
        rarity_weights = pack_qualities[pack_quality]

        if rarity_weights is not None:
            rarities, r_weights = zip(*rarity_weights)
            total_weight = sum(r_weights)
            if total_weight < 0 or any(w < 0 for w in r_weights):
                raise ValueError("Invalid weights: all weights must be non-negative and total must be > 0.")
        
        pearl_weights = {
            # pearl_val : weight
            1           : (4 / 5), 
            2           : (1 / 5)
        }

        # Sorted in increasing order of Rarity
        pulled = []

        pearl_values, pearl_weights_list = zip(*pearl_weights.items())
        god_pack_num = 0

        burner = Mon()
        for _ in range(pack_num): # packs loop
            god_pack = random.random() < god_pack_chance
            god_pack_num += 1 if god_pack else 0
            leg_num = random.randint(mon_num // 2, mon_num) if god_pack else 0
            pearl_num = random.randint(mon_num // 4, mon_num // 2) if god_pack else 0
            #print(leg_num, pearl_num)

            for _ in range(mon_num): # mons loop
                pull_rar = burner.assign_rarity_weighted(custom_weights=rarity_weights)
                move_priority = (False, False, False)
                if leg_num > 0:
                    leg_rar = random.choice(("Legendary", "Ultra", "Omega"))
                    pull_rar = burner.assign_rarity_weighted(minimum_rarity=leg_rar)
                    leg_num -= 1
                    move_priority = (True, True, True)
                pull_pearl = None
                if pearl_num > 0:
                    pull_pearl = random.choices(pearl_values, weights=pearl_weights_list, k=1)[0]
                    pearl_num -= 1

                mon = Mon(
                    tp=Type.assign_types_weighted(mon_types_weighted),
                    level=1,
                    rarity=pull_rar, 
                    pearl=pull_pearl
                )
                mon.name = mon.make_name(wild=False)
                mon.assign_moves(mon.type, move_priority=move_priority)
                if min_keep_rarity is not None and Mon.rarities[mon.rarity] >= Mon.rarities[min_keep_rarity]:
                    pulled.append(mon)
                elif min_keep_rarity is None: 
                    pulled.append(mon)
        
        # Sort pulled
        pulled.sort(
            key=lambda m: (
                Mon.rarities[m.rarity], # primary: rarity (low to high)
                ord(str(m.type)[0].upper()) if m.type and m.type else 0 # secondary: type name (A to Z)
            )
        )

        if pulled:
            # Print pulled Mons
            print("Pulled Mons (Sorted):")
            for i, mon in enumerate(pulled):
                Tools.text(f"{i + 1} : ")
                Tools.text(f"{mon.name_str()}\n")
            
            # selection for kept cards, then return
            while True:
                kept = []
                if god_pack_num == 1:
                    print(f"You pulled a God Pack!")
                elif god_pack_num > 1:
                    print(f"You pulled {god_pack_num} God Packs!")
                print("Choose all Mons you would like to keep (enter numbers one at a time). Type 0 when done:")


                while True:
                    try:
                        inp = int(input("> "))
                        if inp == 0:
                            break
                        if 1 <= inp <= len(pulled):
                            kept.append(pulled[inp - 1])
                        else:
                            print("Invalid number.")
                    except ValueError:
                        print("Please enter a valid number.")

                print("\nYou selected to keep the following Mons:")
                for i, keeper in enumerate(kept):
                    print(f"\t{i + 1} : {keeper.name}")

                confirm = input("And discard all others? Type 'Yes' to confirm, anything else to reselect: ")
                if confirm.strip().lower() == "yes":
                    break

            return kept
        else: # pack empty (if no Mons met min_keep_rarity)
            return None
    
    @staticmethod
    def choice(player : Player, prompt : str, choices : List[Tuple[str, Optional[str]]]): 
        """
        Prompts a choice to the Player and takes their input to trigger events via method names.

        :param player: The Player object.
        :param prompt: A string that prompts the Player with a question or instruction.
        :param choices: A list of tuples where:
            - The first element is a display string for the choice.
            - The second element is an optional method name (as a string) on the Player instance.

        :returns: The result of calling the selected method, or None if no method was mapped.
        """

        Tools.text(prompt + "\n", params=Game.text_effects["Miniaturizer"])

        for idx, (label, _) in enumerate(choices):
            Tools.text(f"{idx}: {label}", params=Game.text_effects["Miniaturizer"])

        while True:
            try:
                choice_index = int(input("\nEnter the number of your choice: "))

                if 0 <= choice_index < len(choices):
                    _, method_name = choices[choice_index]

                    if method_name:
                        method = getattr(player, method_name, None)

                        if callable(method):
                            return method()
                        else:
                            Tools.text(f"The selected action '{method_name}' is not available.", params=Game.text_effects["Miniaturizer"])
                            return None
                    else:
                        Tools.text("You chose an option with no associated action.\n", params=Game.text_effects["Miniaturizer"])
                        return None
                else:
                    Tools.text("Invalid choice. Please enter a valid option number.", params=Game.text_effects["Miniaturizer"])

            except ValueError:
                Tools.text("Invalid input. Please enter a number.\n", params=Game.text_effects["Miniaturizer"])

    @staticmethod
    def encounter_testing(player: Player, 
                        num_encounters: int = 1, 
                        encounter_type: str = None, 
                        test_style: str = None, 
                        specified_mon: str = None, 
                        biome: str = None):
        """Encounter testing for normal or legendary encounters, in specified or standard test styles."""

        # Defensive checks
        if not encounter_type or encounter_type.lower() not in ("legendary", "normal"):
            raise ValueError(f"[ERROR] Invalid encounter_type: '{encounter_type}'. Valid types are 'legendary' or 'normal'.")

        if not test_style or test_style.lower() not in ("specified-mon", "standard"):
            raise ValueError(f"[ERROR] Invalid test_style: '{test_style}'. Valid styles are 'specified-mon' or 'standard'.")

        # LEGENDARY (currently placeholder)
        if encounter_type.lower() == "legendary":
            print("[TODO] Legendary encounter testing not implemented.")
            return

        # NORMAL ENCOUNTER
        if encounter_type.lower() == "normal":

            if test_style.lower() == "specified-mon":
                if not specified_mon:
                    raise ValueError("[ERROR] specified_mon is required for 'specified-mon' test_style.")

                mon_names = [m.name.lower() for m in player.mons]
                if specified_mon.lower() not in mon_names:
                    raise ValueError(f"[ERROR] Invalid Mon name: '{specified_mon}'. Mon must be in Player's Mon roster.")

                if biome is not None and biome not in Type.type_biomes:
                    raise ValueError(f"[ERROR] Invalid Biome name: '{biome}'.")

                # Get the Mon instance
                for m_ in player.mons:
                    if m_.name.lower() == specified_mon.lower():
                        if m_.health <= 0:
                            m_.health = m_.max_health
                        the_one = m_
                        break

                for _ in range(num_encounters):
                    Game.mon_encounter(player, biome=biome, player_use_mon=the_one, skip_tame=True)

            elif test_style.lower() == "standard":
                for _ in range(num_encounters):
                    Game.mon_encounter(player)
                    Miniaturizer.home_screen(player)

                    while True:
                        Tools.text("Cash out early? (Yes / No)", params=Game.text_effects["Yellow"])
                        inp = input().strip().lower()

                        if inp in ("yes", "no"):
                            break
                        Tools.text("Please enter 'Yes' or 'No'.", params=Game.text_effects["Yellow"])

                    if inp == "yes":
                        break

class Achievement: 
    """A class for implementing Achievements."""

    def __init__(self, 
                 name : Optional[str] = "Achievement", 
                 description : Optional[str] = "", 
                 experience_reward : Optional[int] = 0, 
                 item_rewards : Optional[List[str]] = []):
        self.name = name
        self.description = description
        self.experience_reward = experience_reward
        self.item_rewards = item_rewards

    def __str__(self):

        xp = f"\t\t{self.experience_reward} XP\n" if self.experience_reward else ""
        items = f"\t\t{self.item_rewards}\n" if self.item_rewards else ""

        if xp == "" and items == "":
            xp = "\t\tNone\n"

        return (
            f"{self.name}:\n"
            f"\tRewards:\n"
            f"{xp}"
            f"{items}"
            f"\tDescription: {self.description}\n"
        )

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "experience_reward": self.experience_reward,
            "item_reward": self.item_rewards, 
        }

    @staticmethod
    def parse(name : str, data : dict):
        """Parses a dictionary into an Achievement object using its name key."""
        try:
            return Achievement(
                name=name,
                description=data.get("description"),
                experience_reward=data.get("experience_reward"),
                item_rewards=data.get("item_rewards")
            )
        except KeyError as e:
            print(f"[Error] Missing field {e} in Achievement data for: {name}")
            return None

class Miniaturizer:
    """A class for implementing the Miniaturizer 9000, which acts as the UI and Item Inventory."""

    ## Miniaturizer text tools: 
        # Tools.text(f"\n\n", params=Game.text_effects["Miniaturizer"]) 

    def __init__(self, 
                 mon_packs : Optional[int] = 0, 
                 health_potions : Optional[int] = 0, # must make class for health potions...may merge with Items and use type attributes
        ): 
        self.mon_packs = mon_packs
        self.health_potions = health_potions

    def to_dict(self):
        return {
            "mon_packs": self.mon_packs,
            "health_potions": self.health_potions
        }

    @staticmethod
    def parse(name : str, data : dict):
        """Parses a dictionary into an Miniaturizer object using its name key."""
        try:
            return Miniaturizer(
                mon_packs=data.get("mon_packs"),
                health_potions=data.get("health_potions")
            )
        except KeyError as e:
            print(f"[Error] Missing field {e} in Miniaturizer data")
            return None

    @staticmethod
    def home_screen(player : Player):
        """Miniaturizer Home Screen."""

        while True:
            Tools.text(f"Please make a selection:\n", params=Game.text_effects["Miniaturizer"]) 
            Tools.text(f"\t1 : Your Mons\n", params=Game.text_effects["Miniaturizer"]) 
            Tools.text(f"\t2 : Your Items\n", params=Game.text_effects["Miniaturizer"]) 
            Tools.text(f"\t3 : Your Achievements\n", params=Game.text_effects["Miniaturizer"]) 
            Tools.text(f"\t4 : Your Stats\n", params=Game.text_effects["Miniaturizer"]) 
            Tools.text(f"\t5 : Info\n", params=Game.text_effects["Miniaturizer"]) 
            Tools.text(f"\t0 : Exit the Miniaturizer\n\n", params=Game.text_effects["Miniaturizer"]) 

            try:
                inp = int(input(">> "))
            except ValueError:
                Tools.text("Invalid input. Please enter a number.\n\n", params=Game.text_effects["Miniaturizer"])
                continue

            if inp == 1:
                Miniaturizer.mon_list(player)
            elif inp == 2:
                while True:
                    Tools.text(f"Please make a selection:\n", params=Game.text_effects["Miniaturizer"]) 
                    Tools.text(f"\t1 : ", params=Game.text_effects["Miniaturizer"])
                    Tools.text(f"Health Potions ", params=Game.text_effects["Red"])
                    Tools.text(f"(x{player.health_potions})\n", params=Game.text_effects["Miniaturizer"])
                    Tools.text(f"\t2 : ", params=Game.text_effects["Miniaturizer"])
                    Tools.text(f"M", params=Game.text_effects["Red"])
                    Tools.text(f"o", params=Game.text_effects["Orange"])
                    Tools.text(f"n ", params=Game.text_effects["Yellow"])
                    Tools.text(f"P", params=Game.text_effects["Green"])
                    Tools.text(f"a", params=Game.text_effects["Blue"])
                    Tools.text(f"c", params=Game.text_effects["Purple"])
                    Tools.text(f"k", params=Game.text_effects["Pink"])
                    Tools.text(f"s ", params=Game.text_effects["Red"])
                    Tools.text(f"(x{player.mon_packs})\n", params=Game.text_effects["Miniaturizer"])
                    Tools.text(f"\t3 : ", params=Game.text_effects["Miniaturizer"])
                    Tools.text(f"Learn Random Move ", params=Game.text_effects["Orange"])
                    Tools.text(f"(x{player.learn_random_moves})\n", params=Game.text_effects["Miniaturizer"])
                    Tools.text(f"\t4 : ", params=Game.text_effects["Miniaturizer"])
                    Tools.text(f"Learn Specific Move ", params=Game.text_effects["Purple"])
                    Tools.text(f"(x{player.learn_specific_moves})\n", params=Game.text_effects["Miniaturizer"])
                    Tools.text(f"\t0 : Go back.\n\n", params=Game.text_effects["Miniaturizer"])

                    try:
                        sub_inp = int(input(">> "))
                    except ValueError:
                        Tools.text("Invalid input. Please enter a number.\n\n", params=Game.text_effects["Miniaturizer"])
                        continue

                    if sub_inp == 1: 
                        player.use_health_potion()
                    elif sub_inp == 2: 
                        player.use_mon_pack()
                    elif sub_inp == 3:
                        player.use_learn_random_move()
                    elif sub_inp == 0: 
                        break
                    else:
                        Tools.text("Invalid selection. Try again.\n", params=Game.text_effects["Miniaturizer"])

            elif inp == 3:
                for ach in player.achievements:
                    Tools.text(f"{ach}\n\n", params=Game.text_effects["Miniaturizer"])
            elif inp == 4:
                Tools.text(f"{player.player_stats()}\n\n", params=Game.text_effects["Miniaturizer"])
            elif inp == 5:
                Tools.text("Info section not implemented yet.\n\n", params=Game.text_effects["Miniaturizer"])
            elif inp == 0:
                Tools.text(f"Closing Miniaturizer 9000...\n\n", params=Game.text_effects["Miniaturizer"])
                return
            else: 
                Tools.text("Invalid selection. Please choose a valid option.\n\n", params=Game.text_effects["Miniaturizer"])
            
    def mon_list(player: Player, 
                 isolate_mons : List[Mon] = None, 
                 type_filter : List[Type] = None, 
                 filter_is_alive : bool = False, 
                 filter_is_dead : bool = False, 
                 filter_is_hurt : bool = False, 
                 rarity_filter : str = None,
                 attribute_sort : List[str] = None, 
                 pearl_short_hand : bool = True
        ): 
        """Prints the Player's Mon list, with optional filters."""

        if not player.mons:
            Tools.text("You have no Mons.\n", params=Game.text_effects["Miniaturizer"])
            return

        print_mons = []

        if isolate_mons:
            for mon in isolate_mons:
                if mon not in player.mons:
                    raise ValueError(f"[ERROR] Mon '{mon.name}' is not part of the player's roster.")
            m_list = isolate_mons
        else: 
            m_list = player.mons

        for mon in m_list:
            #print(mon.health)
            if type_filter and not any(tp in mon.type for tp in type_filter):
                continue

            if rarity_filter and mon.rarity != rarity_filter:
                continue

            # Combine status filters intelligently
            if filter_is_dead or filter_is_hurt or filter_is_alive:
                is_dead = mon.health <= 0
                is_hurt = 0 < mon.health < mon.max_health
                is_alive = mon.health > 0

                # If none of the conditions match, skip
                if not (
                    (filter_is_dead and is_dead) or 
                    (filter_is_hurt and is_hurt) or 
                    (filter_is_alive and is_alive)
                ):
                    continue

            print_mons.append(mon)

        if not print_mons:
            #Tools.text("[DEBUG] No Mons match the given filters.\n", 0, True, False, [255, 255, 255])
            return
        
        # sort here
        if attribute_sort:
            if isinstance(attribute_sort, str):
                attribute_sort = [attribute_sort]

            def sort_key(mon: Mon):
                key = []
                for attr_name in attribute_sort:
                    attr_value = getattr(mon, attr_name, None)

                    if attr_name == "rarity":
                        key.append(Mon.rarities.get(attr_value, -1))
                    else:
                        key.append(attr_value if attr_value is not None else 0)
                return tuple(key)

            print_mons.sort(key=sort_key, reverse=True)

        for i, mon in enumerate(print_mons):
            type_str = "/".join(str(tp).split()[0] for tp in mon.type)
            Tools.text(f"{i + 1:>3} - ", params=Game.text_effects["Miniaturizer"])
            Tools.text(f"Perf ", rgb=[255, 145, 40]) if mon.perfect else None
            Mon.pearlize(Mon.pearls[mon.pearl].split()[0], short_hand=True) if mon.pearl else None
            if mon.pearl and not mon.perfect:
                Tools.text(f"{mon.name:<17}", params=Mon.rarity_effects[mon.rarity])
            elif not mon.pearl and mon.perfect:
                Tools.text(f"{mon.name:<16}", params=Mon.rarity_effects[mon.rarity])
            elif mon.pearl and mon.perfect:
                Tools.text(f"{mon.name:<12}", params=Mon.rarity_effects[mon.rarity])
            else:
                Tools.text(f"{mon.name:<20}", params=Mon.rarity_effects[mon.rarity])
            #Tools.text(f"{mon.name:<20}", params=Mon.rarity_effects[mon.rarity]) if not mon.pearl else Tools.text(f"{mon.name:<17}", params=Mon.rarity_effects[mon.rarity])
            Tools.text(f" (LVL{mon.level:>3}): {type_str:>13} | {(mon.attack_boost + 1.0):.0%} ATK | {mon.defense:>3,} DEF | {mon.stamina:>4,} / {mon.max_stamina:,} STM | ", params=Game.text_effects["Miniaturizer"])
            if mon.health <= 0:
                hp_col_width = 13
                dead_str = "DEAD".center(hp_col_width + 1)
                Tools.text(f"{dead_str} ", params=Game.text_effects["Red"])
                Tools.text(f"|", params=Game.text_effects["Miniaturizer"])
            else:
                if mon.health == mon.max_health:
                    hp_color = Game.text_effects["Green"]
                elif mon.health >= mon.max_health * 0.5:
                    hp_color = Game.text_effects["Yellow"]
                else:
                    hp_color = Game.text_effects["Orange"]

                # Build the HP numerals string (including the "/" separator)
                hp_numerals_str = f"{mon.health:>4,} / {mon.max_health:<4,}"

                # Print the colorized HP numerals
                Tools.text(hp_numerals_str, params=hp_color)

                # Then print " HP |" with the Miniaturizer effect
                Tools.text(" HP |", params=Game.text_effects["Miniaturizer"])

            wins = mon.wins
            total_battles = mon.battles
            losses = total_battles - wins
            win_pct = f"{(wins / total_battles * 100):.1f}" if total_battles else "0"

            Tools.text("   ", params=Game.text_effects["Miniaturizer"])  # spacer

            Tools.text(f"{wins}", params=Game.text_effects["Green"])
            Tools.text(" / ", params=Game.text_effects["Miniaturizer"])
            Tools.text(f"{losses}", params=Game.text_effects["Red"])
            Tools.text(f" ({win_pct} W%)\n\n", params=Game.text_effects["Miniaturizer"])

        return print_mons

class Item:
    """A class for implementing Items."""

class Weapon:
    """A class for implementing Weapons."""

class Rubix: 
    """A class for implementing the Rubix Cube Minigame."""

    print_order = [
        "right", 
        "top", 
        "front", 
        "bottom", 
        "back", 
        "left"
    ]

    sides = {
        "right" : 0,
        "top" : 1,
        "front" : 2,
        "bottom" : 3,
        "back" : 4,
        "left" : 5
    }

    colors = [
        "Red", 
        "Yellow", 
        "Blue", 
        "White", 
        "Green", 
        "Orange"
    ]

    def __init__(self):
            F = []
            for i in range(6):
                l = []
                for j in range(9):
                    l.append(Rubix.colors[i][0])

                F.append(Face(l))

            self.right = F[0]
            self.top = F[1]
            self.front = F[2]
            self.bottom = F[3]
            self.back = F[4]
            self.left = F[5]
            self.faces = F

    def __str__(self):
        stagger = []
        stagger.append(self.top)
        stagger.append(self.front)
        stagger.append(self.bottom)
        stagger.append(self.back)

        row1 = []
        row2 = []
        row3 = []

        ## IDEA: just add together the faces around the center, then strip by newline character, then piece them back together

        for tl, fc in enumerate(stagger):
            if tl % 9 == 0 or tl % 9 == 1 or tl % 9 == 2:
                row1.append(fc[tl])
            elif tl % 9 == 3 or tl % 9 == 4 or tl % 9 == 5:
                row2.append(fc[tl])
            elif tl % 9 == 6 or tl % 9 == 7 or tl % 9 == 8:
                row3.append(fc[tl])

        result = ""
        for i, fc in enumerate(self.faces):
            # Indent front and right faces
            if i == 0 or i == 5:
                result += fc.__str__(" " * 10)
            else:
                result += fc.__str__()  # No indent
        return result

    @staticmethod
    def info():
        """A method for printing info about the Rubix Cube layout, solving, algorithms, etc."""

        Rubix.layout()

    @staticmethod
    def layout():
        """A method for printing the flattened view of the Rubix Cube with labeled Faces."""

        print (
            "Rubix Cube Layout:\n"
            f"          |‾‾‾‾‾‾‾‾|\n"
            f"          |  right |\n"
            f"          |        |\n"
            f"           ‾‾‾‾‾‾‾‾\n"
            f"|‾‾‾‾‾‾‾‾||‾‾‾‾‾‾‾‾||‾‾‾‾‾‾‾‾||‾‾‾‾‾‾‾‾|\n"
            f"|  top   || front  || bottom ||  back  |\n"
            f"|        ||        ||        ||        |\n"
            f" ‾‾‾‾‾‾‾‾  ‾‾‾‾‾‾‾‾  ‾‾‾‾‾‾‾‾  ‾‾‾‾‾‾‾‾\n"
            f"          |‾‾‾‾‾‾‾‾|\n"
            f"          |  left  |\n"
            f"          |        |\n"
            f"           ‾‾‾‾‾‾‾‾\n"
        )

class Face: 
    """A class for constructing the sides of Rubix Cube for the Minigame."""

    def __init__(self, tls : List[str]):
        if len(tls) != 9:
            raise ValueError("Could not make Face - invalid number of tiles")
        self.tiles = tls

    def __str__(self, line_header : Optional[str] = ""):
        result = ""
        for i in range(9):
            if (i + 1) % 3 == 1:
                result += f"{line_header}| {self.tiles[i]}"
            else:
                result += f"|{self.tiles[i]}"
            if (i + 1) % 3 == 0:
                result += f" |\n"
            elif i == 8:
                result += f" |"
        return result