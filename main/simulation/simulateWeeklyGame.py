import psycopg2
from pulp import LpProblem, LpVariable, LpMaximize, lpSum
import sys

sys.path.append("../helpers")  # Add the parent directory to the Python path
import lineuphelper


team = ["Patrick Mahomes", "Geno Smith","Amari Cooper", "Christian Kirk", "Mike Evans", "Jakobi Meyers",
        "Dalvin Cook", "Derrick Henry", "Jamaal Williams","Alexander Mattison", "Travis Kelce",
        "George Kittle", "WAS", "Jake Moody"]
lineuphelper.find_optimal_lineup(team, "week_13", 0.5)