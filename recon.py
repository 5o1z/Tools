import subprocess
import os

def run_in_terminal(command, title):
    if os.name == 'posix':  # For Unix/Linux/MacOS
        subprocess.run(['gnome-terminal', '--tab', '--title', title, '--', 'bash', '-c', f"{command}; exec bash"])
    else:
        print("This script is designed for Unix/Linux systems.")

def main():
    # Prompt the user to enter the IP address for nmap
    target_ip = input("Please enter the IP address for nmap scan: ")

    # Prompt the user to enter the URL for ffuf
    target_url = input("Please enter the URL for ffuf scan: ")

    # Prompt the user to enter the path to the wordlist for directory/file scan with ffuf
    wordlist = input("Please enter the path to your wordlist for directory scan: ")
    if not os.path.isfile(wordlist):
        print(f"Wordlist not found: {wordlist}")
        return

    # Prompt the user to enter the subdomain list for ffuf scan
    subdomain_list = input("Please enter the path to your subdomain list for subdomain scan (optional): ")
    if subdomain_list and not os.path.isfile(subdomain_list):
        print(f"Subdomain list not found: {subdomain_list}")
        return

    # Prompt the user to enter the output filenames
    nmap_output = input("Please enter the output filename for nmap results: ")
    ffuf_output = input("Please enter the output filename for ffuf directory scan results: ")
    ffuf_subdomain_output = input("Please enter the output filename for ffuf subdomain scan results: ")

    # Ask the user if they want to use a cookie for the ffuf scan
    use_cookie = input("Do you want to use a cookie for the ffuf scan? (y/n): ")
    cookie_option = ""
    if use_cookie.lower() == 'y':
        cookie = input("Please enter the cookie string: ")
        cookie_option = f"-b '{cookie}'"

    # Run nmap in a new terminal tab
    nmap_command = f"nmap -sC -sV -T4 --min-rate 1000 -n -p- {target_ip} -oN {nmap_output}"
    run_in_terminal(nmap_command, "nmap scan")

    # Run ffuf directory/file scan in a new terminal tab
    ffuf_command = f"ffuf -w {wordlist} {cookie_option} -u {target_url}/FUZZ -o {ffuf_output}"
    run_in_terminal(ffuf_command, "ffuf directory scan")

    # Run ffuf subdomain scan if subdomain list is provided
    if subdomain_list:
        ffuf_subdomain_command = f"ffuf -w {subdomain_list} {cookie_option} -u https://FUZZ.{target_url} -o {ffuf_subdomain_output}"
        run_in_terminal(ffuf_subdomain_command, "ffuf subdomain scan")

        # Ask the user if they want to filter the subdomain scan results
        filter_subdomain_option = input("Do you want to filter the subdomain scan results by size or HTTP code? (y/n): ")
        if filter_subdomain_option.lower() == 'y':
            # Enter the size to filter by
            filter_size_subdomain = input("Please enter the size to filter by (e.g., 1234): ")
            size_option_subdomain = f"-fs {filter_size_subdomain}"

            # Enter the HTTP code to filter by
            filter_code_subdomain = input("Please enter the HTTP code to filter by (e.g., 200): ")
            code_option_subdomain = f"-fc {filter_code_subdomain}"

            # Prompt the user to enter the output filename for the filtered subdomain ffuf results
            ffuf_filtered_subdomain_output = input("Please enter the output filename for filtered ffuf subdomain results: ")

            # Run ffuf again with the filters applied in a new terminal tab
            ffuf_filtered_subdomain_command = f"ffuf -w {subdomain_list} {cookie_option} {size_option_subdomain} {code_option_subdomain} -u https://FUZZ.{target_url} -o {ffuf_filtered_subdomain_output}"
            run_in_terminal(ffuf_filtered_subdomain_command, "ffuf filtered subdomain scan")
        else:
            print("No filtering applied to subdomain scan. Exiting.")

    # Ask the user if they want to scan for sensitive files
    scan_sensitive = input("Do you want to scan for sensitive files? (y/n): ")
    if scan_sensitive.lower() == 'y':
        sensitive_wordlist = input("Please enter the path to your wordlist for sensitive file scan: ")
        if not os.path.isfile(sensitive_wordlist):
            print(f"Sensitive file wordlist not found: {sensitive_wordlist}")
            return

        sensitive_output = input("Please enter the output filename for sensitive file scan results: ")

        # Run ffuf sensitive file scan in a new terminal tab
        ffuf_sensitive_command = f"ffuf -w {sensitive_wordlist} {cookie_option} -u {target_url}/FUZZ -o {sensitive_output}"
        run_in_terminal(ffuf_sensitive_command, "ffuf sensitive file scan")

        # Ask the user if they want to filter the sensitive file scan results
        filter_sensitive_option = input("Do you want to filter the sensitive file scan results by size or HTTP code? (y/n): ")
        if filter_sensitive_option.lower() == 'y':
            # Enter the size to filter by
            filter_size_sensitive = input("Please enter the size to filter by (e.g., 1234): ")
            size_option_sensitive = f"-fs {filter_size_sensitive}"

            # Enter the HTTP code to filter by
            filter_code_sensitive = input("Please enter the HTTP code to filter by (e.g., 200): ")
            code_option_sensitive = f"-fc {filter_code_sensitive}"

            # Prompt the user to enter the output filename for the filtered sensitive file ffuf results
            ffuf_filtered_sensitive_output = input("Please enter the output filename for filtered ffuf sensitive file results: ")

            # Run ffuf again with the filters applied in a new terminal tab
            ffuf_filtered_sensitive_command = f"ffuf -w {sensitive_wordlist} {cookie_option} {size_option_sensitive} {code_option_sensitive} -u {target_url}/FUZZ -o {ffuf_filtered_sensitive_output}"
            run_in_terminal(ffuf_filtered_sensitive_command, "ffuf filtered sensitive file scan")
        else:
            print("No filtering applied to sensitive file scan. Exiting.")

    # Ask the user if they want to filter the directory/file scan results
    filter_option = input("Do you want to filter the directory/file scan results by size or HTTP code? (y/n): ")
    if filter_option.lower() == 'y':
        # Enter the size to filter by
        filter_size = input("Please enter the size to filter by (e.g., 1234): ")
        size_option = f"-fs {filter_size}"

        # Enter the HTTP code to filter by
        filter_code = input("Please enter the HTTP code to filter by (e.g., 200): ")
        code_option = f"-fc {filter_code}"

        # Prompt the user to enter the output filename for the filtered ffuf results
        ffuf_filtered_output = input("Please enter the output filename for filtered ffuf results: ")

        # Run ffuf again with the filters applied in a new terminal tab
        ffuf_filtered_command = f"ffuf -w {wordlist} {cookie_option} {size_option} {code_option} -u {target_url}/FUZZ -o {ffuf_filtered_output}"
        run_in_terminal(ffuf_filtered_command, "ffuf filtered scan")
    else:
        print("No filtering applied to directory/file scan. Exiting.")

if __name__ == "__main__":
    main()
