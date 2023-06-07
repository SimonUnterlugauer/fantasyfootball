import psycopg2



def insert_schedule(team_name, schedule_data):

    # Verbindung zur PostgreSQL-Datenbank herstellen
    conn = psycopg2.connect(host='localhost', database='posty', user='sulu', password='Nadine1995')
    cur = conn.cursor()

    # SQL-Abfrage, um das Team anhand des Namens zu suchen
    query = "SELECT id FROM schedule WHERE team = %s"
    cur.execute(query, (team_name,))

    # Team-ID abrufen
    team_id = cur.fetchone()

    if team_id is not None:
        team_id = team_id[0]  # Extrahieren der Team-ID

        # SQL-Abfrage, um die Daten für jede Woche einzufügen
        query = "UPDATE schedule SET Week_{} = %s WHERE id = %s".format("{}")

        for week, data in enumerate(schedule_data, start=1):
            cur.execute(query.format(week), (data, team_id))

        # Änderungen in der Datenbank bestätigen
        conn.commit()

        print("Die Daten wurden erfolgreich in die PostgreSQL-Datenbank eingefügt.")
    else:
        print("Das Team wurde nicht in der Datenbank gefunden.")

    # Verbindung zur Datenbank beenden
    cur.close()
    conn.close()

schedule_array = [
  'ATL',
  'NO',
  'SEA',
  'MIN',
  'DET',
  'MIA',
  'BYE',
  'HOU',
  'IND',
  'CHI',
  'DAL',
  'TEN',
  'TB',
  'NOS',
  'ATL',
  'GB',
  'JAC',
  'TB'
]


insert_schedule("CAR", schedule_array)