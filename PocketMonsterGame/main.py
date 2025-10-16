from copy import copy, deepcopy
import json
import math
import os
from typing import List, Optional, Tuple
from Mon import Mon, Type, Move, Effect, Tools
from Game import Game, Miniaturizer, Player, Rubix, Face
from collections import defaultdict
import random

def main1():
    num_trials = 100_000
    rarity_counts = defaultdict(int)

    for _ in range(num_trials):
        rarity = Mon.assign_rarity()
        rarity_counts[rarity] += 1

    print("Rarity Distribution After 100,000 Trials:\n")
    for rarity in ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Ultra', 'Omega']:
        count = rarity_counts[rarity]
        percentage = (count / num_trials) * 100
        print(f"{rarity:<10}: {count:>7} ({percentage:.4f}%)")

def main2():
    roster = []
    rarity_counts = defaultdict(int)

    for i in range(10): 
        print("/" * 150)

    num_trials = 10_000

    for i in range(num_trials):
        mon = Mon()
        roster.append(mon)
        rarity_counts[mon.rarity] += 1
        print("-=" * 40) if Mon.rarities[mon.rarity] >= 0 else None
        print(mon, "\n") if Mon.rarities[mon.rarity] >= 0 else None

    print(f"\nRarity Distribution After {num_trials} Trials:\n")
    for rarity in ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Ultra', 'Omega']:
        count = rarity_counts[rarity]
        percentage = (count / len(roster)) * 100
        print(f"{rarity:<10}: {count:>5} ({percentage:.2f}%)")

def main3():
    types = []
    for i in range(10):
        t = Type.tps()
        types.append(t)
        print(t)

def main4():
    for i in range(1):
        Game.mon_pack()

def main5():
    test = Mon()

    move = test.moves[0]

    move.export("test_move.json")

def main6():
    test = Mon()

    test.name = "Boss4"
    test.rarity = "Legendary"
    test.type = [Type("Water", None)]
    test.rarity_boost(test.rarity)
    test.assign_moves(test.type)

    test.export("test_mon.json")

def main7():
    test = Mon()

    test.name = "Young Padawon"
    test.rarity = "Legendary"
    test.rarity_boost(test.rarity)
    test.assign_moves(test.type)

    print(test)

    test.learn_move()

    print(test)

    test.learn_move()

def main8():
    test = Mon()
    
    test.name = "Big'n"
    test.rarity = "Legendary"
    test.rarity_boost(test.rarity)
    test.assign_moves(test.type)

    print(test)

    test.add_experience(260000/4)
    print(f"LVl: {test.level} \nEXP: {test.experience} \nNeeded: {test.experience_needed}\n")

    print(test)

def main9():
    m = Mon()

    m.name = "Prestiger"
    m.type = [Type("Fire", "Explosion")]
    m.assign_moves(m.type)
    m.moves[0] = Move.get(m.type, "Explosive Burst")
    print(m)
    total = 0
    for i in range(5):
        total += m.moves[0].prestige.experience_needed
        attempts = m.moves[0].prestige.experience_needed / 5
        iterations = m.moves[0].prestige.experience_needed / 15
        hits = m.moves[0].prestige.experience_needed / (50 * m.moves[0].iterations)
        print(f"Current needed: {m.moves[0].prestige.experience_needed} \n\tAs attempts: {attempts}\n\tAs successful iterations: {iterations}\n\tAs successful chain-hits: {hits}\n\t")
        m.moves[0].prestige.add_experience(m.moves[0], m.moves[0].prestige.experience_needed)
        print(m.moves[0])
        print(f"{m.moves[0].prestige.experience} {m.moves[0].prestige.experience_needed}")

    attempts_ = total / 5
    iterations_ = total / 15
    hits_ = total / (50 * 3)
    print(f"Total needed: {total} \n\tAs attempts: {attempts_}\n\tAs successful iterations: {iterations_}\n\tAs successful chain-hits: {hits_}\n\t")
    m.moves[0].hit_probabilities()
    m.moves[0].move_statistics()

def main10():
    m = Mon()

    m.name = "Prestiger"
    m.type = [Type("Earth", None)]
    m.assign_moves(m.type)
    m.moves[0] = Move.get(m.type, "Pebble")
    print(m)
    total = 0
    for i in range(5):
        total += m.moves[0].prestige.experience_needed
        attempts = m.moves[0].prestige.experience_needed / 5
        iterations = m.moves[0].prestige.experience_needed / 15
        hits = m.moves[0].prestige.experience_needed / (50 * m.moves[0].iterations)
        print(f"Current needed: {m.moves[0].prestige.experience_needed} \n\tAs attempts: {attempts}\n\tAs successful iterations: {iterations}\n\tAs successful chain-hits: {hits}\n\t")
        m.moves[0].prestige.add_experience(m.moves[0], m.moves[0].prestige.experience_needed)
        print(m.moves[0])
        print(f"{m.moves[0].prestige.experience} {m.moves[0].prestige.experience_needed}")

    attempts_ = total / 5
    iterations_ = total / 15
    hits_ = total / (50 * 3)
    print(f"Total needed: {total} \n\tAs attempts: {attempts_}\n\tAs successful iterations: {iterations_}\n\tAs successful chain-hits: {hits_}\n\t")
    m.moves[0].hit_probabilities1()
    m.moves[0].move_statistics()

    #print(m)

def main14():
    m = Mon()

    m.name = "Prestiger"
    m.type = [Type("Nature", None)]
    m.assign_moves(m.type)
    m.moves[0] = Move.get(m.type, "Acorn Fury")
    print(m)
    total = 0
    for i in range(5):
        total += m.moves[0].prestige.experience_needed
        attempts = m.moves[0].prestige.experience_needed / 5
        iterations = m.moves[0].prestige.experience_needed / 15
        hits = m.moves[0].prestige.experience_needed / (50 * m.moves[0].iterations)
        print(f"Current needed: {m.moves[0].prestige.experience_needed} \n\tAs attempts: {attempts}\n\tAs successful iterations: {iterations}\n\tAs successful chain-hits: {hits}\n\t")
        m.moves[0].prestige.add_experience(m.moves[0], m.moves[0].prestige.experience_needed)
        print(m.moves[0])
        print(f"{m.moves[0].prestige.experience} {m.moves[0].prestige.experience_needed}")
        m.moves[0].hit_probabilities()
        m.moves[0].move_statistics()

    attempts_ = total / 5
    iterations_ = total / 15
    hits_ = total / (50 * 3)
    print(f"Total needed: {total} \n\tAs attempts: {attempts_}\n\tAs successful iterations: {iterations_}\n\tAs successful chain-hits: {hits_}\n\t")

def main11():
    c = Rubix()
    print(c)

    for fc in c.faces:
        print(fc)

def main13():
    m1 = Mon()
    m1.name = "Prestiger"
    m1.type = [Type("Fire", "Explosion")]
    m1.assign_moves(m1.type)
    m1.moves[0] = Move.get(m1.type, "Explosive Burst")
    for i in range(5):
        m1.moves[0].prestige.add_experience(m1.moves[0], m1.moves[0].prestige.experience_needed)

    m2 = Mon()

    print(m1)
    print(m2)

    m1.moves[0].use(m1, m2)

    print(m1)
    print(m2)

def main15():
    m1 = Mon()
    m1.name = "Prestiger"
    m1.type = [Type("Nature", None)]
    m1.assign_moves(m1.type)
    m1.moves[0] = Move.get(m1.type, "Acorn Fury")
    for i in range(100):
        m1.add_experience(m1.experience_needed)
    for i in range(5):
        i
        #m1.moves[0].prestige.add_experience(m1.moves[0], m1.moves[0].prestige.experience_needed)

    m2 = Mon()
    m2.rarity = "Omega" 
    m2.rarity_boost(m2.rarity)   
    m2.assign_moves(m2.type)
    for i in range(100):
        m2.add_experience(m2.experience_needed)
    m2_def = m2.defense
    m2.defense = 0
    m2_hp = m2.health
    m2.health = 1000000

    print(m1)
    print(m2)
    
    m1.moves[0].hit_probabilities()
    m1.moves[0].move_statistics()

    dmg_sum = 0
    uses = 190
    xp_sum = 0
    for i in range(uses):
        curr_hp = m2.health
        curr_xp = m1.moves[0].prestige.experience
        m1.moves[0].use(m1, m2)
        dmg_sum += curr_hp - m2.health
        xp_sum += m1.moves[0].prestige.experience - curr_xp if m1.moves[0].prestige.experience - curr_xp > 0 else curr_xp
        print(f"{m1.moves[0].prestige.experience} {m1.moves[0].prestige.experience_needed}")
    print(f"{m1.moves[0].name} did {dmg_sum} damage in {uses} uses! ({dmg_sum / 100 * 120 / 3600 / 8} days | {xp_sum / (dmg_sum / 100 * 120 / 3600 / 8 * 24)} XP / Hour)")

    m2.defense = m2_def
    m2.health = m2_hp

    print(m1)
    print(m2)

def main16():
    m1 = Mon()
    m1.name = "Prestiger"
    m1.type = [Type("Fire", "Explosion")]
    m1.assign_moves(m1.type)
    m1.moves[0] = Move.get(m1.type, "Explosive Burst")
    for i in range(100):
        m1.add_experience(m1.experience_needed)
    for i in range(5):
        i
        #m1.moves[0].prestige.add_experience(m1.moves[0], m1.moves[0].prestige.experience_needed)

    m2 = Mon()
    m2.rarity = "Omega" 
    m2.rarity_boost(m2.rarity)   
    m2.assign_moves(m2.type)
    for i in range(100):
        m2.add_experience(m2.experience_needed)
    m2_def = m2.defense
    m2.defense = 0
    m2_hp = m2.health
    m2.health = 1000000

    print(m1)
    print(m2)
    
    m1.moves[0].hit_probabilities()
    m1.moves[0].move_statistics()

    dmg_sum = 0
    uses = 817
    xp_sum = 0
    for i in range(uses):
        curr_hp = m2.health
        curr_xp = m1.moves[0].prestige.experience
        m1.moves[0].use(m1, m2)
        dmg_sum += curr_hp - m2.health
        xp_sum += m1.moves[0].prestige.experience - curr_xp if m1.moves[0].prestige.experience - curr_xp > 0 else curr_xp
        print(f"{m1.moves[0].prestige.experience} {m1.moves[0].prestige.experience_needed}")
    print(f"{m1.moves[0].name} did {dmg_sum} damage in {uses} uses! ({dmg_sum / 100 * 120 / 3600 / 8} days | {xp_sum / (dmg_sum / 100 * 120 / 3600 / 8 * 24)} XP / Hour)")

    m2.defense = m2_def
    m2.health = m2_hp

    print(m1)
    print(m2)

def main17():
    m1 = Mon()
    m1.name = "Prestiger"
    m1.type = [Type("Earth", None)]
    m1.assign_moves(m1.type)
    m1.moves[0] = Move.get(m1.type, "Pebble")
    for i in range(100):
        m1.add_experience(m1.experience_needed)
    for i in range(5):
        i
        #m1.moves[0].prestige.add_experience(m1.moves[0], m1.moves[0].prestige.experience_needed)

    m2 = Mon()
    m2.rarity = "Omega" 
    m2.rarity_boost(m2.rarity)   
    m2.assign_moves(m2.type)
    for i in range(100):
        m2.add_experience(m2.experience_needed)
    m2_def = m2.defense
    m2.defense = 0
    m2_hp = m2.health
    m2.health = 1000000

    print(m1)
    print(m2)
    
    m1.moves[0].hit_probabilities()
    m1.moves[0].move_statistics()

    dmg_sum = 0
    uses = 350
    xp_sum = 0
    for i in range(uses):
        curr_hp = m2.health
        curr_xp = m1.moves[0].prestige.experience
        m1.moves[0].use(m1, m2)
        dmg_sum += curr_hp - m2.health
        xp_sum += m1.moves[0].prestige.experience - curr_xp if m1.moves[0].prestige.experience - curr_xp > 0 else curr_xp
        print(f"{m1.moves[0].prestige.experience} {m1.moves[0].prestige.experience_needed}")
    print(f"{m1.moves[0].name} did {dmg_sum} damage in {uses} uses! ({dmg_sum / 100 * 120 / 3600 / 8} days | {xp_sum / (dmg_sum / 100 * 120 / 3600 / 8 * 24)} XP / Hour)")

    m2.defense = m2_def
    m2.health = m2_hp

    print(m1)
    print(m2)

def main18():
    for i in range(100):
        attacker = Mon()
        defender = Mon()

        for tp in attacker.type:
            for tp_ in defender.type:
                if tp.is_strong_against(tp_) and not tp.is_weak_against(tp_):
                    print(f"{attacker.name}'s {tp} is {Tools.rgb(0, 255, 0, f'STRONG')} against {defender.name}'s {tp_}")
                elif not tp.is_strong_against(tp_) and tp.is_weak_against(tp_):
                    print(f"{attacker.name}'s {tp} is {Tools.rgb(255, 0, 0, f'WEAK')} against {defender.name}'s {tp_}")
                elif tp.is_strong_against(tp_) and tp.is_weak_against(tp_):
                    print(f"{attacker.name}'s {tp} is {Tools.rgb(0, 255, 0, f'STRONG')} and {Tools.rgb(255, 0, 0, f'WEAK')} against {defender.name}'s {tp_}")
                else:
                    print(f"{attacker.name}'s {tp} is {Tools.rgb(0, 0, 255, f'NEITHER')} strong nor weak against {defender.name}'s {tp_}")

def main19():
    a = Mon()
    a.rarity = "Legendary" 
    a.name = "Splode"
    a.type = [Type("Fire", "Explosion")]
    a.rarity_boost(a.rarity)   
    a.assign_moves(a.type)
    a.moves[0] = Move.get(a.type, "Explosive Burst")
    a.moves[1] = Move.get(a.type, "Supernova")
    xp_sum = 0
    for i in range(50):
        xp_sum += a.experience_needed
        a.add_experience(a.experience_needed)
        print(f"{a.level} {a.experience_needed} {xp_sum}\n"
              f"battles: {a.experience_needed / 100} \t\t{a.experience_needed / 50} \t\t{a.experience_needed / 25}\n"
              f"battles: {xp_sum / 100} \t\t{xp_sum / 50} \t\t{xp_sum / 25}\n")
    for i in range(5):
        a.moves[0].prestige.add_experience(a.moves[0], a.moves[0].prestige.experience_needed)

    print(a)

def main20():
    a = Mon()
    a.rarity = "Omega" 
    a.name = "Splode"
    a.type = [Type("Fire", "Explosion")]
    a.rarity_boost(a.rarity)   
    a.assign_moves(a.type)
    a.moves[0] = Move.get(a.type, "Explosive Burst")
    a.moves[1] = Move.get(a.type, "Supernova")
    a.adjust_level(10)
    a.moves[0].prestige.adjust_rank(a.moves[0], 5)

    d = Mon()
    d.rarity = "Omega" 
    d.name = "Trunk"
    d.type = [Type("Nature", None)]
    d.rarity_boost(d.rarity)   
    d.assign_moves(d.type)
    d.moves[0] = Move.get(d.type, "Acorn Fury")
    d.adjust_level(10)
    d.moves[0].prestige.adjust_rank(d.moves[0], 5)

    print(a)
    print(d)

    a.battle(d, False, 0.01, 0.05)

    print(a)
    print(d)

def main21():
    a = Mon()
    a.rarity = "Omega" 
    a.name = "Splode"
    a.type = [Type("Fire", "Explosion")]
    a.rarity_boost(a.rarity)   
    a.assign_moves(a.type)
    a.moves[0] = Move.get(a.type, "Explosive Burst")
    a.moves[1] = Move.get(a.type, "Supernova")
    #a.adjust_level(100)
    #a.moves[0].prestige.adjust_rank(a.moves[0], 5)

    d = Mon()
    #d.rarity = "Omega" 
    #d.name = "Trunk"
    #d.type = [Type("Nature", None)]
    #d.rarity_boost(d.rarity)   
    #d.assign_moves(d.type)
    #d.moves[0] = Move.get(d.type, "Acorn Fury")
    #d.adjust_level(100)
    #d.moves[0].prestige.adjust_rank(d.moves[0], 5)

    battles = 220
    wins = 0
    uses = 0
    for i in range(battles):
        uses += a.battle(d, a.moves[0], True, 0, 0)
        
        if a.health > 0 and a.stamina > 0:
            wins += 1
        
        a.health = a.max_health
        d.health = d.max_health
        a.stamina = a.max_stamina
        d.stamina = d.max_stamina

    print(a)
    print(f"{a.name} won: {wins} out of {battles} and used {a.moves[0].name} {uses} times. ({uses / battles})\n\n"
          f"{a.experience}")
    
def main22():
    a = Mon()
    a.rarity = "Legendary" 
    a.name = "Splode"
    a.type = [Type("Fire", "Explosion")]
    a.rarity_boost(a.rarity)   
    a.assign_moves(a.type)
    a.adjust_level(100)

    print(a)
    
def main23():
    """Weighted rarity testing"""
    num_trials = 10_000
    standard_counts = defaultdict(int)
    weighted_counts = defaultdict(int)

    for _ in range(num_trials):
        mon_standard = Mon()  # Uses default assign_rarity()
        mon_standard.rarity = mon_standard.assign_rarity()  # Uses default assign_rarity()
        
        mon_weighted = Mon()
        mon_weighted.rarity = mon_weighted.assign_rarity_weighted(minimum_rarity="Legendary")  # Override with weighted

        standard_counts[mon_standard.rarity] += 1
        weighted_counts[mon_weighted.rarity] += 1

    # Output results
    print(f"\n{'='*25} Rarity Distribution After {num_trials} Trials {'='*25}\n")
    print(f"{'Rarity':<10} | {'Standard':>10} | {'%':>6} || {'Weighted':>10} | {'%':>6}")
    print("-" * 60)

    rarities = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Ultra', 'Omega']
    for rarity in rarities:
        std_count = standard_counts[rarity]
        wgt_count = weighted_counts[rarity]
        std_pct = (std_count / num_trials) * 100
        wgt_pct = (wgt_count / num_trials) * 100
        print(f"{rarity:<10} | {std_count:>10} | {std_pct:>5.2f}% || {wgt_count:>10} | {wgt_pct:>5.2f}%")

    print("\nNote: Comparison uses default logic in both assign_rarity() and assign_rarity_weighted().")

def main24():
    num_trials = 10_000
    standard_counts = defaultdict(int)
    weighted_counts = defaultdict(int)

    # Define your custom weights (can include base types, sets, or subclassed strings)
    custom_type_weights = [
        ("Fire", 5),
        ("Explosion (Sub: Fire)", 3),
        ("Water", 22),
        ("Earth", 50),
        ("Nature", 20)
    ]
    
    for _ in range(num_trials):
        # Standard Mon with default type assignment
        mon_standard = Mon()
        mon_standard.types = Type.assign_types()

        # Weighted Mon with custom type assignment
        mon_weighted = Mon()
        mon_weighted.types = Type.assign_types_weighted()

        standard_key = " + ".join(sorted(str(t) for t in mon_standard.types))
        standard_counts[standard_key] += 1

        weighted_key = " + ".join(sorted(str(t) for t in mon_weighted.types))
        weighted_counts[weighted_key] += 1

    # Get all unique types for display
    all_types = sorted(set(standard_counts.keys()) | set(weighted_counts.keys()))

    print(f"\n{'='*25} Type Distribution After {num_trials} Trials {'='*25}\n")
    print(f"{'Type':<30} | {'Standard':>10} | {'%':>6} || {'Weighted':>10} | {'%':>6}")
    print("-" * 80)

    for t in all_types:
        std_count = standard_counts[t]
        wgt_count = weighted_counts[t]
        std_pct = (std_count / num_trials) * 100
        wgt_pct = (wgt_count / num_trials) * 100
        print(f"{t:<30} | {std_count:>10} | {std_pct:>5.2f}% || {wgt_count:>10} | {wgt_pct:>5.2f}%")

    print("\nNote: Output reflects one or more types per Mon. Percentages may exceed 100% total.")

def main25():
    from collections import defaultdict

    num_trials = 10_000
    standard_counts = defaultdict(int)
    biased_counts = defaultdict(int)
    standard_total = 0
    biased_total = 0

    def get_level_range(level):
        """Helper to bucket levels into ranges of 10."""
        upper = ((level - 1) // 10 + 1) * 10
        lower = upper - 9
        return f"{lower:02d}-{upper:02d}"

    for _ in range(num_trials):
        # Standard Mon with no bias
        level_standard = Mon.assign_random_level(max_level=100, bias_factor=0.5)
        standard_total += level_standard
        standard_counts[get_level_range(level_standard)] += 1

        # Biased Mon with favor toward higher levels
        level_biased = Mon.assign_random_level(max_level=100, bias_factor=1.3)
        biased_total += level_biased
        biased_counts[get_level_range(level_biased)] += 1

    all_ranges = sorted(set(standard_counts.keys()) | set(biased_counts.keys()), key=lambda x: int(x.split("-")[0]))

    print(f"\n{'='*25} Level Distribution After {num_trials} Trials {'='*25}\n")
    print(f"{'Level Range':<15} | {'Standard':>10} | {'%':>6} || {'Biased':>10} | {'%':>6}")
    print("-" * 70)

    for r in all_ranges:
        std_count = standard_counts[r]
        bia_count = biased_counts[r]
        std_pct = (std_count / num_trials) * 100
        bia_pct = (bia_count / num_trials) * 100
        print(f"{r:<15} | {std_count:>10} | {std_pct:>5.2f}% || {bia_count:>10} | {bia_pct:>5.2f}%")

    mean_standard = standard_total / num_trials
    mean_biased = biased_total / num_trials

    print("\n" + "-" * 70)
    print(f"{'Mean Level':<15} | {mean_standard:>10.2f}       || {mean_biased:>10.2f}")
    print("\nNote: Bias factor shifts distribution toward higher levels (e.g., 0.5 vs. 1.3).")

def main26():
    m = Mon()
    m.rarity = m.assign_rarity_weighted(minimum_rarity="Legendary") # assign_rarity_weighted applies rarity_boost() automatically
    #m.type = Type.assign_types_weighted()
    m.type = [Type("Fire", "Explosion")]
    m.name = m.make_name()
    m.assign_moves(m.type)
    m.moves[0] = Move.get(m.type, "Explosive Burst")
    m.adjust_level(Mon.assign_random_level(max_level=1000, bias_factor=2))

    print(m)

    a = Mon()
    a.rarity = a.assign_rarity_weighted(minimum_rarity="Legendary") # assign_rarity_weighted applies rarity_boost() automatically
    a.type = [Type("Nature", None)]
    a.name = a.make_name()
    a.assign_moves(a.type)
    a.adjust_level(Mon.assign_random_level(max_level=1000, bias_factor=2))
    a_def = a.defense
    a.defense = 0

    print(a)

    m.battle(a, is_random=False, typewriter_delay=0, timing=0)

def main27():
    a = Mon()

    print(a)

def main28():
    class Tester:
        def tame_chance(rarity: int, level: int, 
                        base_chance: float = 1.0, 
                        rarity_factor: float = 0.35, 
                        level_factor: float = 0.03) -> float:
            """
            Computes the chance to tame a Mon based on rarity and level.
            
            Parameters:
                rarity (int): The Mon's rarity (1 = easiest, 7 = hardest)
                level (int): The Mon's level (1 = lowest)
                base_chance (float): Max tame chance (1.0 = 100%)
                rarity_factor (float): How strongly rarity reduces tame chance
                level_factor (float): How strongly level reduces tame chance
            
            Returns:
                float: The taming chance (0.0 to 1.0)
            """
            rarity_penalty = math.exp(rarity_factor * (rarity - 1))
            level_penalty = math.exp(level_factor * (level - 1))
            
            chance = base_chance / (rarity_penalty * level_penalty)
            return min(max(chance, 0.0), 1.0)
        
        @staticmethod
        def tame_chance_2(rarity, level, base=0.95, rarity_decay=1.6, level_decay=0.04):
            """
            Returns a taming probability between 0 and 1.

            Parameters:
            - rarity: int (1 = Common, ..., 7 = Omega)
            - level: int (1 to 100)
            - base: base probability multiplier (e.g. 0.95 for high base chance)
            - rarity_decay: how much harder each rarity step is (exponential factor)
            - level_decay: per-level penalty (linear or exponential)
            """
            rarity_penalty = rarity_decay ** (rarity - 1)
            level_penalty = 1 - (level_decay * (level - 1))
            level_penalty = max(level_penalty, 0.01)  # avoid zero or negative chances

            chance = base / rarity_penalty * level_penalty
            return max(min(chance, 1.0), 0.0001)  # clamp between 0.0001 and 1.0

        @staticmethod
        def assign_rarity_weighted(
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
            return chosen
        
    num_trials = 10_000
    buckets = defaultdict(list)

    def get_bucket(rarity_int, level):
        level_range = f"{((level - 1) // 10) * 10 + 1:02d}-{((level - 1) // 10) * 10 + 10:02d}"
        return (f"R{rarity_int}", level_range)

    for _ in range(num_trials):
        rarity_str = Tester.assign_rarity_weighted(minimum_rarity="Legendary")  # returns a string like 'Uncommon'
        rarity_int = Mon.rarities[rarity_str]         # convert to integer 1–7
        level = Mon.assign_random_level(max_level=100, bias_factor=2.9)
        tame_chance = Tester.tame_chance_2(rarity_int, level, base=0.9999, rarity_decay=1.8, level_decay=0.009)
        bucket = get_bucket(rarity_int, level)
        buckets[bucket].append(tame_chance)

    all_keys = sorted(buckets.keys(), key=lambda x: (int(x[0][1:]), int(x[1].split("-")[0])))

    print(f"\n{'='*20} Tame Chance Diagnostic After {num_trials} Trials {'='*20}\n")
    print(f"{'Rarity':<8} | {'Level Range':<11} | {'Trials':>7} | {'Mean %':>7} | {'Min %':>7} | {'Max %':>7}")
    print("-" * 65)

    for key in all_keys:
        values = buckets[key]
        mean = sum(values) / len(values) * 100
        min_val = min(values) * 100
        max_val = max(values) * 100
        print(f"{key[0]:<8} | {key[1]:<11} | {len(values):>7} | {mean:>6.2f}% | {min_val:>6.2f}% | {max_val:>6.2f}%")

    print("\nNote: Rarity 1 + Level 1 should yield close to 100%. Rarity 7 + high level should be <1%.")

def main29():
    f = Effect(
        name="Burn", 
        effect_type="chip-damage",
        target_type="Mon", 
        target_self=False, 
        target_attribute="health", 
        value=-1, 
        stackable=True, 
        duration=4, 
        trigger="on_hit", 
        trigger_chance=1.0
    )

    f.export(path="Game/data/effects/effects.json")

def main30():
    m = Mon(
        name="Test Monass"
    )

    move = Move.get([Type("Fire", None)], "Inferno")

    print(m)
    print(f"Active Effects: {[e.name for e in m.effects]}")
    
    for _ in range(6):
        move.apply_effects(user=m, target=m)

        print(f"\nAfter apply_effects:")
        print(f"{m.name} HP: {m.health}")
        print(f"Active Effects: {[e.name for e in m.effects]}")

        # Trigger effects like chip damage (e.g., Burn)
        m.trigger_effects(trigger_event="on_hit")

        print(f"\nAfter trigger_effects:")
        print(f"{m.name} HP: {m.health}")
        print(f"Active Effects: {[e.name for e in m.effects]}")

        # Update durations
        m.update_effects()

        print(f"\nAfter update_effects:")
        print(f"{m.name} HP: {m.health}")
        print(f"Remaining durations: {[e.duration_remaining for e in m.effects]}")

def main31():
    m = Mon(name="Test Mon", tp=[Type("Fire", None)])
    m.rarity = m.assign_rarity_weighted(minimum_rarity="Omega")

    move = Move.get([Type("Fire", None)], "Inferno")

    m.replace_move(m.moves[0], move)

    a = Mon(tp=[Type("Nature", None)])
    a.rarity = a.assign_rarity_weighted(minimum_rarity="Omega")

    m.battle(a, attacker_use_move=move, typewriter_delay=0.005, timing=0)

def main32():
    m = Mon(name="Test Mon", tp=[Type("Magic", None)])
    m.rarity = m.assign_rarity_weighted(minimum_rarity="Omega")

    move = Move.get([Type("Magic", None)], "Accuracy Hex")

    m.replace_move(m.moves[0], move)

    a = Mon(tp=[Type("Magic", None)])
    a.rarity = a.assign_rarity_weighted(minimum_rarity="Omega")

    m.battle(a, attacker_use_move=move, typewriter_delay=0.005, timing=0)

def main33():
    m = Mon(name="Test Mon", tp=[Type("Magic", None)])
    m.rarity = m.assign_rarity_weighted(minimum_rarity="Omega")

    move = Move.get([Type("Magic", None)], "Magi-Flash Burst")
    move = Move.get([Type("Magic", None)], "Magi-Flash Burst")

    m.replace_move(m.moves[0], move)

    a = Mon(tp=[Type("Magic", None)])
    a.rarity = a.assign_rarity_weighted(minimum_rarity="Omega")

    m.battle(a, is_random=False, typewriter_delay=0.005, timing=0)
    #m.battle(a, attacker_use_move=move, typewriter_delay=0.005, timing=0)

def main34():
    def get_boost_range(boost: float) -> str:
        """Buckets attack boosts into 0.05-wide ranges."""
        bucket_min = int((boost - 0.01) // 0.01 + 1) * 0.01
        #bucket_min = int((boost - 0.05) // 0.05 + 1) * 0.05
        bucket_max = bucket_min + 0.0099  # Slightly under next to keep range tight
        #bucket_max = bucket_min + 0.049  # Slightly under next to keep range tight
        return f"{bucket_min:.2f}-{bucket_max:.2f}"
    
    def map_floored_boost_value(boost: float) -> str:
        """Maps a floored attack boost value (e.g., 0.01) to a string label for histogram output."""
        return f"{boost:.2f}"

    num_trials = 10000
    min_val = 0.00
    max_val = 0.051

    uniform_counts = defaultdict(int)
    biased_counts = defaultdict(int)
    uniform_values = []
    biased_values = []

    for _ in range(num_trials):
        u_val = Mon.assign_attack_boost(dist=False, min_val=min_val, max_val=max_val)
        b_val = Mon.assign_attack_boost(dist=True, bias=.01, min_val=min_val, max_val=max_val, squish=0.005)
        b_val = Tools.floor_to_nearest_float(b_val, 0.01)
        print(b_val)

        uniform_values.append(u_val)
        biased_values.append(b_val)

        uniform_counts[map_floored_boost_value(u_val)] += 1
        #uniform_counts[get_boost_range(u_val)] += 1
        biased_counts[map_floored_boost_value(b_val)] += 1
        #biased_counts[get_boost_range(b_val)] += 1

    all_ranges = sorted(set(uniform_counts.keys()) | set(biased_counts.keys()),
                        key=lambda r: float(r.split("-")[0]))

    uniform_mean = sum(uniform_values) / num_trials
    biased_mean = sum(biased_values) / num_trials

    print(f"\n{'='*25} Attack Boost Distribution After {num_trials} Trials {'='*25}\n")
    print(f"{'Boost Range':<13} | {'Uniform':>8} | {'%':>6} || {'Biased':>8} | {'%':>6}")
    print("-" * 65)

    for r in all_ranges:
        u_count = uniform_counts[r]
        b_count = biased_counts[r]
        print(f"{r:<13} | {u_count:>8} | {u_count / num_trials * 100:>6.2f} || {b_count:>8} | {b_count / num_trials * 100:>6.2f}")

    print("\nSummary Stats:")
    print(f"{'':<13} | {'Uniform':>8} || {'Biased':>8}")
    print(f"{'Mean':<13} | {uniform_mean:>8.3f} || {biased_mean:>8.3f}")
    print(f"{'Min':<13} | {min(uniform_values):>8.3f} || {min(biased_values):>8.3f}")
    print(f"{'Max':<13} | {max(uniform_values):>8.3f} || {max(biased_values):>8.3f}")

def main35():
    p1 = Player("1")
    p2 = Player("2")

    for p in (p1, p2):
        for _ in range(3):
            m = Mon()
            for x in m.moves:
                m.moves.remove(x)
            m.rarity = m.assign_rarity_weighted(minimum_rarity="Legendary")
            for _ in range(m.moves_limit - 1):
                m.learn_move()
            for mv in m.moves:
                if mv.prestige:
                    mv.prestige.adjust_rank(mv, mv.prestige.max_rank)
            p.add_mons([m])
            #p.mons.extend([m])

    """
    for p in (p1, p2):
        for m in p.mons:
            print(m)

        print("x" * 230)
    """

    Game.versus(p1, p2)

def main36():
    m = Mon(name="Test Mon", tp=[Type("Fire", None)])
    m.rarity = m.assign_rarity_weighted(minimum_rarity="Omega")
    #m.adjust_level(200, True)

    move = Move.get([Type("Fire", None)], "Solar Flare")
    move2 = Move.get([Type("Fire", None)], "Plasma Wave")

    m.replace_move(m.moves[0], move)
    m.replace_move(m.moves[1], move2)

    a = Mon(tp=[Type("Air", None)])
    a.rarity = a.assign_rarity_weighted(minimum_rarity="Omega")
    #a.adjust_level(200, True)

    print(f"{m.name:>20} - L{m.level:<3}: H{m.health:<4} D{m.defense:<4} | {a.name:>20} - L{a.level:<3}: H{a.health:<4} D{a.defense:<4}")

    m.battle(a, is_random=False, typewriter_delay=0.005, timing=0)
    #m.battle(a, attacker_use_move=move, typewriter_delay=0.005, timing=0)

def main37():
    m = Mon(name="Test Mon", tp=[Type("Water", "Ice")])
    m.rarity = m.assign_rarity_weighted(minimum_rarity="Omega")
    m.adjust_level(200, True)

    move = Move.get([Type("Water", "Ice")], "Iceburst")
    move2 = Move.get([Type("Water", "Ice")], "Absolute Zero")
    move3 = Move.get([Type("Water", "Ice")], "Hailstorm")

    m.replace_move(m.moves[0], move)
    m.replace_move(m.moves[1], move2)
    m.replace_move(m.moves[2], move3)

    for mv in m.moves:
        if mv.prestige:
            mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

    a = Mon(tp=[Type("Air", None)])
    a.rarity = a.assign_rarity_weighted(minimum_rarity="Omega")
    a.adjust_level(200, True)

    print(f"{m.name:>20} - L{m.level:<3}: H{m.health:<4} D{m.defense:<4} | {a.name:>20} - L{a.level:<3}: H{a.health:<4} D{a.defense:<4}")

    m.battle(a, is_random=False, typewriter_delay=0.005, timing=0)
    #m.battle(a, attacker_use_move=move, typewriter_delay=0.005, timing=0)

def main37():
    m = Mon(name="Test Mon", tp=[Type("Fire", None)])
    m.rarity = m.assign_rarity_weighted(minimum_rarity="Omega")
    m.adjust_level(200, True)

    move = Move.get([Type("Fire", None)], "Fireshot")

    m.replace_move(m.moves[0], move)

    for mv in m.moves:
        if mv.prestige:
            mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

    a = Mon(tp=[Type("Air", None)])
    a.rarity = a.assign_rarity_weighted(minimum_rarity="Omega")
    a.adjust_level(200, True)

    print(f"{m.name:>20} - L{m.level:<3}: H{m.health:<4} D{m.defense:<4} | {a.name:>20} - L{a.level:<3}: H{a.health:<4} D{a.defense:<4}")

    m.battle(a, is_random=False, typewriter_delay=0.005, timing=0)
    #m.battle(a, attacker_use_move=move, typewriter_delay=0.005, timing=0)

def main38():
    p = Player()
    for i in range(6):
        m = Mon(name=f"Flamz {i}", tp=[Type("Fire", None)])
        m.rarity = m.assign_rarity_weighted(minimum_rarity="Common")
        lvl = m.level
        atk = m.attack_boost
        Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Fire", None)], "Fireshot")
        #move2 = Move.get([Type("Fire", None)], "Solar Flare")

        m.replace_move(m.moves[0], move)
        #m.replace_move(m.moves[1], move2)

        m.moves[0].prestige.adjust_rank(m.moves[0], m.moves[0].prestige.max_rank)

        p.add_mons([m], skip_name=True)

    """
    num_encs = 150

    for _ in range(num_encs):
        #m.battle(opp, is_random=False, typewriter_delay=0.005, timing=0)
        Game.mon_encounter(p, player_use_mon=m, skip_battle=True, skip_tame=True)
        m.health = m.max_health
    """
    
    for _ in range(1):
        #Game.mon_encounter(p, player_use_mon=m, skip_battle=False, skip_tame=True)
        opp_mons = []
        for _ in range(1):
            opp_tp = [random.choice([Type.parse(tps) for tps in Type.strong_against[str(m.type[0])]])]
            opp_m = Mon(tp=opp_tp)
            opp_m.rarity = opp_m.assign_rarity_weighted(minimum_rarity="Omega")
            opp_m.adjust_level(300, suppress_output=True)
            for mv in opp_m.moves:
                if mv.prestige:
                    mv.prestige.adjust_rank(mv, mv.prestige.max_rank)
            opp_mons.append(opp_m)
        p2 = Player(mons=opp_mons)
        Game.versus(p, p2, 6)

    print(m)
    diff = m.attack_boost - atk
    level_diff = m.level - lvl
    ratio = diff / level_diff if level_diff != 0 else "N/A"

    Tools.text(f"{lvl} -> {m.level} || {atk} -> {m.attack_boost} = {diff} | {ratio}\n", params=Mon.rarity_effects[m.rarity])
    print(f"{move.prestige.experience}/{move.prestige.experience_needed}")

def main40():
    """Pearl testing."""

    def assign_pearl_for_rarity(rarity: str) -> int:
        """Returns 0 (None), 1 (White), or 2 (Black) based on the rarity and weighted chances."""
        rarities_pearl_weights = {
            "Common":                        (1 / 256, 1 / 1024),
            ("Uncommon", "Rare"):           (1 / 128, 1 / 512),
            "Epic":                         (1 / 32, 1 / 128),
            ("Legendary", "Ultra", "Omega"): (1 / 8, 1 / 16),
        }

        for rarity_group, (white_chance, black_chance) in rarities_pearl_weights.items():
            group = (rarity_group,) if isinstance(rarity_group, str) else rarity_group
            if rarity in group:
                if random.random() < black_chance:
                    return 2  # Black
                elif random.random() < white_chance:
                    return 1  # White
                else:
                    return 0
        return 0  # Default fallback

    # Rarities to test and counts
    test_rarities = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Ultra", "Omega"]
    num_trials = 10000
    results = {rarity: defaultdict(int) for rarity in test_rarities}

    for rarity in test_rarities:
        for _ in range(num_trials):
            result = assign_pearl_for_rarity(rarity)
            results[rarity][result] += 1

    # Pearl label map (optional)
    pearls = {0: "None", 1: "White", 2: "Black"}

    # Display results
    print(f"\n{'='*30} Pearl Assignment Test ({num_trials} per rarity) {'='*30}\n")
    print(f"{'Rarity':<10} | {'None':>8} | {'%':>6} | {'White':>8} | {'%':>6} | {'Black':>8} | {'%':>6}")
    print("-" * 70)

    for rarity in test_rarities:
        none = results[rarity][0]
        white = results[rarity][1]
        black = results[rarity][2]

        none_pct = (none / num_trials) * 100
        white_pct = (white / num_trials) * 100
        black_pct = (black / num_trials) * 100

        print(f"{rarity:<10} | {none:>8} | {none_pct:>6.2f} | {white:>8} | {white_pct:>6.2f} | {black:>8} | {black_pct:>6.2f}")

def main41():
    """Pearlize testing"""
    for _ in range(10):
        color = Mon.pearls[random.randint(1,2)].split()[0]

        Mon.pearlize(color)
        print(f" {color}")

def main39():
    """Raid testing"""
    p = Player()
    p.add_health_potion(50)
    for i in range(6):
        m = Mon(name=f"Flamz {i}", tp=[Type("Fire", None)], rarity="Legendary")
        lvl = m.level
        atk = m.attack_boost
        Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Fire", None)], "Fireshot")
        #move2 = Move.get([Type("Fire", None)], "Solar Flare")

        m.replace_move(m.moves[0], move)
        #m.replace_move(m.moves[1], move2)

        m.moves[0].prestige.adjust_rank(m.moves[0], m.moves[0].prestige.max_rank)

        p.add_mons([m])

    Game.legendary_encounter(p)

    print(*p.mons, sep="\n")

def main42():
    """Drain effect testing"""
    p = Player()
    p.add_health_potion(50)
    for i in range(6):
        m = Mon(name=f"Magi {i}", tp=[Type("Magic", None)], rarity="Legendary")
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Magic", None)], "Accuracy Hex")
        move2 = Move.get([Type("Magic", None)], "Reflect")

        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)

        for mv in m.moves:
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        p.add_mons([m])

    Game.legendary_encounter(p)

    print(*p.mons, sep="\n")

def main43():
    """Brain damage effect testing"""
    p = Player()
    p.add_health_potion(50)
    for i in range(6):
        m = Mon(name=f"Iron {i}", tp=[Type("Earth", "Metal")], rarity="Omega")
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Earth", "Metal")], "Clang")
        move2 = Move.get([Type("Earth", "Metal")], "Gargantua Impact")
        move3 = Move.get([Type("Earth", "Metal")], "Density")

        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)
        m.learn_move()
        m.replace_move(m.moves[2], move3)

        for mv in m.moves:
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        p.add_mons([m])

    Game.legendary_encounter(p)

    print(*p.mons, sep="\n")

def main43():
    """Enraged effect testing"""
    p = Player()
    p.add_health_potion(50)
    burner = Mon()
    for i in range(6):
        #m = Mon(name=f"Icy {i}", tp=[Type("Beast", "Reptilian")], rarity="Epic")
        m = Mon(name=f"Icy {i}", level=80, pearl=2, tp=[Type("Water", "Ice")], rarity="Omega")
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        #move = Move.get([Type("Beast", "Reptilian")], "Coiling Constrictor")
        #move2 = Move.get([Type("Beast", "Reptilian")], "Venomstrike")
        move = Move.get([Type("Water", "Ice")], "Iceburst")
        move2 = Move.get([Type("Water", "Ice")], "Flurry")

        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)
        #m.learn_move()
        #m.replace_move(m.moves[2], move3)

        for mv in m.moves:
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        p.add_mons([m])

    Game.legendary_encounter(p)

    print(*p.mons, sep="\n")

def main44():
    """Fire raid / water effects testing"""
    p = Player()
    p.add_health_potion(50)
    burner = Mon()
    for i in range(6):
        m = Mon(name=f"Soaks {i}", level=80, pearl=2, tp=[Type("Water", None)], rarity="Omega")
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Water", None)], "Water Burst")
        move2 = Move.get([Type("Water", None)], "Flood")
        move3 = Move.get([Type("Water", None)], "Tsunami")

        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)
        m.learn_move()
        m.replace_move(m.moves[2], move3)

        for mv in m.moves:
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        p.add_mons([m])

    Game.legendary_encounter(p)

    print(*p.mons, sep="\n")

def main45():
    """Photosythesis effect testing"""
    p = Player()
    p.add_health_potion(50)
    burner = Mon()
    for i in range(6):
        m = Mon(name=f"Root {i}", level=80, pearl=2, tp=[Type("Nature", None)], rarity="Omega")
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Nature", None)], "Acorn Fury")
        move2 = Move.get([Type("Nature", None)], "Photosythesis")
        #move3 = Move.get([Type("Water", None)], "Tsunami")

        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)
        #m.learn_move()
        #m.replace_move(m.moves[2], move3)
        
        del_mvs = []
        for i, mv in enumerate(m.moves):
            if i >= 2:
                del_mvs.append(mv)
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        for mv in del_mvs:
            m.moves.remove(mv)

        p.add_mons([m])

    Game.legendary_encounter(p)

    print(*p.mons, sep="\n")

def main45():
    """Surge effect testing"""
    p = Player()
    p.add_health_potion(50)
    burner = Mon()
    for i in range(6):
        m = Mon(name=f"Soaks {i}", level=100, pearl=2, tp=[Type("Water", None)], rarity=burner.assign_rarity_weighted(minimum_rarity="Omega"))
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Water", None)], "Water Burst")
        move2 = Move.get([Type("Water", None)], "Hydropulse")
        move3 = Move.get([Type("Water", None)], "Tsunami")


        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)
        m.learn_move()
        m.replace_move(m.moves[2], move3)
        
        del_mvs = []
        for i, mv in enumerate(m.moves):
            if i >= 3:
                del_mvs.append(mv)
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        for mv in del_mvs:
            m.moves.remove(mv)

        p.add_mons([m])

    Game.legendary_encounter(p)

    print(*p.mons, sep="\n")

def main47():
    p1 = Player("1")
    p2 = Player("2")

    burner = Mon()

    for p in (p1, p2):
        for _ in range(3):
            m = Mon(
                rarity = burner.assign_rarity_weighted(minimum_rarity="Legendary"), 
                level=burner.assign_random_level(bias_factor=2.0)
            )
            m.moves.clear()
            #print(*m.moves, sep="\n")
            for _ in range(m.moves_limit):
                m.learn_move(move_priority=(True, True, True))
            for mv in m.moves:
                if mv.prestige:
                    mv.prestige.adjust_rank(mv, mv.prestige.max_rank)
            p.add_mons([m])
            #p.mons.extend([m])

    """
    for p in (p1, p2):
        for m in p.mons:
            print(m)

        print("x" * 230)
    """

    Game.versus(p1, p2)

    print(*p1.mons, sep="\n")
    print(*p2.mons, sep="\n")

def main48():
    """Mon pack testing"""

    Game.mon_pack(pack_num=1, min_keep_rarity="Legendary")

def main46():
    """Surge effect testing 2"""
    p = Player()
    p.add_health_potion(50)
    burner = Mon()
    rand_rarity = [
        #"Common", 
        #"Uncommon", 
        #"Rare",
        "Epic",
        "Legendary",
        "Ultra",
        "Omega"
    ]
    for i in range(len(rand_rarity) * 3):
        #m = Mon(name=f"Soaks {i}", level=random.randint(50,70), pearl=0, tp=[Type("Air", None), Type("Water", None)], rarity=burner.assign_rarity_weighted(minimum_rarity="Omega"))
        m = Mon(
            name=f"Soaks {i}", 
            level=20, 
            pearl=i%3, 
            tp=[Type("Air", None), Type("Water", None)], 
            rarity=rand_rarity[i//3%len(rand_rarity)]
        )
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Air", None), Type("Water", None)], "Hurricane")
        move2 = Move.get([Type("Water", None)], "Hydropulse")
        move3 = Move.get([Type("Water", None)], "Tsunami")

        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)
        m.learn_move()
        if m.moves_limit >= 3:
            m.replace_move(m.moves[2], move3)
        
        del_mvs = []
        for i, mv in enumerate(m.moves):
            if i >= 3:
                del_mvs.append(mv)
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        for mv in del_mvs:
            m.moves.remove(mv)

        p.add_mons([m])

    #Game.mon_encounter(p, rarity=burner.assign_rarity_weighted(minimum_rarity="Rare"))
    Game.legendary_encounter(p, mon_num=len(rand_rarity) * 3)

    print(*p.mons, sep="\n")

def main49():
    """Volcanic type testing"""
    p = Player()
    p.add_health_potion(50)
    burner = Mon()
    rand_rarity = [
        #"Common", 
        #"Uncommon", 
        #"Rare",
        "Epic",
        "Legendary",
        "Ultra",
        "Omega"
    ]
    for i in range(len(rand_rarity) * 3):
        #m = Mon(name=f"Soaks {i}", level=random.randint(50,70), pearl=0, tp=[Type("Air", None), Type("Water", None)], rarity=burner.assign_rarity_weighted(minimum_rarity="Omega"))
        m = Mon(
            name=f"Lavy {i}", 
            level=20, 
            pearl=i%3, 
            tp=[Type("Earth", None), Type("Fire", None)], 
            rarity=rand_rarity[i//3%len(rand_rarity)]
        )
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Earth", None), Type("Fire", None)], "Volcanic Rock Splatter")
        move2 = Move.get([Type("Earth", None), Type("Fire", None)], "Krakatoa")
        move3 = Move.get([Type("z", None)], "Surge")

        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)
        m.learn_move()
        if m.moves_limit >= 3:
            m.replace_move(m.moves[2], move3)
        
        del_mvs = []
        for i, mv in enumerate(m.moves):
            if i >= 3:
                del_mvs.append(mv)
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        for mv in del_mvs:
            m.moves.remove(mv)

        p.add_mons([m])

    #Game.mon_encounter(p, rarity=burner.assign_rarity_weighted(minimum_rarity="Rare"))
    Game.legendary_encounter(p, mon_num=len(rand_rarity) * 3)

    print(*p.mons, sep="\n")

def main50():
    """New nature move testing"""
    p = Player()
    p.add_health_potion(50)
    burner = Mon()
    rand_rarity = [
        #"Common", 
        #"Uncommon", 
        #"Rare",
        "Epic",
        "Legendary",
        "Ultra",
        "Omega"
    ]
    for i in range(len(rand_rarity) * 3):
        #m = Mon(name=f"Soaks {i}", level=random.randint(50,70), pearl=0, tp=[Type("Air", None), Type("Water", None)], rarity=burner.assign_rarity_weighted(minimum_rarity="Omega"))
        m = Mon(
            name=f"Root {i}", 
            level=20, 
            pearl=i%3, 
            tp=[Type("Nature", None)], 
            rarity=rand_rarity[i//3%len(rand_rarity)]
        )
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Nature", None)], "Acorn Fury")
        move2 = Move.get([Type("Nature", None)], "Giant Sequoia Slam")
        move3 = Move.get([Type("Nature", None)], "Photosynthesis")
        move4 = Move.get([Type("z", None)], "Surge")

        print(m.name, m.rarity, m.moves_limit)

        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)
        m.learn_move()
        if m.moves_limit >= 3:
            m.replace_move(m.moves[2], move3)
        m.learn_move()
        if m.moves_limit >= 4:
            m.replace_move(m.moves[3], move4)
        
        del_mvs = []
        for i, mv in enumerate(m.moves):
            if i >= 2: # deleting excessive moves for less clutter
                del_mvs.append(mv)
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        for mv in del_mvs:
            m.moves.remove(mv)

        p.add_mons([m])

    #Game.mon_encounter(p, rarity=burner.assign_rarity_weighted(minimum_rarity="Rare"))
    Game.legendary_encounter(p, mon_num=len(rand_rarity) * 3)

    print(*p.mons, sep="\n")

def main51():
    """New air move jetstream blast testing"""
    p = Player()
    p.add_health_potion(50)
    burner = Mon()
    rand_rarity = [
        #"Common", 
        #"Uncommon", 
        #"Rare",
        "Epic",
        "Legendary",
        "Ultra",
        "Omega"
    ]
    for i in range(len(rand_rarity) * 3):
        #m = Mon(name=f"Soaks {i}", level=random.randint(50,70), pearl=0, tp=[Type("Air", None), Type("Water", None)], rarity=burner.assign_rarity_weighted(minimum_rarity="Omega"))
        m = Mon(
            name=f"Airy {i}", 
            level=20, 
            pearl=i%3, 
            tp=[Type("Air", None)], 
            rarity=rand_rarity[i//3%len(rand_rarity)]
        )
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Air", None)], "Jetstream Blast")
        move2 = Move.get([Type("z", None)], "Surge")
        move3 = Move.get([Type("Air", None)], "Vayu Vortex")
        move4 = Move.get([Type("Air", None)], "Supercell")

        print(m.name, m.rarity, m.moves_limit)

        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)
        m.learn_move()
        if m.moves_limit >= 3:
            m.replace_move(m.moves[2], move3)
        m.learn_move()
        if m.moves_limit >= 4:
            m.replace_move(m.moves[3], move4)
        
        del_mvs = []
        for i, mv in enumerate(m.moves):
            if i >= 4: # deleting excessive moves for less clutter
                del_mvs.append(mv)
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        for mv in del_mvs:
            m.moves.remove(mv)

        p.add_mons([m])

    #Game.mon_encounter(p, rarity=burner.assign_rarity_weighted(minimum_rarity="Rare"))
    Game.legendary_encounter(p, mon_num=len(rand_rarity) * 3)

    print(*p.mons, sep="\n")

def main52():
    """New magic move drain prestige testing"""
    p = Player()
    p.add_health_potion(50)
    burner = Mon()
    rand_rarity = [
        #"Common", 
        #"Uncommon", 
        #"Rare",
        "Epic",
        "Legendary",
        "Ultra",
        "Omega"
    ]
    for i in range(len(rand_rarity) * 3):
        #m = Mon(name=f"Soaks {i}", level=random.randint(50,70), pearl=0, tp=[Type("Air", None), Type("Water", None)], rarity=burner.assign_rarity_weighted(minimum_rarity="Omega"))
        m = Mon(
            name=f"Magy {i}", 
            level=20, 
            pearl=i%3, 
            tp=[Type("Magic", None)], 
            rarity=rand_rarity[i//3%len(rand_rarity)]
        )
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Magic", None)], "Draining Aura")
        move2 = Move.get([Type("z", None)], "Surge")
        move3 = Move.get([Type("Magic", None)], "Reflect")
        move4 = Move.get([Type("Magic", None)], "Health Charm")

        print(m.name, m.rarity, m.moves_limit)

        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)
        m.learn_move()
        if m.moves_limit >= 3:
            m.replace_move(m.moves[2], move3)
        m.learn_move()
        if m.moves_limit >= 4:
            m.replace_move(m.moves[3], move4)
        
        del_mvs = []
        for i, mv in enumerate(m.moves):
            if i >= 4: # deleting excessive moves for less clutter
                del_mvs.append(mv)
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        for mv in del_mvs:
            m.moves.remove(mv)

        p.add_mons([m])

    #Game.mon_encounter(p, rarity=burner.assign_rarity_weighted(minimum_rarity="Rare"))
    Game.legendary_encounter(p, mon_num=len(rand_rarity) * 3)

    print(*p.mons, sep="\n")

def main53():
    """dual-typing effectiveness testing"""
    p = Player()
    p.add_health_potion(50)
    burner = Mon()
    rand_rarity = [
        #"Common", 
        #"Uncommon", 
        #"Rare",
        "Epic",
        "Legendary",
        "Ultra",
        "Omega"
    ]
    for i in range(len(rand_rarity) * 3):
        #m = Mon(name=f"Soaks {i}", level=random.randint(50,70), pearl=0, tp=[Type("Air", None), Type("Water", None)], rarity=burner.assign_rarity_weighted(minimum_rarity="Omega"))
        m = Mon(
            name=f"Magy {i}", 
            level=20, 
            pearl=i%3, 
            tp=[Type("Air", None), Type("Fire", None)], 
            rarity=rand_rarity[i//3%len(rand_rarity)]
        )
        lvl = m.level
        atk = m.attack_boost
        #Tools.text(f"{m.rarity} {m.level} {m.attack_boost}\n", params=Mon.rarity_effects[m.rarity])

        move = Move.get([Type("Air", None), Type("Fire", None)], "Heatwave")
        move2 = Move.get([Type("z", None)], "Surge")
        move3 = Move.get([Type("Air", None)], "Vayu Vortex")
        move4 = Move.get([Type("Fire", None)], "Fireshot")

        print(m.name, m.rarity, m.moves_limit)

        m.replace_move(m.moves[0], move)
        m.replace_move(m.moves[1], move2)
        m.learn_move()
        if m.moves_limit >= 3:
            m.replace_move(m.moves[2], move3)
        m.learn_move()
        if m.moves_limit >= 4:
            m.replace_move(m.moves[3], move4)
        
        del_mvs = []
        for i, mv in enumerate(m.moves):
            if i >= 4: # deleting excessive moves for less clutter
                del_mvs.append(mv)
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)

        for mv in del_mvs:
            m.moves.remove(mv)

        p.add_mons([m])

    #Game.mon_encounter(p, rarity=burner.assign_rarity_weighted(minimum_rarity="Rare"))
    Game.legendary_encounter(p, mon_num=len(rand_rarity) * 3)

    print(*p.mons, sep="\n")

def main12():
    """Game testing"""
    #Game.start()
    p = Player("")
    p = Player.parse("2025-05-22_03-09-15_Kai.json") # 2025-05-23_15-30-32_Tester.json
    Game.load_checkpoint(p, p.checkpoint_needed)

def main54():
    """Best moves by type"""

    ## Move retrieval method:
        # For each Type in Type.types dict, pull all Moves from corresponding Move file
        # in current directory -> "Game/data/moves", Move files in the formats: 
        # "type_moves.json" or "type1,type2_moves.json" <- type names take from Type.types[i].split()[0] 
        # Moves are dicts, parsable by Move.parse(data : dict, name : Optional[str] = None)

    # moves by probablistic damage output via Move.damage_output()

    move_dir = "Game/data/moves"
    move_files = os.listdir(move_dir)
    type_best_moves = {}

    for type_key in Type.types:
        # Normalize type key(s)
        if isinstance(type_key, (set, tuple, list)):
            base_type_parts = [t.split()[0].lower() for t in type_key]
        else:
            base_type_parts = [type_key.split()[0].lower()]

        base_type = ",".join(sorted(base_type_parts))
        print(f"\n[Info] Looking for moves for: {base_type}")

        relevant_files = [
            f for f in move_files
            if f.startswith(base_type) and f.endswith("_moves.json")
        ]

        moves: List[Move] = []

        for fname in relevant_files:
            path = os.path.join(move_dir, fname)
            with open(path, 'r') as f:
                move_data = json.load(f)

            for move_name, move_dict in move_data.items():
                move = Move.parse(move_dict, name=move_name)
                if move is not None:
                    moves.append(move)

        if not moves:
            continue

        # Extend with maxed prestige versions
        maxed_versions = []
        for mv in moves:
            if mv.prestige:
                new_mv = deepcopy(mv)
                new_mv.prestige.adjust_rank(new_mv, new_mv.prestige.max_rank)
                maxed_versions.append(new_mv)

        moves.extend(maxed_versions)

        # Store tuples of (move, raw_dmg, chip_dmg, total_dmg)
        enriched_moves = []

        for mv in moves:
            raw_dmg = mv.damage_output()
            #raw_dmg = mv.damage_output([Effect.get("Surge 3"), Effect.get("Photosynthesis"), Effect.get("Enraged")])
            chip_dmg = 0.0

            if mv.effects:
                for e in mv.effects:
                    for i, etype in enumerate(e.effect_type):
                        if etype in ("chip-damage", "diminishing-chip-damage"):
                            try:
                                chip_dmg += abs(e.value[i]) * e.application_chance * mv.iterations * mv.accuracy
                            except IndexError:
                                print(f"[Warning] Mismatch in lengths for effect in {mv.name}: effect_type[{i}] but value missing")
                            except Exception as err:
                                print(f"[Error] Unexpected issue in {mv.name}: {err}")

            print(f"{mv.name} -> Chip Dmg: {chip_dmg}")

            total_dmg = raw_dmg + chip_dmg
            enriched_moves.append((mv, raw_dmg, chip_dmg, total_dmg))

        # Rank by raw damage and by total damage (w/ chip)
        by_raw = sorted(enriched_moves, key=lambda x: x[1], reverse=True)[:10]
        by_total = sorted(enriched_moves, key=lambda x: x[3], reverse=True)[:10]

        type_best_moves[base_type] = {
            "raw": by_raw,
            "total": by_total
        }

    # === Display results ===
    for typ, data in type_best_moves.items():
        print(f"\n=== Best Moves for {typ.title()} ===")
        print(f"{'Raw Damage':<50} | {'Total Damage (w/ Chip)':<50}")
        print("-" * 105)

        for i in range(10):
            raw_entry = data["raw"][i] if i < len(data["raw"]) else None
            tot_entry = data["total"][i] if i < len(data["total"]) else None

            def format_entry(entry, show_chip=False):
                if not entry:
                    return ""
                mv, raw, chip, total = entry
                name = f"{mv.name} [MAX]" if mv.prestige and mv.prestige.rank == mv.prestige.max_rank else mv.name
                if show_chip and chip:
                    return f"{name:<30} | Avg Dmg: {round(raw, 2)} + {round(chip, 2)} CD = {round(total, 2)}"
                else:
                    return f"{name:<30} | Avg Dmg: {round(raw, 2)}"

            print(f"{format_entry(raw_entry, show_chip=False):<50} | {format_entry(tot_entry, show_chip=True):<50}")

    # moves by average over 5 uses (subtracting stamina) for each rarity @ lvl 20

    # moves by average over 10 uses (subtracting stamina) for each rarity @ lvl 20

    ## Reference:
        # mv_hit, mv_dmg, mv_hits, mv_str, mv_wk = Move.use(self, user, target) # move data return signature

def main55():
    """Battle tournament style testing"""

    from itertools import product
    from collections import defaultdict

    player = Player() # add all mons to player.mons

    # Normalize all types to set of (parent, subclass)
    def parse_type(t):
        if isinstance(t, str):
            if "(Sub: " in t:
                sub, par = t.split(" (Sub: ")
                par = par[:-1]
                return {(par, sub)}
            else:
                return {(t, None)}
        return {parse_type(x).pop() for x in t}  # set of strings

    types = [parse_type(t) for t in Type.types]

    rarities = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Ultra", "Omega"]
    pearls = [0, 1, 2]

    all_mons = []
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

    # Generate every mon
    for tp, rarity, pearl in product(types, rarities, pearls):
        mon = Mon(level=20, tp=[Type(par, sub) for par, sub in tp], rarity=rarity, pearl=pearl)
        mon.assign_moves(mon.type, mon.moves_limit, move_priority=[True, True, True])
        for mv in mon.moves:
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank, verbose=False)
        all_mons.append(mon)
        player.mons.append(mon)

    # Battle every mon against every other mon
    for i, mon1 in enumerate(all_mons):
        for j, mon2 in enumerate(all_mons):
            if i == j:
                continue
            mon1.assign_best_moves()
            mon1.restore_health()
            mon2.restore_health()
            mon1_won, _ = mon1.battle(mon2, typewriter_delay=0, timing=0, apply_experience=False, verbose=False)

            tp_str1 = tuple(sorted(str(t) for t in mon1.type))
            tp_str2 = tuple(sorted(str(t) for t in mon2.type))

            if mon1_won is True:
                outcome = "Win"
            elif mon1_won is False:
                outcome = "Loss"
            else:
                outcome = "Draw"

            results[(mon1.rarity, mon1.pearl)][tp_str1][tp_str2] = outcome

    # Print results with win/loss percentage, scoped to each rarity-pearl bracket
    for (rarity, pearl), matchups in results.items():
        print(f"\n\n===== Rarity: {rarity} | Pearls: {pearl} =====")

        def compress_type(tp_tuple):
            return [t.split()[0] for t in tp_tuple]

        type_keys = list(matchups.keys())
        header = "Type".ljust(22) + " | ".join(f"{', '.join(compress_type(k))[:3]:^3}" for k in type_keys)
        print(header)
        print("-" * len(header))
        
        for tp, vs_dict in matchups.items():
            row = f"{', '.join(compress_type(tp)):<20}:"

            win_count = 0
            battle_count = 0

            for opp_tp in type_keys:
                result = vs_dict.get(opp_tp, "-")
                if result == "Win":
                    win_count += 1
                    battle_count += 1
                    row += "  W  |"
                elif result == "Loss":
                    battle_count += 1
                    row += "  L  |"
                elif result == "Draw":
                    battle_count += 1
                    row += "  D  |"
                else:
                    row += "|   -"

            if battle_count > 0:
                win_pct = 100 * win_count / battle_count
                row += f" W%: {win_pct:.1f}%"
            else:
                row += " W%: N/A"

            print(row)

        print("=" * len(header))

    #player.export_to_json(filepath="testing/data")

    Miniaturizer.mon_list(player, attribute_sort="wins")

    def export_mon_data(mons, filename="tournament_results.txt"):
        with open(filename, "w") as f:
            for i, mon in enumerate(mons):
                type_str = "/".join(str(tp).split()[0] for tp in mon.type)
                pearl_str = Mon.pearls[mon.pearl].split()[0] if mon.pearl else ""
                name_padding = 15 if not mon.pearl else 13
                name_str = f"{mon.name:<{name_padding}}"
                atk_pct = f"{(mon.attack_boost + 1.0):.0%}"
                def_val = f"{mon.defense:,}"
                stam_str = f"{mon.stamina:>4,} / {mon.max_stamina:,}"

                if mon.health <= 0:
                    hp_str = "   DEAD    "
                else:
                    hp_str = f"{mon.health:>4,} / {mon.max_health:<4,}"

                wins = mon.wins
                total_battles = mon.battles
                losses = total_battles - wins
                win_pct = f"{(wins / total_battles * 100):.1f}" if total_battles else "0.0"

                f.write(
                    f"{i + 1:>3} - {pearl_str:<3} {name_str} "
                    f"(LVL{mon.level:>3}): {type_str:>13} | {atk_pct} ATK | "
                    f"{def_val:>3} DEF | {stam_str} STM | {hp_str} HP |   "
                    f"{wins} / {losses} ({win_pct} W%)\n\n"
                )
    
    export_mon_data(all_mons)

def main56():
    """Battle AI testing"""

    burner = Mon()

    mon = Mon(
        level=50,
        rarity="Legendary"
    )
    mon.assign_moves(mon.type, move_num=mon.moves_limit, move_priority=[True, True, True])
    #mon.moves[0] = Move.get(mon.type, "Explosive Burst")
    for mv in mon.moves:
        if mv.prestige:
            mv.prestige.adjust_rank(mv, mv.prestige.max_rank, verbose=False)

    opp = Mon(
        level=Mon.assign_random_level(bias_factor=2.5), 
        rarity=burner.assign_rarity_weighted(minimum_rarity="Legendary")
    )
    opp.assign_moves(opp.type, move_num=opp.moves_limit, move_priority=[True, True, True])
    for mv in opp.moves:
        if mv.prestige:
            mv.prestige.adjust_rank(mv, mv.prestige.max_rank, verbose=False)

    mon.battle(opp, is_random=False, typewriter_delay=0.005, timing=0.0001)

    print(mon, opp)

def main57():
    """assign_best_moves() testing"""

    for t_strs in Type.types:

        if isinstance(t_strs, str):
            t_strs = [t_strs]  

        m = Mon(
            rarity="Legendary", 
            tp=[Type.parse(t) for t in t_strs]
        )
    
        m.assign_best_moves()

        print(m)

    m = Mon(
        rarity="Omega", 
        tp=[Type("Fire", "Explosion")]
    )

    m.assign_best_moves()

    print(m)

def main58():
    """Type specific battle win % ai testing"""

    fighter = Mon(
        name="Larry",
        level=50,
        tp=[Type.parse(ftp) for ftp in ["Earth", "Fire"]], 
        rarity="Common", 
        pearl=0
    )
    fighter.assign_best_moves()
    #fighter.moves[0] = Move.get([Type("Fire", "Explosion")], "Explosive Burst")
    #fighter.moves[2] = Move.get([Type("Fire", None)], "Solar Flare")
    #fighter.name = fighter.make_name(wild=False)
    for mv in fighter.moves:
        if mv.prestige:
            mv.prestige.adjust_rank(mv, mv.prestige.max_rank)
        mv.hit_probabilities()

    #print(fighter)
    fighter_wins = 0
    fighter_losses = 0
    fighter_draws = 0
    num_battles = 25  # adjust as needed

    # Type-specific stats
    type_battle_stats = defaultdict(lambda: {"wins": 0, "losses": 0, "draws": 0, "battles": 0})

    ftp = [str(ftp_) for ftp_ in [Type.parse(ftp__) for ftp__ in ["Air"]]]

    for t in Type.types:
    #for t in [ftp]:
        if isinstance(t, str):
            t = [t]
        t_str = ", ".join(str(t_) for t_ in t)  # readable key for type

        opp = Mon(
            level=1,
            leveled=True,
            tp=[Type.parse(t_) for t_ in t], 
            rarity="Common",
            boosted=True, 
            pearl=0
        )

        for r in [fighter.rarity]:
            if r == "Any":
                continue

            for p in [fighter.pearl]:
                opp.leveled = False
                opp.boosted = False
                opp.rarity = r
                opp.pearl = p
                opp.rarity_boost(opp.rarity)
                opp.adjust_level(fighter.level, verbose=False)
                opp.assign_best_moves()
                opp.name = opp.make_name()

                for _ in range(num_battles):
                    #fighter_won, _ = fighter.battle(opp, typewriter_delay=0.01, timing=0.0, verbose=True, apply_experience=False)
                    fighter_won, _ = fighter.battle(opp, typewriter_delay=0, timing=0, verbose=True, apply_experience=False)

                    type_battle_stats[t_str]["battles"] += 1
                    if fighter_won is None:
                        fighter_draws += 1
                        type_battle_stats[t_str]["draws"] += 1
                    elif fighter_won is True:
                        fighter_wins += 1
                        type_battle_stats[t_str]["wins"] += 1
                    elif fighter_won is False:
                        fighter_losses += 1
                        type_battle_stats[t_str]["losses"] += 1

                    fighter.restore_health()
                    opp.restore_health()

                #print(fighter)
                #print(opp)

    #fighter.print_battle_log()
    print(fighter)
    print(f"Battle Summary for {fighter.name}:")
    print(f"Wins:   {fighter_wins}")
    print(f"Losses: {fighter_losses}")
    print(f"Draws:  {fighter_draws}")
    print(f"Total:  {fighter_wins + fighter_losses + fighter_draws}\n")
    print(f"Fighter W% = {(fighter.wins / fighter.battles):.1%} ({fighter.wins} / {fighter.battles})")

    print(f"Winrates for {[str(ftp) for ftp in fighter.type]} by Opponent Type:")
    print("Type(s)      | Wins | Loss | Draw | Battles | Win%")
    print("-" * 50)

    for t_str, stats in type_battle_stats.items():
        def short_type_name(t_str):
            return ",".join(part.strip().split()[0][:3] for part in t_str.split(","))

        short_type = short_type_name(t_str)
        w, l, d, b = stats["wins"], stats["losses"], stats["draws"], stats["battles"]
        win_rate = f"{(w / b * 100):.1f}%" if b else "N/A"
        print(f"{short_type:<12} | {w:>4} | {l:>4} | {d:>4} | {b:>7} | {win_rate:>5}")

    #print(fighter)

    #fighter.print_battle_log()

class Stock:
    """A Class to represent a Stock."""

    MAX_HISTORY = 100  # Limit history to save memory

    def __init__(self, name : str, price: float, price_history: Optional[List[float]] = None, total_shares: int = 1000):
        self.name = name
        self.price = price
        self.price_history = price_history or [price]
        self.total_shares = total_shares

    def _record_price(self):
        self.price_history.append(self.price)
        if len(self.price_history) > Stock.MAX_HISTORY:
            self.price_history.pop(0)

    def adjust_price_on_buy(self, shares: int):
        proportion = shares / self.total_shares
        percent_increase = random.uniform(0.005, 0.03) * proportion
        self.price *= (1 + percent_increase)
        self._record_price()

    def adjust_price_on_sell(self, shares: int):
        proportion = shares / self.total_shares
        percent_decrease = random.uniform(0.005, 0.03) * proportion
        self.price *= (1 - percent_decrease)
        self._record_price()

    def __eq__(self, other):
        return isinstance(other, Stock) and id(self) == id(other)  # identity comparison

    def __hash__(self):
        return id(self)  # hash by object identity so it works in dicts
    
    def print_price_history(self):
        print(f"\nPrice history for {self.name} (${self.price:.2f}):")
        for i, price in enumerate(self.price_history[-10:], 1):
            print(f"  [{-10 + i:>2}] ${price:.2f}")

class Purchaser:
    """A Class to represent a Purchaser of Stocks."""

    def __init__(self, starting_balance: float = 10000.0):
        self.stocks = defaultdict(int)  # Stock -> number of shares
        self.balance = starting_balance

    def buy(self, stock: Stock, shares: int):
        cost = stock.price * shares
        if self.balance < cost:
            print(f"Not enough funds to buy {shares} shares at ${stock.price:.2f}")
            return
        stock.adjust_price_on_buy(shares)
        self.stocks[stock] += shares
        self.balance -= cost

    def sell(self, stock: Stock, shares: int):
        if self.stocks[stock] < shares:
            print(f"Not enough shares to sell ({shares} requested, {self.stocks[stock]} owned).")
            return
        stock.adjust_price_on_sell(shares)
        self.stocks[stock] -= shares
        self.balance += stock.price * shares
        if self.stocks[stock] == 0:
            del self.stocks[stock]

    def portfolio(self):
        print(f"\nBalance: ${self.balance:.2f}")
        total_stock_value = 0.0
        for stock, shares in self.stocks.items():
            stock_value = stock.price * shares
            total_stock_value += stock_value
            print(f"{stock.name} - {shares} shares @ ${stock.price:.2f} | Value: ${stock_value:.2f} | History length: {len(stock.price_history)}")
        total_assets = self.balance + total_stock_value
        print(f"Total Assets: ${total_assets:.2f}")
        print("")

    def ai_trade(self, all_stocks: List[Stock], trend_window: int = 5):
        """Simple AI: sell if trending down, buy more if trending up, reinvest leftover cash."""

        for stock in list(self.stocks.keys()):
            history = stock.price_history[-trend_window:]
            if len(history) < trend_window:
                continue

            avg_past = sum(history[:-1]) / (trend_window - 1)
            recent = history[-1]

            if recent < avg_past:
                print(f"[AI] Selling {self.stocks[stock]} shares of declining {stock.name} (${stock.price:.2f})")
                self.sell(stock, self.stocks[stock])
            elif recent > avg_past and self.balance >= stock.price:
                num_to_buy = int(self.balance // stock.price)
                if num_to_buy > 0:
                    print(f"[AI] Buying {num_to_buy} more shares of trending {stock.name} (${stock.price:.2f})")
                    self.buy(stock, num_to_buy)

        if self.balance > 0:
            fallback = self.select_fallback_stock(all_stocks)
            if fallback and fallback.price <= self.balance:
                fallback_shares = int(self.balance // fallback.price)
                print(f"[AI] Reinvesting ${fallback.price:.2f} x {fallback_shares} in {fallback.name}")
                self.buy(fallback, fallback_shares)

    def select_fallback_stock(self, stocks: List[Stock]):
        """Pick the stock with lowest recent volatility as a stable reinvestment."""
        best_stock = None
        lowest_volatility = float("inf")

        for stock in stocks:
            recent = stock.price_history[-10:]
            if len(recent) < 2:
                continue
            volatility = max(recent) - min(recent)
            if volatility < lowest_volatility:
                best_stock = stock
                lowest_volatility = volatility

        return best_stock
    
    def demo_ai(self, all_stocks: List[Stock], cycle: int, hold_limit: int = 5):
        """
        Demo trading strategy:
          - If holding a stock and it's up (vs last recorded price), sell.
          - Otherwise, hold until 'hold_limit' cycles pass, then sell.
          - If market stocks are down (vs last price), buy the cheapest one.
        """
        # 1. Sell logic
        for stock in list(self.stocks.keys()):
            if len(stock.price_history) < 2:
                continue
            prev_price = stock.price_history[-2]
            curr_price = stock.price_history[-1]

            if curr_price > prev_price:
                # Stock is up → sell all
                print(f"[DEMO] Selling {self.stocks[stock]} shares of {stock.name} (up to ${curr_price:.2f})")
                self.sell(stock, self.stocks[stock])
            elif cycle % hold_limit == 0:
                # Time-based forced sell
                print(f"[DEMO] Selling {self.stocks[stock]} shares of {stock.name} after {hold_limit} cycles (${curr_price:.2f})")
                self.sell(stock, self.stocks[stock])

        # 2. Buy logic → pick the cheapest stock that went down
        cheapest = None
        cheapest_price = float("inf")
        for stock in all_stocks:
            if len(stock.price_history) < 2:
                continue
            if stock.price_history[-1] < stock.price_history[-2]:  # stock is down
                if stock.price < cheapest_price:
                    cheapest = stock
                    cheapest_price = stock.price

        if cheapest and self.balance >= cheapest.price:
            num_to_buy = int(self.balance // cheapest.price)
            if num_to_buy > 0:
                print(f"[DEMO] Buying {num_to_buy} shares of cheapest down stock {cheapest.name} @ ${cheapest.price:.2f}")
                self.buy(cheapest, num_to_buy)

def main59():
    """SIDETRACK: Stock sim testing — N stocks, 10 purchasers with day-by-day control."""

    num_stocks = 10
    starting_price = 50.0
    num_investors = 100
    num_days = 50

    # Create list of stocks all starting at $50 with names
    stocks = [Stock(name=f"Stock {i+1}", price=starting_price) for i in range(num_stocks)]

    # Create 10 purchasers
    investors = [Purchaser() for _ in range(num_investors)]

    # Prime all stocks with some random small fluctuations
    for _ in range(10):
        for stock in stocks:
            stock.price *= random.uniform(0.98, 1.02)
            stock._record_price()

    print("=== INITIAL STATE ===")
    for idx, investor in enumerate(investors, 1):
        print(f"\nInvestor {idx} Portfolio:")
        investor.portfolio()
    for stock in stocks:
        print(f"{stock.name} Price: ${stock.price:.2f}")
    print("-" * 30)

    def apply_daily_volatility(stock: Stock, drift_range: float = 0.02):
        """Apply a small random drift to simulate market forces."""
        percent_change = random.uniform(-drift_range, drift_range)
        stock.price *= (1 + percent_change)
        stock._record_price()

    def simulate_price_increase(stock: Stock):
        """Simulates a relatively large price increase for a Stock (5% to 30%)."""
        if random.random() < 0.10:  # 10% chance
            percent_increase = random.uniform(0.05, 0.30)
            stock.price *= (1 + percent_increase)
            stock._record_price()
            print(f"[SURGE] {stock.name} surges +{percent_increase*100:.2f}% to ${stock.price:.2f}")

    # Simulate 10 rounds of AI trading
    for day in range(1, num_days + 1):
        input(f"\nPress Enter to simulate DAY {day}...")  # Gate day-by-day
        print(f"\n--- DAY {day} ---")

        # Apply volatility and price surges
        for stock in stocks:
            apply_daily_volatility(stock)
            simulate_price_increase(stock)

        # Each investor makes decisions
        for idx, investor in enumerate(investors, 1):
            print(f"\nInvestor {idx} Trading:")
            investor.ai_trade(stocks)

        # Print portfolios
        for idx, investor in enumerate(investors, 1):
            print(f"\nInvestor {idx} Portfolio:")
            investor.portfolio()

        # Print current stock prices
        for stock in stocks:
            print(f"{stock.name} Price: ${stock.price:.2f}")

    print("\n=== FINAL STATE ===")
    for idx, investor in enumerate(investors, 1):
        print(f"\nInvestor {idx} Final Portfolio:")
        investor.portfolio()

    for stock in stocks:
        print(f"{stock.name} Final Price History:")
        stock.print_price_history()

def main59_a():
    """Demo trading strategy simulation using demo_ai()."""

    num_stocks = 5
    starting_price = 50.0
    num_investors = 3
    num_days = 1000

    # Create stocks
    stocks = [Stock(name=f"Stock {i+1}", price=starting_price) for i in range(num_stocks)]
    investors = [Purchaser() for _ in range(num_investors)]

    # Prime with small fluctuations
    for _ in range(5):
        for stock in stocks:
            stock.price *= random.uniform(0.98, 1.02)
            stock._record_price()

    print("=== DEMO INITIAL STATE ===")
    for idx, inv in enumerate(investors, 1):
        print(f"\nInvestor {idx} Portfolio:")
        inv.portfolio()
    for stock in stocks:
        print(f"{stock.name} Price: ${stock.price:.2f}")
    print("-" * 30)

    def apply_daily_volatility(stock: Stock, drift_range: float = 0.03):
        """Random small drift per day."""
        stock.price *= (1 + random.uniform(-drift_range, drift_range))
        stock._record_price()

    # Run demo loop
    for day in range(1, num_days + 1):
        print(f"\n--- DEMO DAY {day} ---")

        # Move market
        for stock in stocks:
            apply_daily_volatility(stock)

        # Each investor makes demo AI decisions
        for idx, inv in enumerate(investors, 1):
            print(f"\nInvestor {idx} Trading:")
            inv.demo_ai(stocks, cycle=day)

        # Print daily portfolios
        for idx, inv in enumerate(investors, 1):
            print(f"\nInvestor {idx} Portfolio:")
            inv.portfolio()

        # Print stock prices
        for stock in stocks:
            print(f"{stock.name} Price: ${stock.price:.2f}")

    print("\n=== DEMO FINAL STATE ===")
    for idx, inv in enumerate(investors, 1):
        print(f"\nInvestor {idx} Final Portfolio:")
        inv.portfolio()

    for stock in stocks:
        stock.print_price_history()

def main60(designated_rarity = "Common", designated_pearl = 0, level = 50, num_battles = 25):
    """Type vs Type battle win % collection for all Mon types at a given rarity and pearl."""

    from collections import defaultdict

    type_battle_stats = defaultdict(lambda: defaultdict(lambda: {
        "wins": 0,
        "losses": 0,
        "draws": 0,
        "battles": 0
    }))

    # Create one fighter per type
    fighters = []
    for t_raw in Type.types:
        if isinstance(t_raw, str):
            parsed_types = [Type.parse(t_raw)]
        elif isinstance(t_raw, Type):
            parsed_types = [t_raw]
        else:
            parsed_types = [Type.parse(t) if isinstance(t, str) else t for t in t_raw]

        fighter = Mon(
            level=level,
            tp=parsed_types,
            rarity=designated_rarity,
            pearl=designated_pearl
        )

        fighter.assign_best_moves()
        for mv in fighter.moves:
            if mv.prestige:
                mv.prestige.adjust_rank(mv, mv.prestige.max_rank)
            mv.hit_probabilities()
        fighters.append(fighter)

    # Use single opponents per type
    opponent_bank = {}
    for t_raw in Type.types:
        if isinstance(t_raw, str):
            parsed_types = [Type.parse(t_raw)]
        elif isinstance(t_raw, Type):
            parsed_types = [t_raw]
        else:
            parsed_types = [Type.parse(t) if isinstance(t, str) else t for t in t_raw]

        # Create opponent Mon
        opponent = Mon(
            level=level,
            tp=parsed_types,
            rarity=designated_rarity,
            pearl=designated_pearl
        )
        opponent.rarity_boost(opponent.rarity)
        opponent.assign_best_moves()
        opponent.name = opponent.make_name()

        # Use a string key that joins the short names of each type
        type_key = ",".join(str(tp).split()[0] for tp in opponent.type)
        opponent_bank[type_key] = opponent

    # Battle loop
    for fighter in fighters:
        for t_str, opponent in opponent_bank.items():
            for _ in range(num_battles):
                fighter_won, _ = fighter.battle(opponent, typewriter_delay=0, timing=0, verbose=False, apply_experience=False)

                fighter_type_str = ",".join(str(tp) for tp in fighter.type)
                type_battle_stats[fighter_type_str][t_str]["battles"] += 1

                if fighter_won is None:
                    type_battle_stats[fighter_type_str][t_str]["draws"] += 1
                elif fighter_won is True:
                    type_battle_stats[fighter_type_str][t_str]["wins"] += 1
                else:
                    type_battle_stats[fighter_type_str][t_str]["losses"] += 1

                fighter.restore_health()
                opponent.restore_health()

    # Print
    print("\n=== Type Matchup Summary ===\n")

    for atk_type, results in type_battle_stats.items():
        total_wins = sum(stats["wins"] for stats in results.values())
        total_losses = sum(stats["losses"] for stats in results.values())
        total_draws = sum(stats["draws"] for stats in results.values())
        total_battles = sum(stats["battles"] for stats in results.values())
        win_rate = f"{(total_wins / total_battles * 100):.1f}%" if total_battles else "N/A"

        print(f"{atk_type} Matchups:")
        print(f"Wins:   {total_wins}")
        print(f"Losses: {total_losses}")
        print(f"Draws:  {total_draws}")
        print(f"Total:  {total_battles}")
        print(f"Win%:   {win_rate}\n")

        print(f"{'Vs Type':<8} | {'W':>3} | {'L':>3} | {'D':>3} | {'B':>5} | {'Win%':>5}")
        print("-" * 36)

        for def_type, stats in results.items():
            w, l, d, b = stats["wins"], stats["losses"], stats["draws"], stats["battles"]
            pct = f"{(w / b * 100):.1f}%" if b else "N/A"
            print(f"{def_type[:6]:<8} | {w:>3} | {l:>3} | {d:>3} | {b:>5} | {pct:>5}")

        print("\n" + "=" * 36 + "\n")


    import csv

    csv_filename = f"{designated_rarity.lower()}_fighter_winrates.csv"
    with open(csv_filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Fighter Type", "Wins", "Losses", "Draws", "Battles", "Win%"])

    print(f"\n=== {designated_rarity} Fighter Win/Loss/Draw Totals ===\n")
    print(f"{'Fighter Type':<15} | {'Wins':>4} | {'Losses':>6} | {'Draws':>5} | {'Battles':>7} | {'Win%':>5}")
    print("-" * 58)

    with open(csv_filename, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        for atk_type, results in type_battle_stats.items():
            w = sum(stats["wins"] for stats in results.values())
            l = sum(stats["losses"] for stats in results.values())
            d = sum(stats["draws"] for stats in results.values())
            b = sum(stats["battles"] for stats in results.values())
            win_pct_raw = (w / b * 100) if b else None
            win_pct = f"{win_pct_raw:.1f}%" if win_pct_raw is not None else "N/A"

            # Fix: Show shortened but accurate fighter type string
            short_name = ",".join(part.strip()[:3] for part in atk_type.split(","))

            print(f"{short_name:<15} | {w:>4} | {l:>6} | {d:>5} | {b:>7} | {win_pct:>5}")
            writer.writerow([atk_type, w, l, d, b, f"{win_pct_raw:.1f}" if win_pct_raw is not None else "N/A"])

def main61():
    """Pearl stats comparison by rarity"""

    pl = Player()

    for r in Mon.rarities:
        if r == "Any": 
            continue
        for p in Mon.pearls:
            for per in (True, False):
                mon = Mon(
                    level=20, 
                    perfect=per,
                    tp=[Type.parse(t_) for t_ in ["Fire"]],
                    rarity=r, 
                    pearl=p
                )
                tp_str = "/".join(str(tp).split()[0][:3] for tp in mon.type)
                mon.name = f"{mon.rarity[:3]} {tp_str}"

                pl.add_mons([mon])

    Miniaturizer.mon_list(pl, attribute_sort=["rarity", "pearl"])
    #Miniaturizer.mon_list(pl, attribute_sort=["attack_boost"], pearl_short_hand=False)

def main62():
    """High rarity encounter battle testing against low rarities (with good moves)"""

    burner = Mon()
    ct = random.choice(Type.types)

    tp = (
        [Type.parse(ct)] if isinstance(ct, str)
        else [Type.parse(t) if isinstance(t, str) else t for t in ct]
    )

    fighter = Mon(
        name="Test Mon", 
        perfect=True,
        tp=tp, 
        rarity=burner.assign_rarity_weighted(minimum_rarity="Epic")
    )
    fighter.assign_best_moves()
    #fighter.assign_moves(fighter.type, move_num=fighter.moves_limit, move_priority=(True, True, True))

    print(fighter)


    opp = Mon(
        rarity=burner.assign_rarity_weighted(minimum_rarity="Legendary"),
    )
    opp.assign_best_moves()

    for mon in (fighter, opp):
        print(f"{mon.name}")
        for mv in mon.moves:
            dop = mv.damage_output(include_damaging_effects=True, attack_boost=mon.attack_boost, simulate_prestige=True)
            print(f"{mv.name} : {dop}")

    fighter.battle(opp, is_random=True, typewriter_delay=0.005, timing=0.01, use_self_ai=True, use_opp_ai=True)

def main63():
    """Mon pack opening funsies"""

    """
    b = Mon()
    for _ in range(20):
        m = Mon(
            rarity=b.assign_rarity_weighted(
                custom_weights=[
                    ("Common", 0.5), # 50%
                    ("Uncommon", 0.25), # 25%
                    ("Rare", 0.15), # 15%
                    ("Epic", 0.06), # 6%
                    ("Legendary", 0.0345), # 3.45%
                    ("Ultra", 0.005), # 0.5%
                    ("Omega", 0.0005) # 0.05%
                ]
            )
        )

        print(m)
    """

    pack_types = {
        "Flame" : [
            ({"Fire", "Water"}, 0.2), 
            ({"Earth", "Fire"}, 0.1), 
            ("Explosion (Sub: Fire)", 0.05),
            ({"Demon (Sub: Magic)", "Fire"}, 0.03),
            ({"Air", "Fire"}, 0.22),
            ("Fire", 0.5)
        ], 
        "Ocean" : [
            ("Water", 0.66), 
            ({"Air", "Water"}, 0.15), 
            ({"Fire", "Water"}, 0.04), 
            ("Ice: (Sub: Water)", 0.05)
        ],
        "Elementals" : [
            ("Water", 0.20), 
            ("Fire", 0.20), 
            ("Air", 0.20), 
            ("Earth", 0.20), 
            ("Electric", 0.14), 
            ("Ice (Sub: Water)", 0.03), 
            ("Metal (Sub: Earth)", 0.03), 
            ("Nature", 0.03), 
            ({"Air", "Earth"}, 0.01), 
            ({"Air", "Water"}, 0.01), 
            ({"Air", "Fire"}, 0.01), 
            ({"Earth", "Fire"}, 0.01), 
            ({"Earth", "Magic"}, 0.01), 
            ({"Fire", "Water"}, 0.01), 
        ]
    }

    mons = Game.mon_pack(
        pack_num=1, 
        mon_types_weighted=pack_types["Elementals"],
        #min_keep_rarity="Legendary", 
        pack_quality="Enhanced", 
        #god_pack_chance=(1/10)
    )

    for m in mons:
        print(m)

def main64():
    """Bernoulli Expected Value Table method"""
    def expected_value_table(
        input_chances: List[Tuple[str, float]],
        sample_size: int,
        runs: int,
        steps: float,
        multiplicative: bool = False
    ):
        """Generates a table of expected values for each rarity over multiple sample sizes."""

        print(f"{'Sample Size':<12} | " + " | ".join(f"{rarity:<10}" for rarity, _ in input_chances))
        print("-" * (14 + 13 * len(input_chances)))

        current_sample = sample_size

        for _ in range(runs):
            row = [f"{current_sample:<12} |"]
            for _, chance in input_chances:
                expected = current_sample * chance
                row.append(f"{expected:<12.2f}")
            print(" ".join(row))

            if multiplicative:
                current_sample *= steps
            else:
                current_sample += steps

    rarities = [
            ("Common", 0.30), # 30%
            ("Uncommon", 0.23), # 23%
            ("Rare", 0.20), # 20%
            ("Epic", 0.13), # 13%
            ("Legendary", 0.085), # 8.5%
            ("Ultra", 0.035), # 3.5%
            ("Omega", 0.02) # 2%
        ]

    expected_value_table(rarities, sample_size=10, runs=5, steps=10, multiplicative=True)

def main65():
    """Grid class testing"""

    class Grid:
        """A Class to store Mons, Loot, Player position, etc. in a square matrix with designated dimensions."""

        def __init__(self, 
                     dimension : int = 10, 
                     mon_density : float = None
                     ):
            self.dimension = dimension
            self.mon_density = mon_density
            self.grid = [[None for _ in range(dimension)] for _ in range(dimension)]
            self.player_position = None  # Optional: set to (x, y) when the player is placed

            if self.mon_density is not None:
                self.place_random_mons()

        def in_bounds(self, x, y):
            """Check if the coordinates are within grid bounds."""
            return 0 <= x < self.dimension and 0 <= y < self.dimension

        def place(self, x, y, obj):
            """Place an object (Mon, loot, etc.) at the specified location."""
            if not self.in_bounds(x, y):
                raise IndexError("Grid position out of bounds")
            self.grid[y][x] = obj

        def place_random_mons(self):
            """Place random Mons throughout the Grid based on self.mon_density (a float from 0 to 1)."""
            if self.mon_density is None:
                return  # Safety check — shouldn't be called if density is None

            for y in range(self.dimension):
                for x in range(self.dimension):
                    if self.grid[y][x] is None and random.random() < self.mon_density:
                        try:
                            b = Mon()
                            self.place(x, y, Mon(rarity=b.assign_rarity_weighted(minimum_rarity="Epic")))
                        except Exception as e:
                            print(f"Failed to place Mon at ({x}, {y}): {e}")

        def get(self, x, y):
            """Get the object at the specified location."""
            if not self.in_bounds(x, y):
                raise IndexError("Grid position out of bounds")
            return self.grid[y][x]

        def remove(self, x, y):
            """Remove and return the object at the specified location."""
            if not self.in_bounds(x, y):
                raise IndexError("Grid position out of bounds")
            obj = self.grid[y][x]
            self.grid[y][x] = None
            return obj

        def move_player(self, new_x, new_y):
            """Move the player to a new position."""
            if not self.in_bounds(new_x, new_y):
                raise ValueError("New position out of bounds")
            self.player_position = (new_x, new_y)

        def __str__(self):
            """Return a string representation of the grid with coordinate labels for debugging."""
            cell_width = 2  # Adjust this if your characters take up more space
            rows = []

            # Column headers
            header = "   " + " ".join(f"{x:>{cell_width - 1}}" for x in range(self.dimension))
            rows.append(header)

            for y in range(self.dimension):
                row = [f"{y:>2}"]  # Row label (left side)
                for x in range(self.dimension):
                    if self.player_position == (x, y):
                        row.append("P")
                    elif self.grid[y][x] is None:
                        row.append(".")
                    elif isinstance(self.grid[y][x], Mon):
                        m = self.grid[y][x]
                        # Use Mon's rarity color function with a single-character override
                        symbol = Mon.rarity_colors(m.rarity, str_override=m.name.split()[2][0])
                        row.append(symbol)
                    else:
                        row.append("O")
                rows.append(" ".join(row))

            return "\n".join(rows)

    
    g = Grid(
        dimension=10,
        mon_density=0.15
    )

    print(g)

    fighter = Mon(
        #name="Fighter"
        #perfect=True,
        #rarity="Omega",
        #tp=[Type("Water", None), Type("Fire", None)]
    )
    fighter.moves_limit = 3 
    fighter.assign_best_moves()
    #fighter.moves[0] = Move.get([Type("Fire", None)], "Fireshot")
    #fighter.moves[0].prestige.adjust_rank(fighter.moves[0], fighter.moves[0].prestige.max_rank)

    print(fighter)

    wins = 0
    losses = 0
    draws = 0

    for y in range(g.dimension):
        for x in range(g.dimension):
            if fighter.health <= 0:
                break
            
            if isinstance(g.grid[y][x], Mon):
                m = g.grid[y][x]
                if Mon.rarities[m.rarity] >= 4:
                    print(g)
                    print(f"Fighting {m.name} @ POS=({x},{y})")
                    outcome, _ = fighter.battle(m, 
                                                is_random=False, 
                                                typewriter_delay=0.005, 
                                                use_opp_ai=True,
                                                timing=0.01)
                    if outcome == True:
                        print(f"{m.name} lost, removed {g.remove(x, y)} @ POS=({x},{y})")
                        wins += 1
                    elif outcome == False:
                        print(f"Fighter {fighter.name} lost.")
                        losses += 1
                    else:
                        print(f"Draw.")
                        draws += 1
        
        if fighter.health <= 0:
                break
    
    print(g, f"\nWins: {wins}\nLosses: {losses}\nDraws: {draws}")

def main66():
    """Mon case testing"""

    Game.mon_case()
    i = input()

class Cell:
    """Models a human cell with essential organelles and processes."""

    def __init__(self):
        self.energy = 100  # Energy level from 0 to 100
        self.alive = True

        # Core organelles - will be class instances
        self.nucleus = Nucleus()
        self.cell_membrane = CellMembrane()
        self.mitochondria = [Mitochondrion() for _ in range(10)]
        self.ribosomes = [Ribosome() for _ in range(1000)]
        self.endoplasmic_reticulum = EndoplasmicReticulum()
        self.golgi_apparatus = GolgiApparatus()
        self.lysosomes = [Lysosome() for _ in range(20)]
        self.peroxisomes = [Peroxisome() for _ in range(20)]

    def check_vital_status(self):
        """Updates cell alive status based on energy and damage."""
        if self.energy <= 0:
            self.alive = False
            print("Cell has died due to lack of energy.")

    def metabolize(self):
        """Simulate metabolism via mitochondria, generating energy."""
        energy_produced = sum(mito.produce_energy() for mito in self.mitochondria)
        self.energy = min(100, self.energy + energy_produced)
        print(f"Cell metabolized. Energy is now {self.energy:.2f}%.")
        self.check_vital_status()

    def perform_protein_synthesis(self):
        """Simulate protein synthesis from DNA to protein."""
        if not self.alive:
            print("Cell is dead. Cannot synthesize proteins.")
            return

        mrna = self.nucleus.transcribe_dna()
        protein = self.endoplasmic_reticulum.translate_mrna(mrna, self.ribosomes)
        self.golgi_apparatus.package_protein(protein)

    def mitosis(self):
        """Simulates mitosis by duplicating the cell."""
        if not self.alive:
            print("Cell is dead. Cannot divide.")
            return

        print("Starting mitosis...")
        # Placeholder logic for now; real mitosis would involve replicating all organelles and splitting
        daughter_cell = Cell()
        print("Mitosis complete. Daughter cell created.")
        return daughter_cell

    def degrade_waste(self):
        """Uses lysosomes and peroxisomes to clean up cell waste."""
        for lysosome in self.lysosomes:
            lysosome.digest()
        for peroxisome in self.peroxisomes:
            peroxisome.break_down_toxins()
        print("Cell has degraded waste.")

# Placeholder organelle classes:
class Nucleus:
    def transcribe_dna(self):
        return "mRNA"

class CellMembrane:
    pass

class Mitochondrion:
    def produce_energy(self):
        return 1.5  # Energy units per cycle

class Ribosome:
    pass

class EndoplasmicReticulum:
    def translate_mrna(self, mrna, ribosomes):
        return "protein"

class GolgiApparatus:
    def package_protein(self, protein):
        print(f"Protein packaged: {protein}")

class Lysosome:
    def digest(self):
        pass

class Peroxisome:
    def break_down_toxins(self):
        pass

def main67():
    """sim_battle_stats method testing & setup for dog_fight method"""

    m1 = Mon(
        name="Bicth", 
        level=20, 
        rarity="Common", 
        tp=[Type("Fire", "Explosion")]
    )

    m2 = Mon(
        name="Opp", 
        level=20, 
        perfect=True,
        rarity="Legendary", 
        tp=[Type("Fire", "Explosion")]
    )

    m1.assign_best_moves()
    m2.assign_best_moves()

    m1.sim_battle_stats(m2)

def main68():
    """dog_fight testing loop"""

    p = Game.pPlayer("--> Kai")
    bal_hist = []

    while True: 
    #for _ in range(100):
        # Create two Mons
        pf = random.random() < 0.1
        m1 = Mon(rarity=random.choice(["Omega"]), perfect=pf, level=50)
        pf = random.random() < 0.1
        m2 = Mon(rarity=random.choice(["Omega"]), perfect=pf, level=50)

        m1.assign_best_moves()
        m2.assign_best_moves()

        # Odds sim
        odds = m1.sim_battle_stats(m2)

        #Tools.text(f"DEBUG {[v for v in odds]}\n\n", rgb=[255, 255, 0])

        # Display Mons
        for idx, mon in enumerate((m1, m2)):
            print(f"{idx}: {mon.name_str()}")

        def mon_prediction(m1: Mon, m2: Mon) -> bool:
            """
            Predicts winner of Mon Battle, based on Type effectiveness, rarity, pearl, and perfection. 
            Returns True if prediction is m1, else False.
            """
            scores = {m1.name: 0, m2.name: 0}

            for m in (m1, m2):
                r = m1 if m == m2 else m2

                strong = any(
                    mon_type.is_strong_against(rcpt_tp)
                    for mon_type in m.type
                    for rcpt_tp in r.type
                )

                weak = any(
                    mon_type.is_weak_against(rcpt_tp)
                    for mon_type in m.type
                    for rcpt_tp in r.type
                )

                type_advantage = strong and not weak
                rarity_advantage = m.rarity > r.rarity
                pearl_advantage = m.pearl > r.pearl
                perf_advantage = m.perfect and not r.perfect

                if type_advantage:
                    scores[m.name] += 3
                if rarity_advantage:
                    scores[m.name] += 1
                if pearl_advantage:
                    scores[m.name] += 1
                if perf_advantage:
                    scores[m.name] += 2

            #print(f"Scores: {m1.name}={scores[m1.name]}, {m2.name}={scores[m2.name]}")

            equal = scores[m1.name] == scores[m2.name]

            return scores[m1.name] >= scores[m2.name] if not equal else random.choice([True, False])

        def smart_mon_prediction(m1 : Mon, m2 : Mon) -> bool:
            """
            Predicts winner of Mon Battle, based on Type effectiveness and movesets, which considers respective Mon stats. 
            Returns True if prediciton is m1, else False.
            """

            for m in (m1, m2):
                for mv in m.moves:
                    strong = any(
                        move_type.is_strong_against(rcpt_tp)
                        for move_type in mv.move_types
                        for rcpt_tp in m.type
                    )

                    weak = any(
                        move_type.is_weak_against(rcpt_tp)
                        for move_type in mv.move_types
                        for rcpt_tp in m.type
                    )

                    # check for stun moves, specials, and damage output factoring in defense and type effectiveness

        # Generate random bets from AI players
        bets = []
        for bnum in range(10):
            pred_meth = False
            if random.random() > 0.5:
                pred = mon_prediction(m1, m2) 
                pred_meth = True
            else: 
                pred = random.choice([True, False])
            bets.append(
                Game.Bet(
                    f"P{bnum}-{'p' if pred_meth else 'r'}", 
                    pred, 
                    Tools.ceil_to_nearest(random.randint(int(p.balance * 0.10), p.balance), 1000)
                )
            )

        # Get user input
        def kelly_criterion(b, p, q): 
            """Kelly Criterion"""

            return (b * p - q) / b
        
        if True:
            mon_choice = input("Specify your chosen Mon (0 or 1):\n")
            bet_amount = input(f"Specify your bet amount (Funds: {p.balance:,}):\n")

            try:
                #mon_choice_int = int(mon_choice)
                #bet_amount_int = int(bet_amount)
                mon_choice_int = 0 if odds[0] > odds[1] - odds[2] else 1
                bet_amount_int = int(bet_amount)
            except ValueError:
                print("Invalid input. Please enter integers.")
                continue
        else:
            mon_choice_int = 0 if odds[0] > odds[1] - odds[2] else 1
            bet_amount_int = -1

        if mon_choice_int not in (0, 1) or bet_amount_int <= 0 or bet_amount_int > p.balance:
            if bet_amount_int == -1:
                p_w = odds[0] if mon_choice_int == 0 else odds[1] - odds[2]
                kelly_bet = int(abs(kelly_criterion(1.5, p_w, 1 - p_w) * p.balance)) 
                bet_amount_int = min(p.balance, kelly_bet)
            else:
                print("Invalid choice or bet amount.")
                continue

        bets.append(Game.Bet(
            p, # player 
            True if mon_choice_int == 0 else False,
            bet_amount_int
        ))

        # Run the dog fight
        #Tools.text(f"DEBUG {[v for v in odds]}\n\n", rgb=[255, 255, 0])
        prev_bal = p.balance
        Game.dog_fight(m1=m1, m2=m2, bets=bets, odds=odds)
        #Tools.text(f"DEBUG {[v for v in odds]}\n\n", rgb=[255, 255, 0])

        if p.balance != prev_bal:
            bal_hist.append(p.balance)

        if p.balance <= 0:
            print(f"{p.name} out of funds!!")
            break

        # Optional: ask to continue or exit
        if True:
            cont = input("Do you want to run another battle? (y/n):\n")
            if cont.lower() != 'y':
                break        

    import csv

    # Example: bal_hist = [1000, 1500, 2000, 2500]

    with open('balance_history.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Turn', 'Balance'])
        
        # Write each balance with its turn number
        for turn, balance in enumerate(bal_hist, start=1):
            writer.writerow([turn, balance])

    print("Balance history exported to balance_history.csv")

def proposal():
    def party():
        print("Me: Yay!")

    def kill_myself():
        print("Me: 😵")

    answer = input("Me: Will you marry me? 💍\nYou: ")

    if answer.lower() == "yes":
        party()
    else:
        kill_myself()

def main69():
    """ascii code"""

    def tta(text: str) -> str:
        ascii_codes = ' '.join(str(ord(char)) for char in text)
        print(f"Original string: {text} -> ASCII: {ascii_codes}")
        return ascii_codes

    def att(ascii_str: str) -> str:
        text = ''.join(chr(int(code)) for code in ascii_str.split())
        print(f"ASCII string: {ascii_str} -> Text: {text}")
        return text

    att(tta("YOU ARE RETARDED"))

def main70():
    class ClassType():
        """Class for Player typing."""

        def __init__(self, parent : str, job : Optional[str] = None):
            self.parent = parent
            self.job = job

        def __str__(self):
            return f"{self.parent}"

    class MPlayer():
        """More advanced, Mock Player Class"""

        def __init__(self, 
                     leveled : Optional[bool] = None,
                     level: Optional[int] = None,
                     experience : int = 0,
                     experience_needed : int = 1000,
                     strength : int = 0,
                     agility : int = 0,
                     intellect : int = 0,
                     perception : int = 0,
                     stamina : int = 0, 
                     skill_points : int = 0):
            self.leveled = leveled if leveled is not None else False
            self.level = level if level is not None and leveled == True else 0
            self.experience = experience
            self.experience_needed = experience_needed
            self.strength = strength
            self.agility = agility
            self.intellect = intellect
            self.perception = perception
            self.stamina = stamina
            self.skill_points = skill_points
            #self.class_type
            #self.health
            #self.defense
            #self.damage_taken # ClassType affects HP progression from damage_taken (e.g., 'Warrior' ClassType might get an extra hit-point every 100 damage taken)
            #self.damage_blocked # ClassType affects DEF progression from damage_blocked (e.g., 'Tank' ClassType might get 1 extra defense every 100 damage blocked)

            if self.leveled is False and self.level == 0 and level is not None:
                #Tools.text(f"[DEBUG] init {self.level} {level}\n", rgb=[255, 0, 0])
                self.level = 1
                self.adjust_level(level, verbose=False)

            if self.level == 0:
                #Tools.text(f"[DEBUG] {level}\n", rgb=[255, 0, 0])
            
                self.level = 1
                self.adjust_level(1, verbose=False) # default to level 1

        def adjust_level(self, new_level : int, verbose : bool = True): 
            """A method to adjust a Player's level and corresponding stats from an input number of levels."""
            
            _num_levels = new_level - self.level

            if _num_levels == 0 and self.leveled == False:
                self.leveled = True
            #Tools.text(f"[DEBUG] {new_level} {self.level}\n", rgb=[255,0,0])
            for _ in range(_num_levels):
                #Tools.text(f"[DEBUG] {self.experience} {self.experience_needed}\n", rgb=[255,0,0])
                xp_to_next = self.experience_needed
                self.add_experience(xp_to_next, verbose=verbose)

        def level_up(self, recursed_levels : Optional[int] = None): 
            """A method to level-up a Player, if possible, and adjust stats accordingly."""

            # instantiate the recursive count
            if recursed_levels is None:
                recursed_levels = 0

            if self.experience < self.experience_needed: 
                if recursed_levels > 0:
                    if recursed_levels == 1:
                        Tools.text(f"You leveled up! You are now level {self.level}!\n\n", rgb=[100, 150, 0])
                    else:
                        Tools.text(f"You leveled up {recursed_levels} times!\n\n", rgb=[100, 150, 0])
                return
            
            self.level += 1 # increase level
            self.experience -= self.experience_needed # deduct needed experience from the total amount
            self.experience_needed = int(self.experience_needed + (self.level * 1000)) # adjust needed experience for next level 

            # update stats
            self.skill_points += 5 
            self.strength += 1 # all stats +1
            self.agility += 1
            self.stamina += 1
            self.perception += 1
            self.intellect += 1

            # increase recursive level counter for printing
            recursed_levels += 1
            self.level_up(recursed_levels) # recursively call for remaining levels

        def add_experience(self, points : int, verbose : bool = True):
            """A method to add experience points to the Player and automatically check if the Player can level up."""

            self.experience += points
            if verbose:
                Tools.text(f"You gained ", rgb=[100, 150, 0])
                Tools.text(f"{points:,} XP\n\n", rgb=[100, 150, 0])
            self.level_up()

        def stat_selection(self):
            """Allows the Player to spend skill points to increase their choice of Stats."""

            stats = [
                ("Strength", "strength"),
                ("Agility", "agility"),
                ("Intellect", "intellect"),
                ("Perception", "perception"),
                ("Stamina", "stamina")
            ]

            while self.skill_points > 0:
                print(f"\nYou have {self.skill_points} skill point(s) remaining.")
                print("Choose a stat to increase (or type 'q' to quit and save points):")
                for i, (label, attr) in enumerate(stats):
                    print(f"{i}: {label} ({getattr(self, attr)})")

                choice = input("Enter the number of the stat to increase (or 'q' to quit): ")

                if choice.lower() == 'q':
                    print("\nExiting stat allocation. Unused skill points will be saved.")
                    break

                try:
                    choice = int(choice)
                    if 0 <= choice < len(stats):
                        attr = stats[choice][1]

                        # If player has >1 points, ask how many to allocate
                        if self.skill_points > 1:
                            amount = input(f"How many points would you like to allocate to {stats[choice][0]}? ")
                            try:
                                amount = int(amount)
                                if amount < 1 or amount > self.skill_points:
                                    print("Invalid amount. Please choose between 1 and your remaining points.")
                                    continue
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                                continue
                        else:
                            amount = 1  # auto-allocate if only 1 point left

                        # Apply the allocation
                        setattr(self, attr, getattr(self, attr) + amount)
                        self.skill_points -= amount
                        print(f"{stats[choice][0]} increased to {getattr(self, attr)}!")
                    else:
                        print("Invalid choice. Please select a valid stat number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            print("\nFinal stats:")
            for label, attr in stats:
                print(f"{label}: {getattr(self, attr)}")
            print(f"Unspent skill points: {self.skill_points}")
        
        def calc_power(self):
            """"""
            str_pwr = self.strength
            agl_pwr = self.agility * self.agility
            prc_pwr = self.perception
            int_pwr = int(self.intellect * self.intellect * 2.5)
            stm_pwr = int(self.stamina * 1.25)

            return int(0.5 * (str_pwr * agl_pwr)) + prc_pwr + int_pwr + stm_pwr

    p = MPlayer(
        level=1
    )

    for _ in range(10):
        p.adjust_level(p.level + 100)
        p.skill_points += 10 if p.level % 10 == 0 else 0
        p.stat_selection()
        print(f"Power Level: {p.calc_power():,}")

if __name__ == "__main__":
    main70()
    
    """
    for r in Mon.rarities:
        if r == "Any": 
            continue
        main60(designated_rarity=r, designated_pearl=2)
    """
    # 12 : game testing
    # 34 : atk boost / level-up testing
    # 58 : type-spec w% testing per type
    # 54 : best moves by type