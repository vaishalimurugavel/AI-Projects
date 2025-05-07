from ortools.sat.python import cp_model
import json
import csv

# ----- Load Pantry Data -----
pantry = {}
with open('pantry.csv') as csvFile:
    pantryData = csv.DictReader(csvFile)
    for row in pantryData:
        item = row['items'].strip()
        pantry[item] = {
            'servings': float(row['servings']),
            'price': float(row['price'])
        }

# ----- Load Recipes Data -----
with open('recipes.json') as json_file:
    data = json.load(json_file)

recipeList = list(data.keys())

# ----- Precompute cost, protein info, meal type -----
recipe_costs = []
is_protein = []
meal_types = {'breakfast': [], 'lunch': [], 'dinner': []}
nutrientType = 'protein'

for i, recipe in enumerate(recipeList):
    items = data[recipe]["items"]
    cost = 0.0
    for item in items:
        if item in pantry:
            cost += pantry[item]['price']
        else:
            print(f"Warning: '{item}' not found in pantry!")
            # Penalty for missing item
            cost += 10
    recipe_costs.append(round(cost, 2))
    is_protein.append(1 if data[recipe]["rich nutrient"] == nutrientType else 0)
    meal_types[data[recipe]["meal type"]].append(i)

# ----- Initialize CP-SAT model -----
model = cp_model.CpModel()

totalMeals = 21  # 7 days × 3 meals
BUDGET_LIMIT = 800  # dollars

# ----- Decision variables -----
mealList = [model.NewIntVar(0, len(recipeList) - 1, f"meal_{i}") for i in range(totalMeals)]

# ----- Cost variables -----
cost_vars = []
scaled_costs = [int(c * 100) for c in recipe_costs]
for i in range(totalMeals):
    cost_var = model.NewIntVar(0, max(scaled_costs), f"cost_{i}")
    model.AddElement(mealList[i], scaled_costs, cost_var)
    cost_vars.append(cost_var)

total_cost = model.NewIntVar(0, 10000, "total_cost")
model.Add(total_cost == sum(cost_vars))
model.Add(total_cost <= BUDGET_LIMIT * 100)
#
# # ----- Protein constraint -----
protein_flags = []
for i in range(totalMeals):
    flag = model.NewBoolVar(f"protein_flag_{i}")
    model.AddElement(mealList[i], is_protein, flag)
    protein_flags.append(flag)
model.Add(sum(protein_flags) >= 12)

# ----- Meal type constraint (3 meals per day: breakfast, lunch, dinner) -----
for day in range(7):
    b = mealList[3 * day]
    l = mealList[3 * day + 1]
    d = mealList[3 * day + 2]

    model.AddAllowedAssignments([b], [[i] for i in meal_types['breakfast']])
    model.AddAllowedAssignments([l], [[i] for i in meal_types['lunch']])
    model.AddAllowedAssignments([d], [[i] for i in meal_types['dinner']])

# ----- Solve -----
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("Feasible Meal Plan Found!")
    for i in range(totalMeals):
        print(f"Meal {i + 1}: {recipeList[solver.Value(mealList[i])]}")
    print("Total Cost:", round(solver.Value(total_cost) / 100, 2))
    print("Protein-rich meals:", sum(solver.Value(f) for f in protein_flags))
else:
    print("No feasible solution found.")
