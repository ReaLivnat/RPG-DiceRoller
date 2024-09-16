import random


# Dice rolling functions
def roll_dice(sides):
    """Rolls dice with the given number of sides and returns a random number."""
    return random.randint(1, sides)


def get_bardic_die(level):
    """Determines the Bardic Inspiration die based on the level."""
    if level >= 15:
        return roll_dice(12)
    elif level >= 10:
        return roll_dice(10)
    elif level >= 5:
        return roll_dice(8)
    else:
        return roll_dice(6)


def get_conditions(roll_type):
    """Prompts the user for conditions based on the roll type and validates them."""
    valid_conditions = ["A", "D", "B+", "B-", "G", "I"]
    if roll_type == "Damage Roll":
        return ""  # No conditions for Damage Roll

    while True:
        conditions = input(f"Enter the conditions ({', '.join(valid_conditions)}): ").strip().upper()
        if 'A' in conditions and 'D' in conditions:
            print("Advantage and Disadvantage cancel each other out.")
            conditions = conditions.replace('A', '').replace('D', '')
        if 'B+' in conditions and 'B-' in conditions:
            print("Bless and Bane cancel each other out.")
            conditions = conditions.replace('B+', '').replace('B-', '')
        conditions = ''.join(c for c in conditions if c in valid_conditions)
        return conditions


def get_any_modifier():
    """Prompts the user for modifiers and validates the input."""
    while True:
        try:
            return int(input("Enter sum of modifiers: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_bardic_level():
    """Prompts the user for Bardic Inspiration level and validates the input."""
    while True:
        try:
            level = int(input("Enter Bardic Inspiration level (1-20): "))
            if 1 <= level <= 20:
                return level
            else:
                print("Invalid level. Bardic Inspiration level must be between 1 and 20.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_weapon_damage(weapon):
    """Returns the dice type and damage type for a given weapon."""
    weapons = {
        "Club": (4, "bludgeoning"), "Dagger": (4, "piercing"), "Light Hammer": (4, "bludgeoning"),
        "Sickle": (4, "slashing"), "Sling": (4, "bludgeoning"), "Dart": (4, "piercing"),
        "Whip": (4, "slashing"), "Shortsword": (6, "piercing"), "Handaxe": (6, "slashing"),
        "Javelin": (6, "piercing"), "Mace": (6, "bludgeoning"), "Quarterstaff": (6, "bludgeoning"),
        "Spear": (6, "piercing"), "Shortbow": (6, "piercing"), "Hand Crossbow": (6, "piercing"),
        "Trident": (6, "piercing"), "Scimitar": (6, "slashing"), "Light Crossbow": (8, "piercing"),
        "Battleaxe": (8, "slashing"), "Flail": (8, "bludgeoning"), "Longsword": (8, "slashing"),
        "Morningstar": (8, "piercing"), "War Pick": (8, "piercing"), "Warhammer": (8, "bludgeoning"),
        "Greatclub": (8, "bludgeoning"), "Longbow": (8, "piercing"), "Rapier": (8, "piercing"),
        "Pike": (10, "piercing"), "Glaive": (10, "slashing"), "Heavy Crossbow": (10, "piercing"),
        "Greatsword": (12, "slashing"), "Greataxe": (12, "slashing"), "Lance": (12, "piercing"),
        "Maul": (12, "bludgeoning"), "Blowgun": (1, "piercing"),  # Special handling for Blowgun
    }
    return weapons.get(weapon, (0, "unknown"))


def roll_with_conditions(conditions, roll_fn):
    """Rolls with advantage, disadvantage, or normal."""
    if 'A' in conditions or 'D' in conditions:
        roll1, roll2 = roll_fn(), roll_fn()
        result = max(roll1, roll2) if 'A' in conditions else min(roll1, roll2)
        print(f"{'Advantage' if 'A' in conditions else 'Disadvantage'}: Rolled {roll1} and {roll2}. Result is {result}.")
        return result, 20 in (roll1, roll2)
    else:
        roll = roll_fn()
        print(f"Rolled a {roll}.")
        return roll, roll == 20


def apply_conditions_to_total(total, conditions, bardic_level=None):
    """Applies conditions to the total roll value."""
    if 'I' in conditions:
        extra = get_bardic_die(bardic_level)
        total += extra
        print(f"Bardic Inspiration: Rolled {extra}. Added to total.")
    if 'G' in conditions:
        extra = roll_dice(4)
        total += extra
        print(f"Guidance: Rolled {extra}. Added to total.")
    if 'B+' in conditions:
        extra = roll_dice(4)
        total += extra
        print(f"Bless: Rolled {extra}. Added to total.")
    if 'B-' in conditions:
        extra = roll_dice(4)
        total -= extra
        print(f"Bane: Rolled {extra}. Subtracted from total.")
    return total


def process_roll(modifiers, conditions, roll_fn):
    """Process a roll with given modifiers and conditions."""
    bardic_level = None
    if 'I' in conditions:
        bardic_level = get_bardic_level()

    roll, nat20_occurred = roll_with_conditions(conditions, roll_fn)

    if roll == 1:
        use_luck = input("Rolled a 1. Halfling Luck? (Y/N): ").strip().upper()
        if use_luck == 'Y':
            roll = roll_dice(20)
            print("Rerolled using Halfling Luck.")
            nat20_occurred = roll == 20

    total = roll + modifiers
    total = apply_conditions_to_total(total, conditions, bardic_level)
    print(f"Final total is {total}")
    return roll, nat20_occurred


def process_damage_roll(nat20_occurred):
    """Process the damage roll."""
    weapon = input("Enter your Weapon of Choice: ").strip().title()
    damage_dice, damage_type = get_weapon_damage(weapon)
    roll = roll_dice(damage_dice)
    original_roll = roll
    if nat20_occurred:
        roll *= 2  # Double the damage roll if the last attack roll was a natural 20
        print("Nat20! Doubling damage dice roll.")
    modifiers = get_any_modifier()
    total = roll + modifiers
    if nat20_occurred:
        print(f"Weapon: {weapon}, Damage Roll: {original_roll} (doubled), Total: {total} {damage_type.capitalize()} Damage.")
    else:
        print(f"Weapon: {weapon}, Damage Roll: {original_roll}, Total: {total} {damage_type.capitalize()} Damage.")


def main():
    while True:
        roll_type = input("Enter the type of roll (Ability Check, Skill Check, Saving Throw, Attack Roll): ").strip().title()
        if roll_type not in ["Ability Check", "Skill Check", "Saving Throw", "Attack Roll"]:
            print("Invalid roll type. Please choose from Ability Check, Skill Check, Saving Throw or Attack Roll.")
            continue

        if roll_type == "Damage Roll":
            process_damage_roll(nat20_occurred=True)
        else:
            modifiers = get_any_modifier()
            conditions = get_conditions(roll_type)
            roll_fn = lambda: roll_dice(20)
            roll, nat20_occurred = process_roll(modifiers, conditions, roll_fn)

            if roll_type == "Attack Roll":
                hit_check = input("Does that hit? (Y/N): ").strip().upper()
                if hit_check == 'Y':
                    process_damage_roll(nat20_occurred)


if __name__ == "__main__":
    main()