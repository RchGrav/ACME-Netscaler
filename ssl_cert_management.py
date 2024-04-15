import requests
import json
import subprocess

# Settings - replace with your actual details
NETSCALER_IP = 'netscaler-ip-address'
USERNAME = 'api-user'
PASSWORD = 'api-password'
DOMAIN = 'yourdomain.com'
CERT_NAME = 'your_cert_name'
VSERVER_NAME = 'your_ssl_vserver_name'

# Step 1: Generate Certificate using Certbot (ACME Client)
def generate_certificate(domain):
    # Run certbot command to generate certificate
    cmd = [
        'certbot', 'certonly', '--manual', '--preferred-challenges', 'dns', 
        '--non-interactive', '--agree-tos', '-m', 'youremail@example.com', '-d', domain
    ]
    subprocess.run(cmd, check=True)

# Step 2: Upload Certificate and Key to NetScaler
def upload_certificate(cert_name, cert_path, key_path):
    url = f'https://{NETSCALER_IP}/nitro/v1/config/sslcertkey'
    headers = {'Content-Type': 'application/json'}
    data = {
        "sslcertkey": {
            "certkey": cert_name,
            "cert": cert_path,
            "key": key_path
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False, auth=(USERNAME, PASSWORD))
    return response.text

# Step 3: Bind Certificate to Virtual Server
def bind_certificate_to_vserver(vserver_name, cert_name):
    url = f'https://{NETSCALER_IP}/nitro/v1/config/sslvserver_sslcertkey_binding'
    data = {
        "sslvserver_sslcertkey_binding": {
            "vservername": vserver_name,
            "certkeyname": cert_name
        }
    }
    response = requests.put(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data), verify=False, auth=(USERNAME, PASSWORD))
    return response.text

# Main execution
if __name__ == '__main__':
    try:
        # Generate SSL Certificate
        generate_certificate(DOMAIN)
        
        # Paths to the generated certificate and key
        cert_path = f'/etc/letsencrypt/live/{DOMAIN}/fullchain.pem'
        key_path = f'/etc/letsencrypt/live/{DOMAIN}/privkey.pem'

        # Upload the certificate and key to NetScaler
        upload_result = upload_certificate(CERT_NAME, cert_path, key_path)
        print('Upload Result:', upload_result)

        # Bind the certificate to the SSL virtual server
        binding_result = bind_certificate_to_vserver(VSERVER_NAME, CERT_NAME)
        print('Binding Result:', binding_result)

    except Exception as e:
        print('An error occurred:', e)
