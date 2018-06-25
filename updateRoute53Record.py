#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit
from requests import get
import boto3
from datetime import datetime
from botocore.exceptions import ClientError as BotoClientError
import argparse

__version__ = '0.1'
__author__ = 'Sandro CAZZANIGA'
__license__ = "GPLv3+"
__maintainer__ = "Sandro CAZZANIGA"
__email__ = "sandro@cazzaniga.fr"
__status__ = "Production"


def getIp():
	'''Simple function to get your ip'''

	return(get('https://ipinfo.io').json()['ip'])

# Parse args
parser = argparse.ArgumentParser(description="Update your AWS DNS record with your new IP address")
parser.add_argument('-v', '--version', action='store_true', help='Print version and exit')
parser.add_argument('id', help='DNS zone\'s id you want to update')
parser.add_argument('record', help='DNS zone\'s record you want to update')

args = vars(parser.parse_args())

if not args['id'] or not args['record']:
	parser.print_help()
	exit(1)

route53 = boto3.client('route53')
hostedZoneId = args['id']
currentIp = getIp()
date = datetime.now().strftime("%d-%m-%y-%H:%M")
dnsRecord = args['record']

# validate the zone's id
try:
	record = route53.list_resource_record_sets(
		HostedZoneId = hostedZoneId,
		StartRecordType = 'A',
		StartRecordName = dnsRecord,
		MaxItems = '1'
	)

except BotoClientError:
	print("Zone id", hostedZoneId, "seems incorrect")
	exit(1)

# get old ip
oldIp = record['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']

# do the magic and update IP in the A record
if oldIp != currentIp:

	try:
		updateRecord = route53.change_resource_record_sets(
			HostedZoneId = hostedZoneId,
			ChangeBatch = {
				'Comment': date,
				'Changes': [
					{
						'Action': 'UPSERT',
						'ResourceRecordSet': {
							'Name': dnsRecord,
							'Type': 'A',
							'TTL': 900,
							'ResourceRecords': [
								{
									'Value': currentIp
								}
							]
						}
					}
				]
			}
		)

	except BotoClientError:
		print("Something went wrong, please check the IP:", currentIp)
		exit(1)

	print(dnsRecord, "has been updated to:", currentIp)

exit(0)
