import sys
import requests
from datetime import datetime

def fetch_certificates(domain):
    # Construct the URL for the crt.sh API with the updated match parameter
    url = f"https://crt.sh/json?identity={domain}&match=="
    
    # Make the GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Print the JSON response
        return response.json()
    else:
        print(f"Error: Unable to fetch data (Status code: {response.status_code})")


def compare_dates(date1, date2):
    date1 = datetime.fromisoformat(date1)
    date2 = datetime.fromisoformat(date2)

    if date1 < date2:
        return [date1, date2]


def findGap(logs):
    active_from = logs[0]["not_before"]
    print(active_from)
    for i in range(len(logs)-1):
        
            before_date = logs[i]["not_after"]
            after_date = logs[i+1]["not_before"]

            gap = compare_dates( before_date, after_date)

            if type(gap) == list:
                print(f"From : {active_from}    To : {gap[1]}")
                active_from = gap[0]
    
    if gap == None:
        print(f"The SSL certificate of this domain is active from {active_from}")


if __name__ == "__main__":
    # Check if the domain name is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <domain_name>")
        sys.exit(1)

    # Get the domain name from command-line arguments
    domain_name = sys.argv[1]
    
    # Fetch and print the certificates for the given domain
    certs = fetch_certificates(domain_name)
    certs.reverse()

    filtered_certs = [d for d in certs if domain_name == d["common_name"] or '*.'+domain_name == d["common_name"]]

    print(filtered_certs)

    findGap(filtered_certs)