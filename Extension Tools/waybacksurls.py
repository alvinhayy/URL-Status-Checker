import argparse
import requests

def find_endpoints(domain):
    wayback_url = f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey&page=/"
    
    try:
        response = requests.get(wayback_url)
        if response.status_code == 200:
            data = response.json()
            endpoints = set()

            for entry in data[1:]:
                if entry:
                    endpoints.add(entry[0])

            return endpoints
        else:
            print(f"Failed to retrieve data. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def save_to_file(endpoints, output_file):
    with open(output_file, 'w') as file:
        for endpoint in endpoints:
            file.write(endpoint + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find endpoints using Wayback Machine.")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-o", "--output", required=True, help="Output file")

    args = parser.parse_args()

    target_domain = args.url
    output_file = args.output

    discovered_endpoints = find_endpoints(target_domain)

    if discovered_endpoints:
        print("Discovered Endpoints:")
        for endpoint in discovered_endpoints:
            print(endpoint)

        save_to_file(discovered_endpoints, output_file)
        print(f"Endpoints saved to {output_file}")
    else:
        print("No endpoints discovered.")
