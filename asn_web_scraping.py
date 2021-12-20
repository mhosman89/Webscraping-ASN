#!/usr/bin/env python3

from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import urljoin
# Get beautifulsoup4 with: pip install beautifulsoup4
import bs4
import json
import time
from concurrent.futures import ThreadPoolExecutor
#import lxml
#import cchardet

# To help get you started, here is a function to fetch and parse a page.
# Given url, return soup.


def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read().decode('utf-8')
    soup = bs4.BeautifulSoup(html, features="html.parser")
    print(f'  [Finished parsing the html report of {url.rsplit("/",1)[-1]}] ', flush=True)
    return soup


# This function to get full list of the report url of each country from the world report soup
# Give the main url site and the soup object if the world report, return a list of each country's report link
def get_reports_urls(url, soup):
    print(' Get the linked report of each country:')
    reports_links_el = soup.tbody.select("a")
    links = []
    for report_link_el in reports_links_el:
        link = urljoin(url, report_link_el.get("href"))
        links.append(link)
    print(f'  [Found {len(links)} linked country reports] ', flush=True)
    return links


# This function is to map each ASN to the information about that ASN and structure a dictionary of the information
# Given the soup obejct of html report for each company and the country code, return a dictionary with the information
def asn_mapping_to_info(soup, code):
    company_info = soup.select("td")
    company_asn = int(company_info[0].string[2:])
    company_name = company_info[1].string
    company_routes_v4 = int(company_info[3].string.replace(',', ''))
    company_routes_v6 = int(company_info[5].string.replace(',', ''))
    map_dict = {
        company_asn: {
            'Country': code,
            'Name': company_name,
            'Routes v4': company_routes_v4,
            'Routes  v6': company_routes_v6
        }
    }
    return map_dict


# This function is to collect all the mapped ASN data over multiple threads concurrently for better performance
# it decreased runtime to 60% faster than running sequentially
def collect_asn_data(urls, num):
    collected_asn_data_dict = {}
    with ThreadPoolExecutor(max_workers=num) as executor:
        reports_soup_list = executor.map(url_to_soup, urls)
        for report_soup in reports_soup_list:
            country_code = report_soup.h1.find("a").get("href")[-2:]
            companies_info_list = report_soup.select("tbody tr")
            for company_info_soup in companies_info_list:
                asn_info_map_dict = asn_mapping_to_info(company_info_soup, country_code)
                collected_asn_data_dict.update(asn_info_map_dict)
    return collected_asn_data_dict


# This function is to output the collected data to a json file
# Given the file name and the collected data dictionary, output the data into json file
def output_data_to_json_file(json_file_name, asn_info_dict):
    print(' Starting to output the collected data to a json file.......', flush=True)
    out_file = open(json_file_name, "w", encoding='utf8')
    json.dump(asn_info_dict, out_file, indent=6)
    out_file.close()
    print('...Json file is created...', flush=True)


# Main Function
if __name__ == '__main__':
    start = time.perf_counter()
    print('Execution started.............', flush=True)
    bgp_url = "https://bgp.he.net"
    print(" Start parsing world report html.", flush=True)
    world_reports_soup = url_to_soup(urljoin(bgp_url, "/report/world"))
    reports_urls = get_reports_urls(bgp_url, world_reports_soup)
    thread_no = 120
    print(f' Run {thread_no} thread(s) to parse each country report', flush=True)
    asn_info_map = collect_asn_data(reports_urls, thread_no)
    print(f'  [All reports html are done parsing in {round(time.perf_counter()-start)} second(s)] ', flush=True)
    print(' Done mapping each ASN to info about the ASN', flush=True)
    asn_file_name = "asn_info_map1.json"
    output_data_to_json_file(asn_file_name, asn_info_map)
    print("Execution completed.", flush=True)
    print(f'Time taken {round(time.perf_counter()-start)} second(s)')
