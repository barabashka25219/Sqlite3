# PLaylist database with songs
import sqlite3
from sqlite3 import Error

database_path = "playlist.db"

def connect_to_db(path):
	connection = None

	try:
		connection = sqlite3.connect(path)

	except Error as e:
		print(f"Can't connect to database '{path}': {e}")

	return connection

def execute_query(connection, query):
	cursor = connection.cursor()

	try:
		cursor.execute(query)
		connection.commit()

	except Error as e:
		print(f"Can't execute a query: {query}: {e}")

def execute_and_read_query(connection, query):
	cursor = connection.cursor()
	result = None

	try:
		cursor.execute(query)
		result = cursor.fetchall()
		return result


	except Error as e:
		print(f"Can't execute a query: {query}: {e}")

# Connect to our database
connection = connect_to_db(database_path)

# Create a playlist table
query = """
	CREATE TABLE IF NOT EXISTS playlist (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		playlist_name TEXT NOT NULL
	);
"""

execute_query(connection, query)

# Append three elements into
query = """
	INSERT INTO 
	playlist (playlist_name)
	VALUES ('chill'), ('rock'), ('pop');
"""

execute_query(connection, query)

# Create a table of songs 
query = """
	CREATE TABLE IF NOT EXISTS song (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		song_name TEXT NOT NULL,
		author TEXT NOT NULL,
		playlist_id INTEGER,
		FOREIGN KEY (playlist_id) REFERENCES playlist(id)
	);
"""

execute_query(connection, query)

# Append some songs into the table
query = """
	INSERT INTO 
		song (song_name, author, playlist_id)
	VALUES
		('Autumn stories week #5', 'Fabrizio Patterlini', 1),
		('Rise, Rise', 'Rammstein', 2),
		('Millions of stars', 'Spaceouters', 1),
		('Morphine', 'Low XY', 1),
		('In the end', 'Linkin Park', 2),
		('Moon', 'Michael Jackson', 3),
		('BlaBla', 'Madonna', 3),
		('The noise inside my head', 'BONES', NULL);
"""

execute_query(connection, query)

# Let's make three queries to the table that to get songs from each category
query = """
	SELECT song.song_name, song.author, playlist.playlist_name
	FROM song
	INNER JOIN playlist 
	ON song.playlist_id = playlist.id AND playlist_id = 1
"""

chill_songs = execute_and_read_query(connection, query)

for song in chill_songs:
	print(song)
print("...")

query = """
	SELECT song.song_name, song.author, playlist.playlist_name
	FROM song
	INNER JOIN playlist 
	ON song.playlist_id = playlist.id AND playlist_id = 2
"""

rock_songs = execute_and_read_query(connection, query)

for song in rock_songs:
	print(song)
print("...")

query = """
	SELECT song.song_name, song.author, playlist.playlist_name
	FROM song
	INNER JOIN playlist 
	ON song.playlist_id = playlist.id AND playlist_id = 3
"""

pop_songs = execute_and_read_query(connection, query)

for song in pop_songs:
	print(song)
print("...")

query = """
	SELECT song_name, author FROM song WHERE playlist_id IS NULL;
"""

unknown_category = execute_and_read_query(connection, query)

for song in unknown_category:
	print(song)
print('...')

# Append a song without a playlist
query = """
	UPDATE song SET playlist_id=1 WHERE playlist_id IS NULL;
"""

execute_query(connection, query)

# Is update query successful?
query = """
	SELECT song.song_name, song.author, playlist.playlist_name
	FROM song
	INNER JOIN playlist
	ON song.playlist_id = playlist.id AND song.playlist_id = 1
"""

songs = execute_and_read_query(connection, query)

for song in songs:
	print(song)
