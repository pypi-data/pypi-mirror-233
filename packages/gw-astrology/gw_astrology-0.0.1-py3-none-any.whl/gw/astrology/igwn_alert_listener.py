#!/usr/bin/env python3

from igwn_alert.client import client as IGWNAlertClient
import json
import logging
from optparse import OptionParser

def parse_command_line():
	parser = OptionParser()
	parser.add_option('--verbose', action="store_true", help = 'Be verbose.')
	opts, args = parser.parse_args()
	return opts, args

class on_alert(object):
	def __init__(self, options):
		# stub

	def process_alert(self, topic=None, payload=None):
		# unpack data
		uid = payload['uid']	
		alert_type = payload['alert_type']
		data = payload['data']
		object = payload['object']
	
		if alert_type == 'new':
			logger.info(f'Received alert from {topic} | alert type: {alert_type} | event UID: {uid} | FAR: {object["far"]}')
		else:
			logger.info(f'Received {alert_type} alert for {uid}')


def main():
	# parse command line
	opts, args = parse_command_line()

	## set up logging
	logger = logging.getLogger()
	if opts.verbose:
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)

	h = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	h.setFormatter(formatter)
	logger.addHandler(h)

	listener = on_alert(opts)

	# initialize a client and listener
	client = IGWNAlertClient(group='gracedb')

	topics = 'superevent'
	client.listen(listener.process_alert, topics)

if __name__ == "__main__":
    main()
