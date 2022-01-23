import requests
from bs4 import BeautifulSoup


def get_stack_jobs(term):
    URL = 'https://stackoverflow.com/'
    result = requests.get(f'{URL}jobs?q={term}')
    soup = BeautifulSoup(result.text, 'html.parser')
    jobs = soup.find('div', {'class': 'listResults'}).find_all(
        'div', {'class': 'js-result'})

    jobs_list = []
    for job in jobs:
        link_id = job['data-result-id']
        title = job.find('h2').get_text(strip=True)
        company = job.find('h3').find('span').get_text(strip=True)
        jobs_list.append(
            {'title': title, 'link': f'{URL}/{link_id}', 'company': company})

    return jobs_list
