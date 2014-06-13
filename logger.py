import logging, logging.handlers

def setup(name=__name__):
	"""
	Setup a logger with a rotating file handler
	"""
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)

	# Make sure log files are 5mb or smaller and only keep 5 of them
	handler = logging.handlers.RotatingFileHandler('logs/photostreamer.log',
		maxBytes=5242880, backupCount=3)
	handler.setLevel(logging.INFO)

	formatter = logging.Formatter(
		'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)

	logger.addHandler(handler)

	return logger