import bs4 as bs
import urllib3 as lib2
from urllib.request import urlopen

def scraper(page=0):
    scraper_list = []
    api_url = "http://programmableweb.com/apis/directory"
    if page != 0:
        api_url = '%s?page=%s' % (api_url, page)
    response = urlopen(api_url)
    soup = bs.BeautifulSoup(response.read())
    table = soup.find('table')
    for i in table.findAll('tr'):
        entry_dict = {}
        for s in i.findAll('a'):
            if 'api' in s.get('href'):
                print('href = %s, text = %s' % (s.get('href'), s.text))
                entry_dict['API Company'] = s.text
                spec = 'http://programmableweb.com%s' % s.get('href')
                try:
                    spec_resp = urlopen(spec)
                except:
                    print("An issue occured trying to open %s" % spec)
                    continue
                soup_rec = bs.BeautifulSoup(spec_resp.read())
                for div in soup_rec.findAll('div'):
                    if div.get('class') == 'field':
                        label = div.find('label')
                        if label.text == 'API Homepage':
                            entry_dict['API Homepage'] = div.find('a').text
                            print(div.find('a').text)
                        elif label.text == 'Primary Category':
                            entry_dict['Primary Category'] = div.find('a').text
                        elif label.text == 'API Provider':
                            entry_dict['API Provider Page'] = div.find('a').text
        scraper_list.append(entry_dict)
    return scraper_list

if __name__ == '__main__':
    comp_s = 'API Company'
    prov_s = 'API Provider Page'
    home_s = 'API Homepage'
    prime_s = 'Primary Category'
    for i in range(0,100):
        try:
            scraper_list = scraper(i)
            file_name = 'output_%s.txt' % i
            with open(file_name, 'w') as f:
                f.write('API Company,API Provider Page,API Homepage,Primary Category\n')
                for j in scraper_list:
                    comp = j[comp_s] if comp_s in list(j.keys()) else ''
                    prov = j[prov_s] if prov_s in list(j.keys()) else ''
                    home = j[home_s] if home_s in list(j.keys()) else ''
                    prime = j[prime_s] if prime_s in list(j.keys()) else ''
                    f.write("%s,%s,%s,%s\n" % (comp, prov, home, prime))
                f.close()
        except:
            print(i, scraper_list)
