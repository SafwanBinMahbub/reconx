#!/usr/bin/env python3

import os
import random
import time
import argparse
import requests
import socket
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = [21,22,23,25,53,80,110,139,143,443,445,8080,8443]

def voice_intro():
    os.system("espeak 'Access granted. Welcome S C S Safwan' 2>/dev/null")

def slow_print(text, delay=0.02):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def progress_bar(text="Loading"):
    for i in range(1, 21):
        bar = "█" * i + "-" * (20 - i)
        print(f"\r{text}: [{bar}] {i*5}%", end="", flush=True)
        time.sleep(0.05)
    print()

def matrix_rain():
    os.system("clear")
    chars = "01"
    for _ in range(10):
        line = "".join(random.choice(chars) for _ in range(60))
        print("\033[1;32m" + line + "\033[0m")
        time.sleep(0.03)

def hacker_banner():
    matrix_rain()

    colors = [
        "\033[1;31m","\033[1;32m","\033[1;33m",
        "\033[1;34m","\033[1;35m","\033[1;36m"
    ]
    color = random.choice(colors)

    os.system("figlet -f slant 'SCS SAFWAN' | lolcat")

    print(color + "="*45)
    slow_print("SYSTEM   : Specter Cyber Security [SCS]")
    slow_print("OPERATOR : SCS SAFWAN")
    slow_print("MODE     : GHOST MODE [ACTIVE]")
    slow_print("STATUS   : ONLINE • UNTRACED")
    print("="*45 + "\033[0m")

    progress_bar("Initializing")
    slow_print(">> Recon Module Ready...\n", 0.03)

def get_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        subs = set()
        for entry in data:
            for sub in entry['name_value'].split("\n"):
                if domain in sub:
                    subs.add(sub.strip())
        return list(subs)
    except:
        return []

def resolve(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def scan_port(domain, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((domain, port))
        sock.close()
        return port
    except:
        return None

def port_scan(domain):
    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as ex:
        results = ex.map(lambda p: scan_port(domain, p), COMMON_PORTS)
    for r in results:
        if r:
            open_ports.append(r)
    return open_ports

def run(target):
    print(f"\033[1;36m[+] Target:\033[0m {target}")
    slow_print("[+] Collecting subdomains...", 0.02)

    subs = get_subdomains(target)

    for sub in subs[:20]:
        ip = resolve(sub)
        ports = port_scan(sub) if ip else []

        print(f"\033[1;32m[+]\033[0m {sub} | {ip} | {ports}")
        time.sleep(0.05)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", required=True)
    args = parser.parse_args()

    voice_intro()
    hacker_banner()
    run(args.target)

if __name__ == "__main__":
    main()
