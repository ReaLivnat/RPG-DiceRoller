import random
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


# Dice rolling functions
def roll_dice(sides):
    return random.randint(1, sides)


def get_bardic_die(level):
    if level >= 15:
        return roll_dice(12)
    elif level >= 10:
        return roll_dice(10)
    elif level >= 5:
        return roll_dice(8)
    else:
        return roll_dice(6)

weapon_dice = {
    'Club': '1d4', 'Dagger': '1d4', 'Light Hammer': '1d4', 'Sickle': '1d4', 'Sling': '1d4', 'Dart': '1d4',
    'Whip': '1d4', 'Shortsword': '1d6', 'Handaxe': '1d6', 'Javelin': '1d6', 'Mace': '1d6', 'Quarterstaff': '1d6',
    'Spear': '1d6', 'hortbow': '1d6', 'Hand Crossbow': '1d6', 'Trident': '1d6', 'Scimitar': '1d6',
    'Light Crossbow': '1d8', 'Battleaxe': '1d8', 'Flail': '1d8', 'Longsword': '1d8', 'Morningstar': '1d8',
    'War Pick': '1d8', 'Warhammer': '1d8', 'Greatclub': '1d8', 'Longbow': '1d8', 'Rapier': '1d8', 'Pike': '1d10',
    'Glaive': '1d10', 'Heavy Crossbow': '1d10', 'Greatsword': '1d12', 'Greataxe': '1d12', 'Lance': '1d12',
    'Maul': '1d12'
}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/roll', methods=['POST'])
def roll():
    roll_type = request.form['roll_type']
    modifiers = int(request.form['modifiers'])
    conditions = request.form.getlist('conditions')
    bardic_level = int(request.form.get('bardic_level', 0))

    roll = roll_dice(20)
    nat1_or_20 = ""

    if 'A' in conditions:
        advantage_roll = roll_dice(20)
        chosen_roll = max(roll, advantage_roll)
        result = {
            'Roll': roll,
            'Advantage Roll': advantage_roll,
            'Choosing higher roll': chosen_roll
        }
        if chosen_roll == 20:
            nat1_or_20 = "Nat20!"
        elif chosen_roll == 1:
            nat1_or_20 = "Nat1!"
    elif 'D' in conditions:
        disadvantage_roll = roll_dice(20)
        chosen_roll = min(roll, disadvantage_roll)
        result = {
            'Roll': roll,
            'Disadvantage Roll': disadvantage_roll,
            'Choosing lower roll': chosen_roll
        }
        if chosen_roll == 20:
            nat1_or_20 = "Nat20!"
        elif chosen_roll == 1:
            nat1_or_20 = "Nat1!"
    else:
        chosen_roll = roll
        result = {'Roll': roll}
        if chosen_roll == 20:
            nat1_or_20 = "Nat20!"
        elif chosen_roll == 1:
            nat1_or_20 = "Nat1!"

    result['Modifiers'] = modifiers
    total = chosen_roll + modifiers

    if 'G' in conditions:
        guidance_roll = roll_dice(4)
        result['Guidance'] = guidance_roll
        total += guidance_roll
    if 'B+' in conditions:
        bless_roll = roll_dice(4)
        result['Bless'] = bless_roll
        total += bless_roll
    if 'B-' in conditions:
        bane_roll = roll_dice(4)
        result['Bane'] = bane_roll
        total -= bane_roll
    if 'I' in conditions:
        bardic_roll = get_bardic_die(bardic_level)
        result['Bardic Inspiration'] = bardic_roll
        total += bardic_roll

    result['Total'] = total
    if nat1_or_20:
        result['Nat1_or_20'] = nat1_or_20
    result['roll_type'] = roll_type

    return jsonify(result)


@app.route('/roll_damage', methods=['POST'])
def roll_damage():
    data = request.get_json()
    dice = data['dice']
    modifiers = data['modifiers']

    dice_count, dice_sides = map(int, dice.split('d'))
    roll = sum(roll_dice(dice_sides) for _ in range(dice_count))
    total = roll + modifiers

    result = {
        'Roll': roll,
        'Total': total
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)