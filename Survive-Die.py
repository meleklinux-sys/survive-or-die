#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Survive or Die — Story Mode (Bilingual: Arabic + English)
Features added:
 - 3 new stages (Desert, Lab, Forest) + Boss Final
 - ANSI colors + improved terminal UI
 - Save / Load game (results and checkpoint)
 - Bilingual prompts (switch at start)
 - Input validation and robust flow

Save file as: survive_or_die_story_en_ar.py
Run: python3 survive_or_die_story_en_ar.py
"""

import sys
import time
import random
import os
import json
from datetime import datetime

# Optional color support for Windows
try:
    import colorama
    colorama.init()
except Exception:
    pass

# ----------------- Terminal Colors -----------------
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

FG_RED = "\033[31m"
FG_GREEN = "\033[32m"
FG_YELLOW = "\033[33m"
FG_BLUE = "\033[34m"
FG_MAGENTA = "\033[35m"
FG_CYAN = "\033[36m"
FG_WHITE = "\033[37m"

BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"

# ----------------- Settings -----------------
TYPE_DELAY = 0.018
FAST_DELAY = 0.005
SAVE_FILENAME = "sod_checkpoint.json"
RESULTS_FILENAME = "sod_results.txt"

# --------------- Utility Functions ----------------

def type_text(text, delay=TYPE_DELAY, newline=True, color=None):
    """Typewriter effect with optional color."""
    if color:
        sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    if color:
        sys.stdout.write(RESET)
    if newline:
        sys.stdout.write("\n")
    sys.stdout.flush()


def loading_bar(text="Loading", steps=20, speed=0.03, color=None):
    if color:
        type_text(text, color=color)
    else:
        type_text(text)
    for i in range(steps):
        bar = "[" + "#" * (i+1) + "-" * (steps-i-1) + "]"
        sys.stdout.write(bar + "\r")
        sys.stdout.flush()
        time.sleep(speed)
    print()


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def ask_int(prompt, valid=None, lang="en"):
    """Ask for integer with optional set of valid answers."""
    while True:
        try:
            val = input(prompt).strip()
            num = int(val)
            if valid and num not in valid:
                if lang == "ar":
                    type_text("   .", FAST_DELAY, color=FG_YELLOW)
                else:
                    type_text("Please choose a valid option.", FAST_DELAY, color=FG_YELLOW)
                continue
            return num
        except ValueError:
            if lang == "ar":
                type_text("   .", FAST_DELAY, color=FG_YELLOW)
            else:
                type_text("Please enter a valid number.", FAST_DELAY, color=FG_YELLOW)


# ----------------- Player -----------------
class Player:
    def __init__(self, name, lang="en"):
        self.name = name
        self.hp = 3
        self.score = 0
        self.char = None
        self.inventory = []
        self.lang = lang
        self.stage = 0  # track progress for save/load

    def to_dict(self):
        return {
            "name": self.name,
            "hp": self.hp,
            "score": self.score,
            "char": self.char,
            "inventory": self.inventory,
            "lang": self.lang,
            "stage": self.stage,
        }

    @classmethod
    def from_dict(cls, d):
        p = cls(d.get("name", "player"), d.get("lang", "en"))
        p.hp = d.get("hp", 3)
        p.score = d.get("score", 0)
        p.char = d.get("char")
        p.inventory = d.get("inventory", [])
        p.stage = d.get("stage", 0)
        return p

# ----------------- Save / Load -----------------

def save_checkpoint(player):
    try:
        with open(SAVE_FILENAME, "w", encoding="utf-8") as f:
            json.dump(player.to_dict(), f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        return False


def load_checkpoint():
    try:
        if not os.path.exists(SAVE_FILENAME):
            return None
        with open(SAVE_FILENAME, "r", encoding="utf-8") as f:
            d = json.load(f)
        return Player.from_dict(d)
    except Exception:
        return None


def append_result(player, tag, final_score):
    try:
        with open(RESULTS_FILENAME, "a", encoding="utf-8") as f:
            f.write(f"{datetime.utcnow().isoformat()} | {player.name} | {player.char} | {tag} | Score:{int(final_score)} | HP:{player.hp}\n")
        return True
    except Exception:
        return False

# ----------------- Scenes / Levels -----------------

def intro(player):
    clear()
    type_text(BOLD + "=== SURVIVE OR DIE: STORY MODE ===" + RESET, color=FG_CYAN)
    if player.lang == "ar":
        type_text(f"\n {player.name} –   .", color=FG_CYAN)
        type_text(" :")
        type_text("1)  — +")
        type_text("2)  — +")
        type_text("3)  — +")
        ch = ask_int(" 1-3: ", valid={1,2,3}, lang="ar")
        player.char = {1: "", 2: "", 3: ""}[ch]
        type_text(f": {player.char}.  !", color=FG_GREEN)
    else:
        type_text(f"\nWelcome, {player.name} — Story Mode.", color=FG_CYAN)
        type_text("Choose your character:")
        type_text("1) Trickster — +luck")
        type_text("2) Warrior — +force")
        type_text("3) Scholar — +intellect")
        ch = ask_int("Choose 1-3: ", valid={1,2,3}, lang="en")
        player.char = {1: "Trickster", 2: "Warrior", 3: "Scholar"}[ch]
        type_text(f"You are: {player.char}. Good luck!", color=FG_GREEN)
    type_text("(press Enter to continue)" if player.lang=="en" else " Enter ...")
    input()


# Level 1: Town (reuse earlier logic but bilingual)
def level_town(player):
    player.stage = max(player.stage, 1)
    clear()
    loading_bar("Arriving at the abandoned town..." if player.lang=="en" else "   ...", color=FG_MAGENTA)
    if player.lang == "ar":
        type_text("\n:  ...")
        type_text("1)    ")
        type_text("2)   ")
        type_text("3)   ")
        choice = ask_int(" 1-3: ", valid={1,2,3}, lang="ar")
    else:
        type_text("\nScene: Abandoned town...")
        type_text("1) Approach the occupied-looking house")
        type_text("2) Enter the abandoned house")
        type_text("3) Walk past quickly")
        choice = ask_int("Choose 1-3: ", valid={1,2,3}, lang="en")

    luck = random.random()
    if player.char in ("Trickster", ""):
        luck += 0.15
    elif player.char in ("Warrior", ""):
        luck += 0.05
    else:
        luck += 0.08

    if choice == 1:
        if luck > 0.5 or player.char in ("Scholar", ""):
            player.score += 10
            player.inventory.append("Canned Food")
            type_text("You negotiated and got supplies. +10 pts" if player.lang=="en" else "  ! +10 ", color=FG_GREEN)
        else:
            player.hp -= 1
            type_text("Fight broke out. -1 HP" if player.lang=="en" else "   .", color=FG_RED)
    elif choice == 2:
        if luck > 0.45:
            player.score += 5
            player.inventory.append("Medkit")
            type_text("You found medical supplies. +5 pts" if player.lang=="en" else "  . +5 ", color=FG_GREEN)
        else:
            player.hp -= 1
            type_text("A trap! -1 HP" if player.lang=="en" else "!  .", color=FG_RED)
    else:
        player.score += 1
        type_text("You avoided danger. +1 pt" if player.lang=="en" else " . +1 ", color=FG_YELLOW)

    summary(player)

# Level 2: Desert

def level_desert(player):
    player.stage = max(player.stage, 2)
    clear()
    loading_bar("Crossing the scorching desert..." if player.lang=="en" else "  ...", color=FG_YELLOW)
    if player.lang == "ar":
        type_text("\n:      ...")
        type_text("1)   ")
        type_text("2)   ")
        type_text("3)   ")
        choice = ask_int(" 1-3: ", valid={1,2,3}, lang="ar")
    else:
        type_text("\nScene: Endless sands and a distant oasis...")
        type_text("1) Search for an oasis")
        type_text("2) Follow vehicle tracks")
        type_text("3) Conserve and manage inventory")
        choice = ask_int("Choose 1-3: ", valid={1,2,3}, lang="en")

    luck = random.random()
    if "Canned Food" in player.inventory:
        luck += 0.1

    if choice == 1:
        if luck > 0.5:
            player.score += 8
            player.inventory.append("Oasis Water")
            type_text("You reached an oasis. +8 pts" if player.lang=="en" else " . +8 ", color=FG_GREEN)
        else:
            player.hp -= 1
            type_text("Heatstroke costs you. -1 HP" if player.lang=="en" else "  .  .", color=FG_RED)
    elif choice == 2:
        if luck > 0.6:
            player.score += 10
            player.inventory.append("Spare Parts")
            type_text("You found a broken convoy with supplies. +10 pts" if player.lang=="en" else "   . +10 ", color=FG_GREEN)
        else:
            player.hp -= 1
            type_text("You got lost. -1 HP" if player.lang=="en" else "  .  .", color=FG_RED)
    else:
        player.score += 2
        type_text("You conserved resources. +2 pts" if player.lang=="en" else " . +2 ", color=FG_YELLOW)

    summary(player)

# Level 3: Laboratory

def level_lab(player):
    player.stage = max(player.stage, 3)
    clear()
    loading_bar("Infiltrating an abandoned lab..." if player.lang=="en" else "  ...", color=FG_CYAN)
    if player.lang == "ar":
        type_text("\n:     ...")
        type_text("1)  ")
        type_text("2)   ")
        type_text("3)   ")
        choice = ask_int(" 1-3: ", valid={1,2,3}, lang="ar")
    else:
        type_text("\nScene: Lab with equipment and vials...")
        type_text("1) Inspect equipment")
        type_text("2) Take a sample carefully")
        type_text("3) Steal gear and leave")
        choice = ask_int("Choose 1-3: ", valid={1,2,3}, lang="en")

    luck = random.random()
    if "Medkit" in player.inventory:
        luck += 0.08

    if choice == 1:
        if luck > 0.55:
            player.score += 12
            player.inventory.append("Energy Cell")
            type_text("You repurposed machinery. +12 pts" if player.lang=="en" else "  . +12 ", color=FG_GREEN)
        else:
            player.hp -= 1
            type_text("Alarm! -1 HP" if player.lang=="en" else " .  .", color=FG_RED)
    elif choice == 2:
        if luck > 0.5:
            player.score += 15
            player.inventory.append("Vaccine Sample")
            type_text("Valuable sample acquired. +15 pts" if player.lang=="en" else "   . +15 ", color=FG_GREEN)
        else:
            player.hp -= 1
            type_text("Sample spoiled. -1 HP" if player.lang=="en" else " .  .", color=FG_RED)
    else:
        if luck > 0.4:
            player.score += 6
            player.inventory.append("Toolkit")
            type_text("You stole useful gear. +6 pts" if player.lang=="en" else "  . +6 ", color=FG_GREEN)
        else:
            player.hp -= 1
            type_text("Caught by scavengers. -1 HP" if player.lang=="en" else "  .  .", color=FG_RED)

    summary(player)

# Level 4: Forest

def level_forest(player):
    player.stage = max(player.stage, 4)
    clear()
    loading_bar("Moving through a dense forest..." if player.lang=="en" else "   ...", color=FG_GREEN)
    if player.lang == "ar":
        type_text("\n:    ...")
        type_text("1)   ")
        type_text("2)   ")
        type_text("3)   ")
        choice = ask_int(" 1-3: ", valid={1,2,3}, lang="ar")
    else:
        type_text("\nScene: Trees and unknown noises...")
        type_text("1) Follow the sound of water")
        type_text("2) Avoid the noise")
        type_text("3) Set traps for animals")
        choice = ask_int("Choose 1-3: ", valid={1,2,3}, lang="en")

    luck = random.random()
    if "Oasis Water" in player.inventory:
        luck += 0.07

    if choice == 1:
        if luck > 0.5:
            player.score += 9
            player.inventory.append("Fresh Water")
            type_text("Found a stream. +9 pts" if player.lang=="en" else "  . +9 ", color=FG_GREEN)
        else:
            player.hp -= 1
            type_text("Ambushed by bandits. -1 HP" if player.lang=="en" else "!  .", color=FG_RED)
    elif choice == 2:
        player.score += 3
        type_text("You avoided conflict. +3 pts" if player.lang=="en" else " . +3 ", color=FG_YELLOW)
    else:
        if luck > 0.55:
            player.score += 11
            player.inventory.append("Game Meat")
            type_text("Trap successful. +11 pts" if player.lang=="en" else " . +11 ", color=FG_GREEN)
        else:
            player.hp -= 1
            type_text("Trap failed. -1 HP" if player.lang=="en" else " .  .", color=FG_RED)

    summary(player)

# Final Boss Stage

def boss_final(player):
    player.stage = max(player.stage, 5)
    clear()
    loading_bar("Approaching the stronghold..." if player.lang=="en" else "   ...", color=FG_MAGENTA)
    if player.lang == "ar":
        type_text("\n :      .")
        type_text("1)  ")
        type_text("2) /")
        type_text("3)  ")
        choice = ask_int(" 1-3: ", valid={1,2,3}, lang="ar")
    else:
        type_text("\nFinal Scene: The gang controls the water supply.")
        type_text("1) Direct assault")
        type_text("2) Negotiate/deceive")
        type_text("3) Make a deal/ally")
        choice = ask_int("Choose 1-3: ", valid={1,2,3}, lang="en")

    base_roll = random.random()
    char_mod = 0.0
    if player.char in ("Warrior", ""):
        char_mod = 0.25 if choice == 1 else 0.05
    elif player.char in ("Scholar", ""):
        char_mod = 0.25 if choice == 2 else 0.05
    else:
        char_mod = 0.25 if choice == 2 else 0.1

    inventory_bonus = 0.0
    if "Vaccine Sample" in player.inventory:
        inventory_bonus += 0.2
    if "Game Meat" in player.inventory or "Canned Food" in player.inventory:
        inventory_bonus += 0.05
    if "Energy Cell" in player.inventory:
        inventory_bonus += 0.08

    final_score = player.score + (base_roll + char_mod + inventory_bonus) * 35

    if choice == 1:
        type_text("\nExecuting assault..." if player.lang=="en" else " ...")
        thresh = 45 if player.char in ("Warrior","") else 60
        if final_score >= thresh:
            return "victory_force", final_score
        else:
            return "defeat_force", final_score
    elif choice == 2:
        type_text("\nAttempting negotiation..." if player.lang=="en" else " ...")
        thresh = 48 if player.char in ("Trickster","","Scholar","") else 62
        if final_score >= thresh:
            return "victory_cunning", final_score
        else:
            return "defeat_cunning", final_score
    else:
        type_text("\nForming an alliance..." if player.lang=="en" else " ...")
        if final_score >= 75:
            return "victory_alliance", final_score
        elif final_score >= 45:
            return "compromise", final_score
        else:
            return "betrayed", final_score

# Summary helper

def summary(player):
    type_text("\n--- Status ---", color=FG_CYAN)
    type_text(f"Name: {player.name} | HP: {player.hp} | Score: {player.score}", color=FG_YELLOW)
    if player.inventory:
        type_text("Inventory: " + ", ".join(player.inventory), color=FG_MAGENTA)
    else:
        type_text("Inventory: (empty)", color=FG_MAGENTA)
    type_text("(press Enter to continue)" if player.lang=="en" else " Enter ...")
    input()

# Endings

def endings(tag, final_score, player):
    clear()
    type_text(BOLD + "=== FINAL OUTCOME ===" + RESET, color=FG_CYAN)
    if tag == "victory_force":
        type_text("You led a victorious assault and liberated the stronghold!" if player.lang=="en" else "    !", color=FG_GREEN)
    elif tag == "victory_cunning":
        type_text("Through cunning you secured control and rebalanced resources." if player.lang=="en" else "       .", color=FG_GREEN)
    elif tag == "victory_alliance":
        type_text("A risky alliance paid off — stable resources for many." if player.lang=="en" else "      .", color=FG_GREEN)
    elif tag == "compromise":
        type_text("You compromised — survival with strings attached." if player.lang=="en" else "  —   .", color=FG_YELLOW)
    elif tag == "betrayed":
        type_text("You were betrayed. Learn and adapt." if player.lang=="en" else " .  .", color=FG_RED)
    else:
        type_text("Defeat — you survived barely or perished." if player.lang=="en" else " —     .", color=FG_RED)

    type_text(f"Final Score: {int(final_score)} | HP: {player.hp}", color=FG_CYAN)
    type_text("Do you want to save this run to results file? (y/n)" if player.lang=="en" else "    (y/n)", color=FG_YELLOW)
    ans = input().strip().lower()
    if ans.startswith("y"):
        append_result(player, tag, final_score)
        type_text("Saved to file." if player.lang=="en" else " .", color=FG_GREEN)

# ----------------- Game Flow -----------------

def main():
    clear()
    type_text(BOLD + "Survive or Die — Story (EN/AR)" + RESET, color=FG_CYAN)
    type_text("1) English\n2) ")
    lang_choice = ask_int("Choose language 1-2: ", valid={1,2}, lang="en")
    lang = "en" if lang_choice == 1 else "ar"

    # Offer to load checkpoint
    loaded = None
    if os.path.exists(SAVE_FILENAME):
        type_text("Load previous checkpoint? (y/n)" if lang=="en" else "     (y/n)")
        if input().strip().lower().startswith("y"):
            loaded = load_checkpoint()
            if loaded:
                type_text((f"Loaded checkpoint for {loaded.name}." if lang=="en" else f"   {loaded.name}.") , color=FG_GREEN)
            else:
                type_text(("Failed to load checkpoint." if lang=="en" else "  ."), color=FG_YELLOW)

    if loaded:
        player = loaded
        player.lang = lang
    else:
        name = input("Enter player name: " if lang=="en" else "  : ").strip() or ("Player" if lang=="en" else "")
        player = Player(name, lang=lang)

    # Intro / character selection if new
    if player.stage == 0:
        intro(player)

    # Main sequence with save checkpoints between levels
    levels = [level_town, level_desert, level_lab, level_forest, boss_final]
    for idx, level_func in enumerate(levels, start=1):
        # Allow quick-save before starting each level
        type_text(("Do you want to save a checkpoint now? (y/n)" if player.lang=="en" else "     (y/n)"), color=FG_YELLOW)
        if input().strip().lower().startswith("y"):
            if save_checkpoint(player):
                type_text(("Checkpoint saved." if player.lang=="en" else "  ."), color=FG_GREEN)
            else:
                type_text(("Failed to save." if player.lang=="en" else " ."), color=FG_RED)

        level_func(player)

        if player.hp <= 0:
            type_text(("You have lost all HP. Game Over." if player.lang=="en" else " .  ."), color=FG_RED)
            # Offer reload
            type_text(("Load checkpoint and retry? (y/n)" if player.lang=="en" else "     (y/n)"), color=FG_YELLOW)
            if input().strip().lower().startswith("y"):
                loaded = load_checkpoint()
                if loaded:
                    player = loaded
                    type_text(("Checkpoint loaded. Resuming..." if player.lang=="en" else "  .  ..."), color=FG_GREEN)
                    continue
                else:
                    type_text(("No checkpoint available. Exiting." if player.lang=="en" else "   . ."), color=FG_RED)
            return

    tag, final_score = boss_final(player)
    endings(tag, final_score, player)

    # Remove checkpoint on successful end
    if os.path.exists(SAVE_FILENAME):
        try:
            os.remove(SAVE_FILENAME)
        except Exception:
            pass


if __name__ == "__main__":
    main()