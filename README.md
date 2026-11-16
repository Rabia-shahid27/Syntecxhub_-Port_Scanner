# Project 1 - TCP Port Scanner

A simple TCP Port Scanner built in Python using `socket` programming and `threading`.

## Features
- Scan a single host
- Scan a single port or a range of ports
- Multi-threaded fast scanning
- Prints Open / Closed / Timeout results
- Logs results in `scan_results.txt`
- Handles errors: invalid host, timeout, user stop

## How to Run

### 1. Scan default ports 1-1024
```bash
python port_scanner.py 127.0.0.1
