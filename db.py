import dataset

def connect():
	db = dataset.connect('sqlite:///failures.db')
	return db