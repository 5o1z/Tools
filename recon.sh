#!/bin/bash

# Function to run a command in a new terminal tab
run_in_terminal() {
    local cmd=$1
    local title=$2
    gnome-terminal --tab --title="$title" -- bash -c "$cmd; exec bash"
}

# Prompt the user to enter the IP address for nmap
read -p "Please enter the IP address for nmap scan: " TARGET_IP

# Prompt the user to enter the URL for ffuf
read -p "Please enter the URL for ffuf scan: " TARGET_URL

# Prompt the user to enter the path to the wordlist for directory/file scan with ffuf
read -p "Please enter the path to your wordlist for directory scan: " WORDLIST

# Check if the wordlist exists
if [ ! -f "$WORDLIST" ]; then
  echo "Wordlist not found: $WORDLIST"
  exit 1
fi

# Prompt the user to enter the subdomain list for ffuf scan
read -p "Please enter the path to your subdomain list for subdomain scan (optional): " SUBDOMAIN_LIST

# Check if the subdomain list exists
if [ -n "$SUBDOMAIN_LIST" ] && [ ! -f "$SUBDOMAIN_LIST" ]; then
  echo "Subdomain list not found: $SUBDOMAIN_LIST"
  exit 1
fi

# Prompt the user to enter the output filenames
read -p "Please enter the output filename for nmap results: " NMAP_OUTPUT
read -p "Please enter the output filename for ffuf directory scan results: " FFUF_OUTPUT
read -p "Please enter the output filename for ffuf subdomain scan results: " FFUF_SUBDOMAIN_OUTPUT

# Ask the user if they want to use a cookie for the ffuf scan
read -p "Do you want to use a cookie for the ffuf scan? (y/n): " USE_COOKIE
if [ "$USE_COOKIE" == "y" ]; then
  read -p "Please enter the cookie string: " COOKIE
  COOKIE_OPTION="-b '$COOKIE'"
else
  COOKIE_OPTION=""
fi

# Run nmap in a new terminal tab
run_in_terminal "nmap -sC -sV -T4 --min-rate 1000 -n -p- $TARGET_IP -oN $NMAP_OUTPUT" "nmap scan"

# Run ffuf directory/file scan in a new terminal tab
run_in_terminal "ffuf -w $WORDLIST $COOKIE_OPTION -u $TARGET_URL/FUZZ -o $FFUF_OUTPUT" "ffuf directory scan"

# Run ffuf subdomain scan if subdomain list is provided
if [ -n "$SUBDOMAIN_LIST" ]; then
  run_in_terminal "ffuf -w $SUBDOMAIN_LIST $COOKIE_OPTION -u https://FUZZ.$TARGET_URL -o $FFUF_SUBDOMAIN_OUTPUT" "ffuf subdomain scan"

  # Ask the user if they want to filter the subdomain scan results
  read -p "Do you want to filter the subdomain scan results by size or HTTP code? (y/n): " FILTER_SUBDOMAIN_OPTION
  if [ "$FILTER_SUBDOMAIN_OPTION" == "y" ]; then
    read -p "Please enter the size to filter by (e.g., 1234): " FILTER_SIZE_SUBDOMAIN
    read -p "Please enter the HTTP code to filter by (e.g., 200): " FILTER_CODE_SUBDOMAIN
    read -p "Please enter the output filename for filtered ffuf subdomain results: " FFUF_FILTERED_SUBDOMAIN_OUTPUT

    run_in_terminal "ffuf -w $SUBDOMAIN_LIST $COOKIE_OPTION -fs $FILTER_SIZE_SUBDOMAIN -fc $FILTER_CODE_SUBDOMAIN -u https://FUZZ.$TARGET_URL -o $FFUF_FILTERED_SUBDOMAIN_OUTPUT" "ffuf filtered subdomain scan"
  else
    echo "No filtering applied to subdomain scan."
  fi
fi

# Ask the user if they want to scan for sensitive files
read -p "Do you want to scan for sensitive files? (y/n): " SCAN_SENSITIVE
if [ "$SCAN_SENSITIVE" == "y" ]; then
  read -p "Please enter the path to your wordlist for sensitive file scan: " SENSITIVE_WORDLIST
  if [ ! -f "$SENSITIVE_WORDLIST" ]; then
    echo "Sensitive file wordlist not found: $SENSITIVE_WORDLIST"
    exit 1
  fi

  read -p "Please enter the output filename for sensitive file scan results: " SENSITIVE_OUTPUT

  run_in_terminal "ffuf -w $SENSITIVE_WORDLIST $COOKIE_OPTION -u $TARGET_URL/FUZZ -o $SENSITIVE_OUTPUT" "ffuf sensitive file scan"

  # Ask the user if they want to filter the sensitive file scan results
  read -p "Do you want to filter the sensitive file scan results by size or HTTP code? (y/n): " FILTER_SENSITIVE_OPTION
  if [ "$FILTER_SENSITIVE_OPTION" == "y" ]; then
    read -p "Please enter the size to filter by (e.g., 1234): " FILTER_SIZE_SENSITIVE
    read -p "Please enter the HTTP code to filter by (e.g., 200): " FILTER_CODE_SENSITIVE
    read -p "Please enter the output filename for filtered ffuf sensitive file results: " FFUF_FILTERED_SENSITIVE_OUTPUT

    run_in_terminal "ffuf -w $SENSITIVE_WORDLIST $COOKIE_OPTION -fs $FILTER_SIZE_SENSITIVE -fc $FILTER_CODE_SENSITIVE -u $TARGET_URL/FUZZ -o $FFUF_FILTERED_SENSITIVE_OUTPUT" "ffuf filtered sensitive file scan"
  else
    echo "No filtering applied to sensitive file scan."
  fi
fi

# Ask the user if they want to filter the directory/file scan results
read -p "Do you want to filter the directory/file scan results by size or HTTP code? (y/n): " FILTER_OPTION
if [ "$FILTER_OPTION" == "y" ]; then
  read -p "Please enter the size to filter by (e.g., 1234): " FILTER_SIZE
  read -p "Please enter the HTTP code to filter by (e.g., 200): " FILTER_CODE
  read -p "Please enter the output filename for filtered ffuf results: " FFUF_FILTERED_OUTPUT

  run_in_terminal "ffuf -w $WORDLIST $COOKIE_OPTION -fs $FILTER_SIZE -fc $FILTER_CODE -u $TARGET_URL/FUZZ -o $FFUF_FILTERED_OUTPUT" "ffuf filtered scan"
else
  echo "No filtering applied to directory/file scan."
fi
