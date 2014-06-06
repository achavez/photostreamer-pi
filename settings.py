import ConfigParser

def config():
	config = ConfigParser.ConfigParser()
	config.readfp(open('config.cfg'))
	return config