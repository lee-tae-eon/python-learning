from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def extract_indeed_jobs():
  options = Options()
  browser = webdriver.Chrome(options=options)
  base_url = "https://kr.indeed.com/jobs?q="

  search_terms = str(input("plz search job: "))
  sleep(1)

  browser.get(f"{base_url}{search_terms}")
  soup = BeautifulSoup(browser.page_source, "html.parser")
  # job result
  results = []

  job_list = soup.find("ul", class_="jobsearch-ResultsList")
  jobs = job_list.find_all("li", recursive=False)
  for job in jobs:
    zone = job.find("div", class_="mosaic-zone")
    if zone == None:
      anchor = job.select_one("h2 a")
      title = anchor["aria-label"]
      link = anchor["href"]
      company= job.find("span", class_="companyName")
      location = job.find("div", class_="companyLocation")

      job_data = {
        "link": f"https://kr.indeed.com{link}",
        "company": company.string,
        "location": location.string,
        "position": title,
      }
      results.append(job_data)
  for res in results:
    print(res)
    print("\n\n")




  browser.close()


