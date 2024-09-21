This is a Python-based dice rolling application designed for tabletop RPG games, particularly Dungeons & Dragons. It simulates rolling dice for various actions (Ability Check, Skill Check, Saving Throw, and Attack Roll) and applies additional conditions such as Advantage, Disadvantage, Bardic Inspiration, Guidance, Bless, and Bane. The app also handles Halfling Luck, weapon damage rolls, and critical hits.

## Features

- **Roll Dice:** Simulates rolling a 20-sided die (or other dice based on context).
- **Conditions:** Supports game-specific conditions:
  - **Advantage (A)** and **Disadvantage (D)** cancel each other out.
  - **Bless (B+)** and **Bane (B-)** cancel each other out.
  - **Bardic Inspiration (I):** Rolls a bonus die based on the character's level (d6-d12).
  - **Guidance (G):** Adds a d4 roll to the total.
- **Modifiers:** Allows you to add or subtract modifiers to the roll.
- **Weapon Damage:** Handles different weapon damage types and dice rolls.
- **Critical Hit (Natural 20):** Automatically doubles the damage dice for critical hits.
- **Halfling Luck:** Allows rerolling a natural 1.

## Usage

1. **Roll Type:**
   - Enter the type of roll: Ability Check, Skill Check, Saving Throw, or Attack Roll.
   
2. **Conditions:** 
   - Input any conditions affecting the roll (e.g., A for Advantage, D for Disadvantage).
   
3. **Modifiers:** 
   - Add any modifiers to the roll.

4. **Weapon Damage (for Attack Rolls):** 
   - After a successful hit, select your weapon for the damage roll. If a critical hit occurred, the damage dice will be doubled.

## Example

1. The app prompts you for the type of roll.
2. Enter modifiers and conditions such as Advantage (A) or Bless (B+).
3. The app rolls the dice, applies the conditions, and returns the final result.
4. For Attack Rolls, it asks if the attack was successful and rolls damage dice, applying critical hit rules if applicable.

## Requirements

- Python 3.x

## How to Run

1. Download or clone this repository.
2. Run the script in a Python environment:
   ```bash
   python dice_roller.py


This App uses flask version 24.2
