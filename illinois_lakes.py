import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def get_page(url):
    response = requests.get(url)
    if not response.ok:
        print('server responded: ',response.status_code)
    else:
        soup = BeautifulSoup(response.text,'lxml')
    return soup

def get_all_links(soup):
    try:
        links = []
        for i in range(len(soup.find_all('div',class_="listCol")[0].find_all('a'))):
            links.append('https://www.ifishillinois.org'+soup.find_all('div',class_="listCol")[0].find_all('a')[i].get('href').strip())
        for i in range(len(soup.find_all('div',class_="listCol")[1].find_all('a'))):
            links.append('https://www.ifishillinois.org'+soup.find_all('div',class_="listCol")[1].find_all('a')[i].get('href').strip())
        for i in range(len(soup.find_all('div',class_="listCol")[2].find_all('a'))):
            links.append('https://www.ifishillinois.org'+soup.find_all('div',class_="listCol")[2].find_all('a')[i].get('href').strip())
        for i in range(len(soup.find_all('div',class_="listCol")[3].find_all('a'))):
            links.append('https://www.ifishillinois.org'+soup.find_all('div',class_="listCol")[3].find_all('a')[i].get('href').strip())
        return links
    except:
        print('An exception occured.')
        links = []
        return links


def get_detail_page(soup):
    #getting lake information
    try:
        #Getting lake name
        title = soup.find('h2').contents[0]
    except:
        title = 'unknown'
        print('An exception has occurred.')
    try:
        #Table with lake info
        labels = []
        values =[]
        for i in range(len(soup.find_all('div',class_='amenities')[0].find_all('strong'))):
            labels.append(soup.find_all('div',class_='amenities')[0].find_all('strong')[i].contents[0].strip().strip(':'))
        for i in range(len(labels)):
            values.append(str(soup.find_all('div',class_='amenities')[0].find_all('p')[i].contents[1]))
        lake_overview = pd.DataFrame(values,index=labels,columns=['Information'])
    except:
        lake_overview = pd.Series([])
        print('An exception occured.')
    try:
        #Getting zebra mussels' details
        zebra_mussels = str(soup.find_all('h3',style='margin-left:15px')[0].contents[0])+str(soup.find_all('h3',style='margin-left:15px')[0].contents[1].contents[0])+' '+str(soup.find_all('h3',style='margin-left:15px')[0].contents[2]).strip()
        mussels = pd.DataFrame(zebra_mussels,index=['0'],columns=['Zebra Mussels'])
    except:
        mussels = pd.Series([])
        print('An exception has occurred.')
    try:
        #Getting # of tables:
        tables = len(soup.find_all('table',cellspacing='1px'))
    except:
        tables = ''
        print('An exception has occurred.')   
    try:
        if tables ==0:
            fishing_outlook = pd.Series([])
            fish_stocking = pd.Series([])

        if tables == 1:
            if len(soup.find_all('table',cellspacing='1px',width='425px')) == 1:
                table_len = len(soup.find_all('table',cellspacing='1px',width='425px')[0].find_all('tr',bgcolor="#CCCCCC"))
                years =[]
                species = []
                sizes = []
                counts = []
                for i in range(len(soup.find_all('table',cellspacing='1px',width='425px')[0].find_all('tr',bgcolor="#CCCCCC"))):
                    years.append(soup.find_all('table',cellspacing='1px',width='425px')[0].find_all('tr',bgcolor="#CCCCCC")[i].find_all('p',align="center")[0].contents[0])
                    species.append(soup.find_all('table',cellspacing='1px',width='425px')[0].find_all('tr',bgcolor="#CCCCCC")[i].find_all('p',align="left")[0].contents[0])
                    sizes.append(soup.find_all('table',cellspacing='1px',width='425px')[0].find_all('tr',bgcolor="#CCCCCC")[i].find_all('p',align="left")[1].contents[0])
                    counts.append(soup.find_all('table',cellspacing='1px',width='425px')[0].contents[i+5].contents[7].contents[0].contents[0])
                fish_stocking = {'Years':years,'Species':species,'Sizes':sizes,'Counts':counts}
                fish_stocking = pd.DataFrame(fish_stocking)
            else:
                species = []
                ranks = []
                fish_status = []
                for i in range(len(soup.find_all('table',cellspacing='1px')[0].find_all('a'))):
                    species.append(soup.find_all('table',cellspacing='1px')[0].find_all('a')[i].contents[0])
                    ranks.append(soup.find_all('table',cellspacing='1px')[0].find_all('p',align='center')[i].contents[0])
                    fish_status.append(soup.find_all('table',cellspacing='1px')[0].find_all('p',align='justify')[i].contents[0].strip())
                fishing_outlook = {'Species':species,'Ranks':ranks,'Fish Status':fish_status}
                fishing_outlook = pd.DataFrame(fishing_outlook)
                fish_stocking = pd.Series([])
        if tables >=2:
            if len(soup.find_all('table',cellspacing='1px',width='425px')) == 1:
                table_len = len(soup.find_all('table',cellspacing='1px',width='425px')[0].find_all('tr',bgcolor="#CCCCCC"))
                years =[]
                species = []
                sizes = []
                counts = []
                for i in range(len(soup.find_all('table',cellspacing='1px',width='425px')[0].find_all('tr',bgcolor="#CCCCCC"))):
                    years.append(soup.find_all('table',cellspacing='1px',width='425px')[0].find_all('tr',bgcolor="#CCCCCC")[i].find_all('p',align="center")[0].contents[0])
                    species.append(soup.find_all('table',cellspacing='1px',width='425px')[0].find_all('tr',bgcolor="#CCCCCC")[i].find_all('p',align="left")[0].contents[0])
                    sizes.append(soup.find_all('table',cellspacing='1px',width='425px')[0].find_all('tr',bgcolor="#CCCCCC")[i].find_all('p',align="left")[1].contents[0])
                    counts.append(soup.find_all('table',cellspacing='1px',width='425px')[0].contents[i+5].contents[7].contents[0].contents[0])
                fish_stocking = {'Years':years,'Species':species,'Sizes':sizes,'Counts':counts}
                fish_stocking = pd.DataFrame(fish_stocking)
                species = []
                ranks = []
                fish_status = []
                for i in range(len(soup.find_all('table',cellspacing='1px')[1].find_all('a'))):
                    species.append(soup.find_all('table',cellspacing='1px')[1].find_all('a')[i].contents[0])
                    ranks.append(soup.find_all('table',cellspacing='1px')[1].find_all('p',align='center')[i].contents[0])
                    fish_status.append(soup.find_all('table',cellspacing='1px')[1].find_all('p',align='justify')[i].contents[0].strip())
                fishing_outlook = {'Species':species,'Ranks':ranks,'Fish Status':fish_status}
                fishing_outlook = pd.DataFrame(fishing_outlook)
                #print(soup.find_all('table',cellspacing='1px')[1].find_all('p',align='justify')[0].contents[0].strip())
    except:
        fishing_outlook = pd.Series([])
        fish_stocking = pd.Series([])
        print('An exception has ocurred')

    try:
        lake_general_information_labels = []
        lake_general_information_values = []
        for i in range(len(soup.find_all('div',class_='description')[0].find_all('p'))):
            lake_general_information_labels.append(soup.find_all('div',class_='description')[0].find_all('p')[i].contents[0].contents[0])
            lake_general_information_values.append(soup.find_all('div',class_='description')[0].find_all('p')[i].contents[1].strip())
        lake_info = {'Topic':lake_general_information_labels,'Information':lake_general_information_values}
        lake_info = pd.DataFrame(lake_info)
    except:
        lake_info = pd.Series([])
        print('An exception occurred.')
    return title,lake_overview,mussels,fish_stocking,fishing_outlook,lake_info

def to_excel(title,lake_overview,mussels,fish_stocking,fishing_outlook,lake_info):
    try:
        writer = pd.ExcelWriter(title+'.xlsx')
        lake_overview.to_excel(writer,'Lake Overview')
        mussels.to_excel(writer,'Mussels')
        fish_stocking.to_excel(writer,'Fish Stocking')
        fishing_outlook.to_excel(writer,'Fishing Outlook')
        lake_info.to_excel(writer,'Lake Info')
        writer.save()
    except:
        print('Also salio mal')
    return

def main():
    url = 'https://www.ifishillinois.org/profiles/selector.php'
    soup = get_page(url)
    links_list = get_all_links(soup)
    for i in range(len(links_list[:5])):
        soup = get_page(links_list[i])
        title,lake_overview,mussels,fish_stocking,fishing_outlook,lake_info = get_detail_page(soup)
        to_excel(title,lake_overview,mussels,fish_stocking,fishing_outlook,lake_info)
    print('Done')

if __name__ =='__main__':
    main()

