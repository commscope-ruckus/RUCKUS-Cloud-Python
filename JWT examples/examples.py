#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 14:20:26 2023.

@author: Marcelo M. Molinari
"""

import warnings
from rc_new_api import RC_API_calls
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

HOST = 'api.ruckus.cloud'
USERNAME = 'your_email'
PASSWORD = 'your_password'

rc = RC_API_calls()
response = rc.getToken(HOST, USERNAME, PASSWORD)

tenantId = response['tenantId']
# print('tenantId:', tenantId)
jwt = response['jwt']
# print('jwt:', jwt)
tenantDetails = rc.getTenantDetails(HOST, jwt)
# print('tenant details:', tenantDetails)
venues = rc.getVenues(HOST, tenantId, jwt)
# print('venues:', venues)
response = rc.configure_802_11k(HOST, False, jwt)

# Uncomment the lines below to test calls to manage a delegate account
# You need to use MSP credentials, and the MSP needs at least one MSP-EC

# mspEcTenantId = rc.getMspECs(host, tenantId, jwt)[0]['tenant_id']
# print('MSP-EC tenantId:', mspEcTenantId)
# mspEcVenues = rc.getVenues(host, mspEcTenantId, jwt)
# print('MSP-EC venues:', mspEcVenues)
