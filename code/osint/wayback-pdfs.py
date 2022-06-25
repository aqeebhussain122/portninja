import requests
import sys
import json
import os
  
# Suppress SSL warnings
requests.packages.urllib3.disable_warnings()

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
#r = requests.get("https://web.archive.org/web/20220406085043/http://icc.dur.ac.uk/~jlvc76/Files/CV/CV_MatthieuSchaller.pdf", allow_redirects=True, proxies=proxies, verify=False)
#req = requests.get("https://web.archive.org/web/20211127144149/http://icc.dur.ac.uk/~jlvc76/Files/CV/CV_MatthieuSchaller.pdf, timeout=1")

def parse_json(cdx_url):
    urls = []
    # Encode the JSON request into a list we can parse.
    raw_cdx_req = requests.get(cdx_url, verify=False).json()

    for cdx_req in raw_cdx_req:
        timestamp = cdx_req[1]
        url = cdx_req[2]
        #print(timestamp, url)
        urls.append([timestamp, url])

    urls.pop(0)
    return urls

    # Grab all of the JSON fields
    # Grab unique fields of the URLs and loop through the duplicate values to find timestamps
    # Insert everything into a list and then pass to write_pdf

    # return urls <- this should be a list.


def write_pdf(domain):
    json_req = parse_json(f'https://web.archive.org/cdx/search/cdx?url={domain}&output=json&matchType=host&limit=200&filter=length:.......&filter=mimetype:application/pdf')    
    pwd = os.getcwd()
    target_dir = pwd + '/' + domain
    if not os.path.isdir(pwd + '/' + domain):
        os.mkdir(target_dir)

    # Change directories so we can write the files here. 
    os.chdir(target_dir)
    
    for url in json_req:
        # Initialise variables for the request.
        timestamp = url[0]
        pdf_url = url[1]
        req_str = f"https://web.archive.org/web/{timestamp}/{pdf_url}"
        pdf_file = req_str.rsplit('/', 1)[-1]
        print(req_str)
        print(pdf_file)
        # Make the request with redirects to the download endpoint.
        req = requests.get(req_str, allow_redirects=True, verify=False)
        headers = req.headers
        print(req)

        if "Warning" in headers or "warning" in headers:
            print(f"{pdf_file} needs to be skipped")
        elif os.path.exists(target_dir + '/' + pdf_file):
            print("File exists skipping")
        else:
            f = open(f'{pdf_file}', 'wb').write(req.content)
            print("Successfully written file")



def main():
    domain = sys.argv[1]
    write_pdf(domain)

main()
