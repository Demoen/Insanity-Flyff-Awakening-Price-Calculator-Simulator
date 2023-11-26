from flask import Flask, request, render_template
import pandas as pd
import random

app = Flask(__name__)


gr0_table = {
    "STR": 'gr1',
    "STA": 'gr1',
    "DEX": 'gr1',
    "INT": 'gr1',
    "ADOCH": 'gr1',
    "IA": 'gr2',
    "PVE": 'gr2',
    "MP": 'gr2',
    "HP": 'gr2',
    "DCT": 'gr3',
}

gr1_table = {
    24: 16.48,
    25: 16.48,
    28: 16.48,
    33: 16.48,
    36: 16.48,
    38: 16.48,
    40: 1.0,
    41: 0.1,
    43: 0.01,
    45: 0.001,
}

gr2_table = {
    8: 16.48,
    9: 16.48,
    10: 16.48,
    11: 16.48,
    12: 16.48,
    14: 16.48,
    15: 1.0,
    16: 0.1,
    17: 0.01,
    18: 0.001,
}

gr3_table = {
    12: 16.48,
    14: 16.48,
    16: 16.48,
    18: 16.48,
    20: 16.48,
    22: 16.48,
    24: 1.0,
    26: 0.1,
    28: 0.01,
    30: 0.001,
}

group_tables = {
    "gr1": gr1_table,
    "gr2": gr2_table,
    "gr3": gr3_table
}

base_combinations = {
    ('IA', 'IA', 'IA'): {'combined_value_1': 42, 'combined_value_2': 0, 'price': 180000},
    ('PVE', 'PVE', 'PVE'): {'combined_value_1': 42, 'combined_value_2': 0, 'price': 110000},
    ('HP', 'HP', 'HP'): {'combined_value_1': 42, 'combined_value_2': 0, 'price': 170000},
    ('ADOCH', 'ADOCH', 'ADOCH'): {'combined_value_1': 114, 'combined_value_2': 0, 'price': 80000},
    ('MP', 'MP', 'MP'): {'combined_value_1': 42, 'combined_value_2': 0, 'price': 10000},
    ('STR', 'STR', 'STR'): {'combined_value_1': 114, 'combined_value_2': 0, 'price': 3000},
    ('INT', 'INT', 'INT'): {'combined_value_1': 114, 'combined_value_2': 0, 'price': 3000},
    ('DEX', 'DEX', 'DEX'): {'combined_value_1': 114, 'combined_value_2': 0, 'price': 3000},
    ('DCT', 'DCT', 'DCT'): {'combined_value_1': 66, 'combined_value_2': 0, 'price': 10},
    ('STA', 'STA', 'STA'): {'combined_value_1': 114, 'combined_value_2': 0, 'price': 35000},
    ('ADO', 'ADO', 'IA'): {'combined_value_1': 76, 'combined_value_2': 14, 'price': 70000},
    ('IA', 'IA', 'ADO'): {'combined_value_1': 28, 'combined_value_2': 38, 'price': 90000},
    ('IA', 'IA', 'PVE'): {'combined_value_1': 28, 'combined_value_2': 14, 'price': 100000},
    ('ADO', 'ADO', 'PVE'): {'combined_value_1': 76, 'combined_value_2': 14, 'price': 50000},
    ('PVE', 'PVE', 'ADO'): {'combined_value_1': 28, 'combined_value_2': 38, 'price': 30000},
    ('DEX', 'DEX', 'IA'): {'combined_value_1': 76, 'combined_value_2': 14, 'price': 5000},
    ('IA', 'IA', 'DEX'): {'combined_value_1': 28, 'combined_value_2': 38, 'price': 10000},
    ('PVE', 'PVE', 'DEX'): {'combined_value_1': 28, 'combined_value_2': 38, 'price': 5000},
    ('HP', 'HP', 'IA'): {'combined_value_1': 28, 'combined_value_2': 14, 'price': 20000},
    ('HP', 'HP', 'MP'): {'combined_value_1': 28, 'combined_value_2': 14, 'price': 5000},
    ('HP', 'HP', 'STA'): {'combined_value_1': 28, 'combined_value_2': 38, 'price': 120000},
    ('IA', 'IA', 'HP'): {'combined_value_1': 28, 'combined_value_2': 14, 'price': 10000},
    ('IA', 'IA', 'INT'): {'combined_value_1': 28, 'combined_value_2': 38, 'price': 35000},
    ('INT', 'INT', 'IA'): {'combined_value_1': 76, 'combined_value_2': 14, 'price': 10000},
    ('PVE', 'PVE', 'INT'): {'combined_value_1': 28, 'combined_value_2': 38, 'price': 5000},
    ('MP', 'MP', 'HP'): {'combined_value_1': 28, 'combined_value_2': 14, 'price': 5000},
    ('PVE', 'PVE', 'IA'): {'combined_value_1': 28, 'combined_value_2': 14, 'price': 80000},
    ('STA', 'STA', 'HP'): {'combined_value_1': 76, 'combined_value_2': 14, 'price': 60000},
    ('IA', 'IA', 'STR'): {'combined_value_1': 28, 'combined_value_2': 38, 'price': 6000},
    ('PVE', 'PVE', 'STR'): {'combined_value_1': 28, 'combined_value_2': 38, 'price': 5000},
    ('STR', 'STR', 'IA'): {'combined_value_1': 76, 'combined_value_2': 14, 'price': 4000}
}

# Define probabilities for number of lines
probabilities_lines = {
    1: 0.10,  # 10% chance for 1 line
    2: 0.50,  # 50% chance for 2 lines
    3: 0.40   # 40% chance for 3 lines
}

# Function to roll the number of lines
def roll_lines():
    roll = random.random()
    cumulative = 0
    for lines, probability in probabilities_lines.items():
        cumulative += probability
        if roll <= cumulative:
            return lines
    return 1

# Function to roll awakenings for each line
def roll_awakenings(num_lines):
    rolled_awakenings = []
    for _ in range(num_lines):
        awakening_type = random.choice(list(gr0_table.keys()))
        group = gr0_table[awakening_type]
        value = roll_group_value(group)
        rolled_awakenings.append((awakening_type, value))
    return rolled_awakenings

# Function to roll for specific value within a group
def roll_group_value(group):
    table = group_tables[group]
    value = random.choices(list(table.keys()), weights=list(table.values()), k=1)[0]
    return value


# Define the index route
@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize variables outside the if block
    selected_attribute1 = ''
    selected_value1 = ''
    selected_attribute2 = ''
    selected_value2 = ''
    selected_attribute3 = ''
    selected_value3 = ''
    
    combined_chance = None
    price_range_lower = None
    price_range_upper = None
    rolled_awakenings = None
    num_lines = None
    error = None

    if request.method == 'POST':
         # Capture selected attributes and values
        selected_attribute1 = request.form.get('attribute1', '')
        selected_value1 = request.form.get('value1', '')
        selected_attribute2 = request.form.get('attribute2', '')
        selected_value2 = request.form.get('value2', '')
        selected_attribute3 = request.form.get('attribute3', '')
        selected_value3 = request.form.get('value3', '')

        if 'roll_awakenings' in request.form:
            # Handle awakening roll
            num_lines = roll_lines()
            rolled_awakenings = roll_awakenings(num_lines)
        else:
            try:
                attributes_and_values = [
                    (request.form['attribute1'], int(request.form['value1'])),
                    (request.form['attribute2'], int(request.form['value2'])),
                    (request.form['attribute3'], int(request.form['value3']))
                ]


                def get_probability(key, value):
                    if key in gr0_table:
                        table_name = gr0_table[key]
                        if table_name == 'gr1':
                            return gr1_table.get(value, 0)
                        elif table_name == 'gr2':
                            return gr2_table.get(value, 0)
                        elif table_name == 'gr3':
                            return gr3_table.get(value, 0)
                    return 0

                # Calculate the probability of rolling a specific attribute from gr0_table
                probability_of_any_attribute = 1 / len(gr0_table)

                # Count the number of unique attributes
                unique_attributes = len(set([attr for attr, _ in attributes_and_values]))

                # Calculate the probability for the number of lines (1, 2, or 3)
                probability_of_lines = probabilities_lines.get(unique_attributes, 0)

                # Calculate the combined chance for the specific combination entered
                combined_chance = 1.0
                for attribute, value in set(attributes_and_values):
                    probability_of_attribute = probability_of_any_attribute
                    probability_of_value = get_probability(attribute, value) / 100
                    occurrences = attributes_and_values.count((attribute, value))
                    combined_chance *= (probability_of_attribute * probability_of_value) ** occurrences

                # Multiply by the probability of getting that number of lines
                combined_chance *= probability_of_lines

                combined_chance *= 100
                print(f"The percentage chance for the combination is: {combined_chance:.8f}%")

                def calculate_combined_values(attributes_and_values):
                    # A function to calculate combined values for same stats
                    combined_values = {}
                    for attr, val in attributes_and_values:
                        if attr in combined_values:
                            combined_values[attr] += val
                        else:
                            combined_values[attr] = val
                    return combined_values

                def find_base_price(combined_values):
                    # A function to find the base price and combined values for the closest matching combination
                    for combo, details in base_combinations.items():
                        if set(combo) == set(combined_values.keys()):
                            return details
                    return None

                def get_price_adjustment(base_details, combined_values, variability_percentage=10):
                    # Calculate the total combined value for the input attributes
                    total_combined_value = sum(combined_values.values())

                    # Base total combined value for the combination from base_combinations
                    base_total_combined_value = base_details['combined_value_1'] + base_details['combined_value_2']

                    # Calculate deviation
                    deviation = total_combined_value - base_total_combined_value

                    # Define multipliers for price adjustment
                    upward_multiplier = 1.6  # Double the price for each step upwards
                    downward_multiplier = 0.45  # Half the price for each step downwards

                    # Calculate price adjustment
                    if deviation > 0:
                        # Double the price for each step above the base
                        adjusted_price = base_details['price'] * (upward_multiplier ** deviation)
                    elif deviation < 0:
                        # Half the price for each step below the base
                        adjusted_price = base_details['price'] * (downward_multiplier ** abs(deviation))
                    else:
                        adjusted_price = base_details['price']

                    # Apply variability percentage to create a price range
                    price_range_lower = adjusted_price * (1 - variability_percentage / 100)
                    price_range_upper = adjusted_price * (1 + variability_percentage / 100)

                    # Ensure that the prices do not drop below zero
                    price_range_lower = max(0, price_range_lower)
                    price_range_upper = max(0, price_range_upper)

                    return price_range_lower, price_range_upper


                # Get the combined values for the input attributes
                combined_values = calculate_combined_values(attributes_and_values)

                # Find the base price for the closest matching combination
                base_details = find_base_price(combined_values)

                if base_details:
                    # Calculate the adjusted price range
                    price_range_lower, price_range_upper = get_price_adjustment(base_details, combined_values)
                    print(f"The adjusted price range for the combination is: {price_range_lower:.2f} Perins to {price_range_upper:.2f} Perins")
                else:
                    print("No matching combination found for the provided attributes.")

            except ValueError:
                error = "Sorry, only 3 line awakenings are worth noteable amounts of Perin."

     # Render the template with the results or error message
    return render_template('index.html', combined_chance=combined_chance, price_range_lower=price_range_lower, price_range_upper=price_range_upper, rolled_awakenings=rolled_awakenings, num_lines=num_lines, error=error, selected_attribute1=selected_attribute1,
                           selected_value1=selected_value1,
                           selected_attribute2=selected_attribute2,
                           selected_value2=selected_value2,
                           selected_attribute3=selected_attribute3,
                           selected_value3=selected_value3)

if __name__ == '__main__':
    app.run(debug=True)