import requests
import re,os


def get_subs(domain):
    data = requests.get(f"https://crt.sh/?q={domain}&output=json").json()
    
    rawurls = "\n".join(item["name_value"] for item in data)
    
    subdomains = [line for line in rawurls.splitlines() if "*" not in line]

    print(f"[>] From {domain} Get {len(subdomains)} Sub-domains.")

    return subdomains




