import requests
from bs4 import BeautifulSoup
import csv

output_file = r'c:\Users\silicon store\Documents\B-Tech Project\btech-project-code\Web Crawler\jobinfocamer_informatique.csv'

# Write CSV header first
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Job Title', 'Link', 'Company', 'Location', 'Job Type'])

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

page = 1

while True:
    if page == 1:
        url = 'https://www.jobinfocamer.com/jobs/Informatique/'
    else:
        url = f'https://www.jobinfocamer.com/jobs/Informatique/?p={page}'

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')

    jobs_found = 0

    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for row in rows:
            try:
                # Extract fields
                date = row.find('td', class_='text-nowrap').text.strip()

                job_link_tag = row.find('a')
                job_title = job_link_tag.find('strong').text.strip()
                job_link = "https://www.jobinfocamer.com" + job_link_tag['href']

                p_tag = row.find('p')
                p_contents = p_tag.contents
                company = p_contents[0].strip()
                location = p_contents[-1].strip()

                job_type = row.find('span').text.strip()

                # Write to CSV
                writer.writerow([date, job_title, job_link, company, location, job_type])
                jobs_found += 1

            except Exception as e:
                continue

    print(f" Page {page} scraped: {jobs_found} jobs")

    if jobs_found == 0:
        print(" No more jobs found. Pagination finished.")
        break

    page += 1

print(" ALL INFORMATIQUE JOBS SCRAPED SUCCESSFULLY!")
 