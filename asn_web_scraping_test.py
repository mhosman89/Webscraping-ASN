#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import patch, mock_open
from bs4 import BeautifulSoup
import asn_web_scraping
import json


class TestASNWebScrap(TestCase):

	# This sets up the url variable before each test case
	def setUp(self):
		TestASNWebScrap.url = 'https://bgp.he.net'

	# This tests the get_reports_urls function
	def test_get_reports_urls(self):
		html = '<html><tbody>' \
			'<tr><td><a href="/country/US">Report</a></td></tr>' \
			'<tr><td><a href="/country/BR">Report</a></td></tr>' \
			'<tr><td><a href="/country/CN">Report</a></td></tr>' \
			'</tbody></html>'
		bsoup = BeautifulSoup(html, 'html.parser')
		url = TestASNWebScrap.url
		expected_results = [url+'/country/US', url+'/country/BR', url+'/country/CN']
		results = asn_web_scraping.get_reports_urls(url, bsoup)
		self.assertEqual(results, expected_results)

	# This tests the asn_mapping_to_info function
	def test_asn_mapping_to_info(self):
		code = 'US'
		html = '<tr>' \
			'<td>AS4648</a></td><td>Global-Gateway Internet</td><td>125</td><td>1,343</td><td>50</td><td>204</td><' \
			'/tr>'
		soup = BeautifulSoup(html, 'html.parser')
		results = asn_web_scraping.asn_mapping_to_info(soup, code)
		expected_results = {
			4648: {
				'Country': 'US',
				'Name': 'Global-Gateway Internet',
				'Routes v4': 1343,
				'Routes  v6': 204
			}
		}
		self.assertEqual(results, expected_results)

	# This tests the collect_asn_data function
	@patch('asn_web_scraping.url_to_soup')
	def test_collect_asn_data(self, mock_url_to_soup):
		urls = [TestASNWebScrap.url + '/country/NZ']
		html = '<h1><a href="/country/NZ" rel="bookmark" title="Networks: New Zealand">Networks: New Zealand</a></h1>' \
			'<tbody>' \
			'<tr> <td>AS123</a></td><td>Test Company I</td><td>456</td><td>1,234</td><td>51</td><td>205</td>' \
			'</tr>' \
			'<tr> <td>AS456</a></td><td>Test Company II</td><td>457</td><td>5,678</td><td>52</td><td>206</td>' \
			'</tr>' \
			'<tr> <td>AS789</a></td><td>Test Company III</td><td>576</td><td>9,1011</td><td>53</td><td>207</td>' \
			'</tr></tbody>'
		mock_url_to_soup.return_value = BeautifulSoup(html, 'html.parser')
		results = asn_web_scraping.collect_asn_data(urls, 1)
		expected_results = {
			123: {
				'Country': 'NZ',
				'Name': 'Test Company I',
				'Routes v4': 1234,
				'Routes  v6': 205
			},
			456: {
				'Country': 'NZ',
				'Name': 'Test Company II',
				'Routes v4': 5678,
				'Routes  v6': 206
			},
			789: {
				'Country': 'NZ',
				'Name': 'Test Company III',
				'Routes v4': 91011,
				'Routes  v6': 207
			},
		}
		self.assertEqual(results, expected_results)

	# This function test the output_data_to_json_file
	def test_output_data_to_json_file(self):
		expected_results = {
			'123': {
				'Country': 'NZ',
				'Name': 'Test Company I',
				'Routes v4': 1234,
				'Routes  v6': 205
			},
			'456': {
				'Country': 'NZ',
				'Name': 'Test Company II',
				'Routes v4': 5678,
				'Routes  v6': 206
			}
		}
		asn_web_scraping.output_data_to_json_file('test_file.json', expected_results)
		test_file = open('test_file.json', "r")
		results = json.loads(test_file.read())
		test_file.close()
		self.assertEqual(results, expected_results)
