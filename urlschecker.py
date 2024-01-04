import aiohttp
import argparse
import asyncio
from tqdm import tqdm
import time

async def check_url_status(session, url, timeout=100, verbose=False, pbar=None):
    try:
        async with session.head(url, allow_redirects=True, timeout=timeout) as response:
            status_code = response.status
            if verbose:
                print(f"Checked {url}: Status Code {status_code}")
            if pbar:
                pbar.update(1)  # Pembaruan loading bar
            return status_code
    except aiohttp.ClientError as e:
        if verbose:
            print(f"Error checking {url}: {e}")
        if pbar:
            pbar.update(1)  # Pembaruan loading bar
        return 500  # Mengembalikan kode status server error (500) jika terjadi error
    except asyncio.TimeoutError:
        if verbose:
            print(f"Timeout checking {url}")
        if pbar:
            pbar.update(1)  # Pembaruan loading bar
        return 408  # Mengembalikan kode status request timeout (408) jika terjadi timeout

def get_response_description(status_code):
    if 100 <= status_code < 200:
        return "(Informational)"
    elif 200 <= status_code < 300:
        return "(Successful)"
    elif 300 <= status_code < 400:
        return "(Redirection)"
    elif 400 <= status_code < 500:
        return "(Client Error)"
    elif 500 <= status_code < 600:
        return "(Server Error)"
    else:
        return "Unknown"

async def main():
    parser = argparse.ArgumentParser(description="Check status response of URLs and save the results.")
    parser.add_argument('-f', '--file', help='Input file containing URLs')
    parser.add_argument('-u', '--urls', nargs='+', help='Input URLs (space-separated)')
    parser.add_argument('-o', '--output', help='Output file for storing status responses')
    parser.add_argument('-r', '--response-codes', nargs='+', type=int, help='Response codes to include (space-separated)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-ts', '--time-sec', type=int, default=100, help='Timeout in seconds for each request')

    args = parser.parse_args()

    if not args.file and not args.urls:
        print("Please provide either an input file or a list of URLs.")
        return

    if args.file and args.urls:
        print("Please provide either an input file or a list of URLs, not both.")
        return

    if args.file:
        with open(args.file, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]  # Hanya ambil baris yang bukan kosong
    else:
        lines = args.urls

    url_statuses = {}

    connector = aiohttp.TCPConnector()
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        with tqdm(total=len(lines), desc="Checking URLs", unit="URL", dynamic_ncols=True) as pbar:
            for line in lines:
                url = line.strip()
                task = check_url_status(session, url, timeout=args.time_sec, verbose=args.verbose, pbar=pbar)
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

            for url, status in zip(lines, responses):
                if not args.response_codes or status in args.response_codes:
                    description = get_response_description(status)
                    url_statuses[url] = f"{status} {description}"

    if args.output:
        with open(args.output, 'w') as output_file:
            for url, status in url_statuses.items():
                output_file.write(f"{url}: {status}\n")
        print(f"Status responses of URLs have been saved in the file '{args.output}'.")
    else:
        for url, status in url_statuses.items():
            print(f"{url}: {status}")

if __name__ == "__main__":
    asyncio.run(main())
