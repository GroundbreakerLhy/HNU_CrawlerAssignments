# 代码来自Groundbreaker 
# 想联系我的话花点心思不难找到我的联系方式
# 如果今年题目变了代码用不了了，可以在Github上找到我，我会尽快更新代码
import requests
from bs4 import BeautifulSoup

def fetch_page(session, page_number):
    url = f'https://www.job001.cn/jobs?pageNo={page_number}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    r = session.get(url=url, headers=headers)
    r.encoding = 'utf-8'
    return r.text

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    jobList = soup.find_all('div', attrs={'class': 'jobsList'})
    for i in jobList:
        workName = i.find('a', attrs={"class": "jobNameCon"}).string
        jobRight = i.find('div', attrs={'class': 'jobRight'})
        company = jobRight.find('a', attrs={'target': '_blank'}).string.strip()
        salary = i.find('span', attrs={'class': 'salaryList'}).string.replace(' ', '').replace('\n', '')
        add = i.find('span', attrs={'class': 'cityConJobsWork'}).string.replace(' ', '')
        time = i.find('span', attrs={'class': 'time'}).string.strip().replace(' ', '').replace('刷新过', '')
        yield workName, company, salary, add, time

with requests.Session() as session, open("./advertise.txt", 'w', encoding="utf-8") as f:
    for j in range(1, 16):
        html = fetch_page(session, j)
        for workName, company, salary, add, time in parse_page(html):
            data = f'{workName}|{company}|{salary}|{add}|{time}'
            f.write(data + '\n')
            print(data)
            print()
        f.write(f'第{j}页\n\n')
        print(f'第{j}页\n')