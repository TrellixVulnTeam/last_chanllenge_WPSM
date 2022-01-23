import requests
from bs4 import BeautifulSoup


def get_wework_jobs(term):
    URL = 'https://weworkremotely.com'
    result = requests.get(f'{URL}/remote-jobs/search?term={term}')
    soup = BeautifulSoup(result.text, 'html.parser')
    jobs_category = soup.find_all('section', {'class': 'jobs'})

    jobs_list = []

    for jobs in jobs_category:
        jobs_link = jobs.find('a')['href']
        link = f'{URL}{jobs_link}'
        get_category(URL, link, jobs_list)

    print(jobs_list)
    return jobs_list


def get_category(URL, link, jobs_list):
    result = requests.get(f'{link}')
    soup = BeautifulSoup(result.text, 'html.parser')
    jobs = soup.find('section', {'class': 'jobs'}).find_all(
        'li', {'class': 'feature'})
    for job in jobs:
        link = job.find_all('a')[-1]['href']
        print(link)
        company = job.find('span', {'class': 'company'}).get_text(strip=True)
        title = job.find('span', {'class': 'title'}).get_text(strip=True)
        jobs_list.append(
            {'title': title, 'link': f'{URL}{link}', 'company': company})
