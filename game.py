
import random
import json
import os

# -------------------- Player Initialization -------------------- #
def create_player():
    name = input("Enter your name, brave adventurer: ")
    player = {
        "name": name,
        "health": 100,
        "attack": 10,
        "gold": 50,
        "inventory": ["Health Potion"],
        "location": "forest"
    }
    print(f"\nWelcome, {name}! Your journey begins in a mysterious forest.")
    return player


# -------------------- Utility Functions -------------------- #
def print_status(player):
    print("\n" + "=" * 40)
    print(f"Name: {player['name']}")
    print(f"Health: {player['health']}")
    print(f"Attack: {player['attack']}")
    print(f"Gold: {player['gold']}")
    print(f"Inventory: {player['inventory']}")
    print("=" * 40)


def get_choice(options):
    while True:
        choice = input("Choose an option: ").strip().lower()
        if choice in options:
            return choice
        print("Invalid choice. Please try again.")


# -------------------- Save and Load -------------------- #
SAVE_FILE = "savegame.json"

def save_game(player):
    with open(SAVE_FILE, "w") as f:
        json.dump(player, f, indent=4)
    print("Game saved successfully!")


def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            player = json.load(f)
        print("Game loaded successfully!")
        return player
    else:
        print("No saved game found.")
        return None


# -------------------- Inventory Management -------------------- #
def use_potion(player):
    if "Health Potion" in player["inventory"]:
        player["health"] = min(100, player["health"] + 30)
        player["inventory"].remove("Health Potion")
        print("You used a Health Potion. Health restored by 30!")
    else:
        print("You don't have any Health Potions!")


# -------------------- Combat System -------------------- #
def combat(player, enemy_name, enemy_health, enemy_attack, reward_gold):
    print(f"\n⚔️ A wild {enemy_name} appears!")

    while enemy_health > 0 and player["health"] > 0:
        print(f"\nYour Health: {player['health']} | {enemy_name} Health: {enemy_health}")
        print("1. Attack")
        print("2. Use Health Potion")
        print("3. Run")

        choice = get_choice(["1", "2", "3"])

        if choice == "1":
            damage = random.randint(player["attack"] - 2, player["attack"] + 5)
            enemy_health -= damage
            print(f"You dealt {damage} damage to the {enemy_name}!")

        elif choice == "2":
            use_potion(player)
            continue

        elif choice == "3":
            if random.choice([True, False]):
                print("You successfully escaped!")
                return
            else:
                print("Escape failed!")

        if enemy_health > 0:
            enemy_damage = random.randint(enemy_attack - 2, enemy_attack + 4)
            player["health"] -= enemy_damage
            print(f"The {enemy_name} dealt {enemy_damage} damage to you!")

    if player["health"] <= 0:
        print("\n💀 You have been defeated. Game Over.")
        exit()
    else:
        print(f"\n🎉 You defeated the {enemy_name} and earned {reward_gold} gold!")
        player["gold"] += reward_gold


# -------------------- Shop System -------------------- #
def village(player):
    print("\n🏘️ You arrive at a peaceful village.")
    while True:
        print("\n1. Buy Health Potion (20 gold)")
        print("2. Upgrade Weapon (+5 attack for 50 gold)")
        print("3. Leave Village")

        choice = get_choice(["1", "2", "3"])

        if choice == "1":
            if player["gold"] >= 20:
                player["gold"] -= 20
                player["inventory"].append("Health Potion")
                print("You bought a Health Potion.")
            else:
                print("Not enough gold!")

        elif choice == "2":
            if player["gold"] >= 50:
                player["gold"] -= 50
                player["attack"] += 5
                print("Your weapon has been upgraded!")
            else:
                print("Not enough gold!")

        elif choice == "3":
            break


# -------------------- Locations -------------------- #
def forest(player):
    print("\n🌲 You are in the forest.")
    print("1. Explore Cave")
    print("2. Visit Village")
    print("3. Go to Castle")
    print("4. Save Game")
    print("5. Exit Game")

    choice = get_choice(["1", "2", "3", "4", "5"])

    if choice == "1":
        cave(player)
    elif choice == "2":
        village(player)
    elif choice == "3":
        castle(player)
    elif choice == "4":
        save_game(player)
    elif choice == "5":
        print("Thanks for playing!")
        exit()


def cave(player):
    print("\n🕳️ You enter a dark cave.")
    combat(player, "Goblin", enemy_health=40, enemy_attack=8, reward_gold=30)
    if random.choice([True, False]):
        player["inventory"].append("Health Potion")
        print("You found a Health Potion in the cave!")


def castle(player):
    print("\n🏰 You approach the haunted castle.")
    print("The final battle awaits!")
    combat(player, "Dragon", enemy_health=80, enemy_attack=12, reward_gold=100)
    print("\n👑 Congratulations! You defeated the Dragon and completed your adventure!")
    exit()


# -------------------- Main Game Loop -------------------- #
def main():
    print("====== 🏹 ADVENTURE QUEST 🏹 ======")
    print("1. New Game")
    print("2. Load Game")

    choice = get_choice(["1", "2"])

    if choice == "1":
        player = create_player()
    else:
        player = load_game()
        if player is None:
            player = create_player()

    while True:
        print_status(player)
        forest(player)


if __name__ == "__main__":
    main()
    
