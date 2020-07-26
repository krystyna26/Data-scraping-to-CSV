import requests
import shutil
import time
import csv
import os.path
from urllib.request import Request, urlopen
import schedule

def scrape_fund_holdings():
    print("I'm working...")
    url = "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv"
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    requested_file = requests.get(url, verify=False,stream=True)
    request = Request(url, headers=headers)
    response = urlopen(request)
# ----- get current time to name the file -----
    fname = lambda : "{}.csv".format(time.strftime("%Y%m%d-%H.%M.%S"))
# ----- get date from csv to name the file -----
    line = 0
    for row in response:
        if line == 1:
            result = row.split()[0]
            current_date = str(result).split(",",1)[0][2:]
        line += 1
    file_name = (f"{current_date}.csv") # <---- whats' wrong with this file_name? fname is working
# ----- write to csv file -----
    if requested_file.status_code != 200:
        print("Failure!!")
        exit()
    else:
        requested_file.raw.decode_content = True
        with open(fname(), 'wb') as f:  # <---- FileNotFoundError: [Errno 2] No such file or directory:
            shutil.copyfileobj(requested_file.raw, f)
        print("Success")

# ----- run manually -----
# if __name__ == '__main__':
#     scrape_fund_holdings()

# ----- run on schedule -----
schedule.every().monday.at("13:00").do(scrape_fund_holdings)
schedule.every().tuesday.at("13:00").do(scrape_fund_holdings)
schedule.every().wednesday.at("13:00").do(scrape_fund_holdings)
schedule.every().thursday.at("13:00").do(scrape_fund_holdings)
schedule.every().friday.at("13:00").do(scrape_fund_holdings)

while True:
    schedule.run_pending()
    time.sleep(14400) # wait 4h 
