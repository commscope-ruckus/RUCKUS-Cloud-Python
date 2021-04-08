#!/usr/bin/env python3

from time import sleep
import requests


# GLOBAL PARAMS
DOMAIN = 'https://ruckus.cloud'
username = 'YOUR_RUCKUS_CLOUD_USERNAME'
password = 'YOUR_RUCKUS_CLOUD_PASSWORD'
tenant_id = 'YOUR_RUCKUS_CLOUD_TENANT_ID'   # e.g. '39b5110074134f61bf8cc73d8f0cf9fc'
source_venue_id = 'SOURCE_VENUE_ID'         # e.g. 'e57de25ea39e6d228eb310d4318c3fe9'
target_venue_id = 'SOURCE_VENUE_ID'         # e.g. '268618a6f17d4031bc4301f22ace99a3'


def login(session):
    # Obtain authentication cookie (cookie is saved to the session)
    print('Logging in to:', DOMAIN)
    print({'username': username, 'password': password})
    print(f'{DOMAIN}/token')
    r = session.post(f'{DOMAIN}/token', json={'username': username, 'password': password, 'region': 'US'})
    if r.status_code != 200:
        print('Error logging-in:', r)
        return False
    print('Logged-in')
    return True


def wait_for_async_response(session, response, sleep_time=2):
    """
    Helper function to wait for asynchronous requests.
    Details: Ruckus Cloud write-APIs can be asynchronous (note: read-APIs are always synchronous).
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
        r = session.get(f'{DOMAIN}/api/tenant/{tenant_id}/request/{request_id}')
        if r.status_code != 200 or not r.text:
            print(f'Request status undefined [{r.status_code}]: "{r.text}"')
        else:
            request_details = r.json()
            print(f'\nrequest: {request_details["status"]}, {request_details}')
            if request_details['status'] in ['SUCCESS', 'FAIL']:
                break
        sleep(sleep_time)

    if request_details['status'] != 'SUCCESS':
        raise Exception(request_details['status'])

    return response.json()['response']


def move_aps(source_venue_id, target_venue_id):
    """
    Moves all APs from source-venue to target-venue
    :param source_venue_id: source venue id
    :param target_venue_id: target venue id
    :return: None
    """

    # Use a session to save the authentication cookie between API calls
    s = requests.Session()

    login(s)

    # Iterate over the source-venue AP-Groups
    r = s.get(f'{DOMAIN}/api/tenant/{tenant_id}/wifi/venue/{source_venue_id}/ap-group')
    for group in r.json():
        # Iterate over the APs in the AP-Group
        if 'aps' in group:
            for ap in group['aps']:
                ap_id = ap['serialNumber']
                ap['venueId'] = target_venue_id
                ap['apGroupId'] = None

                r = s.put(f'{DOMAIN}/api/tenant/{tenant_id}/wifi/ap/{ap_id}', json=ap)
                wait_for_async_response(s, r)


move_aps(source_venue_id, target_venue_id)
