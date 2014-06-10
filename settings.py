import ConfigParser
import logger
l = logger.setup(__name__)

def config():
	config = ConfigParser.ConfigParser()
	try:
		config.readfp(open('config.cfg'))
		return config
	except IOError as e:
		l.exception("Error reading config.cfg file.")
		raise