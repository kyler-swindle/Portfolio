from __future__ import annotations
from collections import defaultdict
from copy import deepcopy
import time
import itertools
import random
import json
import os
import re
import math
import sys
from typing import Any, Dict, List, Optional, Tuple

class Mon: 
    """A class to define a Mon with Type, Level, Moves, Health, Defense, Stamina, Rarity attributes."""

    rarities = { 
        # Rarities may assign boosts to Mon stats or Moveset.
        "Any" : 0, 
        "Common" : 1,
        "Uncommon" : 2, 
        "Rare" : 3, 
        "Epic" : 4,
        "Legendary" : 5, 
        "Ultra" : 6, 
        "Omega" : 7 
    }

    rarity_effects = { 
        "Any" : [0, True, True, [0, 0, 0]], 
        "Common" : [0, True, True, [0, 0, 0]],
        "Uncommon" : [0, True, True, [85, 255, 0]], 
        "Rare" : [0, True, True, [0, 47, 255]], 
        "Epic" : [0, True, True, [255, 0, 230]],
        "Legendary" : [0, True, True, [252, 169, 3]], 
        "Ultra" : [0, True, True, [170, 0, 255]], 
        "Omega" : [0, True, True, [255, 0, 0]] 
    }

    pearls = {
        0 : "", 
        1 : "White Pearl", 
        2 : "Black Pearl"
    }

    def __init__(self, 
                name: Optional[str] = None,
                leveled : Optional[bool] = None,
                level: Optional[int] = None,
                perfect: Optional[bool] = None,
                # species # coming soon? 
                experience: int = 0,
                experience_needed: int = 100,
                health: int = 100,
                max_health: int = 100,
                attack_boost : float = None,
                defense: int = 0,
                stamina: int = 100,
                max_stamina : int = 100, 
                moves_limit: int = 2,
                wins : Optional[int] = 0, 
                battles : Optional[int] = 0,
                battle_log : Optional[List[str]] = None,
                pearl : Optional[int] = None,
                boosted : Optional[bool] = None,
                rarity: Optional[str] = None,
                tp: Optional[List["Type"]] = None,
                moves: Optional[List["Move"]] = None ): 
        self.type = tp if tp is not None else Type.assign_types_weighted()
        self.leveled = leveled if leveled is not None else False
        self.level = level if level is not None and leveled == True else 0
        self.perfect = perfect if perfect is not None else False
        self.experience = experience
        self.experience_needed = experience_needed
        self.health = health
        self.max_health = max_health
        self.attack_boost = attack_boost if attack_boost is not None else 0.00
        self.defense = defense
        self.stamina = stamina
        self.max_stamina = max_stamina
        self.moves_limit = moves_limit
        self.wins = wins
        self.battles = battles
        self.battle_log = battle_log if battle_log is not None else []
        self.pearl = pearl
        self.boosted = boosted if boosted is not None else False
        self.rarity = rarity if rarity is not None else self.assign_rarity_weighted()
        self.name = name if name is not None else self.make_name()
        self.moves = moves if moves is not None else []
        self.effects = []
        self.original_values: Dict[str, Any] = {} 
        self.original_move_values: Dict[str, Dict[str, Any]] = {}

        if self.pearl is None:
            self.pearl = Mon.assign_pearl(self.rarity)

        if self.boosted is False:
            self.rarity_boost(self.rarity)

        if not self.moves:
            self.assign_moves(self.type)

        if self.leveled is False and self.level == 0 and level is not None:
            #Tools.text(f"[DEBUG] init {self.level} {level}\n", rgb=[255, 0, 0])
            self.level = 1
            self.adjust_level(level, verbose=False)

        if self.level == 0:
            #Tools.text(f"[DEBUG] {level}\n", rgb=[255, 0, 0])
        
            self.level = 1
            rnd_lvl = Mon.assign_random_level()
            self.adjust_level(rnd_lvl, verbose=False)

    def __str__(self):
        types_str = ', '.join(str(t) for t in self.type)
        moves_str = '\n'.join(str(move) for move in self.moves)
        effect_str = ', '.join(efct.name for efct in self.effects)
        perf_str = Mon.rarity_colors(self.rarity, rgb_override=[255, 145, 40], str_override="Perf ") if self.perfect else ""
        pearl_color = [255, 255, 255] if self.pearl == 1 else [20, 20, 20]
        pearl_str = Mon.rarity_colors(self.rarity, rgb_override=pearl_color, str_override=Mon.pearls[self.pearl]+" ") if self.pearl >= 1 else ""
        atk_bst = f"Atk: {self.attack_boost + 1.0:.0%}"
        hp_str = f"HP: ({self.health} / {self.max_health})"
        def_str = f"Def: {self.defense}"
        stam_str = f"Stm: ({self.stamina} / {self.max_stamina})"
        return (
            f"{perf_str}{pearl_str}"
            f"{Mon.rarity_colors(self.rarity, str_override=self.name)} "
            f"(Lv{self.level}): {effect_str:>50}\n"
            f"Typ: {types_str:<17} {atk_bst} {hp_str:>18} {def_str:>10} {stam_str:>18}   Rar: {Mon.rarity_colors(self.rarity)}\n"
            f"Moves ({len(self.moves)}/{self.moves_limit}): \n{moves_str}"
        )
    
    def __eq__(self, other : Mon) -> bool:
        if not isinstance(other, Mon):
            return NotImplemented

        return (
            self.name == other.name and
            self.leveled == other.leveled and
            self.level == other.level and
            self.perfect == other.perfect and
            self.experience == other.experience and
            self.experience_needed == other.experience_needed and
            self.health == other.health and
            self.max_health == other.max_health and
            self.attack_boost == other.attack_boost and
            self.defense == other.defense and
            self.stamina == other.stamina and
            self.max_stamina == other.max_stamina and
            self.moves_limit == other.moves_limit and
            self.wins == other.wins and 
            self.battles == other.battles and 
            self.battle_log == other.battle_log and
            self.pearl == other.pearl and
            self.boosted == other.boosted and
            self.rarity == other.rarity and
            self.type == other.type and
            self.moves == other.moves
        )
    
    def export(self, filename : str): 
        """A method to export the Mon to the specified JSON file."""

        new_data = self.to_dict()

        # If file exists, load existing data
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {}  # File is empty or invalid
        else:
            existing_data = {}

        # Merge new Mon into existing data
        existing_data.update(new_data)

        # Write back the updated dictionary
        with open(filename, 'w') as f:
            json.dump(existing_data, f, indent=4)

    def to_dict(self):
        """Returns a dictionary for the Mon."""

        type_dicts = [{"parent_class": tp.parent_class, "subclass": tp.subclass} for tp in self.type]
        moves = [mv.to_dict() for mv in self.moves]

        return { 
            self.name : {
                "leveled" : self.leveled,
                "level" : self.level,
                "perfect" : self.perfect,
                "experience" : self.experience,
                "experience_needed" : self.experience_needed,
                "health" : self.health,
                "max_health" : self.max_health,
                "attack_boost" : self.attack_boost,
                "defense" : self.defense,
                "stamina" : self.stamina,
                "max_stamina" : self.max_stamina,
                "moves_limit" : self.moves_limit,
                "wins" : self.wins,
                "battles" : self.battles,
                "battle_log" : self.battle_log,
                "type" : type_dicts,
                "pearl" : self.pearl,
                "boosted" : self.boosted,
                "rarity" : self.rarity,
                "moves" : moves
            }
        }
    
    @staticmethod
    def parse(name: str, data: dict):
        """Parses a dictionary into a Mon object using its name key."""
        try:
            types = []
            for type_entry in data.get("type", []):
                # Now type_entry is a dict with keys "parent_class" and "subclass"
                parent_class = type_entry.get("parent_class")
                subclass = type_entry.get("subclass")
                types.append(Type(parent_class, subclass))

            moves = []
            for move_entry in data.get("moves", []):
                for move_name, move_info in move_entry.items():
                    parsed_move = Move.parse(move_info, name=move_name)
                    if parsed_move:
                        moves.append(parsed_move)
            
            battle_logs = []
            for battle_entry in data.get("battle_log", []):
                for battle_info in battle_entry.items():
                    battle_logs.append(battle_info)

            return Mon(
                name=name,
                leveled=data.get("leveled", None),
                level=data.get("level", 1),
                perfect=data.get("perfect", None),
                experience=data.get("experience", 0),
                experience_needed=data.get("experience_needed", 100),
                health=data.get("health", 100),
                max_health=data.get("max_health", 100),
                attack_boost=data.get("attack_boost", None),
                defense=data.get("defense", 0),
                stamina=data.get("stamina", 100),
                max_stamina=data.get("max_stamina", 100),
                moves_limit=data.get("moves_limit", 2),
                wins=data.get("wins", 0),
                battles=data.get("battles", 0),
                battle_log=battle_logs,
                pearl=data.get("pearl", None),
                boosted=data.get("boosted", None),
                rarity=data.get("rarity"),
                tp=types,
                moves=moves
            )
        except KeyError as e:
            print(f"[Error] Missing field {e} in Mon data for: {name}")
            return None
    
    def make_name(self, wild = True):
        """A method for making a generic name for wild Mons."""

        type_name = "/".join(str(tp).split()[0] for tp in self.type)
        wild_str = "Wild " if wild else ""

        return f"{wild_str}{self.rarity} {type_name} Mon"

    def assign_moves(self, tp : List[Type], move_num : int = 2, move_priority : Tuple[bool, bool, bool] = (False, False, False)):
        """A method to assign two unique default random Moves to a Mon, corresponding to their given Type."""
        
        self.moves = set() # sets moves to new empty set
        attempts = 0

        while len(self.moves) < move_num and attempts < 10:
            mv = Move.choose_random_move(self, tp, move_priority=move_priority)
            if mv:
                self.moves.add(mv)
            attempts += 1

        self.moves = list(self.moves)

    def reload_moves(self):
        """A method to reload the Mon's moves from the JSON file, updating attributes as needed and keeping earned data."""
        
        for i, old_move in enumerate(self.moves):
            #Tools.text(f"[Debug] {self.name} {old_move.name}\n", rgb=[255, 0, 255])
            new_move = Move.get(old_move.move_types, old_move.name)

            if old_move.prestige:
                new_move = Move.get(old_move.move_types, old_move.prestige.name)
                
            if old_move.prestige and new_move.prestige:
                new_move.prestige.adjust_rank(new_move, old_move.prestige.rank, verbose=False)
                new_move.prestige.add_experience(new_move, old_move.prestige.experience, verbose=False)

            self.moves[i] = new_move

    def assign_best_moves(self):
        """Assigns the best possible moves to the Mon, using AI-like classification logic."""

        from itertools import combinations

        self.moves.clear()

        base_dir = os.path.dirname(__file__)
        rarity_level = Mon.rarities[self.rarity]
        type_variants = set()

        for t in self.type:
            base = str(t).split()[0].lower()
            type_variants.add(base)
            if t.subclass:
                type_variants.add(t.parent_class.lower())

        seen_files = set()
        valid_moves = []

        for r in range(1, len(type_variants) + 1):
            for combo in combinations(type_variants, r):
                joined = ",".join(sorted(combo))
                if joined in seen_files:
                    continue
                seen_files.add(joined)

                filename = f"{joined}_moves.json"
                filepath = os.path.join(base_dir, "Game/data/moves", filename)

                try:
                    with open(filepath, "r") as f:
                        move_data = json.load(f)
                        for name, move in move_data.items():
                            if Mon.rarities.get(move.get("rarity", "Any"), 0) <= rarity_level and move not in valid_moves:
                                valid_moves.append((name, move))
                except FileNotFoundError:
                    continue

        if not valid_moves:
            print(f"[assign_best_moves] No valid moves found for {[str(t) for t in self.type]} ({self.rarity})")
            return

        # ==== CLASSIFY AND SORT MOVES ====
        def parse_effect_score(mv_obj : Move) -> int:
            buff_score = 0
            for efct in mv_obj.effects:
                for i, tp in enumerate(efct.effect_type):
                    if tp == "buff" and efct.target_self[i]:
                        buff_score += 1
                    elif tp == "debuff" and not efct.target_self[i]:
                        buff_score += 1
            return buff_score
        
        def stun_score(mv_obj : Move) -> int:
            buff_score = 0
            for efct in mv_obj.effects:
                for i, tp in enumerate(efct.effect_type):
                    if tp == "stun" and not efct.target_self[i]:
                        buff_score += efct.duration
            return buff_score

        dmg_moves = []
        heal_moves = []
        spc_moves = []
        stun_moves = []

        for name, raw_mv in valid_moves:
            mv = Move.parse(raw_mv, name)
            dmg_out = mv.damage_output(include_damaging_effects=True, attack_boost=self.attack_boost, simulate_prestige=True)
            heal_out = mv.damage_output(include_healing_effects=True, simulate_prestige=True)

            if dmg_out > 0:
                #print(f"{mv.name} dmg = {dmg_out}")
                dmg_moves.append((mv, dmg_out))
            elif heal_out < 0:
                heal_moves.append((mv, heal_out))

            if dmg_out == 0:
                if any(
                    tp in efct.effect_type
                    for efct in mv.effects
                    for tp in ("buff", "debuff")
                ):
                    spc_moves.append((mv, parse_effect_score(mv)))
                    #print(mv)
            
            if any(
                    "stun" in efct.effect_type
                    for efct in mv.effects
                ):
                    stun_moves.append((mv, stun_score(mv)))

        dmg_moves.sort(key=lambda x: x[1], reverse=True)
        heal_moves.sort(key=lambda x: x[1])  # More negative = stronger heal
        spc_moves.sort(key=lambda x: parse_effect_score(x[0]), reverse=True)
        stun_moves.sort(key=lambda x: stun_score(x[0]), reverse=True)

        # ==== ASSIGN FINAL MOVES ====
        chosen = []
        chosen_names = set()

        def try_add_move(move_obj):
            if move_obj.name not in chosen_names:
                chosen.append(move_obj)
                chosen_names.add(move_obj.name)

        # Add best from each category
        if dmg_moves:
            try_add_move(dmg_moves[0][0])
        if heal_moves:
            try_add_move(heal_moves[0][0])
        if spc_moves:
            try_add_move(spc_moves[0][0])
        if stun_moves:
            try_add_move(stun_moves[0][0])

        # Fill remaining with top damage moves
        for mv, _ in dmg_moves:
            try_add_move(mv)

        # Assign
        self.moves = chosen[:self.moves_limit]

    def rarity_boost(self, _rarity: str):
        """Assigns random stat boosts corresponding to Rarity ranges. Modifies boost ranges for Pearls."""

        if _rarity not in Mon.rarities:
            print("Invalid Rarity.")
            return

        rar = Mon.rarities[_rarity]
        bh = self.max_health
        bs = self.max_stamina

        # Data structure for rarity boost ranges
        boost_data = {
            1: {  # Common
                "hp_stam": (0.00, 0.00),
                "defense": (0.00, 0.00),
                "attack": (0.00, 0.00),
                "moves": 0,
            },
            2: {  # Uncommon
                "hp_stam": (0.01, 0.14),
                "defense": (0.0439, 0.1078),
                "attack": (0.01, 0.05),
                "moves": 0,
            },
            3: {  # Rare
                "hp_stam": (0.15, 0.29),
                "defense": (0.1079, 0.1678),
                "attack": (0.06, 0.10),
                "moves": 0,
            },
            4: {  # Epic
                "hp_stam": (0.30, 0.49),
                "defense": (0.1679, 0.2261),
                "attack": (0.11, 0.20),
                "moves": 0,
            },
            5: {  # Legendary
                "hp_stam": (0.50, 0.99),
                "defense": (0.2262, 0.2842),
                "attack": (0.21, 0.30),
                "moves": 1,
            },
            6: {  # Ultra
                "hp_stam": (1.00, 1.99),
                "defense": (0.2843, 0.3124),
                "attack": (0.31, 0.40),
                "moves": 2,
            },
            7: {  # Omega
                "hp_stam": (2.00, 3.00),
                "defense": (0.3125, 0.4),
                "attack": (0.41, 0.50),
                "moves": 3,
            }
        }

        data = boost_data.get(rar)
        if data is None:
            print(f"Unexpected Rarity value _rarity = {_rarity} rar = {rar}.")
            return None

        # Pearl logic modifiers
        def apply_pearl_modifiers(attribute: str):
            min_val, max_val = data[attribute]
            pearl = self.pearl

            # --- pearl math (same as now) ---
            if pearl == 1:                        # white
                if attribute in ("defense", "hp_stam"):
                    new_min = (max_val - min_val) * 0.80 + min_val
                    new_max = (max_val - min_val) * 0.10 + max_val
                else:
                    new_min = (max_val - min_val) * 0.80 + min_val
                    new_max = (max_val - min_val) * 0.25 + max_val

            elif pearl == 2:                      # black
                if attribute in ("defense", "hp_stam"):
                    new_min = new_max = (max_val - min_val) * 0.25 + max_val
                else:
                    new_min = new_max = (max_val - min_val) * 1.25 + max_val

            else:                                 # no pearl
                new_min, new_max = min_val, max_val

            # --- perfection collapse ---
            if getattr(self, "perfect", False):
                return (new_max, new_max)         # flawless roll

            return (new_min, new_max)

        hp_stam_boost_min, hp_stam_boost_max = apply_pearl_modifiers("hp_stam") 
        defense_boost_min, defense_boost_max = apply_pearl_modifiers("defense")
        attack_boost_min, attack_boost_max = apply_pearl_modifiers("attack")
        #Tools.text(f"{Mon.rarity_colors(self.rarity)}\n")
        #print(f"Old {self.attack_boost}, {self.defense}, {self.max_health}, {self.max_stamina}")

        # Apply boosts
        self.max_health += random.randint(int(bh * hp_stam_boost_min), int(bh * hp_stam_boost_max))
        self.health = self.max_health

        self.defense += random.randint(int(self.max_health * defense_boost_min),
                                    int(self.max_health * defense_boost_max))

        self.max_stamina += random.randint(int(bs * hp_stam_boost_min), int(bs * hp_stam_boost_max))
        self.stamina = self.max_stamina

        self.attack_boost = random.randint(int(100 * attack_boost_min), int(100 * attack_boost_max)) / 100
        self.attack_boost = Tools.floor_to_nearest_float(self.attack_boost, 0.01)

        # Add move capacity if applicable
        self.moves_limit += data["moves"]
        #print(f"New {self.attack_boost}, {self.defense}, {self.max_health}, {self.max_stamina}")

        self.boosted = True

        return _rarity

    def rarity_boost2(self, _rarity : str):
        """[OUTDATED] A method to assign random stat boosts corresponding to Rarity ranges."""

        if _rarity not in Mon.rarities:
            print("Invalid Rarity.")
            return
        
        rar = Mon.rarities[_rarity]
        bh = self.max_health
        bs = self.max_stamina

        if rar == 1: # Common = base stats
            rarity_boost_min = 0.00
            rarity_boost_max = 0.00
            defense_boost_min = 0.00
            defense_boost_max = 0.00
            attack_boost_min = 0.00
            attack_boost_max = 0.00
        elif rar == 2: # Uncommon = base stats + (1% - 14% boost)
            rarity_boost_min = 0.01
            rarity_boost_max = 0.14
            defense_boost_min = 0.0439
            defense_boost_max = 0.1078
            attack_boost_min = 0.01
            attack_boost_max = 0.05
        elif rar == 3: # Rare = base stats + (15% - 29% boost)
            rarity_boost_min = 0.15
            rarity_boost_max = 0.29
            defense_boost_min = 0.1079
            defense_boost_max = 0.1678
            attack_boost_min = 0.06
            attack_boost_max = 0.10
        elif rar == 4: # Epic = base stats + (30% - 49% boost)
            rarity_boost_min = 0.30
            rarity_boost_max = 0.49
            defense_boost_min = 0.1679
            defense_boost_max = 0.2261
            attack_boost_min = 0.11
            attack_boost_max = 0.20
        elif rar == 5: # Legendary = base stats + (50% - 99% boost)
            rarity_boost_min = 0.50
            rarity_boost_max = 0.99
            defense_boost_min = 0.2262
            defense_boost_max = 0.2842
            attack_boost_min = 0.21
            attack_boost_max = 0.30
            self.moves_limit += 1
        elif rar == 6: # Ultra = base stats + (100% - 199% boost)
            rarity_boost_min = 1.00
            rarity_boost_max = 1.99
            defense_boost_min = 0.2843
            defense_boost_max = 0.3124
            attack_boost_min = 0.31
            attack_boost_max = 0.40
            self.moves_limit += 2
        elif rar == 7: # Omega = base stats + (200% - 300% boost)
            rarity_boost_min = 2.00
            rarity_boost_max = 3.00
            defense_boost_min = 0.3125
            defense_boost_max = 0.4
            attack_boost_min = 0.41
            attack_boost_max = 0.50
            self.moves_limit += 3
        else: 
            print(f"Unexpected Rarity value _rarity = {_rarity} rar = {rar}.")
            return None
        
        # Assign random boosts
        self.max_health += random.randint(int(bh * rarity_boost_min), int(bh * rarity_boost_max))
        self.health = self.max_health
        self.defense += random.randint(int(self.max_health * defense_boost_min), int(self.max_health * defense_boost_max)) # based on a percentage of health
        self.max_stamina += random.randint(int(bs * rarity_boost_min), int(bs * rarity_boost_max))
        self.stamina = self.max_stamina
        self.attack_boost = random.randint(int(100 * attack_boost_min), int(100 * attack_boost_max)) / 100
        self.attack_boost = Tools.floor_to_nearest_float(self.attack_boost, 0.01)
        #Tools.text(f".", rgb=[255,0,0])
        #Tools.text(f"{_rarity} {self.level} {self.attack_boost}\n", rgb=[255,0,0]) if self.attack_boost is not None else Tools.text(f"NONE\n", rgb=[255,0,0])

        return _rarity
    
    @staticmethod
    def assign_attack_boost(dist: bool = False, min_val: float = 0.05, max_val: float = 0.50, bias: float = 0.65, squish: float = 0.15):
        """Returns a random float between min and max.
        
        If dist is True, applies a power-law distribution shaped by bias:
        - bias > 1: skewed toward max
        - bias < 1: skewed toward min
        - bias = 1: uniform
        - squish = 0.0 to 1.0, higher tightens dist
        """
        squish = max(0.0, min(1.0, squish))
        max_samples = 5  # you can raise this for sharper peaks
        samples = 1 + int(squish * (max_samples - 1))

        # Generate average of multiple samples
        values = []
        for _ in range(samples):
            if dist:
                r = random.random() ** (1 / bias)
            else:
                r = random.random()
            values.append(r)

        r_avg = sum(values) / samples
        boost = min_val + r_avg * (max_val - min_val)
        return boost #Tools.floor_to_nearest_float(boost, 0.01) #round(boost, 2)
        
    def assign_rarity(self, minimum_rarity : Optional[str] = None): 
        """A method to assign Rarity and resolve corresponding stat boosts."""

        if minimum_rarity is not None and minimum_rarity not in Mon.rarities:
            raise ValueError(f"Rarity {minimum_rarity} not found.")
        
        rand = random.randint(1,1000)

        if minimum_rarity in ("Legendary", "Ultra", "Omega"): 
            rand = 1000
        elif minimum_rarity in ("Uncommon", "Rare", "Epic"): 
                rand = 667
        elif minimum_rarity == "Common": 
                rand = 1

        # if-block for Legendary+ Rarity 
        if rand == 1000: 
            rand = random.randint(1, 10)

            if minimum_rarity in ("Ultra", "Omega"): 
                rand = 10
            
            # if-block for Ultra+ Rarity 
            if rand == 10: 
                rand = random.randint(1, 10)

                if minimum_rarity == "Omega": 
                    rand = 10
                
                # if-block for Omega Rarity 
                if rand == 10: 
                    return self.rarity_boost("Omega") # 1/1000 * 1/10 * 1/10 = 1 in 100,000 (0.001%)
                
                return self.rarity_boost("Ultra") # 1/1000 * 1/10 - 1/100,000 = 9 in 100,000 (0.009%)
            
            return self.rarity_boost("Legendary") # 1/1000 - 1/10,000 - 1/100,000 = 89 in 100,000 (0.089%)
        
        # if-block for Uncommon+ 
        elif rand >= 667: 
            rand = random.randint(1, 10)

            if minimum_rarity in ("Rare", "Epic"): 
                rand = 8

            # if-block for Rare+ 
            if rand > 7: 
                rand = random.randint(1, 10)

                if minimum_rarity == "Epic":
                    rand = 10

                # if-block for Epic 
                if rand == 10: 
                    return self.rarity_boost("Epic") # 1/3 * 3/10 * 1/10 = 1 in 100 (1.00%)
                
                return self.rarity_boost("Rare") # 1/3 * 3/10 - 1/100 = 9 in 100 (9.00%)
            
            return self.rarity_boost("Uncommon") # 1/3 - 1/10 - 1/100 = 67 in 300 (23.31%)
        
        # default block for Common
        else:
            # Base stats
            return self.rarity_boost("Common") # 2/3 = 2 in 3 (66.6%)
        
    def assign_rarity_weighted(
        self,
        custom_weights: Optional[List[Tuple[str, int]]] = None,
        minimum_rarity: Optional[str] = None
    ):
        """Assigns a Rarity to the Mon using weighted randomness."""

        # Valid rarity order and default weights (you can adjust these)
        default_rarity_weights = [
            ("Common", 666),     # 66.6%
            ("Uncommon", 233),   # 23.3%
            ("Rare", 90),        # 9.0%
            ("Epic", 10),        # 1.0%
            ("Legendary", 0.89), # 0.089%
            ("Ultra", 0.09),     # 0.009%
            ("Omega", 0.01)      # 0.001%
        ]

        # Use custom weights if provided
        rarity_weights = custom_weights if custom_weights else default_rarity_weights

        # Convert to dict for lookup
        weight_dict = dict(rarity_weights)

        # Filter based on minimum_rarity if given
        if minimum_rarity is not None:
            if minimum_rarity not in weight_dict:
                raise ValueError(f"Rarity '{minimum_rarity}' not found in weights.")

            # Filter to minimum and higher
            allowed = False
            filtered = []
            for rarity, weight in default_rarity_weights:
                if rarity == minimum_rarity:
                    allowed = True
                if allowed:
                    filtered.append((rarity, weight))
            rarity_weights = filtered

        # Unzip rarities and weights
        rarities, weights = zip(*rarity_weights)

        # Normalize weights to integers for random.choices if needed
        total_weight = sum(weights)
        if total_weight < 0 or any(w < 0 for w in weights):
            raise ValueError("Invalid weights: all weights must be non-negative and total must be > 0.")

        # Pick rarity
        chosen = random.choices(rarities, weights=weights, k=1)[0]

        if self.pearl is None:
            self.pearl = Mon.assign_pearl(chosen)

        return self.rarity_boost(chosen)

    @staticmethod
    def rarity_colors(rarity : str, rgb_override : List[int] = None, str_override : str = None): 
        if rarity not in Mon.rarities:
            print("Rarity not found.")
            return rarity
        
        value = Mon.rarities[rarity]

        if str_override: 
            rarity = str_override

        if rgb_override and len(rgb_override) == 3: 
            for i, v in enumerate(rgb_override): 
                if not (0 <= v <= 255):
                    inds = {0: "R", 1: "G", 2: "B"}
                    raise ValueError(f"Invalid RGB Override value: {inds[i]} - {v}")
            
            return Tools.rgb(rgb_override[0], rgb_override[1], rgb_override[2], rarity)

        if value == 2: 
            return Tools.rgb(85, 255, 0, rarity)
        elif value == 3: 
            return Tools.rgb(0, 47, 255, rarity)
        elif value == 4: 
            return Tools.rgb(255, 0, 230, rarity)
        elif value == 5: 
            return Tools.rgb(252, 169, 3, rarity)
        elif value == 6: 
            return Tools.rgb(170, 0, 255, rarity)
        elif value == 7: 
            return Tools.rgb(255, 0, 0, rarity)            
        else: 
            return rarity
        
    @staticmethod
    def assign_pearl(rarity : str):
        """Assigns a Pearl value to a Mon: 0 = None, 1 = White, 2 = Black."""

        #print(f"{rarity}")

        if rarity not in Mon.rarities:
            raise ValueError(f"[Error] Invalid rarity: {rarity}")

        # Define weighted chances for each rarity
        rarities_pearl_weights = {
            "Common":                        (1 / 256, 1 / 1024),
            ("Uncommon", "Rare"):           (1 / 128, 1 / 512),
            "Epic":                         (1 / 32, 1 / 128),
            ("Legendary", "Ultra", "Omega"): (1 / 8, 1 / 16),
        }

        # Default to no pearl
        pearl = 0

        for rarity_group, (white_chance, black_chance) in rarities_pearl_weights.items():
            # Support for both single string and tuple of strings
            if isinstance(rarity_group, str):
                rarities = [rarity_group]
            else:
                rarities = rarity_group

            if rarity in rarities:
                if random.random() < black_chance:
                    pearl = 2  # Black
                elif random.random() < white_chance:
                    pearl = 1  # White

                return pearl  

    @staticmethod
    def pearlize(color : str, 
                 base_weight : float = 0.5,
                 midtone_weight : float = 0.1,
                 prefix : str = "IRIDESCENT ", 
                 short_hand : bool = False):
        """Generates a Pearlized prefix for a Mon for base colors 'White' or 'Black'."""

        """
        # previous shorthand
        if short_hand:
            rgb = [255, 255, 255] if color == "White" else [20, 20, 20]
            Tools.text("P ", rgb=rgb)
            return
        """
        if short_hand:
            rgb = [255, 255, 255] if color == "White" else [20, 20, 20]
            Tools.text(f"{color[0]}P ", rgb=rgb)
            return

        ## For White: 
        # base color    (50%)   : white (255, 255, 255) - 50%
        # midtone       (40%)   : assign 1 RBG value to 255, assign 1 value to 130, and last any 130-255 
        # highlight     (10%)   : assign 1 RGB value to zero, others any 0-255
        # iterate over string "IRIDESCENT" with Tools.text(f"{character}", rgb=[R,G,B])
        # alternating between base color and either midtone / highlight

        ## For Black:
        # base color    (50%)   : black (0, 0, 0) - 50%
        # midtone       (40%)   : assign 1 RBG value to 74, assign 1 RGB value to 37, and last any 37-74 
        # highlight     (10%)   : assign 1 RGB value to zero, others any 0-255
        # iterate over string "IRIDESCENT" with Tools.text(f"{character}", rgb=[R,G,B])
        # alternating between base color and either midtone / highlight

        def get_white_accent():
            rand = random.random()
            if rand < midtone_weight:  # Midtone (40%)
                indices = [0, 1, 2]
                random.shuffle(indices)
                rgb = [0, 0, 0]
                rgb[indices[0]] = 255
                rgb[indices[1]] = 170
                rgb[indices[2]] = random.randint(170, 255)
                return rgb
            else:  # Highlight (10%)
                zero_idx = random.randint(0, 2)
                rgb = [random.randint(0, 255) for _ in range(3)]
                rgb[zero_idx] = 0
                return rgb

        def get_black_accent():
            rand = random.random()
            if rand < midtone_weight:  # Midtone (40%)
                indices = [0, 1, 2]
                random.shuffle(indices)
                rgb = [0, 0, 0]
                rgb[indices[0]] = 74
                rgb[indices[1]] = 37
                rgb[indices[2]] = random.randint(37, 74)
                return rgb
            else:  # Highlight (10%)
                zero_idx = random.randint(0, 2)
                rgb = [random.randint(0, 255) for _ in range(3)]
                rgb[zero_idx] = 0
                return rgb

        get_accent = get_white_accent if color == "White" else get_black_accent
        base_rgb = [255, 255, 255] if color == "White" else [0, 0, 0]
        start_with_base = random.choice([True, False])

        # Alternate between base and accent
        for i, char in enumerate(prefix):
            use_base = (i % 2 == 0) if start_with_base else (i % 2 != 0)
            rgb = base_rgb if use_base else get_accent()
            Tools.text(f"{char}", rgb=rgb)

        ### the Lord God Jesus Christ is my shepherd. John 8:34, Job 1:12, 2 Chronicles 15:2b ###
        #print() # no new line?

    @staticmethod
    def assign_random_level(max_level: int = 100, bias_factor: float = 0.5) -> int:
        """
        Assigns a random starting level to a Mon, skewed toward lower levels.
        
        Parameter:
        - max_level: The highest possible level (default: 100)
        - bias_factor: A multiplier that shifts distribution slightly higher (default: 1.0)
        
        Returns:
        - An integer level between 1 and max_level (inclusive).
        """

        levels = list(range(1, max_level + 1))

        # Generate skewed weights: higher weights for lower levels
        # Weight formula: weight = (max_level - level + 1) ** skew_strength
        skew_strength = 2.5  # Higher = more skew toward level 1
        weights = [(max_level - lvl + 1) ** skew_strength for lvl in levels]

        # Apply optional bias toward higher levels
        if bias_factor != 1.0:
            weights = [w * (lvl ** (bias_factor - 1)) for w, lvl in zip(weights, levels)]

        chosen_level = random.choices(levels, weights=weights, k=1)[0]
        return chosen_level

    def adjust_level(self, new_level : int, verbose : bool = True): 
        """A method to adjust a Mon's level and corresponding stats from an input number of levels."""
        
        _num_levels = new_level - self.level

        if _num_levels == 0 and self.leveled == False:
            self.leveled = True
        #Tools.text(f"[DEBUG] {new_level} {self.level}\n", rgb=[255,0,0])
        for _ in range(_num_levels):
            #Tools.text(f"[DEBUG] {self.experience} {self.experience_needed}\n", rgb=[255,0,0])
            xp_to_next = self.experience_needed
            self.add_experience(xp_to_next, verbose=verbose)

    def level_up(self, recursed_levels : Optional[int] = None, verbose : bool = True): 
        """A method to level-up a Mon, if possible, and adjust stats accordingly."""

        # instantiate the recursive count
        if recursed_levels is None:
            recursed_levels = 0

        if self.experience < self.experience_needed: 
            if verbose and recursed_levels > 0:
                if recursed_levels == 1:
                    print(f"{self.name} leveled up!\n")
                else:
                    print(f"{self.name} leveled up {recursed_levels} times!\n")

            if self.leveled == False:
                self.leveled = True
                #print(f"self.leveled set to {self.leveled}")
            return
            
        self.level += 1 # increase level
        self.experience -= self.experience_needed # deduct needed experience from the total amount
        self.experience_needed += int(self.experience_needed * 0.05) # adjust needed experience for next level 
        self.experience_needed = Tools.ceil_to_nearest(self.experience_needed, 5)  

        #print(f"PEARL IN LEVEL_UP {self.pearl}")

        # update stats
        if self.pearl == 0:
            self.max_health += int(self.max_health * 0.01)
        elif self.pearl == 1:
            self.max_health += int(self.max_health * 0.01125)
        elif self.pearl == 2:
            self.max_health += int(self.max_health * 0.0125)
        if self.health > 0: # restore health, if alive
            self.health = self.max_health
        if self.level % 5 == 0:
            if self.pearl == 0:
                self.defense += 1
            elif self.pearl == 1:
                self.defense += 2
            elif self.pearl == 2:
                self.defense += 3
        if self.pearl == 0:
            self.max_stamina += int(self.max_stamina * 0.01)
        elif self.pearl == 1:
            self.max_stamina += int(self.max_stamina * 0.01125)
        elif self.pearl == 2:
            self.max_stamina += int(self.max_stamina * 0.0125)
        if self.stamina > 0: # restore stamina, if conscious
            self.stamina = self.max_stamina
        if self.level % 20 == 0:
            self.learn_move(verbose=verbose)
        if self.pearl == 0:
            if self.perfect:
                atk_boost_incr = Mon.assign_attack_boost(dist=True, min_val=0.051, max_val=0.051, bias=0.08, squish=0.005)
            else:
                atk_boost_incr = Mon.assign_attack_boost(dist=True, min_val=0.00, max_val=0.051, bias=0.08, squish=0.005)
        elif self.pearl == 1:
            if self.perfect:
                atk_boost_incr = Mon.assign_attack_boost(dist=True, min_val=0.051, max_val=0.051, bias=0.15, squish=0.012)
            else:
                atk_boost_incr = Mon.assign_attack_boost(dist=True, min_val=0.00, max_val=0.051, bias=0.15, squish=0.012)
        elif self.pearl == 2:
            if self.perfect:
                atk_boost_incr = Mon.assign_attack_boost(dist=True, min_val=0.051, max_val=0.051, bias=0.21, squish=0.019)
            else:
                atk_boost_incr = Mon.assign_attack_boost(dist=True, min_val=0.00, max_val=0.051, bias=0.21, squish=0.019)
        atk_boost_incr = Tools.floor_to_nearest_float(atk_boost_incr, 0.01)
        self.attack_boost += atk_boost_incr
        self.attack_boost = Tools.floor_to_nearest_float(self.attack_boost, 0.01)

        # increase recursive level counter for printing
        recursed_levels += 1
        self.level_up(recursed_levels, verbose=verbose) # recursively call for remaining levels

    def add_experience(self, points : int, verbose : bool = True):
        """A method to add experience points to a Mon and automatically check if the Mon can level up."""

        self.experience += points
        self.level_up(verbose=verbose)

    def ai_move_choice(self, opponent: Mon, verbose : bool = False) -> int:
        """Selects the best Move index to use against the opponent, based on conditions like damage output, status, and type matchups."""

        # Classify moves
        dmg_inds = []
        hl_inds = []
        spc_inds = []
        stn_inds = []

        for i, mv in enumerate(self.moves):
            dmg = mv.damage_output(include_damaging_effects=True, attack_boost=self.attack_boost)
            heal = mv.damage_output(include_healing_effects=True)

            if dmg > 0:
                dmg_inds.append((i, dmg))
            elif heal < 0:
                hl_inds.append((i, heal))  # healing = negative damage

            for efct in mv.effects:
                if "stun" in efct.effect_type:
                    stn_inds.append(i)
                elif any(t in efct.effect_type for t in ("buff", "debuff", "damage-reflection")) and dmg == 0:
                    spc_inds.append(i)

        # Sort dmg and heal by magnitude
        dmg_inds.sort(key=lambda x: x[1], reverse=True)
        hl_inds.sort(key=lambda x: x[1])  # More negative = stronger heal

        # === ONE-SHOT CHECK ===
        for i, mv in enumerate(self.moves):
            base_dmg = mv.damage_output(include_damaging_effects=True, attack_boost=self.attack_boost)

            multiplier = 1.0
            for mv_tp in mv.move_types:
                for opp_tp in opponent.type:
                    if mv_tp.is_strong_against(opp_tp):
                        multiplier *= 2
                    elif mv_tp.is_weak_against(opp_tp):
                        multiplier *= 0.33

            potential_dmg = base_dmg * multiplier - opponent.defense
            if potential_dmg >= opponent.health:
                if verbose:
                    print(f"{self.name} went for a one-shot kill!")
                return i

        # === PRIORITIZE SELF CONDITIONS ===
        if hl_inds and self.health < self.max_health * 0.5:
            if verbose:
                print(f"{self.name} tried to heal!")
            return hl_inds[0][0]

        if any("buff" in e.effect_type for e in self.effects):
            if verbose:
                print(f"{self.name} went for a buffed damager!")
            return dmg_inds[0][0] if dmg_inds else 0
        ## requires more robust move classification
        #elif any("debuff" in e.effect_type for e in opponent.effects):
        #    if verbose:
        #        print(f"{self.name} went for a damager paired with debuff!")
        #    return dmg_inds[0][0] if dmg_inds else 0

        # === CHECK OPPONENT CONDITIONS ===
        opp_stunned = any("stun" in e.effect_type for e in opponent.effects)

        if opp_stunned:
            if spc_inds:
                if verbose:
                    print(f"Opponent stunned! {self.name} went for a special move!")
                return spc_inds[0]
            elif dmg_inds:
                if verbose:
                    print(f"Opponent stunned but no special. {self.name} went for a damager!")
                return dmg_inds[0][0]
        else:
            if stn_inds:
                if verbose:
                    print(f"Opponent not stunned. {self.name} went for a stun move!")
                return stn_inds[0]
            elif spc_inds:
                if verbose:
                    print(f"Opponent not stunned, no stun moves. {self.name} went for a special move!")
                return spc_inds[0]
            elif dmg_inds:
                if verbose:
                    print(f"Opponent not stunned, no stun moves, no special. {self.name} went for a damager!")
                return dmg_inds[0][0]

        # === FAILSAFE ===
        if verbose:
            print(f"Failsafe. Random move selected!")
        return None # default to None for handling in battle()

    def battle(self,
               opponent : Mon, 
               attacker_use_move : Move = None, 
               is_random : bool = True, 
               typewriter_delay : float = 0.05, 
               timing : float = 0.5, 
               apply_experience : bool = True, 
               verbose : bool = True, 
               use_self_ai : bool = False, 
               use_opp_ai : bool = False
               ): 
        """
        A method to simulate a battle between the Mon and another input Mon. Returns a Tuple with bools: (Win/Loss/Draw, Leveled_Up)
        """
        
        leveled_up_during_battle = False
        self_start_level = self.level
        
        if self.health <= 0 or self.stamina <= 0 or opponent.health <= 0 or opponent.stamina <= 0: 
            raise ValueError(f"[ERROR] Could not meet Battle pre-conditions: Living, conscious Mons --\n\t{self.name} - [HP: ({self.health} / {self.max_health}) | STM: ({self.stamina} / {self.max_stamina})]\n\t{opponent.name} - ({opponent.health} / {opponent.max_health}) | STM: ({opponent.stamina} / {opponent.max_stamina})]")

        if verbose:
            print(f"Battle begins: {self.name} vs {opponent.name}!")

        first, second = (self, opponent) if random.randint(1, 2) == 1 else (opponent, self)

        round_num = 1
        while self.health > 0 and opponent.health > 0 and self.stamina > 0 and opponent.stamina > 0:
            if verbose:
                Tools.text(f"--- Round {round_num} ---\n\n", typewriter_delay)
            for attacker, defender in [(first, second), (second, first)]:
                if verbose:
                    for _m_ in (attacker, defender):
                        def_str = f"{_m_.defense} / {_m_.defense * 2}" if any(efct.name == "Defense Debuff" for efct in _m_.effects) else f"{_m_.defense}"
                        Tools.text((Mon.rarity_colors(_m_.rarity, rgb_override=[255, 145, 40], str_override="Perf "))) if _m_.perfect else ""
                        Mon.pearlize(Mon.pearls[_m_.pearl].split()[0], short_hand=True) if _m_.pearl else None
                        Tools.text(f"{_m_.name:>25} ", params=Mon.rarity_effects[_m_.rarity])
                        Tools.text(f"(L{_m_.level}) - [DF: {def_str:<10} | HP: ({_m_.health} / {_m_.max_health}) | STM: ({_m_.stamina} / {_m_.max_stamina})]\n", typewriter_delay)
                    print()

                # defender.trigger_effects(trigger_event="on_round_start") will need checks?
                if attacker.health <= 0 or attacker.stamina <= 0:
                    continue  # attacker is out of the fight
                if defender.health <= 0 or defender.stamina <= 0:
                    continue

                if any(t.lower() == "stun" for e in attacker.effects for t in e.effect_type):
                    if verbose:
                        Tools.text(f"{attacker.name} is stunned and can't act this turn!\n\n", typewriter_delay)
                    continue

                if hasattr(attacker, "abilities"):
                    if any(t.lower() == "quick-draw" for a in attacker.abilities for t in a.effect_type):
                        if verbose:
                            Tools.text(f"Quick Draw granted {attacker.name} another chance to attack!\n\n", typewriter_delay)
                        continue

                if verbose:
                    time.sleep(timing)

                if not is_random and attacker == self:
                    inp = -1

                    while True:
                        Tools.text(f"Select a Move for {self.name}:\n", typewriter_delay)

                        for i, mv in enumerate(attacker.moves):
                            print(f"{i + 1} : {mv}")  # Show 1-based options

                        try:
                            inp = int(input("Enter move number: "))
                            if 1 <= inp <= len(attacker.moves):  # Valid 1-based input
                                break
                            else:
                                Tools.text("Invalid move. Try again.\n\n")
                        except ValueError:
                            Tools.text("Please enter a number.\n\n")

                    move = attacker.moves[inp - 1]
                elif attacker == self and attacker_use_move: # move is from input
                    if attacker_use_move not in self.moves:
                        raise ValueError(f"[Error] Parameter 'attacker_use_move' must be one of self's (Mon Name: {self.name}) Moves.")
                    
                    move = attacker_use_move

                elif (attacker == self and use_self_ai) or (attacker != self and use_opp_ai): # move is AI orr andom
                    move_ind = attacker.ai_move_choice(defender, verbose=verbose) # verbose strictly for debugging
                    if move_ind is not None:
                        move = attacker.moves[move_ind]
                    else:
                        move = random.choice(attacker.moves)
                else: # move is random
                    move = random.choice(attacker.moves)
                
                # i think we can just add a check here for attacker.effects == stunned? if stunned, then continue? attacker gets turn skipped?
                move.use(attacker, defender, typewriter_delay, timing, verbose=verbose) 
                attacker.trigger_effects(trigger_event="on_hit", verbose=verbose)
                defender.trigger_effects(trigger_event="on_hit", verbose=verbose) # optionally add return to trigger_effects() for interactivity?
                                                                # e.g., "{defender.name} succumbed to {killing_effect}"
                
                #attacker.print_effects()
                #defender.print_effects()

                attacker.update_effects(verbose=verbose)
                defender.update_effects(verbose=verbose)
                
                #attacker.print_effects()
                #defender.print_effects()
                                    
                if verbose:
                    print()
                    time.sleep(timing)

                if attacker.health <= 0 and defender.health <= 0:
                    if verbose:
                        Tools.text(f"\n{attacker.name} and {defender.name} have both perished...\n", typewriter_delay)
                        Tools.text(f"Draw...\n\n", typewriter_delay)

                    if self.level > self_start_level:
                        leveled_up_during_battle = True

                    Mon.finalize_battle(attacker, defender, round_num, apply_experience=apply_experience, verbose=verbose)

                    return None, leveled_up_during_battle

                if defender.health <= 0:
                    if attacker.stamina <= 0:
                        attacker.stamina = 1 # prevent faulty categorizing
                    if verbose:
                        Tools.text(f"\n{defender.name} has perished...\n", typewriter_delay)
                        Tools.text(f"{attacker.name} wins the battle!\n\n", typewriter_delay)
                    
                    Mon.finalize_battle(attacker, defender, round_num, apply_experience=apply_experience, verbose=verbose)

                    if self.level > self_start_level:
                        leveled_up_during_battle = True

                    # Tools.text(f"[DEBUG] {self.name} level: {self.level} (started at {self_start_level})\n\n", rgb=[255,0,0])

                    return self == attacker, leveled_up_during_battle # round_num # attacker.name
                
                if attacker.health <= 0: 
                    if verbose:
                        Tools.text(f"\n{attacker.name} has killed itself in its struggle...\n", typewriter_delay)
                        Tools.text(f"{defender.name} wins the battle!\n\n", typewriter_delay)
                    
                    Mon.finalize_battle(attacker, defender, round_num, apply_experience=apply_experience, verbose=verbose)

                    if self.level > self_start_level:
                        leveled_up_during_battle = True

                    # Tools.text(f"[DEBUG] {self.name} level: {self.level} (started at {self_start_level})\n\n", rgb=[255,0,0])

                    return self == defender, leveled_up_during_battle # round_num # defender.name
                
                if attacker.stamina <= 0:
                    if verbose:
                        Tools.text(f"\n{attacker.name} has fainted...\n", typewriter_delay)
                        Tools.text(f"{defender.name} wins the battle!\n\n", typewriter_delay)
                    
                    Mon.finalize_battle(defender, attacker, round_num, apply_experience=apply_experience, verbose=verbose)

                    if self.level > self_start_level:
                        leveled_up_during_battle = True

                    # Tools.text(f"[DEBUG] {self.name} level: {self.level} (started at {self_start_level})\n\n", rgb=[255,0,0])

                    return self == defender, leveled_up_during_battle # round_num # defender.name
                
            round_num += 1

        print("⚠️ Battle ended with an unexpected state.")
        return round_num # None

    @staticmethod
    def finalize_battle(mon1: Mon, mon2: Mon, num_rounds: int, apply_experience : bool = True, verbose: bool = True):
        """Finalizes battle results. Applies win/loss or draw logic based on Mon health and stamina."""

        # Corrected outcome checks to include both health and stamina
        mon1_defeated = mon1.health <= 0 or mon1.stamina <= 0
        mon2_defeated = mon2.health <= 0 or mon2.stamina <= 0

        # Clear effects
        mon1.clear_effects(verbose=verbose)
        mon2.clear_effects(verbose=verbose)

        # Log battle info
        mon1.record_battle_log(mon2, num_rounds)
        mon2.record_battle_log(mon1, num_rounds)

        # Restore stamina
        mon1.restore_stamina()
        mon2.restore_stamina()

        def calc_xp_multiplier(mon, opponent):
            # Rarity multiplier — reward if opponent's rarity is higher
            rarity_diff = Mon.rarities[opponent.rarity] / Mon.rarities[mon.rarity]

            # Level multiplier — >1 if opponent is higher level, <1 if weaker
            level_diff = (opponent.level - mon.level) / 10
            level_multiplier = 1 + max(level_diff, -0.9)  # never drop below 0.1x

            return rarity_diff * level_multiplier

        # Usage inside battle resolution
        if mon1_defeated and mon2_defeated:
            # Draw — base XP reduced
            xp1 = 25 * calc_xp_multiplier(mon1, mon2)
            xp2 = 25 * calc_xp_multiplier(mon2, mon1)
            if apply_experience:
                mon1.add_experience(xp1, verbose=verbose)
                mon2.add_experience(xp2, verbose=verbose)
            mon1.battles += 1
            mon2.battles += 1
        else:
            winner, loser = (mon1, mon2) if not mon1_defeated else (mon2, mon1)
            xp_winner = 100 * calc_xp_multiplier(winner, loser)
            xp_loser = 25 * calc_xp_multiplier(loser, winner)

            if apply_experience:
                winner.add_experience(xp_winner, verbose=verbose)
                loser.add_experience(xp_loser, verbose=verbose)

            winner.battles += 1
            winner.wins += 1
            loser.battles += 1

    def record_battle_log(self, opponent: Mon, num_rounds: int):
        """Logs battle summary with opponent info, move names, and outcome (based on health and stamina)."""

        winrate = f"{(opponent.wins / opponent.battles * 100):.1f}%" if opponent.battles > 0 else "N/A"
        move_names = ", ".join(mv.name for mv in opponent.moves)

        self_defeated = self.health <= 0 or self.stamina <= 0
        opp_defeated = opponent.health <= 0 or opponent.stamina <= 0

        outcome = "XXX"

        if not self_defeated and opp_defeated:
            outcome = "Win"
        elif self_defeated and not opp_defeated:
            outcome = "Loss"
        elif self_defeated and opp_defeated:
            outcome = "Draw"

        entry = (
            f"VS {opponent.name} ({winrate}) | "
            f"{opponent.rarity}, LVL {opponent.level} | "
            f"Moves: {move_names} | "
            f"Outcome: {outcome} in {num_rounds} rounds"
        )
        #print(f"{outcome} SD:{self_defeated} SH{self.health} SS{self.stamina} ||| OD{opp_defeated} OH{opponent.health} OS{opponent.stamina}")
        self.battle_log.append(entry)

    def sim_battle_stats(self, opponent : Mon, num_sims : int = 100):
        """Simulates Battles between the Mon and a specified Opponent to calculate their likelihood of winning."""

        self_copy = deepcopy(self)
        opp_copy = deepcopy(opponent)

        wins = 0
        losses = 0
        draws = 0

        for _ in range(num_sims):
            self_copy.health = self_copy.max_health
            opp_copy.health = opp_copy.max_health

            outcome, _ = self_copy.battle(opp_copy, typewriter_delay=0, timing=0, verbose=False, apply_experience=False, use_self_ai=True, use_opp_ai=True)

            if outcome == True:
                wins += 1
            elif outcome == False:
                losses += 1
            elif outcome is None:
                draws += 1

        print(f"{self.name} has a {(wins / num_sims):.2%} chance of winning against {opponent.name}")
        print(f"Wins: {wins} / {num_sims} ({(wins / num_sims):.2%})")
        print(f"Losses: {losses} / {num_sims} ({(losses / num_sims):.2%})")
        print(f"Draws: {draws} / {num_sims} ({(draws / num_sims):.2%})\n")

        return wins / num_sims, losses / num_sims, draws / num_sims

    def restore_stamina(self):
        """Restores a Mon's stamina to max."""

        self.stamina = self.max_stamina

    def restore_health(self):
        """Restores a Mon's health to max."""

        self.health = self.max_health

    def clear_effects(self, verbose : bool = True): 
        """Fully clears all active effects and restores previous values."""

        # === Restore Mon attributes ===
        for attr, original_val in self.original_values.items():
            if hasattr(self, attr):
                setattr(self, attr, original_val)
                if verbose:
                    print(f"All effects cleared — {self.name}'s {attr} restored to {original_val}")
            else:
                if verbose:
                    print(f"[Warning] Mon has no attribute '{attr}' to restore")

        # === Restore Move attributes ===
        for attr, move_restore_map in self.original_move_values.items():
            for move in self.moves:
                if move.name in move_restore_map:
                    prev_val = move_restore_map[move.name]
                    setattr(move, attr, prev_val)

                    if verbose:
                        val_str = f"{prev_val:.1%}" if attr == "accuracy" and isinstance(prev_val, (int, float)) else str(prev_val)
                        print(f"All effects cleared — {self.name}'s {attr} on '{move.name}' restored to {val_str}")

        # Clear all effects and original values
        self.effects.clear()
        self.original_values.clear()
        self.original_move_values.clear()

    def update_effects(self, verbose : bool = True): 
        """Decrements a Mon's currently active Effects' durations, if any."""

        expired_effects = []

        for effect in self.effects:
            effect.duration_remaining -= 1
            if effect.duration_remaining <= 0:
                expired_effects.append(effect)

        for effect in expired_effects:
            self.effects.remove(effect)

            for i in range(len(effect.effect_type)):
                etype = effect.effect_type[i]
                ttype = effect.target_type[i]

                if not isinstance(effect.target_attribute, list) or i >= len(effect.target_attribute):
                    if verbose:
                        print(f"[Warning] Effect '{effect.name}' missing target_attribute at index {i}")
                    continue

                attr = effect.target_attribute[i]
                if not isinstance(attr, str):
                    if verbose:
                        print(f"[Warning] Invalid attribute type in '{effect.name}': {type(attr)}")
                    continue

                # print EFFECT INSTANCE 
                """PRINT EFFECT INSTANCE"""

                # Check if any remaining effect still modifies this attribute
                still_active = any(
                    t == ttype and a == attr
                    for e in self.effects
                    if isinstance(e.target_type, list) and isinstance(e.target_attribute, list)
                    for t, a in zip(e.target_type, e.target_attribute)
                )
                if still_active:
                    continue  # Don't restore yet

                # === Restore Mon attributes ===
                if ttype == "Mon":
                    if attr in self.original_values:
                        original_val = self.original_values.pop(attr)
                        setattr(self, attr, original_val)
                        if verbose:
                            print(f"{effect.name} wears off — {self.name}'s {attr} returns to {original_val}")
                    else:
                        if verbose:
                            print(f"[Warning] No original value stored for {attr} on Mon '{self.name}'")

                # === Restore Move attributes ===
                elif ttype == "Move":
                    if attr in self.original_move_values:
                        move_restore_map = self.original_move_values.pop(attr)
                        for move in self.moves:
                            if move.name in move_restore_map:
                                prev_val = move_restore_map[move.name]
                                setattr(move, attr, prev_val)
                                if verbose:
                                    val_str = f"{prev_val:.1%}" if attr == "accuracy" and isinstance(prev_val, (int, float)) else str(prev_val)
                                    print(f"{effect.name} wears off — {self.name}'s {attr} on '{move.name}' returns to {val_str}")
                    else:
                        if verbose:
                            print(f"[Warning] No original move value stored for {attr} on Mon '{self.name}'")

    def trigger_effects(self, trigger_event: str, verbose : bool = True):  
        """
        Triggers any currently active Effects on this Mon that match the given trigger event.
        Intended to be called at key times like 'on_hit', 'on_round_start', etc.
        """
        # Group chip-damage effects by name
        chip_groups = {}

        for effect in self.effects:
            if effect.trigger != trigger_event:
                continue

            # Loop through all effect components
            for i in range(len(effect.effect_type)):
                etype = effect.effect_type[i]
                ttype = effect.target_type[i]
                tself = effect.target_self[i]
                attr = effect.target_attribute[i]
                val = effect.value[i]
                stack = effect.stackable[i]

                # --- CHIP DAMAGE EFFECTS ---
                if etype in ("chip-damage", "diminishing-chip-damage", "chip-stamina", "chip-heal") and ttype == "Mon":
                    if etype == "diminishing-chip-damage": 
                        elapsed_turns = max(0, effect.duration - effect.duration_remaining)
                        val /= (2 ** elapsed_turns)
                    chip_groups.setdefault(effect.name, []).append((etype, Tools.ceil_to_nearest(val, 1)))
                    continue

                # --- DEBUFF TARGETING MOVES ---
                if etype in ("debuff", "buff") and ttype == "Move":
                    if not stack and effect.triggered:
                        continue

                    for move in self.moves:
                        if hasattr(move, attr):
                            old_val = getattr(move, attr)

                            if attr == "accuracy":
                                new_val = max(0.0, min(old_val * (1 + val), 1.0))
                                if verbose:
                                    verb_str = "lowers" if new_val <= old_val else "raises"
                                    print(f"{effect.name} {verb_str} {self.name}'s {attr} on '{move.name}' from {old_val:.1%} to {new_val:.1%}!")
                            elif attr == "iterations":
                                new_val = old_val + val
                                if verbose:
                                    verb_str = "lowers" if new_val <= old_val else "raises"
                                    print(f"{effect.name} {verb_str} {self.name}'s {attr} on '{move.name}' from {old_val} to {new_val}!")
                            else:
                                new_val = max(0, int(old_val * (1 + val)))
                                if verbose:
                                    verb_str = "lowers" if new_val <= old_val else "raises"
                                    print(f"{effect.name} {verb_str} {self.name}'s {attr} on '{move.name}' from {old_val} to {new_val}!")

                            setattr(move, attr, new_val)
                        else:
                            print(f"[Warning] Move has no attribute '{attr}' for debuff effect.")

                    # only mark the whole effect as triggered after all subeffects have been processed
                    effect.triggered = True if i == len(effect.effect_type) - 1 else False
                    continue

                # --- DEBUFF TARGETING MON ---
                if etype in ("debuff", "buff") and ttype == "Mon":
                    if not stack and effect.triggered:
                        continue

                    if hasattr(self, attr):
                        old_val = getattr(self, attr)

                        if attr == "accuracy":
                            new_val = max(0.0, min(old_val * (1 + val), 1.0))
                            if verbose:
                                verb_str = "lowers" if new_val <= old_val else "raises"
                                print(f"{effect.name} {verb_str} {self.name}'s {attr} from {old_val:.1%} to {new_val:.1%}!")
                        else:
                            new_val = max(0, int(old_val * (1 + val)))
                            if verbose:
                                verb_str = "lowers" if new_val <= old_val else "raises"
                                print(f"{effect.name} {verb_str} {self.name}'s {attr} from {old_val} to {new_val}!")

                        setattr(self, attr, new_val)
                    else:
                        print(f"[Warning] Mon has no attribute '{attr}' for debuff effect.")

                    # only mark the whole effect as triggered after all subeffects have been processed
                    effect.triggered = True if i == len(effect.effect_type) - 1 else False
                    continue

                # --- NON-MODIFYING EFFECTS ---
                if etype == "stun" or etype == "damage-reflection":
                    if not stack and effect.triggered:
                        continue

                    # only mark the whole effect as triggered after all subeffects have been processed
                    effect.triggered = True if i == len(effect.effect_type) - 1 else False
                    continue

                # --- DEFAULT CATCH ---
                print(f"[Warning] Unhandled effect type '{etype}' or target_type '{ttype}' in trigger_effects.")

        # Apply grouped chip effects
        for name, entries in chip_groups.items():
            damage_total = 0
            heal_total = 0
            stam_total = 0

            for etype, val in entries:
                if etype == "chip-damage" or etype == "diminishing-chip-damage":
                    damage_total += val
                elif etype == "chip-heal":
                    heal_total += val
                elif etype == "chip-stamina":
                    stam_total += val

            stack_count = len(entries)
            stack_text = f" ({stack_count} stack{'s' if stack_count > 1 else ''})"

            if damage_total != 0:
                self.health = max(0, self.health + damage_total)
                if verbose:
                    print(f"{name} deals {-(damage_total)} chip damage to {self.name}!{stack_text}")

            if heal_total != 0:
                self.health = min(self.max_health, self.health + heal_total)
                if verbose:
                    print(f"{name} restored {heal_total} health to {self.name}!{stack_text}")

            if stam_total != 0:
                verb_str = "restored" if stam_total > 0 else "drained"
                prep_str = "from" if verb_str == "drained" else "to"
                self.stamina = min(self.max_stamina, self.stamina + stam_total)
                if verbose:
                    print(f"{name} {verb_str} {abs(stam_total)} stamina {prep_str} {self.name}!{stack_text}")

    def restore_health_via_potion(self):
        """Restore a Mon's health to max via potion and grants experience to Mon."""
        if self.health == self.max_health:
            raise ValueError(f"[Error] {self.name} is already at max health!")
        
        self.health = self.max_health
        self.stamina = self.max_stamina
        self.add_experience(10) # grant 10 XP to Mon for using a potion
        
    def learn_move(self, _move : Optional[Move] = None, verbose : bool = True, move_priority : Tuple[bool, bool, bool] = (False, False, False)):
        """A method to assign a new unique move to the Mon if a Move slot is empty. May specify a Move or assign randomly via None."""

        # check if moves list is full
        if len(self.moves) >= self.moves_limit:
            if verbose: 
                print("Cannot learn new Move -- Moves list is already full.")
            return # replace_move([prompt Move replacement options] , _move)
        
        current_moves = set(self.moves)

        if _move is not None:
            if _move in current_moves:
                if verbose:
                    print(f"{self.name} already knows {_move.name}.")
                return
            self.moves.append(_move)
            if verbose:
                print(f"{self.name} has learned {_move.name}!")
            return

        # Random move learning
        attempts = 0
        added = False
        while not added and attempts < 10:
            mv = Move.choose_random_move(self, self.type, move_priority=move_priority)
            if mv and mv not in current_moves:
                self.moves.append(mv)
                if verbose:
                    print(f"{self.name} has randomly learned {mv.name}!")
                added = True
            attempts += 1

        if not added:
            if verbose:
                print(f"{self.name} failed to learn a new unique move after {attempts} attempts.")
        
    def replace_move(self, _replace : Move, _with : Optional[Move] = None): 
        """Replaces an existing Move in the Mon's moveset with another, or learns a random one if not full."""

        # Make sure the move to replace is in the current moveset
        if _replace not in self.moves:
            print(f"{self.name} does not know {_replace.name}. Cannot replace.")
            return

        # Choose a random replacement move if not provided
        if _with is None:
            _with = Move.choose_random_move(self, self.type)
            if _with is None:
                print("No suitable random move could be found.")
                return

        # Check if the Mon already knows the replacement move
        if _with in self.moves:
            print(f"{self.name} already knows {_with.name}.")
            return

        # Perform the replacement
        idx = self.moves.index(_replace)
        self.moves[idx] = _with
        print(f"{self.name} forgot {_replace.name} and learned {_with.name}!")

    def print_battle_log(self):
        """Prints the battle history of the Mon in a clean, readable format."""
        
        if not self.battle_log:
            print(f"{self.name} has no recorded battles.")
            return

        print(f"\n=== Battle Log for {self.name} ===")
        for i, entry in enumerate(self.battle_log, 1):
            print(f"Battle {i}: {entry}")

    def print_effects(self): 
        """Prints Mon's currently applied Status Effects and their impact."""
    
        if not self.effects:
            print(f"{self.name} currently has no effects.")
            return

        print(f"{self.name} is affected by the following effects:\n")

        from collections import defaultdict
        grouped_effects = defaultdict(list)

        for effect in self.effects:
            key_parts = []
            for i in range(len(effect.effect_type)):
                part = (
                    effect.effect_type[i],
                    effect.target_type[i],
                    effect.target_self[i],
                    effect.target_attribute[i],
                    effect.value[i] if isinstance(effect.value, (list, tuple)) else effect.value
                )
                key_parts.append(part)
            key = (effect.name, tuple(key_parts))
            grouped_effects[key].append(effect)

        for (effect_name, subeffects), effect_group in grouped_effects.items():
            count = len(effect_group)
            label = f"{effect_name} ×{count}" if count > 1 else effect_name

            # Print each subeffect within this effect group
            for i, sub in enumerate(subeffects):
                etype, tgt_type, tgt_self, tgt_attr, val = sub
                effect_type = etype.capitalize()
                source = "Mon" if tgt_type.lower() == "mon" else "Move"
                print(f"- {label} ({effect_type} on {source})")

                # Find representative effect instance for lookup
                representative = effect_group[0]
                prev_val = representative.previous_value or {}

                if not isinstance(tgt_attr, str):
                    print(f"    ↳ No direct attribute affected.")
                    continue

                if tgt_type.lower() == "mon":
                    current_val = getattr(self, tgt_attr, None)
                    prev_display = prev_val.get(tgt_attr) if isinstance(prev_val, dict) else prev_val
                    prev_part = f" (was {prev_display})" if prev_display is not None else ""
                    print(f"    ↳ {tgt_attr}: {current_val}{prev_part} — value: {val}")

                elif tgt_type.lower() == "move":
                    found = False
                    for move in self.moves:
                        if hasattr(move, tgt_attr):
                            current_val = getattr(move, tgt_attr)
                            prev_display = None
                            if isinstance(prev_val, dict):
                                attr_dict = prev_val.get(tgt_attr, {})
                                if isinstance(attr_dict, dict):
                                    prev_display = attr_dict.get(move.name)
                            prev_part = f" (was {prev_display})" if prev_display is not None else ""
                            print(f"    ↳ Move '{move.name}' — {tgt_attr}: {current_val}{prev_part} — value: {val}")
                            found = True
                    if not found:
                        print(f"    ↳ No Move attribute '{tgt_attr}' found in any move.")

        print()

    def name_str(self) -> str:
        """Returns colored string of Mon name, Perfect, and Pearl status."""

        perf_str = Mon.rarity_colors(self.rarity, rgb_override=[255, 145, 40], str_override="Perf ") if self.perfect else ""
        pearl_color = [255, 255, 255] if self.pearl == 1 else [20, 20, 20]
        pearl_str = Mon.rarity_colors(self.rarity, rgb_override=pearl_color, str_override=Mon.pearls[self.pearl]+" ") if self.pearl >= 1 else ""

        return (
            f"{perf_str}{pearl_str}"
            f"{Mon.rarity_colors(self.rarity, str_override=self.name)} "
        )
        
class Type: 
    """A class to define Mon Type Classes and Subclasses."""

    # Type Classes & Subclasses are defined to determine a Mon's Moveset. More info in the Move Class.

    types = [
        "Air",
        {"Air", "Earth"},
        {"Air", "Fire"},
        {"Air", "Water"},
        "Beast",
        "Demon (Sub: Magic)",
        {"Demon (Sub: Magic)", "Fire"},
        "Earth", 
        {"Earth", "Fire"}, 
        {"Earth", "Magic"}, 
        "Electric",
        "Explosion (Sub: Fire)", 
        "Fire", 
        {"Fire", "Water"},
        "Holy (Sub: Magic)",
        "Ice (Sub: Water)", 
        "Magic",
        "Metal (Sub: Earth)",
        "Nature",
        "Reptilian (Sub: Beast)", 
        "Water"
    ]

    weak_against = {
        # entry : types it's weak against
        "Air"                       : {"Air"},
        #{"Air", "Earth"}            : {},
        #{"Air", "Fire"}             : {},
        #{"Air", "Water"}            : {},
        "Beast"                     : {"Earth", "Air", "Metal (Sub: Earth)"},
        "Demon (Sub: Magic)"        : {"Holy"},
        "Earth"                     : {"Air", "Water"}, 
        #{"Earth", "Fire"}           : {}, 
        #{"Earth", "Magic"}          : {}, 
        "Electric"                  : {"Earth", "Electric"},
        "Explosion (Sub: Fire)"     : {"Explosion (Sub: Fire)", "Fire", "Water", "Metal (Sub: Earth)"}, 
        "Fire"                      : {"Earth", "Explosion (Sub: Fire)", "Fire", "Water"}, 
        #{"Fire", "Water"}           : {},
        "Holy (Sub: Magic)"         : {"Holy (Sub: Magic)"},
        "Ice (Sub: Water)"          : {"Fire", "Ice (Sub: Water)"}, 
        #"Magic"                     : {},
        "Metal (Sub: Earth)"        : {"Fire", "Explosion (Sub: Fire)"},
        "Nature"                    : {"Fire", "Explosion (Sub: Fire)", "Metal (Sub: Earth)"},
        "Reptilian (Sub: Beast)"    : {"Earth", "Air", "Metal (Sub: Earth)"}, 
        "Water"                     : {"Nature", "Metal (Sub: Earth)"}
    }

    strong_against = {
        # entry                     : type it's strong against
        "Air"                       : {"Fire", "Nature"},
        #{"Air", "Earth"}            : {},
        #{"Air", "Fire"}             : {},
        #{"Air", "Water"}            : {},
        "Beast"                     : {"Beast", "Reptilian (Sub: Beast)"},
        "Demon (Sub: Magic)"        : {"Magic"},
        "Earth"                     : {"Fire", "Electric", "Ice (Sub: Water)"}, 
        #{"Earth", "Fire"}           : {},
        #{"Earth", "Magic"}          : {},
        "Electric"                  : {"Nature", "Air", "Water", "Metal (Sub: Earth)"},
        "Explosion (Sub: Fire)"     : {"Earth", "Ice (Sub: Water)", "Nature"}, 
        "Fire"                      : {"Air", "Ice (Sub: Water)", "Nature", "Metal (Sub: Earth)"}, 
        #{"Fire", "Water"}           : {"Ice", "Water"},
        "Holy (Sub: Magic)"         : {"Demon (Sub: Magic)"},
        "Ice (Sub: Water)"          : {"Reptilian (Sub: Beast)", "Nature", "Beast"}, 
        "Magic"                     : {"Beast", "Holy (Sub: Magic)", "Reptilian (Sub: Beast)"},
        "Metal (Sub: Earth)"        : {"Earth", "Ice (Sub: Water)"},
        "Nature"                    : {"Water", "Earth", "Demon (Sub: Magic)"}, # Nature feeds off of water, penetrates earth, and has a deep-"seeded" (pun) hatred against demon
        "Reptilian (Sub: Beast)"    : {"Beast", "Reptilian (Sub: Beast)"}, 
        "Water"                     : {"Earth", "Explosion (Sub: Fire)", "Fire"}
    }

    type_biomes = {
        "Forest"            : {("Nature", 0.56), 
                               ("Earth", 0.26), 
                               ("Water", 0.1), 
                               ("Beast", 0.05),
                               ("Reptilian (Sub: Beast)", 0.03)}, 
        "Water Body"        : {("Water", 0.85), 
                               ("Ice (Sub: Water)", 0.07), 
                               ("Reptilian (Sub: Beast)", 0.05), 
                               ("Beast", 0.03)}, 
        "Enchanted Forest"  : {("Nature", 0.51), 
                               ("Earth", 0.2), 
                               ("Magic", 0.13),
                               ("Water", 0.05), 
                               ("Demon (Sub: Magic)", 0.04),
                               ("Holy (Sub: Magic)", 0.03),
                               ("Beast", 0.03),
                               ("Reptilian (Sub: Beast)", 0.01)},
        "Volcano"           : {("Fire", 0.33), 
                               ("Earth", 0.33),
                               ("Explosion (Sub: Fire)", 0.33)},
        "Swamp"             : {("Water", 0.45), 
                               ("Reptilian (Sub: Beast)", 0.25),
                               ("Earth", 0.30)}
    }

    def __init__(self, par : str, sub : str):
        self.parent_class = par # required
        self.subclass = sub # may be None

    def __str__(self):
        return f"{self.subclass} (Sub: {self.parent_class})" if self.subclass else f"{self.parent_class}"
    
    def __eq__(self, other : Type) -> bool:
        if not isinstance(other, Type):
            return NotImplemented
        return (
            self.parent_class == other.parent_class and
            self.subclass == other.subclass
        )
    
    @staticmethod
    def parse(type_str: str) -> Type:
        """Parses a type string like 'Explosion (Sub: Fire)' into a Type object."""
        match = re.match(r"(.+?) \(Sub: (.+?)\)", type_str)
        if match:
            subclass = match.group(1).strip()
            parent = match.group(2).strip()
            return Type(parent, subclass)
        else:
            return Type(type_str.strip(), None)

    def is_weak_against(self, target_type: Type):
        """Returns True if this Type is weak against the input Type."""
        self_str = str(self)
        target_str = str(target_type)

        if self_str not in Type.weak_against:
            return False

        return target_str in Type.weak_against[self_str]

    def is_strong_against(self, target_type: Type):
        """Returns True if this Type is strong against the input Type."""
        self_str = str(self)
        target_str = str(target_type)

        if self_str not in Type.strong_against:
            return False

        return target_str in Type.strong_against[self_str]
        
    @staticmethod
    def assign_types():
        """A method to assign random types to a Mon."""

        raw = random.choice(Type.types)

        if isinstance(raw, set):
            return [Type(t.strip(), None) for t in raw]  # each is a base type
        elif isinstance(raw, str):
            match = re.match(r"(.+?) \(Sub: (.+?)\)", raw)
            if match:
                subclass = match.group(1).strip()
                parent = match.group(2).strip()
                return [Type(parent, subclass)]
            else:
                return [Type(raw.strip(), None)]
            
    @staticmethod
    def assign_types_weighted(weighted_pool=None):
        """
        Assigns one or more random Types to a Mon, using optional weights.

        :param weighted_pool: Optional list of tuples like [(Type_str_or_set, weight), ...]
                            If None, it uses an even distribution across all Type.types.
        """
        import random

        # Step 1: Choose the weighted pool
        if weighted_pool is None:
            weighted_pool = [(t, 1.0) for t in Type.types]  # even weights by default

        # Step 2: Validate and normalize
        total_weight = sum(weight for _, weight in weighted_pool)
        if total_weight <= 0 or any(weight < 0 for _, weight in weighted_pool):
            raise ValueError("All weights must be non-negative, and total must be > 0.")

        # Step 3: Weighted random choice
        choices, weights = zip(*weighted_pool)
        raw_type = random.choices(choices, weights=weights, k=1)[0]

        # Step 4: Same logic as before
        if isinstance(raw_type, set):
            return [Type(t, None) for t in raw_type]

        if "(Sub:" in raw_type:
            try:
                name, sub = raw_type.split("(Sub:")
                subclass = name.strip()
                parent = sub.replace(")", "").strip()
                return [Type(parent, subclass)]
            except ValueError:
                raise ValueError(f"Invalid subclass type format: {raw_type}")

        return [Type(raw_type.strip(), None)]

class Move: 
    """A class to define a Mon's Moveset based on their Type."""

    spam_hit_onomatopoeias = [
        "Kck!", 
        "Urg!", 
        "Hrngh!", 
        "Agh!", 
        "Erk!",
        "Ack!", 
        "Mmh!", 
        "Owh!", 
        "Oowh!"
    ]

    big_hit_onomatopoeias = [
        "AAAGH!", 
        "EURGH!", 
        "HGERCK!", 
        "AACK!", 
        "AWWFPH!", 
        "OWGH!", 
        "OWCK", 
        "EURCK!"
    ]

    ## About Subclass Moves: 
        # Subclass Moves choose from a unique list of Moves, specific to that Subclass, but Mons of a Subclass may still have moves 
        # from the Parent Class Moveset, however Mons of the Parent Type Class may not have moves from a Subclass, even if that Subclass 
        # derives from the Parent. 

    ## About Rarity-specific Moves: 
        # Moves specific to a certain Rarity may only be given to a Mon of that specific Rarity (or higher), but Moves without a specified 
        # Rarity may be assigned to any Mon regardless of its Rarity. 

    ## About Type-Combination Moves:
        # Mons of combined Types may use any Move(s) from their specific Type-Combination Moveset or any Move(s) from any of its base 
        # Type Class (or Subclass).

    def __init__(self, nm : str, dmg : int, itrns : int, drtn : int, cldwn : int, acc : float, prcsn : float, rcl : int, stmn : int, mvtps : List[Type], rrt : str, fx : Optional[List[Effect]] = None, prstg : Optional[Prestige] = None):
        self.name = nm # move name
        self.damage = dmg # pos int : 0 to +inf (damage inflicted on the opponent Mon)
        self.iterations = itrns # damage iterations
        self.duration = drtn # time duration seconds across each iteration of damage
        self.cooldown = cldwn # Move time cooldown seconds (a neg value denotes a cooldown on the opponent's Mon as well as the user's Mon)
        self.accuracy = acc # accuracy float percentage (0.00 - 1.00) for each damage iteration
        self.precision = prcsn # precision float percentage (0.00 - 1.00) for each attack, chance to bypass defense
        self.recoil = rcl # neg int : -inf to 0 (damage inflicted on the user Mon) 
        self.stamina = stmn # int : -inf to +inf (stamina cost for the Move -- neg cost takes away Mon stamina; pos cost gives back Mon stamina)
        self.move_types = mvtps # Type list of Type Classes / Subclasses
        self.rarity = rrt # str corresponding to required min Rarity for a Mon to use the Move
        self.effects = fx
        self.prestige = prstg if not prstg == None else None # Prestige for Move upgrades

    def __str__(self):
        type_names = ", ".join(str(tp) for tp in self.move_types)
        effects_list = ", ".join(efct.name for efct in self.effects)

        base_str = (
            f"\t{self.name} ({Mon.rarity_colors(self.rarity)})\t\tTp = {type_names}\n"
            f"\t\tDmg = {self.damage} \tAcc = {self.accuracy * 100:.1f}%\n"
            f"\t\tItr = {self.iterations} \tRcl = {self.recoil}\n"
            f"\t\tDur = {self.duration}s\tCst = {self.stamina}\n"
            f"\t\tCld = {self.cooldown}s\tFx = {effects_list}\n"
        )

        prestige_str = f"{str(self.prestige)}\n" if self.prestige and self.prestige.rank else ""
        return base_str + prestige_str
    
    def __eq__(self, other : Move) -> bool:
        if not isinstance(other, Move):
            return NotImplemented
        return (
            self.name == other.name and
            self.damage == other.damage and
            self.iterations == other.iterations and
            self.duration == other.duration and
            self.cooldown == other.cooldown and
            self.accuracy == other.accuracy and
            self.precision == other.precision and
            self.recoil == other.recoil and
            self.stamina == other.stamina and
            # ignore types, since it's consistent across all of the same Move
            self.rarity == other.rarity and
            self.effects == other.effects and
            self.prestige == other.prestige
        )

    def __hash__(self):
        return hash(self.name)
    
    def update_cooldowns(cooldown_moves):
        """Helper method for Mon.battle() to adjust (temporary) Move cooldowns."""
        updated = {mv for mv in cooldown_moves if mv.cooldown >= 10}
        for mv in updated:
            mv.cooldown = Tools.floor_to_nearest(mv.cooldown - 10, 10)
        return updated
    
    def use(self, 
            user : Mon, 
            target : Mon, 
            typewriter_delay : float = 0.05, 
            timing : float = 0.5, 
            verbose : bool = True
        ): 
        """A method to simulate the user Mon using a Move on the target Mon. Returns True if the Move hit, otherwise False."""

        if verbose:
            Tools.text(f"{user.name} ", params=Mon.rarity_effects[user.rarity])
            Tools.text(f"used {self.name} on ")
            Tools.text(f"{target.name}", params=Mon.rarity_effects[target.rarity])
            Tools.text(f"!\n")

        if self.prestige: 
            self.prestige.add_experience(self, 5, verbose=verbose) # gain 5 Prestige experience for attempting a move

        prec = int(self.precision * 100)
        roll = random.randint(1, 100)
        prec_hit = prec >= roll 

        time.sleep(timing)

        def swap_recipient(recipient : Mon, user : Mon, target : Mon) -> Mon:
            """Swaps the recipient from User to Target or vice versa."""

            return target if recipient == user else user
        
        recipient = target
        healing_move = self.damage < 0
        special_move = self.damage == 0
        reflected = any(
            etype == "damage-reflection"
            for efct in user.effects
            for etype in efct.effect_type
        )
        if healing_move:
            recipient = user
        if reflected:
            recipient = swap_recipient(recipient, user, target)

        strong = False
        weak = False

        strong = any(
            move_type.is_strong_against(rcpt_tp)
            for move_type in self.move_types
            for rcpt_tp in recipient.type
        )

        weak = any(
            move_type.is_weak_against(rcpt_tp)
            for move_type in self.move_types
            for rcpt_tp in recipient.type
        )

        #Tools.text(f"[DEBUG] {[str(u_tp) for u_tp in user.type]} : {self.name} -> {[str(r_tp) for r_tp in recipient.type]} | S:{strong} W:{weak}\n\n", rgb=[255,0,0])

        attack_boost_addition = self.damage * user.attack_boost
        strength_multiplier = 1
        weakness_multiplier = 1
        strength_text = ""
        weakness_text = ""

        if strong and weak:
            strength_multiplier = 1
            weakness_multiplier = 1
            strength_text = f"{recipient.name}'s type resists and is also weak to the move.\n"
        elif strong:
            strength_multiplier = 2
            strength_text = f"Its strength is intensified on {recipient.name}'s type!\n"
        elif weak:
            weakness_multiplier = 0.33
            weakness_text = f"It's weak on {recipient.name}'s type...\n"
        else:
            strength_multiplier = 1
            weakness_multiplier = 1
        
        #print(f"{special_move}")

        if prec_hit:
            damage = int((self.damage + attack_boost_addition) * self.iterations * strength_multiplier * weakness_multiplier)
            if healing_move: # healing move
                recipient.health -= self.damage * self.iterations # use un-strengthed/weakened damage
                recipient.health = min(recipient.health, recipient.max_health)
                if verbose:
                    Tools.text(f"Direct hit!\n", typewriter_delay)
                    if reflected:
                        Tools.text(f"Move reflected! {user.name} healed {recipient.name} for {abs(self.damage * self.iterations)} hit points!\n", typewriter_delay)
                    else:
                        Tools.text(f"{user.name} healed themself for {abs(self.damage * self.iterations)} hit points!\n", typewriter_delay)
            elif special_move: # special move (non-damaging)
                if verbose:
                    Tools.text(f"Direct hit!\n{user.name} used Special Move {self.name}!\n", typewriter_delay)
            else: # regular damaging move
                recipient.health -= damage # ignores defense
                recipient.health = max(recipient.health, 0)
                if verbose:
                    Tools.text(f"Direct hit!\n", typewriter_delay)
                    if reflected:
                        Tools.text(f"Move reflected! {strength_text}{weakness_text}{self.name} slashed through their own defense and dealt {damage} damage!\n", typewriter_delay)
                    else:
                        refl_text = "Move reflected! " if reflected else ""
                        Tools.text(f"{refl_text}{strength_text}{weakness_text}{self.name} slashed through {recipient.name}'s defense and dealt {damage} damage!\n", typewriter_delay)

            user.health -= self.recoil
            user.stamina -= self.stamina
            user.health = max(user.health, 0)
            user.stamina = max(user.stamina, 0)

            if self.prestige: 
                self.prestige.add_experience(self, 100, verbose=verbose) # gain 100 Prestige experience for precision hit
                self.prestige.add_experience(self, 15 * self.iterations, verbose=verbose) # gain 15 Prestige experience per successful iteration
                self.prestige.add_experience(self, 50, verbose=verbose) # gain 50 Prestige experience for a chain hit

            # apply effects per-hit
            self.apply_effects(user, recipient) # method already early-exits when no effects exist
            
            return True, damage, self.iterations, strong, weak

        damage_sum = 0
        hits = 0

        for itr in range(self.iterations):
            acc = int(self.accuracy * 100)
            roll = random.randint(1, 100)
            hit = acc >= roll

            if hit: 
                if healing_move: # healing move
                    damage_sum += self.damage + attack_boost_addition
                else:
                    damage_sum += int((self.damage + attack_boost_addition) * strength_multiplier * weakness_multiplier)
                hits += 1
                if self.iterations > 3:
                    if verbose:
                        Tools.text(f"{random.choice(Move.spam_hit_onomatopoeias)} ")
                        time.sleep(self.duration / self.iterations) if timing else None
                else: 
                    if verbose:
                        Tools.text(f"{random.choice(Move.big_hit_onomatopoeias)} ")
                self.apply_effects(user, recipient) # effects applied regardless of defense
        
        print()
        if healing_move: # healing move
            final_damage = damage_sum
            if hits > 0:
                heal_amount = abs(final_damage)
                recipient.health += heal_amount
                recipient.health = min(recipient.health, recipient.max_health)
        else:
            final_damage = max(damage_sum - target.defense, 0)
            recipient.health -= final_damage
            recipient.health = max(recipient.health, 0)

        if hits > 0:
            if verbose:
                if final_damage > 0 and not healing_move:
                    if reflected:
                        Tools.text(f"Move reflected! {strength_text}{weakness_text}{self.name} dealt {final_damage} damage to themself!\n", typewriter_delay)
                    else:
                        Tools.text(f"{strength_text}{weakness_text}{self.name} dealt {final_damage} damage to {recipient.name}!\n", typewriter_delay)
                elif final_damage < 0 and healing_move:
                    if reflected:
                        Tools.text(f"Move reflected! {user.name} healed {recipient.name} for {abs(final_damage)} hit points!\n", typewriter_delay)
                    else:
                        Tools.text(f"{user.name} healed themself for {abs(final_damage)} hit points!\n", typewriter_delay)
                elif final_damage <= 0 and special_move:
                    Tools.text(f"{user.name} used Special Move: {self.name}!\n", typewriter_delay)
                else:
                    refl_text = "Move reflected! " if reflected else ""
                    Tools.text(f"{refl_text}{strength_text}{weakness_text}{recipient.name}'s defense absorbed the blow... {self.name} dealt no damage.\n", typewriter_delay)

            # add prestige XP regardless of move damage or type
            if self.prestige: 
                self.prestige.add_experience(self, 15 * hits, verbose=verbose) # gain 15 Prestige experience per successful iteration
                if hits >= self.iterations:
                    self.prestige.add_experience(self, 50, verbose=verbose) # gain 50 Prestige experience for a chain hit
            user.health -= self.recoil
            user.stamina -= self.stamina
            user.health = max(user.health, 0)
            user.stamina = max(user.stamina, 0)

            return True, final_damage, hits, strong, weak
        else:
            #Tools.text(f"DEBUG: damage={final_damage} hits={hits}\n", bold=True, rgb=[255, 0, 0])
            if verbose:
                Tools.text(f"{self.name} missed...\n", typewriter_delay)
            if self.prestige: 
                self.prestige.add_experience(self, 10, verbose=verbose) # gain 10 pity Prestige XP if move missed

            return False, final_damage, hits, strong, weak

    def apply_effects(self, user : Mon, target : Mon): 
        """Attempts to apply effects from this Move to the target and/or user Mon.

        Effects are only added to the recipient's effects list if they pass the application_chance roll.
        No actual stat or health changes occur here — those are handled in trigger_effects().
        """

        if not self.effects:
            return

        for effect in self.effects:
            if random.random() > effect.application_chance:
                continue

            # Prepare subeffect buckets
            user_indices = []
            target_indices = []

            for i in range(len(effect.effect_type)):
                recipient = user if effect.target_self[i] else target
                stackable = effect.stackable[i]
                already_has = any(e.name == effect.name for e in recipient.effects)

                if not stackable and already_has:
                    continue

                if effect.target_self[i]:
                    user_indices.append(i)
                else:
                    target_indices.append(i)

            # Helper to build an effect instance for a given recipient
            def build_effect_instance(recipient, indices):
                if not indices:
                    return

                e_instance = deepcopy(effect)
                e_instance.effect_type = [effect.effect_type[i] for i in indices]
                e_instance.target_type = [effect.target_type[i] for i in indices]
                e_instance.target_self = [effect.target_self[i] for i in indices]
                e_instance.target_attribute = [effect.target_attribute[i] for i in indices]
                e_instance.value = [effect.value[i] for i in indices]
                e_instance.stackable = [effect.stackable[i] for i in indices]
                e_instance.previous_value = {}  # still optionally keep for debugging

                #e_instance.e_instance_debug(indices)

                for j in range(len(indices)):
                    i = indices[j]  
                    etype = e_instance.effect_type[j]
                    ttype = e_instance.target_type[j]
                    attr = e_instance.target_attribute[j]

                    if etype in ("buff", "debuff"):
                        # === For Mon attributes ===
                        if ttype == "Mon":
                            if hasattr(recipient, attr):
                                current_val = getattr(recipient, attr)
                                # Save original value if not already saved
                                if attr not in recipient.original_values:
                                    recipient.original_values[attr] = current_val
                                # Optional legacy store
                                e_instance.previous_value[attr] = current_val
                            else:
                                print(f"[Warning] Mon has no attribute '{attr}' for buff/debuff effect")

                        # === For Move attributes ===
                        elif ttype == "Move":
                            e_instance.previous_value[attr] = {}
                            if attr not in recipient.original_move_values:
                                recipient.original_move_values[attr] = {}

                            for move in recipient.moves:
                                if hasattr(move, attr):
                                    val = getattr(move, attr)

                                    # Save only if not already saved
                                    if move.name not in recipient.original_move_values[attr]:
                                        recipient.original_move_values[attr][move.name] = val

                                    # Optional legacy store
                                    e_instance.previous_value[attr][move.name] = val
                                else:
                                    print(f"[Warning] Move '{move.name}' has no attribute '{attr}' for buff/debuff effect")

                recipient.effects.append(e_instance)

            # Apply separate effect instances to user and target
            build_effect_instance(user, user_indices)
            build_effect_instance(target, target_indices)
    
    @staticmethod
    def choose_random_move(mon: Mon, 
                           type_filter: List[Type], 
                           move_priority: Tuple[bool, bool, bool] = (False, False, False)):
        """
        Select a random valid Move based on relevant Type filter combinations, including subclass parents.
        
        Parameter: 
        - mon: The Mon to which the move will be assigned.
        - type_filter (List[Type]): A list of Types used to determine which move files to consider.
        - move_priority (Tuple[bool, bool, bool], optional): A 3-flag tuple indicating sort preferences.
            - Format: (prestige_priority, rarity_priority, damage_output_priority)
            - Example: (True, True, False) prioritizes moves that have prestige and higher rarity.

        Returns:
        - Move or None: A parsed Move object if valid moves are found, else None.
        """

        if isinstance(type_filter, Type):
            type_filter = [type_filter]

        base_dir = os.path.dirname(__file__)
        rarity_level = Mon.rarities[mon.rarity]

        # Collect move names the Mon already has
        owned_move_names = {move.name for move in mon.moves}

        # Build type variants (including parent types if subclassed)
        type_variants = set()
        for t in type_filter:
            base = str(t).split()[0].lower()
            type_variants.add(base)
            if t.subclass:
                parent = t.parent_class.lower()
                type_variants.add(parent)

        type_names = sorted(type_variants)
        seen_files = set()
        valid_moves = []

        for r in range(1, len(type_names) + 1):
            for combo in itertools.combinations(type_names, r):
                joined = ",".join(sorted(combo))
                if joined in seen_files:
                    continue
                seen_files.add(joined)

                filename = f"{joined}_moves.json"
                filepath = os.path.join(base_dir, "Game/data/moves", filename)

                try:
                    with open(filepath, "r") as f:
                        move_data = json.load(f)
                        for name, move in move_data.items():
                            if name in owned_move_names:
                                continue  # Skip duplicate move
                            if Mon.rarities.get(move.get("rarity", "Any"), 0) <= rarity_level:
                                valid_moves.append((name, move))
                except FileNotFoundError:
                    continue

        if not valid_moves:
            print(f"[Warning] No valid moves found for {[str(t) for t in type_filter]} ({mon.rarity})")
            return None

        # Fixed priority order: (prestige, rarity, damage_output)
        def get_priority_tuple(move_data, priority_flags):
            prestige_flag, rarity_flag, damage_flag = priority_flags
            move = Move.parse(move_data, "_temp")  # We just need this for damage_output()

            result = []
            if prestige_flag:
                result.append(1 if move_data.get("prestige") else 0)
            if rarity_flag:
                result.append(Mon.rarities.get(move_data.get("rarity", "Common"), 0))
            if damage_flag:
                result.append(move.damage_output())  # dmg * itr * acc from method

            return tuple(result)

        if move_priority:
            valid_moves.sort(
                key=lambda item: get_priority_tuple(item[1], move_priority),
                reverse=True
            )
            top_n = valid_moves[:5]  # You can adjust this window
            #Tools.text(f"{mon.name}\n", params=Mon.rarity_effects[mon.rarity])
            #print(*valid_moves, sep="\n")
            name, move = random.choice(top_n)
        else:
            name, move = random.choice(valid_moves)

        return Move.parse(move, name)
        
    def export(self, filename : str): 
        """A method for exporting the Move to the specified JSON file."""

        try:
            with open(filename, "w") as f:
                json.dump(self.to_dict(), f, indent=4)
            print(f"Move exported to {filename}")
        except Exception as e:
            print(f"Export failed: {e}")

    def to_dict(self): 
        """Returns a dictionary for the Move."""

        move_types = [{"parent_class": tp.parent_class, "subclass": tp.subclass} for tp in self.move_types ]
        effects_names = []
        for efct in self.effects:
            if isinstance(efct, str):
                effects_names.append(efct)
            elif hasattr(efct, 'name'):
                effects_names.append(efct.name)
            else:
                effects_names.append(str(efct))  

        return {
            self.name : {
                "damage" : self.damage, 
                "iterations" : self.iterations,
                "duration" : self.duration,
                "cooldown" : self.cooldown,
                "accuracy" : self.accuracy,
                "precision" : self.precision,
                "recoil" : self.recoil, 
                "stamina" : self.stamina,
                "move_types" : move_types, 
                "rarity" : self.rarity, 
                "effects" : effects_names,
                "prestige" : self.prestige.to_dict() if self.prestige else None
            }
        }
    
    @staticmethod
    def parse(data: dict, name: Optional[str] = None):
        """Parses a JSON dictionary representing a Move and returns a Move object."""

        try:
            move_name = name if name else data.get("name", "Unnamed Move")
            prstg_data = data.get("prestige")
            effects_data = data.get("effects", []) or []  
            effect_lib = EffectLibrary("Game/data/effects/effects.json")

            #print(f"[Debug] effects_data = {effects_data}")
            #print(f"[Debug] types = {[type(e) for e in effects_data]}")

            return Move(
                nm=move_name,
                dmg=data["damage"],
                itrns=data["iterations"],
                drtn=data["duration"],
                cldwn=data["cooldown"],
                acc=data["accuracy"],
                prcsn=data["precision"],
                rcl=data["recoil"],
                stmn=data["stamina"],
                mvtps=[Type(mt["parent_class"], mt.get("subclass")) for mt in data["move_types"]],
                rrt=data["rarity"],
                fx = [
                    efct if isinstance(efct, Effect)
                    else effect_lib.get_effect(efct) if isinstance(efct, str)
                    else Effect.parse(efct)
                    for efct in effects_data
                ],
                prstg = Prestige.parse(prstg_data) if prstg_data else None
            )
        except KeyError as e:
            print(f"[Error] Missing field {e} in move: {move_name}")
            return None

    @staticmethod
    def get(type : List[Type], name : str):
        """A method to get a Move object by its Name from its respective Moveset JSON."""

        type_names = set()
        for tp in type: 
            type_str = str(tp)

            if type_str not in Type.types and type_str != "z":
                print(f"Could not get Move -- Invalid Type: {type_str}.")
                return None
            
            type_base = type_str.split()[0].lower()
            type_names.add(type_base)

        joined = ",".join(sorted(type_names))
        filename = f"{joined}_moves.json"
        base_dir = os.path.dirname(__file__)
        filepath = os.path.join(base_dir, "Game/data/moves", filename)

        try:
            with open(filepath, "r") as file:
                moveset = json.load(file)
        except FileNotFoundError:
            print(f"Could not find moveset file: {filename}")
            return None
        except json.JSONDecodeError:
            print(f"Failed to parse JSON in: {filename}")
            return None
        
        move_data = moveset.get(name)
        if not move_data:
            print(f"Move '{name}' not found in {filename}")
            return None

        return Move.parse(move_data, name)
    
    def damage_output(self, 
                      modifying_effects: List[Effect] = None, 
                      include_damaging_effects : bool = False, 
                      include_healing_effects : bool = False, 
                      attack_boost : float = None, 
                      simulate_prestige : bool = None
                    ) -> float:
        """
        Returns probabilistic damage output for the Move for Move prioritization,
        optionally incorporating stat boosts or reductions added by a list of Effects.
        Healing and damaging effect components are mutually exclusive.
        """

        if simulate_prestige and self.prestige:
            self.prestige.adjust_rank(self, self.prestige.max_rank, verbose=False)                

        if attack_boost is not None: # attack boost is float, corresponding to a percentage 
            attack_boost += 1.0
            dmg = self.damage * attack_boost
        else:
            # Base values
            dmg = self.damage

        acc = self.accuracy
        itr = self.iterations

        # Apply stat-modifying effects (buffs/debuffs)
        if modifying_effects:
            for effect in modifying_effects:
                for i, etype in enumerate(effect.effect_type):
                    if etype not in ("buff", "debuff"):
                        continue
                    if effect.target_type[i] != "Move":
                        continue

                    attr = effect.target_attribute[i]
                    val = effect.value[i]

                    if attr == "damage":
                        dmg += dmg * val  # percent-based
                    elif attr == "accuracy":
                        acc += acc * val  # percent-based
                    elif attr == "iterations":
                        itr += val  # direct additive

        # Clamp accuracy to [0, 1]
        acc = max(0.0, min(1.0, acc))

        # Probabilistic damage from core move
        prob_dmg = dmg * itr * acc

        #print(f"{self.name} dmg = {dmg}, itr = {itr}, acc = {acc}, prob = {prob_dmg}")
        #print(f"raw = {dmg * itr * acc}")

        # Add effect-based chip damage OR healing
        if include_damaging_effects and not include_healing_effects:
            for efct in self.effects:
                for j, efct_tp in enumerate(efct.effect_type):
                    if efct_tp in ("chip-damage", "diminishing-chip-damage"):
                        prob_dmg -= efct.value[j] * itr * acc * efct.application_chance # chip vals are negative (+dmg = dmg - (-val))

        elif include_healing_effects and not include_damaging_effects:
            for efct in self.effects:
                for j, efct_tp in enumerate(efct.effect_type):
                    if efct_tp == "chip-heal":
                        prob_dmg -= efct.value[j] * itr * acc * efct.application_chance # heal vals are positive (-dmg = dmg - (val))

        #print(f"{self.name} dmg = {dmg}, itr = {itr}, acc = {acc}, prob = {prob_dmg}")
        #print(f"raw = {dmg * itr * acc}")

        return prob_dmg
    
    def hit_probabilities(self):
        """Prints a table of probabilities for the each possible number of attack iterations for the Move."""

        n = self.iterations
        p = self.accuracy

        print(f"Probability distribution for '{self.name}' ({n} iterations @ {self.accuracy * 100:.2f}% accuracy):")
        hits = ""
        percs = ""
        row_count = 0
        print("=" * 153)

        for k in range(n + 1):
            prob = math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
            hits += f"{k:<14}| "
            percs += f"{prob:.4%}\t| "
            row_count += 1

            if row_count % 9 == 0 or k == n:
                print("# Hits || ", end="")
                print(hits)
                print("Prob % || ", end="")
                print(percs)
                print("=" * 153)
                hits = ""
                percs = ""

    def move_statistics(self):
        """A method that prints battle-related statistical info about the Move."""

        print(f"Damage per Hit \t\tx \tExpected # Hits per Move \tx \t# Expected Attacks per Turn")
        print(f"\t{self.damage} \t\tx \t\t{self.iterations * self.accuracy} \t\t\tx \t\t{int(10 / self.cooldown)} \t\t= \t\t{self.damage * self.accuracy * self.iterations * int(10 / self.cooldown)} Expected Damage per Turn")

class Prestige: 
    """A class to implement Move Prestiges, a psuedo-leveling system within Moves, which allows for Moves to 
    evolve and become more powerful. The Prestige object itself acts as a field within Move, defining whether 
    the Move is capable of being Prestiged -- None in the Move.prestige field refers to non-prestigable."""

    ranks = {
        0 : None,
        1 : "Emerald",
        2 : "Sapphire", 
        3 : "Topaz", 
        4 : "Amethyst", 
        5 : "Ruby"
    }

    def __init__(self, nm : str, rnk : int, xp : int, xpndd : int, xpmlt : int, mxrnk : int, mlstns : List[Milestone]):
        self.name = nm # pass in Move name?
        self.rank = rnk
        self.experience = xp
        self.experience_needed = xpndd
        self.experience_multiplier = xpmlt
        self.max_rank = mxrnk
        self.milestones = mlstns 

    def __str__(self):
        header = f"\tPrestige: {Prestige.rank_colors(self.rank)} {(f'(MAX)' if self.rank >= self.max_rank else '')}\n"
        milestones_str = "\t\tMilestones Unlocked:\n"
        
        for i in range(min(self.rank, len(self.milestones))):
            rank_label = Prestige.ranks.get(i + 1, f"Rank {i + 1}")  # Offset by 1 since rank 0 = None
            milestone = self.milestones[i]
            milestones_str += f"\t\t\t{Prestige.rank_colors(i + 1)} Rank Rewards: {str(milestone)}\n"

        return header + milestones_str
    
    def __eq__(self, other : Prestige) -> bool:
        if not isinstance(other, Prestige):
            return NotImplemented
        return (
            self.name == other.name and
            self.rank == other.rank and
            self.experience == other.experience and
            self.experience_needed == other.experience_needed and
            self.experience_multiplier == other.experience_multiplier
        )
    
    def to_dict(self):
        return {
            "name": self.name,
            "rank": self.rank,
            "experience": self.experience,
            "experience_needed": self.experience_needed,
            "experience_multiplier": self.experience_multiplier,
            "max_rank": self.max_rank,
            "milestones": [m.to_dict() for m in self.milestones]  # assuming Milestone also has .to_dict()
        }

    @staticmethod
    def parse(data: dict):
        """Parses a JSON dictionary into a Prestige object."""
        try:
            milestones = [
                Milestone(m["rank"], m["type"], m["event_text"], m["perk"], m["value"], m["applied"])
                for m in data.get("milestones", [])
            ]
            return Prestige(
                nm=data["name"],
                rnk=data["rank"],
                xp=data["experience"],
                xpndd=data["experience_needed"],
                xpmlt=data["experience_multiplier"],
                mxrnk=data["max_rank"],
                mlstns=milestones
            )
        except KeyError as e:
            print(f"[Error] Missing field {e} in prestige: {data.get('name', 'Unnamed Prestige')}")
            return None

    def adjust_rank(self, move : Move, _num_ranks : int, verbose : bool = True): 
        """A method to adjust a Prestige's rank and corresponding stats from an input number of ranks."""
        
        for rnk in range(_num_ranks):
            if self.rank >= self.max_rank:
                return
            self.add_experience(move, self.experience_needed, verbose=verbose)

    def rank_up(self, move : Move, recursed_ranks : Optional[int] = None, verbose : bool = True): 
        """A method to rank-up a Prestige, if possible, and unlock Prestige milestones accordingly."""

        if self.rank >= self.max_rank: 
            # Move already at max Prestige
            return

        # instantiate the recursive count
        if recursed_ranks is None:
            recursed_ranks = 0

        if self.experience < self.experience_needed: 
            if recursed_ranks > 0:
                if recursed_ranks == 1:
                    if verbose:
                        print(f"{self.name} Prestiged!")
                else:
                    if verbose:
                        print(f"{self.name} Prestiged {recursed_ranks} times!")
            return
        
        self.rank += 1 # increase rank
        self.experience -= self.experience_needed # deduct needed experience from the total amount
        self.experience_needed *= self.experience_multiplier # adjust needed experience for next rank 

        # unlock milestones
        for ms in self.milestones:
            if not ms.applied and self.rank == ms.rank:
                ms.apply(move, verbose=verbose)

        # increase recursive rank counter for printing
        recursed_ranks += 1
        self.rank_up(move, recursed_ranks, verbose=verbose) # recursively call for remaining ranks

    def add_experience(self, move : Move, points : int, verbose : bool = True):
        """A method to add experience points to a Prestige and automatically check if the Move can Prestige."""

        self.experience += points
        self.rank_up(move, verbose=verbose)

    @staticmethod
    def rank_colors(rank_value : int): 
        if rank_value not in Prestige.ranks:
            print(f"Rank {rank_value} not found.")
            return rank_value
        
        rank = Prestige.ranks[rank_value]

        if rank_value == 1: 
            return Tools.rgb(85, 255, 0, rank)
        elif rank_value == 2: 
            return Tools.rgb(0, 47, 255, rank)
        elif rank_value == 3: 
            return Tools.rgb(252, 169, 3, rank)
        elif rank_value == 4: 
            return Tools.rgb(170, 0, 255, rank)
        elif rank_value == 5: 
            return Tools.rgb(255, 0, 0, rank)
        else: 
            return rank

class Milestone:
    """A milestone represents an upgrade unlocked at a specific prestige rank. Can boost stats or inflict status effects."""

    def __init__(self, rnk, tp, evnt_txt : str, prk = None, val = None, fx = None, appld = False):
        self.rank = rnk
        self.type = tp  # "stat_boost" or "status_effect"
        self.event_text = evnt_txt
        self.perk = prk     # e.g., "damage", "cooldown" (for stat_boost)
        self.value = val      # numerical value to add (for stat_boost)
        self.effect = fx    # dict for status effect details (for status_effect)
        self.applied = appld

    @classmethod
    def from_dict(cls, data):
        return cls(
            rnk=data["rank"],
            tp=data.get("type", "stat_boost"),  # default to stat_boost
            evnt_txt=data.get("event_text"),
            prk=data.get("perk"),
            val=data.get("value"),
            fx=data.get("effect"), 
            appld=data.get("applied")
        )
    
    def to_dict(self):
        return {
        "rank": self.rank,
        "type": self.type,
        "event_text": self.event_text,
        "perk": self.perk,
        "value": self.value,
        "effect": self.effect,
        "applied": self.applied
    }

    def apply(self, move : Move, verbose : bool = True):
        if self.type == "stat_boost":
            if hasattr(move, self.perk):
                current = getattr(move, self.perk)
                setattr(move, self.perk, current + self.value)

        elif self.type == "status_effect":
            effect_lib = EffectLibrary()  # You may want to pass in a shared instance instead of creating a new one every time
            effect = effect_lib.get_effect(self.value)

            if effect is not None:
                move.effects.append(effect)
            else:
                print(f"[Warning] Failed to add status effect '{self.value}' — effect not found.")

        elif self.type == "swap_status_effect":
            effect_lib = EffectLibrary()
            old_name = self.perk
            new_effect = effect_lib.get_effect(self.value)

            if new_effect is None:
                print(f"[Warning] Failed to add status effect '{self.value}' — effect not found.")
                return

            # Search for a matching effect *by name* in move.effects
            matched = None
            for e in move.effects:
                if isinstance(e, Effect) and e.name == old_name:
                    matched = e
                    break

            if matched:
                move.effects.remove(matched)
                move.effects.append(new_effect)
                if verbose:
                    print(f"Replaced status effect '{old_name}' with '{self.value}' on move '{move.name}'")
            else:
                print(f"[Warning] Move has no effect named '{old_name}' to swap out.")

        elif self.type == "name_change":
            if hasattr(move, self.perk):
                current = getattr(move, self.perk)
                if verbose:
                    print(f"{current} evolved into {self.value}!")
                setattr(move, self.perk, self.value)

        self.applied = True

    def __str__(self):
        if self.perk == "accuracy" or self.perk == "precision": 
            val = f"{self.value * 100}%"
        else: 
            val = f"{self.value}"

        if self.type == "stat_boost":
            return f"{self.event_text}+{val} {self.perk}" if self.value >= 0 else f"{val} {self.perk}"
        elif self.type == "status_effect":
            return f"Grants status effect: {self.value}"
        elif self.type == "swap_status_effect":
            return f"Status effect {self.perk} upgraded to {self.value}!"
        elif self.type == "name_change":
            print(f"elif name change {self.event_text}")
            return f"{self.event_text}"
    
        return f"Unknown milestone: {self.perk}, {self.type}, {self.value}"
    
class EffectLibrary:

    def __init__(self, relative_path: str = "Game/data/effects/effects.json"):
        # Get absolute path relative to this file’s directory
        base_dir = os.path.dirname(__file__)
        full_path = os.path.join(base_dir, relative_path)

        with open(full_path, "r") as f:
            raw_effects = json.load(f)

        self.effects = {e["name"]: e for e in raw_effects}

    def get_effect(self, name: str) -> "Effect":
        """Returns a deepcopied Effect object for safe application."""
        if isinstance(name, Effect):
            print("[Warning] get_effect() called with an Effect object, returning deepcopy of it.")
            return deepcopy(name)

        if name not in self.effects:
            print(f"[Warning] [EffectLibrary] Unknown effect name '{name}'")
            return None

        return Effect(**deepcopy(self.effects[name]))

class Effect: 
    """A class for status effects, applied to Mons or their moves by Moves."""

    _library = None

    def __init__(self, 
                 name : str,
                 effect_type : List[str], 
                 target_type : List[str], 
                 target_self : List[bool], 
                 target_attribute : List[str], 
                 value : List[float], 
                 stackable : List[bool], 
                 duration : int = 1, 
                 trigger : Optional[str] = None, 
                 application_chance : float = 1.0 
                ):
        self.name = name
        self.effect_type = effect_type # type of effect; e.g., 'chip-damage', 'buff', 'stun', etc.
        self.target_type = target_type # designates target object: 'Mon' or 'Move'
        self.target_self = target_self # designates effect applied to self: true = self, false = opponent
        self.target_attribute = target_attribute # attribute to target / modify, may contain None
        self.value = value # amount to modify target attribute by, may contain None
        self.previous_value = None # previous value of target attribute, used for restoring values, only needed while game is running 
        self.stackable = stackable # designates whether effect is stackable
        self.duration = duration # duration in number of rounds from application the effect lasts, including application round and self & opponent rounds
        self.duration_remaining = duration # duration remaining on the effect until it is removed, decremented each (self & opponent) round 
        self.trigger = trigger # when the effect is triggered; i.e., effect takes hold or modifies target attribute; e.g., 'on_round_start', 'on_hit', etc.
        self.triggered = False # stores whether the effect has been triggered
        self.application_chance = application_chance # chance the effect is applied 

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "effect_type": self.effect_type,
            "target_type": self.target_type,
            "target_self": self.target_self,
            "target_attribute": self.target_attribute,
            "value": self.value,
            "stackable": self.stackable,
            "duration": self.duration,
            "trigger": self.trigger,
            "application_chance": self.application_chance
        }
    
    @staticmethod
    def parse(data: dict) -> "Effect":
        return Effect(
            name=data["name"],
            effect_type=data["effect_type"],
            target_type=data["target_type"],
            target_self=data["target_self"],
            target_attribute=data["target_attribute"],
            value=data["value"],
            stackable=data["stackable"],
            duration=data["duration"],
            trigger=data.get("trigger"),
            application_chance=data.get("application_chance", 1.0) 
        )
    
    def export(self, path: str = "Game/data/effects/effects.json"):
        """Exports this effect to a JSON file, appending it if the file exists."""
        data = []

        # If file exists, load current data
        if os.path.exists(path):
            with open(path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    print("[Warning] effects.json was empty or invalid. Starting fresh.")

        # Append this effect
        data.append(self.to_dict())

        # Save updated list
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"[Effect] Exported '{self.name}' to {path}")

    @staticmethod
    def get(name: str) -> Optional["Effect"]:
        """Static shortcut to get an Effect by name using a cached EffectLibrary."""
        if Effect._library is None:
            Effect._library = EffectLibrary()  # Lazy init
        return Effect._library.get_effect(name)

    def e_instance_debug(self, indices : List[int]): 
        """
        Debugging prints for Effect instances.

        Parameter:
        - indices: list of integers for index storage.
        """

        Tools.text("\n[DEBUG] Constructed e_instance from selected indices\n", rgb=[0, 255, 0])

        for i in range(len(indices)):
            Tools.text(f"  Index {indices[i]}:\n", rgb=[0, 255, 0])
            Tools.text(f"    effect_type: {self.effect_type[i]}\n", rgb=[0, 255, 0])
            Tools.text(f"    target_type: {self.target_type[i]}\n", rgb=[0, 255, 0])
            Tools.text(f"    target_self: {self.target_self[i]}\n", rgb=[0, 255, 0])
            Tools.text(f"    target_attribute: {self.target_attribute[i]}\n", rgb=[0, 255, 0])
            Tools.text(f"    value: {self.value[i]}\n", rgb=[0, 255, 0])
            Tools.text(f"    stackable: {self.stackable[i]}\n", rgb=[0, 255, 0])

class Ability(Effect):
    """A class for inherent Mon traits with conditional activation and optional cooldown."""

    def __init__(self,
                 name: str,
                 effect_type: List[str],
                 target_type: List[str],
                 target_self: List[bool],
                 target_attribute: List[str],
                 value: List[float],
                 stackable: List[bool],
                 trigger: Optional[str] = None,
                 application_chance: float = 1.0,
                 duration: Optional[int] = None,  # Used as cooldown, if desired
                 permanent: bool = True,
                 conditional: Optional[str] = None,
                 conditional_operator: Optional[str] = None,  # e.g., '==', '<', '>', 'in'
                 conditional_value: Optional[Any] = None
                ):
        super().__init__(
            name=name,
            effect_type=effect_type,
            target_type=target_type,
            target_self=target_self,
            target_attribute=target_attribute,
            value=value,
            stackable=stackable,
            duration=duration if duration is not None else 0,
            trigger=trigger,
            application_chance=application_chance
        )
        self.permanent = permanent
        self.conditional = conditional
        self.conditional_operator = conditional_operator
        self.conditional_value = conditional_value

class Talisman:
    """A class for applying special effects to Moves, triggered via Items or Mon-specific Traits."""

    types = {"Item", "Trait"}

    def __init__(self, src : str, nm : str, dscr : str, fx : dict, trgr : Optional[str] = None):

        if src not in Talisman.types:
            raise ValueError(f"Talisman source must be one of {Talisman.types}")
        
        self.source = src
        self.name = nm
        self.description = dscr
        self.effects = fx
        #self.trigger = trgr if trgr == None else self.trigger = None

    def apply(self, move, context=None):
        """Apply this talisman's effect to a Move. `context` could include game state info like target Mon, environment, etc."""
        pass

    def __str__(self):
        return f"[{self.source_type}] {self.name}: {self.description}"
        
class Tools: 
    """Assorted helper tools."""
    
    @staticmethod
    def rgb(r, g, b, text):
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
    
    @staticmethod
    def binomial(n, p): 
        """Returns a list of probabilities for getting k successful hits (from 0 to n) in n Bernoulli trials with success probability p."""

        return [
            math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
            for k in range(n + 1)
        ]
    
    @staticmethod
    def ceil_to_nearest(n, multiple):
        """Returns the input number 'n' to the ceilinged nearest multiple of 'multiple.'"""
        return int(math.ceil(n / multiple) * multiple)
    
    @staticmethod
    def floor_to_nearest(n, multiple):
        """Returns the input number 'n' to the floored nearest multiple of 'multiple.'"""
        return int(math.floor(n / multiple) * multiple)
    
    @staticmethod
    def floor_to_nearest_float(n, multiple):
        """Returns the input number 'n' to the floored nearest multiple of 'multiple.'"""
        return math.floor(n / multiple) * multiple
    
    @staticmethod
    def text(text: str, delay : float = 0, italics : bool = False, bold : bool = False, rgb : List[int] = [0,0,0], params : Optional[list] = None):        
        """Prints styled text with optional delay, italics, bold, and RGB color. Can use `params` as shorthand."""

        if params:
            if len(params) > 4:
                raise ValueError(f"[Error] Too many arguments in params: {params}")
            
            if len(params) >= 1:
                delay = params[0]
            if len(params) >= 2:
                italics = params[1]
            if len(params) >= 3:
                bold = params[2]
            if len(params) == 4:
                rgb = params[3]

        if italics:
            text = Tools.italics(text)

        if bold:
            text = Tools.bold(text)

        if rgb != [0, 0, 0]:
            text = Tools.rgb(rgb[0], rgb[1], rgb[2], text)

        if delay > 0:
            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
        else:
            sys.stdout.write(text)
            sys.stdout.flush()

    @staticmethod
    def devowel(text : str):
        """Returns the input string without vowels, excluding those at the start or end of words."""

        vowels = "aeiouyAEIOUY"

        def process_word(word: str) -> str:
            if len(word) <= 2:  # nothing to remove if <= 2 letters
                return word
            return word[0] + "".join(
                ch for ch in word[1:-1] if ch not in vowels
            ) + word[-1]

        # Split into words and separators, preserving spacing/punctuation
        parts = re.split(r"(\W+)", text)
        processed_parts = [
            process_word(part) if part.isalpha() else part
            for part in parts
        ]
        return "".join(processed_parts)

    @staticmethod
    def italics(text: str): 
        return f"\x1B[3m{text}\x1B[0m"
    
    @staticmethod
    def bold(text: str):
        return f"\033[1m{text}\033[0m"