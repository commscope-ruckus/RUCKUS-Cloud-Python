#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:30:28 2023

@author: marcelo
"""

from rcAPI import RC_API_calls
import warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

host = 'ruckus.cloud'
username = 'your_email'
password = 'password'

rc = RC_API_calls()
response = rc.getToken(host, username, password)
tenantId = response['tenantId']
jwt = response['jwt']

tenantDetails = rc.getTenantDetails(host, tenantId, jwt)
venues = rc.getVenues(host, tenantId, jwt)
r = rc.configure_802_11k(host, tenantId, True, jwt)

# uncomment the lines below to test calls to manage a delegate account
# mspEcTenantId = rc.getMspECs(host, tenantId, jwt)[0]['tenant_id']
# mspEcVenues = rc.getVenues(host, mspEcTenantId, jwt)





