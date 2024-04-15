# generate_certificate_http.py
import subprocess

def generate_certificate_http(domain):
    webroot_path = '/path/to/webroot'
    cmd = [
        'certbot', 'certonly', '--webroot', '--webroot-path', webroot_path, '--non-interactive', '--agree-tos', '-m', 'email@example.com', '-d', domain
    ]
    subprocess.run(cmd, check=True)
