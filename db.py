import dataset

def connect():
	"""
	Connect to the database.
	"""
	db = dataset.connect('sqlite:///photostreamer.db')
	return db


# Key/value store-type interface using a settings table in the database

def set(key, value):
	"""
	Set a setting in the database settings table.
	"""
	db = connect()
	settings = db['settings']
	if settings.find_one(key = key):
		settings.update(dict(key=key, value=value), ['key'])
	else:
		settings.insert(dict(key=key, value=value))

def get(key):
	"""
	Return a setting from the database settings table.
	"""
	db = connect()
	settings = db['settings']
	row = settings.find_one(key = key)
	if row:
		return row['value']
	else:
		return None