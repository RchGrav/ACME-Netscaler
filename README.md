# ACME-Netscaler
SSL Certificate Automation for Citrix NetScaler Using Let's Encrypt and NITRO API

## Step 1: Environment Setup

Ensure your environment is ready to use the NITRO API and ACME protocol:

- **NetScaler Access:** Make sure you have administrative access to your NetScaler.
- **API Tools:** Install tools or libraries required for NITRO API calls (e.g., Python requests library).
- **ACME Client:** Install an ACME client that supports Let's Encrypt (e.g., Certbot).

## Step 2: Generate SSL Certificates Using ACME Protocol

Use an ACME client to request and retrieve SSL certificates from Let's Encrypt.

```bash
certbot certonly --manual --preferred-challenges dns -d yourdomain.com
```

- `--manual`: This flag is used for manual configuration, especially when DNS changes are needed.
- `--preferred-challenges dns`: Specifies that DNS challenge is preferred.
- `-d yourdomain.com`: Replace yourdomain.com with your actual domain.

## Step 3: Upload Certificate and Key to NetScaler

Upload the generated certificate and key to NetScaler using NITRO API calls.

```python
import requests
import json

url = 'https://netscaler-ip-address/nitro/v1/config/sslcertkey'
headers = {'Content-Type': 'application/json'}
data = {
    "sslcertkey": {
        "certkey": "your_cert_name",
        "cert": "path_to_certificate_file",
        "key": "path_to_private_key_file"
    }
}

response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
print(response.text)
```

- `url`: API endpoint for SSL certificate configuration.
- `certkey`: A unique name for the certificate-key pair on NetScaler.
- `cert`: Path to your certificate file.
- `key`: Path to your private key file.

## Step 4: Link Certificate to a Virtual Server

Link the uploaded certificate to the SSL virtual server using NITRO API.

```python
url = 'https://netscaler-ip-address/nitro/v1/config/sslvserver_sslcertkey_binding'
data = {
    "sslvserver_sslcertkey_binding": {
        "vservername": "your_ssl_vserver_name",
        "certkeyname": "your_cert_name"
    }
}

response = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
print(response.text)
```

- `vservername`: Name of your SSL virtual server on NetScaler.
- `certkeyname`: Name of the certificate-key pair used in the previous step.

## Step 5: Enable SSL Offloading (Optional)

Configure SSL offloading to improve performance, if applicable.

```python
url = 'https://netscaler-ip-address/nitro/v1/config/ssloffload'
data = {
    "ssloffload": {
        "vservername": "your_ssl_vserver_name",
        "status": "enabled"
    }
}

response = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
print(response.text)
```

### Conclusion

This template guides you through the process of generating SSL certificates using the ACME protocol, uploading them to Citrix NetScaler using the NITRO API, and configuring your virtual server to use these certificates. Be sure to replace placeholder values with actual data specific to your environment.

This setup enhances your system’s security by automating the renewal and installation of SSL certificates, which are crucial for secure communications. Always test changes in a staging environment before applying them in production to avoid disruptions.
