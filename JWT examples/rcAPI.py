import requests
import time

class RC_API_calls:
	def getToken(self, host, username, password):
		url = "https://" + host + "/token"
		body = {'username': username,'password': password}
		r = requests.post(url, json = body, verify=False).json()
		return r

	def getTenantDetails(self, host, tenantID, jwt):
		url = "https://" + host + "/api/tenant/" + tenantID + "?deep=true"
		auth = {'Authorization': 'Bearer {}'.format(jwt)}
		r = requests.get(url, verify=False, headers=auth).json()
		return r

	def getMspECs(self, host, tenantID, jwt):
		url = "https://" + host + "/api/mspservice/tenant/" + tenantID + "/mspecaccounts"
		auth = {'Authorization': 'Bearer {}'.format(jwt)}
		r = requests.get(url, verify=False, headers=auth).json()
		return r

	def configure_802_11k(self, host, tenantID, enableNeighborReport,jwt):
		url = "https://" + host + "/api/tenant/" + tenantID + "/wifi/network"
		auth = {'Authorization': 'Bearer {}'.format(jwt)}
		r = requests.get(url, verify=False, headers=auth).json()
		print(r)
		for network in r:
			networkId = network['id']
			print('\nNetwork: ', network['name'])
			network['wlan']['advancedCustomization']['enableNeighborReport'] = enableNeighborReport
			url = "https://" + host + "/api/tenant/" + tenantID + "/wifi/network/" + networkId
			auth = {'Authorization': 'Bearer {}'.format(jwt)}
			r = requests.put(url, verify=False, headers=auth, json=network)
			print('change response:', r)
			self.wait_for_async_response(host, r, tenantID, jwt)
			
	def wait_for_async_response(self, host, response, tenantID, jwt, sleep_time=3):
		http_response = response.status_code
		if http_response != 202:
			return response
		requestId = response.json()['requestId']
		print('\nWaiting for request to complete:', requestId)
		url = "https://" + host + "/api/tenant/" + tenantID + "/request/" + requestId
		auth = {'Authorization': 'Bearer {}'.format(jwt)}
		while True:
			try:
				r = requests.get(url, verify=False, headers=auth).json()
				print('\nrequest:', r['status'])
				if r['status'] in ['SUCCESS', 'FAIL']:
					break
				time.sleep(sleep_time)
			except Exception as ex:
				print('retrying')
				time.sleep(sleep_time)
		if r['status'] != 'SUCCESS':
			raise Exception(r['status'])

