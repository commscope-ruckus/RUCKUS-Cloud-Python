from __future__ import print_function

from time import sleep

import requests


DOMAIN = 'https://ruckus.cloud'
username = 'YOUR_RUCKUS_CLOUD_USERNAME'
password = 'YOUR_RUCKUS_CLOUD_PASSWORD'
tenant_id = 'YOUR_RUCKUS_CLOUD_TENANT_ID'   #e.g. '39b5110074134f61bf8cc73d8f0cf9fc'


def login(session):
    # Obtain authentication cookie (cookie is saved to the session)
    print('Logging in to: ', DOMAIN)
    r = session.post(DOMAIN + '/token', json={'username': username, 'password': password}).json()
    print('token:', r)


def toggle_802_11kr():
    """
    Disables 802.11 r & k on all networks
    """

    # Use a session to save the authentication cookie between API calls
    s = requests.Session()

    login(s)

    # Get Networks
    r = s.get(DOMAIN + '/api/tenant/%s/wifi/network' % tenant_id)
    for network in r.json():
        networkId = network['id']
        print('Network: ', networkId, network)
        network['wlan']['advancedCustomization']['enableNeighborReport'] = False
        network['wlan']['advancedCustomization']['enableFastRoaming'] = False
        #network['wlan']['advancedCustomization']['mobilityDomainId'] = 1

        r = s.put(DOMAIN + '/api/tenant/%s/wifi/network/%s' % (tenant_id, networkId), json=network)
        print('response', r)
        wait_for_async_response(s, r)


def wait_for_async_response(session, response, sleep_time=2):
    """
    Ruckus Cloud write-APIs can be asynchronous (note: read-APIs are always synchronous).
    A response of 202 indicates an asynchronous response, in which case this function polls the request status
    until it completes.
    Any other response indicates a synchronous response.
    :param session: The requests session with auth cookie
    :param response: All Ruckus write-APIs include the request_id in the response
    :param sleep_time: Duration to wait between polling the status
    :return: The entity as returned by the original response
    """

    http_response = response.status_code
    if http_response != 202:                # 202 "accepted" indicates that this is an async call
        return response

    request_id = response.json()['requestId']
    print('\nWaiting for request to complete:', request_id)

    # Loop while our request is pending
    while True:
        request_details = session.get(f'{DOMAIN}/api/tenant/{tenant_id}/request/{request_id}').json()
        print('\nrequest:', request_details['status'], request_details)
        if request_details['status'] in ['SUCCESS', 'FAIL']:
            break
        sleep(sleep_time)

    if request_details['status'] != 'SUCCESS':
        raise Exception(request_details['status'])

    return response.json()['response']

toggle_802_11kr()



