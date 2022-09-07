from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

options = Options()
options.add_argument('user-agent=' + user_agent)
options.add_argument('headless')
options.add_argument('--blink-settings=imagesEnabled=false')

browser = webdriver.Chrome(options=options)

def get_page_count(keyword):

  base_url = "https://kr.indeed.com/jobs?q="

  browser.get(f"{base_url}{keyword}")
  soup = BeautifulSoup(browser.page_source, "html.parser")

  paginationSoup =  soup.find("ul", class_="pagination-list")
  if paginationSoup == None:
    return 1

  pages = paginationSoup.find_all("li", recursive=False)

  count = len(pages)

  if count >= 5:
    return 5
  else:
    return count



def extract_indeed_jobs(keyword):
  sleep(1)

  pages = get_page_count(keyword)
  print(pages, "pages")
  results = []
  print(pages, "pages")
  for page in range(pages):
    sleep(0.3)
    print(page, "current page")
    base_url = "https://kr.indeed.com/jobs"
    final_url = f"{base_url}?q={keyword}&start={page - 1}"

    browser.get(final_url)
    soup = BeautifulSoup(browser.page_source, "html.parser")

    job_list = soup.find("ul", class_="jobsearch-ResultsList")
    if job_list == None:
      browser.close()
      return print("job_list none")

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
  return results



jobs = extract_indeed_jobs("react")

print(jobs)
print("\n\n")
print(len(jobs))