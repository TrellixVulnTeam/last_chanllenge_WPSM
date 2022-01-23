import csv
from bs4 import BeautifulSoup
import requests
from flask import Flask, request, redirect, send_file
from flask.templating import render_template

app = Flask('searchApp')

fakeDB = {}


def save_to_file(jobs, term):
    file = open(f'{term}.csv', mode='w')
    writer = csv.writer(file)
    writer.writerow(['title', 'company', 'link'])

    for job in jobs:
        for i in range(job):
            writer.writerow(list(job[i].values()))


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

    # print(jobs_list)
    return jobs_list


def get_category(URL, link, jobs_list):
    result = requests.get(f'{link}')
    soup = BeautifulSoup(result.text, 'html.parser')
    jobs = soup.find('section', {'class': 'jobs'}).find_all(
        'li', {'class': 'feature'})
    for job in jobs:
        link = job.find_all('a')[-1]['href']
        # print(link)
        company = job.find('span', {'class': 'company'}).get_text(strip=True)
        title = job.find('span', {'class': 'title'}).get_text(strip=True)
        jobs_list.append(
            {'title': title, 'link': f'{URL}{link}', 'company': company})


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


def get_remote_jobs(term):
    URL = 'https://remoteok.com'
    result = requests.get(f'{URL}/remote-{term}-jobs')
    soup = BeautifulSoup(result.text, 'html.parser')
    jobs = soup.find('div', {'class': 'page'}).find_all('tr', {'class': 'job'})
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


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    term = request.args.get('term')
    if term:
        term = term.lower()
        DB = fakeDB.get(term)
        if DB:
            jobs = DB
        else:
            stack = get_stack_jobs(term)
            wework = get_wework_jobs(term)
            remoteok = get_remote_jobs(term)
            jobs = {'stack': stack, 'wework': wework, 'remoteok': remoteok}
            fakeDB[term] = jobs
    else:
        redirect('/')
    return render_template('search.html', search=term, resultsNumber=len(stack) + len(wework) + len(remoteok), jobs=jobs)


@app.route('/export')
def export():
    try:
        term = request.args.get('term')
        if not term:
            raise Exception()
        term = term.lower()
        jobs = fakeDB.get(term)
        if not jobs:
            raise Exception()

        save_to_file(jobs)
        return send_file(f'{term}.csv')
    except:
        return redirect('/')


app.run(host='127.0.0.1')
