from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


options = Options()
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")



browser = webdriver.Chrome(options=options)

base_url = "https://kr.indeed.com/jobs?q="
search_terms = "react"

sleep(1)

browser.get(f"{base_url}{search_terms}")

soup = BeautifulSoup(browser.page_source, "html.parser")

job_list = soup.find("ul", class_="jobsearch-ResultsList")
jobs = job_list.find_all("li", recursive=False)
for job in jobs:
  zone = job.find("div", class_="mosaic-zone")
  if zone == None:
    print("job li")
  else:
    print("mosaic li")
  print("===========================================")

browser.close()

