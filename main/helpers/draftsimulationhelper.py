import psycopg2


def draft_player(already_drafted):
    conn = psycopg2.connect(
        host='localhost',
        database='posty',
        user='sulu',
        password='Nadine1995'
    )

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Create a comma-separated string of already drafted players
    already_drafted_str = ", ".join([f"'{player}'" for player in already_drafted])

    #print(already_drafted_str)

    query = "SELECT player FROM mock_draft WHERE player NOT IN (%s) ORDER BY rank LIMIT 1;"
    values = tuple([name.strip(" '") for name in already_drafted_str.split(',')])
    #print(values)
    # Generate the placeholder string for the values
    placeholders = ', '.join(['%s'] * len(values))

    # Update the query with the correct placeholders
    query = query % placeholders

    # Execute the query with the values
    cursor.execute(query, values)

    # Fetch the result (next player)
    next_player = cursor.fetchone()[0]

    # Close the cursor
    cursor.close()
    #print(next_player)

    return next_player



already_drafted = ["Ja'Marr Chase", "Christian McCaffrey", "Jonathan Taylor"]


def draft_kicker(already_drafted):
    conn = psycopg2.connect(
        host='localhost',
        database='posty',
        user='sulu',
        password='Nadine1995'
    )

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Create a comma-separated string of already drafted players
    already_drafted_str = ", ".join([f"'{player}'" for player in already_drafted])
    query = "SELECT name FROM mock_draft_kicker WHERE name NOT IN (%s) ORDER BY rank LIMIT 1;"
    values = tuple([name.strip(" '") for name in already_drafted_str.split(',')])
    #print(values)
    # Generate the placeholder string for the values
    placeholders = ', '.join(['%s'] * len(values))

    # Update the query with the correct placeholders
    query = query % placeholders

    # Execute the query with the values
    cursor.execute(query, values)

    # Fetch the result (next player)
    next_player = cursor.fetchone()[0]

    # Close the cursor
    cursor.close()
    #print(next_player)

    return next_player

def draft_def(already_drafted):
    conn = psycopg2.connect(
        host='localhost',
        database='posty',
        user='sulu',
        password='Nadine1995'
    )

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Create a comma-separated string of already drafted players
    already_drafted_str = ", ".join([f"'{player}'" for player in already_drafted])
    query = "SELECT name FROM mock_draft_def WHERE name NOT IN (%s) ORDER BY rank LIMIT 1;"
    values = tuple([name.strip(" '") for name in already_drafted_str.split(',')])
    #print(values)
    # Generate the placeholder string for the values
    placeholders = ', '.join(['%s'] * len(values))

    # Update the query with the correct placeholders
    query = query % placeholders

    # Execute the query with the values
    cursor.execute(query, values)

    # Fetch the result (next player)
    next_player = cursor.fetchone()[0]

    # Close the cursor
    cursor.close()
    print(next_player)

    return next_player



draft_kicker(["Josef Stalin"])







