"""
Project 1 - TCP Port Scanner
Syntecxhub Internship Project
Scans open ports on a host using socket + threading.
Use only on your own / authorized hosts.
"""

import socket
import threading
import argparse
from datetime import datetime
from queue import Queue

open_ports = []
lock = threading.Lock()

def scan_port(host, port, timeout=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))

        with lock:
            if result == 0:
                print(f"[+] Port {port} is OPEN")
                open_ports.append(port)
                log_result(f"Port {port} : OPEN")
        s.close()

    except socket.gaierror:
        print("Error: Hostname could not be resolved.")
        raise SystemExit
    except socket.error:
        print("Error: Could not connect to server.")
        raise SystemExit
    except KeyboardInterrupt:
        print("\nScan stopped by user.")
        raise SystemExit

def log_result(text):
    with open("scan_results.txt", "a") as f:
        f.write(text + "\n")

def worker(queue, host, timeout):
    while not queue.empty():
        port = queue.get()
        scan_port(host, port, timeout)
        queue.task_done()

def main():
    parser = argparse.ArgumentParser(description="Simple TCP Port Scanner")
    parser.add_argument("host", help="Target host, e.g. 127.0.0.1 or localhost")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Port or range, e.g. -p 80 or -p 1-1000")
    parser.add_argument("-t", "--threads", type=int, default=100,
                        help="Number of threads (default 100)")
    parser.add_argument("-to", "--timeout", type=float, default=1,
                        help="Timeout in seconds (default 1)")
    args = parser.parse_args()
    host = args.host

    open("scan_results.txt", "w").close()
    log_result(f"Scan started for {host} at {datetime.now()}")

    try:
        if "-" in args.ports:
            start, end = map(int, args.ports.split("-"))
            ports = range(start, end + 1)
        else:
            ports = [int(args.ports)]
    except ValueError:
        print("Error: Port format wrong. Use like 80 or 1-1000")
        return

    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print("Error: Host not found.")
        return

    print("-" * 50)
    print(f"Scanning {host} ({ip})")
    print(f"Ports: {args.ports} | Threads: {args.threads}")
    print(f"Started at: {datetime.now()}")
    print("-" * 50)

    q = Queue()
    for port in ports:
        q.put(port)

    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(q, ip, args.timeout))
        t.daemon = True
        t.start()

    try:
        q.join()
    except KeyboardInterrupt:
        print("\nScan stopped by user.")

    print("-" * 50)
    print(f"Scan Finished at {datetime.now()}")
    if open_ports:
        print(f"Open Ports: {sorted(open_ports)}")
        log_result(f"Open Ports: {sorted(open_ports)}")
    else:
        print("No open ports found in this range.")
        log_result("No open ports found.")
    print("Results saved in scan_results.txt")

if __name__ == "__main__":
    main()
