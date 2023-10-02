from datetime import datetime
import whois
import requests
import ssl
import socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio
import os
from pathlib import Path
import chromedriver_autoinstaller


# from webdriver_manager.chrome import ChromeDriverManager


class ScamInsight:
    URL_PATTERN = r"(https?://)?[a-zA-Z0-9.-]+\.[a-z]{2,4}"

    OTX_API_URL = 'https://otx.alienvault.com/api/v1/indicators/domain/'

    HTTP_OBSERVATORY_API_URL = 'https://http-observatory.security.mozilla.org/api/v1/analyze'

    def __init__(self, url, screenshot_path, otx_api_key):
        self.url = self.add_http_protocol(url)
        self.screenshot_path = screenshot_path
        self.otx_api_key = otx_api_key

    def format_date(self, date):
        if isinstance(date, list) and len(date) > 0:
            return date[0].strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(date, datetime):
            return date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return ''

    def add_http_protocol(self, url):
        if not url.startswith('http://') and not url.startswith('https://'):
            return 'http://' + url
        else:
            return url

    async def get_otx_info(self, url):
        domain_for_otx = urlparse(url).netloc
        otx_info = {}
        sections = ["geo", "passive_dns", "http_scans"]

        otx_responses = await asyncio.gather(
            *[asyncio.to_thread(requests.get, f'{self.OTX_API_URL}{domain_for_otx}/{section}',
                                headers={'X-OTX-API-KEY': self.otx_api_key}) for section in
              sections])
        for section, otx_response in zip(sections, otx_responses):
            otx_response.raise_for_status()
            otx_info[section] = otx_response.json()

        return otx_info

    def get_latitude_and_longitude(self, otx_info):
        geo_info = otx_info.get('geo', {})
        return geo_info.get('latitude'), geo_info.get('longitude')

    def check_ssl(self, hostname):
        try:
            context = ssl.create_default_context()
            with context.wrap_socket(socket.create_connection((hostname, 443)), server_hostname=hostname) as ssock:
                return ssock.getpeercert() is not None
        except Exception as e:
            return False

    def get_duckduckgo_results(self, url):

        domain = urlparse(url).hostname
        excluded_domains = ["scamadviser.com", "scamdoc.com", "scamwatcher.org", "scam-detector.com", "webparanoid.com",
                            "observatory.mozilla.org", "islegitsite.com", "mywot.com"]

        duckduckgo_url = f'https://duckduckgo.com/html/?q="{domain}"'
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0"}

        duckduckgo_page = requests.get(duckduckgo_url, headers=headers).text
        duckduckgo_soup = BeautifulSoup(duckduckgo_page, 'html.parser').find_all("a", class_="result__url", href=True)

        filtered_results = [result for result in duckduckgo_soup if
                            not any(domain in result['href'] for domain in excluded_domains)]
        return filtered_results

    def check_ssl_and_get_results(self, url):
        hostname = urlparse(url).hostname
        ssl_result = self.check_ssl(hostname)
        return ssl_result

    def scrape_web_page(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def get_meta_tags(self, soup):
        return soup.find_all('meta')

    def get_headings(self, soup):
        return soup.find_all(re.compile('^h[1-6]$'))

    def get_sorted_a_records(self, otx_info):
        a_records = [record for record in otx_info['passive_dns']['passive_dns'] if
                     record['record_type'] == 'A']
        return sorted(a_records, key=lambda x: x['address'])

    def call_http_observatory_api(self, url):
        try:
            hostname = urlparse(url).hostname
            params = {'host': hostname}
            response = requests.get(self.HTTP_OBSERVATORY_API_URL, params=params)
            response.raise_for_status()
            if "error" in response.json():
                requests.post(self.HTTP_OBSERVATORY_API_URL, params=params,
                              data={"hidden": "true", "rescan": "true"})
                tmp = 0
                while True:
                    time.sleep(2)
                    response = requests.get(self.HTTP_OBSERVATORY_API_URL, params=params)
                    tmp += 1
                    if "error" not in response.json():
                        break
                    raise Exception("time exceeded") if tmp == 4 else None
            return response.json()

        except Exception as e:
            return {'error': str(e)}

    def full_screenshot(self, driver, url, output_path):
        driver.get(url)
        time.sleep(2)  # 페이지 로딩을 위한 대기 시간

        # total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        driver.set_window_size("1920", "1260")

        time.sleep(1)
        driver.save_screenshot(output_path)

    def run(self, search_type):

        print(self.url)
        if not re.match(self.URL_PATTERN, self.url):
            error_message = '유효한 URL 형식이 아닙니다.'
            return error_message

        if search_type == "-w":
            try:
                w = whois.whois(self.url)
                domain_info = {
                    "domain_name": w.domain_name[1] if isinstance(w.domain_name, list) else w.domain_name,
                    "registrar": w.registrar,
                    "whois_server": w.whois_server,
                    "referral_url": w.referral_url,
                    "updated_date": self.format_date(w.updated_date),
                    "creation_date": self.format_date(w.creation_date),
                    "expiration_date": self.format_date(w.expiration_date),
                    "name_servers": w.name_servers,
                    "status": w.status,
                    "emails": w.emails,
                    "dnssec": w.dnssec,
                    "name": w.name,
                    "org": w.org,
                    "address": w.address,
                    "city": w.city,
                    "state": w.state,
                    "registrant_postal_code": w.registrant_postal_code,
                    "country": w.country,
                }
                return domain_info
            except Exception as e:
                return e
        elif search_type == "-a":
            try:
                # alienvalut api 호출 결과 가져오기
                otx_info = asyncio.run(self.get_otx_info(self.url))

                # 위도,경도 정보 가져오기
                latitude, longitude = self.get_latitude_and_longitude(otx_info)

                # 인증서 유효 여부 정보
                ssl_result = self.check_ssl_and_get_results(self.url)

                # 웹 페이지 정보 파싱
                soup = self.scrape_web_page(self.url)
                meta_tags = self.get_meta_tags(soup)
                headings = self.get_headings(soup)
                sorted_a_records = self.get_sorted_a_records(otx_info)

                return {"otx_info": otx_info, "latitude": latitude, "longitude": longitude, "ssl_result": ssl_result,
                        "meta_tags": meta_tags, "headings": headings, "sorted_a_records": sorted_a_records}
            except Exception as e:
                return e
        elif search_type == "-d":
            try:
                # duckduckgo search 결과 가져오기
                duckduckgo_results = self.get_duckduckgo_results(self.url)
                return duckduckgo_results

            except Exception as e:
                return e
        elif search_type == "-o":
            try:
                http_observation_result = self.call_http_observatory_api(self.url)
                return http_observation_result
            except Exception as e:
                return e
        elif search_type == "-s":
            driver_path = str(Path.home()) + "/" + chromedriver_autoinstaller.get_chrome_version().split(".")[
                0] + "/" + "chromedriver.exe"
            if not driver_path:
                chromedriver_autoinstaller.install(True)
            chrome_options = Options()
            chrome_options.add_argument('headless')

            driver = webdriver.Chrome(driver_path, options=chrome_options)

            try:
                if not os.path.isdir(self.screenshot_path):
                    os.mkdir(self.screenshot_path)
                screenshot_path = f"{self.screenshot_path}/{urlparse(self.url).hostname}.png"
                self.full_screenshot(driver, self.url, screenshot_path)
            finally:
                driver.quit()
        elif search_type == "-all":
            try:
                w = whois.whois(self.url)

                # alienvalut api 결과 가져오기
                otx_info = asyncio.run(self.get_otx_info(self.url))

                # 위도,경도 정보 가져오기
                latitude, longitude = self.get_latitude_and_longitude(otx_info)

                # 인증서 유효 여부 체크
                ssl_result = self.check_ssl_and_get_results(self.url)

                # 웹 페이지 정보 파싱
                soup = self.scrape_web_page(self.url)
                meta_tags = self.get_meta_tags(soup)
                headings = self.get_headings(soup)
                sorted_a_records = self.get_sorted_a_records(otx_info)

                domain_info = {
                    "domain_name": w.domain_name[1] if isinstance(w.domain_name, list) else w.domain_name,
                    "registrar": w.registrar,
                    "whois_server": w.whois_server,
                    "referral_url": w.referral_url,
                    "updated_date": self.format_date(w.updated_date),
                    "creation_date": self.format_date(w.creation_date),
                    "expiration_date": self.format_date(w.expiration_date),
                    "name_servers": w.name_servers,
                    "status": w.status,
                    "emails": w.emails,
                    "dnssec": w.dnssec,
                    "name": w.name,
                    "org": w.org,
                    "address": w.address,
                    "city": w.city,
                    "state": w.state,
                    "registrant_postal_code": w.registrant_postal_code,
                    "country": w.country,
                    "otx_info": otx_info
                }

                # duckduckgo search 결과 가져오기
                duckduckgo_results = self.get_duckduckgo_results(self.url)

                # observtory api 결과 가져오기
                http_observation_result = self.call_http_observatory_api(self.url)

                driver_path = str(Path.home()) + "/" + chromedriver_autoinstaller.get_chrome_version().split(".")[
                    0] + "/" + "chromedriver.exe"
                if not driver_path:
                    chromedriver_autoinstaller.install(True)
                chrome_options = Options()
                chrome_options.add_argument('headless')

                driver = webdriver.Chrome(driver_path, options=chrome_options)

                try:
                    if not os.path.isdir(self.screenshot_path):
                        os.mkdir(self.screenshot_path)
                    screenshot_path = f"{self.screenshot_path}/{urlparse(self.url).hostname}.png"
                    self.full_screenshot(driver, self.url, screenshot_path)
                finally:
                    driver.quit()

                result = {"url": self.url, "domain_info": domain_info, "ssl_result": ssl_result,
                          "meta_tags": meta_tags, "headings": headings, "duckduckgo_results": duckduckgo_results,
                          "latitude": latitude, "longitude": longitude, "a_records": sorted_a_records,
                          "http_observation_result": http_observation_result, "screenshot": screenshot_path}
                return result
            except Exception as e:
                return e
