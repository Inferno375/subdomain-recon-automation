import requests
import socket # Built-in Python library for networking
import concurrent.futures

def get_subdomains(domain):
    # [Your existing Step 2 code stays exactly the same here]
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    print(f"[*] Querying CT logs for: {domain}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        subdomains = set() 
        for record in data:
            name = record.get('name_value')
            if name:
                for sub in name.split('\n'):
                    clean_sub = sub.replace('*.', '')
                    subdomains.add(clean_sub)
        print(f"[*] Parsed {len(subdomains)} unique subdomains.\n")
        return list(subdomains)
    else:
        print(f"[-] Error. Status code: {response.status_code}")
        return []

def validate_subdomains(subdomain_list):
    print(f"[*] Starting DNS resolution on {len(subdomain_list)} targets using multithreading...")
    live_targets = []
    
    # We create a tiny helper function that a single thread will execute
    def check_dns(sub):
        try:
            ip = socket.gethostbyname(sub)
            # \r clears the line so we don't spam the terminal with dead domains
            print(f"[+] ALIVE: {sub} -> {ip}")
            return sub
        except socket.gaierror:
            return None

    # Set up our Thread Pool with 10 workers (safe speed)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # executor.map assigns our helper function to every subdomain in the list
        results = executor.map(check_dns, subdomain_list)
        
        # Collect the results as the threads finish their jobs
        for result in results:
            if result:
                live_targets.append(result)
                
    print(f"\n[*] Found {len(live_targets)} LIVE subdomains out of {len(subdomain_list)}.")
    return live_targets


import argparse
# (Keep your existing requests and socket imports at the top)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain Recon Automation Tool")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    
    # NEW: Add an optional '-o' argument for the output file
    parser.add_argument("-o", "--output", help="Save live subdomains to a file (e.g., targets.txt)")
    
    args = parser.parse_args()
    
    print(f"[*] Initializing recon on target: {args.domain}\n")
    found_targets = get_subdomains(args.domain)
    
    if found_targets:
        live_ones = validate_subdomains(found_targets)
        
        # NEW: If the user provided an output file, save the list
        if args.output and live_ones:
            print(f"[*] Saving results to {args.output}...")
            # 'w' opens the file in write mode
            with open(args.output, 'w') as f:
                for target in live_ones:
                    f.write(f"{target}\n")
            print("[+] Saved successfully.")