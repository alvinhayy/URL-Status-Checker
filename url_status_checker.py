import aiohttp
import argparse
import asyncio
from tqdm import tqdm
import time
from colorama import Fore, Style

# Inisialisasi Colorama
Fore.CYAN, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.LIGHTCYAN_EX, Fore.WHITE, Style.RESET_ALL

# Logo komputer ASCII
logo_ascii = f"""                                                 
{Fore.GREEN}                              
                                             
                               ##%%%%%%%%%%%%%%%%                                                   
                        %%%%%%%%%%%#          %%%%%%%%%#                                            
                     %%%%%%%                         %%%%%%                                         
                  #%%%%                                 #%%%%#                                      
                %%%%#                          #%%%%%%%%%%%%%%%%#                                   
               %%%%                 #%%%%#     %%%%     %%% %% %%%#                                 
              %%%%         #%%%%%%%%%%%%%%      %%#     %%%%%%   %%%#                               
             %%%%      %%%%%%%%        %%%#       %%%#%%%%%%       %%%                              
             %%%       %%%       %%%%  #%%#           %%            #%%%                            
            %%%%       #%%            %%%%              %%%%%%%%     %%%                            
            %%%#        %%%%%##*#%%%%%%%        %%%%%%%%%%%%#         %%%        ##                 URL STATUS CHECKER For Bug Hunter
            %%%%           %%%%%%%%%    #%%%%%%%%%%%        #%#        %%#      %%%#                
            #%%%                 %%%%%%%%%%%                 %%#      %%%#       %%%#               Author : Alvin Hayy
            %%%#            %%%%%%%%%                        #%%     %%%%        %%%%%#             
             %%#         ####%                          %#    %%    %%%%         %%  %%#            
             %%%*                                       %%%  #%#   %%%%         %%%%%%%             
             #%%%#                                      %%%%#%%  %%%%%        %%%#%%%%              
              %%%%#                                    %%%%%%%  %%%%       #%%%#%%%#                
                %%%%#                                  %%   %%%%%%%      %%% #%%%                   
                 #%%%%%#                               %% %%%%%%%%%   %%%% %%%%                     
                    %%%%%%%#                        %%%%%%%%%%  %%%%%%%  %%%%                       
                       %%%%%%%%%%%         ###%%%%%%%%%%%%%%     %%%% #%%%%                         
                            #%%%%%%%%%%%%%%%%%%%%%% %%%%#        %%%#%%%%                           
                              %%%%         %%%%% #%%%%#           %%%%%                             
                              %%%#      %%%%%% %%%%%               %%%#                             
                             %%%%     #%%%% #%%%%%                 #%%%                             
                             %%%#    %%% %%%%%%                     %%%#                            
                             %%%       %%%%%%                        %%%#                           
                            %%%%      %%%%%                          %%%%#                          
                            %%%#                                      %%%%                          
                            %%%%                                       %%%%                                   
                            %%%%                                        %%%#                            
                            %%%#                                        %%%#                            
                            %%%#                                        %%%#                            
                            45 1 33 33 1  12   31   51 34 32   31 75  1 4444                                                                        
                            45 1 33 33 1  12   31   51 34 32   31 75  1 4444
                            45 1 33 33 1  12   31   51 34 32   31 75  1 4444                                                 
"""
#Function untuk memberikan status code pada URL
# lalu menyimpan / menampilkan nya di output
async def check_url_status(session, url, timeout=100, verbose=False, pbar=None):
    try:
        async with session.head(url, allow_redirects=True, timeout=timeout) as response:
            status_code = response.status
            if verbose:
                print(f"Checked {url}: Status Code {status_code}")
            if pbar:
                pbar.update(1)
            return status_code
    except aiohttp.ClientError as e:
        if verbose:
            print(f"Error checking {url}: {e}")
        if pbar:
            pbar.update(1)
        return 500
    except asyncio.TimeoutError:
        if verbose:
            print(f"Timeout checking {url}")
        if pbar:
            pbar.update(1)
        return 408
      
#Function untuk memberikan status code pada URL
# lalu menyimpan / menampilkan nya di output
def get_response_description(status_code):
    if 100 <= status_code < 200:
        return f"{Fore.BLUE}  Informational{Style.RESET_ALL}"
    elif 200 <= status_code < 300:
        return f"{Fore.GREEN} Successful{Style.RESET_ALL}"
    elif 300 <= status_code < 400:
        return f"{Fore.YELLOW} Redirection{Style.RESET_ALL}"
    elif 400 <= status_code < 500:
        return f"{Fore.RED} Client Error{Style.RESET_ALL}"
    elif 500 <= status_code < 600:
        return f"{Fore.RED} Server Error{Style.RESET_ALL}"
    else:
        return "Unknown"

async def main():
    # Menampilkan logo ASCII
    print(logo_ascii)

    # Tulisan URL Status Checker
    print(f"{Fore.GREEN}URL Status Checker{Style.RESET_ALL}\n")

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
            lines = [line.strip() for line in file.readlines() if line.strip()]
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
                    url_statuses[url] = f"[{Fore.CYAN}{time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL} | {status} | {description}] : {url}"

    if args.output:
        with open(args.output, 'w') as output_file:
            for url, status in url_statuses.items():
                output_file.write(f"{status}\n")
        print(f"\nStatus responses of URLs have been saved in the file '{args.output}'.")
    else:
        for url, status in url_statuses.items():
            print(status)

    # Informasi Tanggal dan Waktu Tools Selesai Running
    print(f"\n{Fore.LIGHTCYAN_EX}The URL checking process has been completed on | {time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")

if __name__ == "__main__":
    asyncio.run(main())
