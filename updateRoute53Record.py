#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit
from requests import get
import boto3
from botocore.exceptions import ClientError as BotoClientError
import argparse

__version__ = '0.1'
__author__ = 'Sandro CAZZANIGA'
__license__ = "GPLv3+"
__maintainer__ = "Sandro CAZZANIGA"
__email__ = "sandro@cazzaniga.fr"
__status__ = "Production"


def getIp():
	'''Simple function to get your ip, using ipinfo.io
	API and JSON. We're modifying it to match AWS SG
	requirements'''

	return(get(('https://ipinfo.io')).json()['ip']+"/32")
