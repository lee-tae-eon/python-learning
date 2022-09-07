from extractors.indeed import extract_indeed_jobs


keyword = input("search for job: ")

jobs = extract_indeed_jobs(keyword)

print(jobs)

file = open(f"{keyword}.csv", "w")

file.write("Position, Company, Location, URL\n")

for job in jobs:
  file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n")

file.close()