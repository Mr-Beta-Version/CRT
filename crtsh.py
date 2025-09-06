#!/usr/bin/env python3
import argparse
import requests
import sys
import os

def get_subs(domain):
    try:
        data = requests.get(f"https://crt.sh/?q={domain}&output=json", timeout=10).json()
    except Exception as e:
        print(f"[x] Error fetching {domain}: {e}")
        return []

    rawurls = "\n".join(item["name_value"] for item in data)
    subdomains = [line for line in rawurls.splitlines() if "*" not in line]

    print(f"[>] From {domain} got {len(subdomains)} subdomains.")
    return list(set(subdomains))


def save_subs(filename, subs):
    existing = set()
    if os.path.exists(filename):
        with open(filename, "r") as f:
            existing = set(line.strip() for line in f if line.strip())

    new_subs = sorted(set(subs) - existing)
    if new_subs:
        with open(filename, "a") as f:
            for sub in new_subs:
                f.write(sub + "\n")
                print(f" [+] {sub}")
        print(f"[✔] {len(new_subs)} new subdomains appended to {filename}\n")
    else:
        print("[!] No new subdomains to append.\n")


def main():
    parser = argparse.ArgumentParser(description="CRT.sh Subdomain Finder")
    parser.add_argument("-d", "--domain", help="Single domain to find subdomains for")
    parser.add_argument("-f", "--file", help="File containing a list of domains")
    parser.add_argument("-s", "--save", help="Save subdomains to a file")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.domain:
        subs = get_subs(args.domain)
        if args.save and subs:
            save_subs(args.save, subs)

    if args.file:
        try:
            with open(args.file, "r") as f:
                domains = [d.strip() for d in f if d.strip()]
            for d in domains:
                subs = get_subs(d)
                if args.save and subs:
                    save_subs(args.save, subs)
        except FileNotFoundError:
            print(f"[x] File not found: {args.file}")
            return


if __name__ == "__main__":
    main()
