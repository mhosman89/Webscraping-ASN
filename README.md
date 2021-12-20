# Webscraping-ASN

**Version 1.0.0**

This is a python project to crawl and scrape the BGP Toolkit website for ASNs (Autonomous System Numbers) in the linked country reports 
and create a mapping from each ASN in use to the company that owns it.

---

## libraries used in the project

1. urllib.request -- Request and urlopen to fetch and open the url request
2. urlib.parse -- urljoin to construct a full url
3. beautifulsoup4 -- to scrap the web
4. json -- dump() to convet the python dictionary object to json obeject
5. concurrent.futures -- ThreadExecutorPool to run the program on multithread for better performance

To install required libraries use pip install
for example: get beautifulsoup4 with: pip install beautifulsoup4

## 

---

The project consists of two main scripts:

asn_web_scrapping.py ---> main script
asn_web_scrapping_test.py ---> unit test script
In the 'asn_web_scrapping' script, I built four other functions in addition to the 'url_to_soup' function that was provided:

 get_reports_urls:  This function gets the full list of the report url of each country from the world report page
 Given the main site URL and the soup object of the world report. 
it searches for all the linked report under <tbody> tag on the world report html and returns a list of the partial links
it loops through the list and join each one to the main URL site and append to the list
Then it returns a list of each country's report link

asn_mapping_to_info: This function maps each ASN to the information about that ASN and structure a dictionary of this mapping
Given the country code and soup object of html report for a company.
It searches for the <td> tags and returns a list of company information.
It maps ASN to the information of that ASN.
Then it returns a dictionary with the mapped information.

collect_asn_data: This function collects all the mapped ASN data over multiple threads concurrently for better performance
Given the list of reports URLs and the number of threads.
It passes the list of URLs to url_to_soup over multiple threads to get the soup object of each country's report page
It loops through the list of soup returned and searches for the country code and a list of companies inforamtion soup objects in a report.
It loops through the list of the companies information and pass the information to the asn_mapping_to_info function to map it
It update collected data dictionary with the returned mapped data 
Then it returns the collected ASN data dictionary. 

output_data_to_json_file: This function outputs the collected ASN data into a json file
Given the Json file name and the collected data dictionary.
It opens a file with the name passed for writing the data and returns a file object.
It converts the collected data dictitionary into a Json object and store it into the opened file.
Then it closes the file.
In 'asn_web_scrapping_test.py' test script, i wrote a unit test case for each of the above functions using the unittest library:
test_get_reports_urls
test_asn_mapping_to_info
test_collect_asn_data
test_output_data_to_json_file
---
## Contributors

- Mohamed H Osman <mhosmanit@outlook.com>

---
