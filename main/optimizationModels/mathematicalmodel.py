import pulp

# Spielerdaten und Statistiken als Eingangsvariablen
player_names = ['Tom_Brady', 'Patrick_Mahomes', 'Aaron_Rodgers', 'Christian_McCaffrey', 'Derrick_Henry']
player_positions = {'Tom_Brady': 'QB', 'Patrick_Mahomes': 'QB', 'Aaron_Rodgers': 'QB', 'Christian_McCaffrey': 'RB', 'Derrick_Henry': 'RB'}
player_costs = {'Tom_Brady': 8000, 'Patrick_Mahomes': 10000, 'Aaron_Rodgers': 9000, 'Christian_McCaffrey': 9500, 'Derrick_Henry': 9300}
player_points = {'Tom_Brady': 30, 'Patrick_Mahomes': 35, 'Aaron_Rodgers': 32, 'Christian_McCaffrey': 25, 'Derrick_Henry': 28}

# Mindestanforderungen und Budget als Einschränkungen
budget = 50000
min_points = 120
qb_count = 1
rb_count = 2

# Erstellung des linearen Programmierungsmodells
model = pulp.LpProblem('Fantasy_Football_Team', pulp.LpMaximize)

# Erstellen der Entscheidungsvariablen
player_vars = pulp.LpVariable.dicts('Players', player_names, lowBound=0, cat='Binary')

# Definieren der Zielfunktion
model += pulp.lpSum([player_points[i] * player_vars[i] for i in player_names]), 'Total Points'
print(model)

# Budgetbeschränkung
model += pulp.lpSum([player_costs[i] * player_vars[i] for i in player_names]) <= budget, 'Total Cost'

# Mindestpunktebeschränkung
model += pulp.lpSum([player_points[i] * player_vars[i] for i in player_names]) >= min_points, 'Minimum Points'

# Anzahl der QBs
model += pulp.lpSum([player_vars[i] for i in player_names if player_positions[i] == 'QB']) == qb_count, 'QB Count'

# Anzahl der RBs
model += pulp.lpSum([player_vars[i] for i in player_names if player_positions[i] == 'RB']) == rb_count, 'RB Count'

# Lösung des linearen Programmierungsmodells
model.solve()

# Ausgabe der Ergebnisse
print('Fantasy Football Team:')
for player in player_names:
    if player_vars[player].value() == 1:
        print(player)

print('Total Cost: $' + str(pulp.value(model.objective)))