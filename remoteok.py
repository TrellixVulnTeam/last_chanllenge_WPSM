import requests
from bs4 import BeautifulSoup


def get_remote_jobs(term):
    URL = 'https://remoteok.com'
    results = requests.get(f'{URL}/remote-{term}-jobs')
    soup = BeautifulSoup(results.text, 'html.parser')
    jobs = soup.find('table', {'class': "jobsboard"}
                     ).find_all('tr', {'class': 'job'})

    job_list = []

    for job in jobs:
        job = job.find('td', {'class': 'company '})
        title = jobs.find('h2', {'itemprop': 'title'}).get_text(strip=True)
        link = jobs['data-href']
        company = jobs.find('span', {'class': 'companyLink'}).find(
            'h3', {'itemprop': 'name'}).get_text(strip=True)
        job_list.append(
            {'title': title, 'link': f'{URL}/{link}', 'company': company})

    return job_list
