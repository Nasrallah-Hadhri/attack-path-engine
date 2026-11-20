import requests
import time

base_url = "http://127.0.0.1:5050"

# 1. Upload Nmap XML
print("Uploading dummy_nmap.xml...")
with open("tests/dummy_nmap.xml", "rb") as f:
    files = {"file": ("dummy_nmap.xml", f, "text/xml")}
    response = requests.post(f"{base_url}/api/nmap/upload", files=files)
    print("Upload Response:", response.json())

# 2. Match Vulnerabilities
print("\nMatching vulnerabilities...")
response = requests.post(f"{base_url}/api/analysis/match-vulns")
print("Match Response:", response.json())

# 3. Test Attack Path
print("\nTesting Attack Path calculation...")
response = requests.get(f"{base_url}/api/analysis/attack-path", params={"source_ip": "192.168.1.10", "target_ip": "192.168.1.20"})
print("Path Response:", response.json())
