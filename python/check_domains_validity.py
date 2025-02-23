"""
Domain Reachability Checker
----------------------------
This script checks the reachability of domains over both HTTP and HTTPS.
It reads domain names from a file, attempts to connect to each one, and prints
their accessibility status using color-coded output.

Features:
- Reads domain names from a text file and processes them line by line.
- Includes a 5-second timeout to avoid long waits on unresponsive domains.

How to Use:
0. domains.txt should be a file that look like this:

    192.168.5.4
    google.com
    facebook.com
    etc....
    
1. Create a text file (e.g., `domains.txt`) containing domain names, one per line.
   Example: python3 ./check_domain_validity.py domains.txt
"""

import requests
import sys

# ANSI color codes
GREEN = "\033[92m"
ORANGE = "\033[38;5;214m"  # Approximation of orange in 256-color palette
RED = "\033[91m"
RESET = "\033[0m"

def check_domain(domain):
    domain = domain.strip()
    if not domain:
        return
    
    # Test HTTP
    try:
        r_http = requests.get(f"http://{domain}", timeout=5)
        status = r_http.status_code
        if 200 <= status < 400:
            print(f"{GREEN}{domain} - Reachable on HTTP, status code: {status}{RESET}")
        else:
            print(f"{ORANGE}{domain} - HTTP error, status code: {status}{RESET}")
    except requests.exceptions.RequestException:
        print(f"{RED}{domain} - NOT reachable on HTTP{RESET}")

    # Test HTTPS
    try:
        r_https = requests.get(f"https://{domain}", timeout=5)
        status = r_https.status_code
        if 200 <= status < 400:
            print(f"{GREEN}{domain} - Reachable on HTTPS, status code: {status}{RESET}")
        else:
            print(f"{ORANGE}{domain} - HTTPS error, status code: {status}{RESET}")
    except requests.exceptions.RequestException:
        print(f"{RED}{domain} - NOT reachable on HTTPS{RESET}")
    
    print("-----------------------------------------")

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_domains.py <file_with_domains>")
        sys.exit(1)

    file_with_domains = sys.argv[1]
    
    with open(file_with_domains, 'r') as f:
        for line in f:
            check_domain(line)

if __name__ == "__main__":
    main()

