import requests
import csv
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# to using this script uncomment any link below
# base_url = "http://hh.ru/search/vacancy?L_is_autosearch=false&area=113&clusters=true&enable_snippets=true&search_period=7&text=python&page=0"  # search in all directions
# base_url = 'https://tyumen.hh.ru/search/vacancy?L_is_autosearch=false&area=95&clusters=true&enable_snippets=true&text=python&page=0'  # search in Tyumen direction
# base_url = 'https://ekaterinburg.hh.ru/search/vacancy?L_is_autosearch=false&area=3&clusters=true&enable_snippets=true&text=python&page=0'  # search in Ekb direction
# base_url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text=python&page=0'  # search in Moscow direction

def hh_parse(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    #request = session.get(("http://hh.ru/search/vacancy?L_is_autosearch=false&area=113&clusters=true&enable_snippets=true&search_period=7&text=python&page={}".format(x)), headers=headers)
    if request.status_code == 200:
        # start = time.time()
        # print('OK') is answer is
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'http://hh.ru/search/vacancy?L_is_autosearch=false&area=113&clusters=true&enable_snippets=true&search_period=7&text=python&page={i}'
                if url not in urls:
                    urls.append(url)
                # print(url)
        except:
            pass

    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
        # print(len(div)) количество вакансий на странице

        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            try:
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            except:
                company = div.find(attrs={'class': 'vacancy-serp-item__meta-info'}).text
                #return div.find('p', attrs={'class': 'vacancy-company-name-wrapper'})
                #return None
            text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            content = (text1 + ' ' + text2)
            jobs.append({
                'title': title,
                'href': href,
                'company': company,
                'content': content
            })

        print(len(jobs))

    else:
        print('ERROR or Done with code ' + str(request.status_code))
    return jobs

def files_writer(jobs):
    # try:
    with open('C:/Users/r-pos/Desktop/moscow_parsed_jobs.csv', 'w', encoding='utf-16') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['content']))


jobs = hh_parse(base_url, headers)
files_writer(jobs)
