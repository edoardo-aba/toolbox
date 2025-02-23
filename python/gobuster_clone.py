"""
Simple Directory Busting Tool (Gobuster Clone)

This script scans a given domain for common web pages and directories by sending HTTP GET requests and analyzing the responses. It’s useful for discovering hidden or misconfigured resources on a web server.

Since this tool only sends one request per endpoint, it is not a stress test but rather a directory enumeration tool.

Features:
- Reads a list of endpoints from a file.
- Tests each endpoint on the target domain for availability.
- Outputs the result in color:
- Green for reachable paths (HTTP 200).
- Red for not found paths (HTTP 404).
- Orange for other status codes or errors.
- Supports both HTTP and HTTPS protocols.

How to Use:

Specify the target domain and the file containing endpoints to check:

Example:

python3 gobuster_clone.py {domain_name} {path_to_file} [--scheme <http|https>]


Ensure the endpoint list file contains one path per line, e.g.:
admin
login
dashboard


Example Command:
python3 gobuster_clone.py example.com paths.txt --scheme https

"""



#!/usr/bin/env python3
import argparse
import requests
from colorama import init, Fore, Style

# Initialize Colorama for colored console output
init(autoreset=True)

# ANSI escape for orange (256-color code 208)
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

def check_endpoint(domain, endpoint, scheme="http"):
    """
    Check a given endpoint appended to the domain and print the result in color.
    """
    # Ensure proper formatting of the URL
    url = f"{scheme}://{domain.rstrip('/')}/{endpoint.lstrip('/')}"
    try:
        response = requests.get(url, timeout=5)
        status = response.status_code

        if status == 200:
            # Green for reachable (HTTP 200)
            print(f"{Fore.GREEN}{endpoint} - {status} (reachable)")
        elif status == 404:
            # Red for not found (HTTP 404)
            print(f"{Fore.RED}{endpoint} - {status} (not found)")
        else:
            # Orange for any other status code
            print(f"{ORANGE}{endpoint} - {status} (other status){RESET}")
    except requests.exceptions.RequestException as e:
        # In case of a connection error or timeout, print in orange
        print(f"{ORANGE}{endpoint} - error: {e}{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="A simple directory busting tool like gobuster."
    )
    parser.add_argument("domain", help="Target domain (e.g. example.com)")
    parser.add_argument("file", help="File containing endpoints to check (one per line)")
    parser.add_argument(
        "--scheme",
        default="http",
        choices=["http", "https"],
        help="Choose the URL scheme (default: http)"
    )
    args = parser.parse_args()

    # Read endpoints from file; ignore blank lines
    try:
        with open(args.file, "r") as f:
            endpoints = [line.strip() for line in f if line.strip()]
    except IOError as e:
        print(f"Error reading file: {e}")
        return

    # Check each endpoint on the target domain
    for endpoint in endpoints:
        check_endpoint(args.domain, endpoint, scheme=args.scheme)

if __name__ == "__main__":
    main()

