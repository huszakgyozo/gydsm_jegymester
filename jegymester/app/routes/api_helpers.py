import requests

def api_get(url, token=""):
    headers = {'Authorization': f'Bearer {token}'}
    return requests.get(url, headers=headers)

def api_post(url, token, json):
    headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
    return requests.post(url, json=json, headers=headers)