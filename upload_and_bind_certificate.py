# upload_and_bind_certificate.py
import requests
import json

def upload_certificate(cert_name, cert_path, key_path, netscaler_ip, username, password):
    url = f'https://{netscaler_ip}/nitro/v1/config/sslcertkey'
    headers = {'Content-Type': 'application/json'}
    data = {
        "sslcertkey": {
            "certkey": cert_name,
            "cert": cert_path,
            "key": key_path
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False, auth=(username, password))
    print(response.text)

def bind_certificate_to_vserver(vserver_name, cert_name, netscaler_ip, username, password):
    url = f'https://{netscaler_ip}/nitro/v1/config/sslvserver_sslcertkey_binding'
    data = {
        "sslvserver_sslcertkey_binding": {
            "vservername": vserver_name,
            "certkeyname": cert_name
        }
    }
    response = requests.put(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data), verify=False, auth=(username, password))
    print(response.text)
