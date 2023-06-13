import sys

import psycopg2
from pulp import LpProblem, LpVariable, LpMaximize, lpSum

sys.path.append("../helpers")  # Add the parent directory to the Python path
import drafthelper


def find_optimal_lineup(team, week, weight_forecast):
    maxPosition = {
        "QB": 1,
        "RB": 3,
        "WR": 2,
        "TE": 1,
        "KI": 1,
        "DEF": 1,
    }

    selected_players = {}
    positions_filled = {position: 0 for position in maxPosition}

    for player in team:

        position = drafthelper.get_player_position(player)
        score = drafthelper.calculate_weekly_score(player, week, weight_forecast)

        print(player + ": " + str(score))
        if positions_filled[position] < maxPosition[position]:
            if position not in selected_players:
                selected_players[position] = []
            selected_players[position].append((player, score))
            positions_filled[position] += 1
        else:
            min_score = min(selected_players[position], key=lambda x: x[1])
            if score > min_score[1]:
                selected_players[position].remove(min_score)
                selected_players[position].append((player, score))

    print(selected_players)

    return selected_players









