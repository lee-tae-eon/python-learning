from bs4 import BeautifulSoup
from requests import get


base_url = "https://kr.indeed.com/jobs?q="
search_terms = "react"


response = get(f"{base_url}{search_terms}")


if response.status_code != 200:
  print("can't request page")
  print(response._content)
else:
  soup = BeautifulSoup(response.text, "html.parser")

  job_list = soup.find("ul", class_="jobsearch-ResultsList")
  jobs = job_list.find_all("li", recursive=False)
  print(len(jobs))

