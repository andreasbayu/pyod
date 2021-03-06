from bs4 import BeautifulSoup
from os import system
import requests as req
from requests.exceptions import RequestException


def print_bar(param='clear'):
    system(param)
    __bar__ = f"""{cl.BLUE}
          .--.  .       .            .                 
         :    :_|_      |            |                 
.,-. .  .|    | |  .-.  |.-. .  . .-.| .-. .--..  .    
|   )|  |:    ; | (   ) |-.' |  |(   |(.-' `--.|  |    
|`-' `--| `--'  `-'`-'`-'  `-`--`-`-'`-`--'`--'`--`-   
|       ;                                              
'    `-'       
{cl.ENDC}
{cl.RED}Author : koplak{cl.ENDC}
    
    """
    print(__bar__)

class Otakudesu():
    def __init__(self, inp):
        self.url = ''  
        self.headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
        self.result_titles = []
        self.download_links_title = []
        self.page_links = []
        self.download_links = []
        self.download_link = []
        if inp == '1':
            self.url = 'https://otakudesu.tv/ongoing-anime/'
            self.get_ongoing_data(self.url)
        else:
            key = input("Masukkan Pencarian > ")
            self.url = (f"https://otakudesu.tv/?s={key.replace(' ','+')}&post_type=anime")
            self.get_search_data(self.url)

    
    def get_ongoing_data(self, url):
        try:
            print_bar()
            _upload_date =[]
            _getData = req.get(url, headers=self.headers).text
            _bs = BeautifulSoup(_getData, 'html.parser')
            _findData = _bs.findAll('div', class_='detpost')
            if len(_findData) != 0:
                for i in _findData:
                    self.download_links.append(i.find('a')['href'])
                    self.result_titles.append(i.find('a').text)
                    _upload_date.append(str(f"{i.find('div',class_='epztipe').text} - {i.find('div',class_='newnime').text}"))
                for i,result_title in enumerate(self.result_titles):
                    print(f'{cl.GREEN}➭ {cl.ENDC}{cl.WB}{i+1}.{cl.ENDC}{cl.TITLE} {result_title}{cl.ENDC} {cl.BLUE}<<{_upload_date[i]} >>{cl.ENDC}')
                self.get_download_page(self.download_links[int(input(f'{cl.GREEN}【 Pilih 】 ➤ {cl.ENDC}'))-1])
        except RequestException as e:
            exit(e)

    def get_search_data(self, url):
        try:
            print_bar()
            _getData = req.get(url,headers=self.headers).text
            _bs = BeautifulSoup(_getData, 'html.parser')
            _findData = _bs.find('ul',class_='chivsrc')
            if len(_findData) != 0:
                for i in _findData:
                    self.result_titles.append(i.find('a').text)
                    self.download_links.append(i.find('a')['href'])
                for i,result_title in enumerate(self.result_titles):
                    print(f'{cl.GREEN}【 ➣ 】{cl.ENDC} {cl.WB}{i+1}.{cl.ENDC} {cl.TITLE}{result_title}{cl.ENDC}')
                opsi_kembali()
                self.get_download_page(self.download_links[int(input(f'\n{cl.GREEN}【 Pilih 】 ➤ {cl.ENDC}'))-1])
            else:
                print(cl.FAIL,'Opps hasil tidak ditemukan !!',cl.ENDC)
                if (input(f'{cl.GREEN}【 Ulangi Pencarian ?[Y/t] 】 ➤ {cl.ENDC}')).lower() == 'y':
                    main()
                else:
                    exit(0)
        except RequestException as e:
            exit(e)

    def get_download_page(self, url):
        if len(self.download_links_title) > 0:
            self.clear_data(ignore="none")
        try:
            print_bar()
            _getData = req.get(url, headers=self.headers).text
            _bs = BeautifulSoup(_getData, 'html.parser')
            _findData = _bs.findAll('div', class_='episodelist')
            _filterData1 = _findData[1].findAll('li')
            _uploadDate = _findData[1].findAll('span',class_='zeebr')
            for i in _filterData1:
                self.page_links.append(i.find('a')['href'])
                self.download_links_title.append(i.find('a').text)
            for i,eps in enumerate(self.download_links_title):
                print(f'{cl.GREEN}➭{cl.ENDC} {cl.WB}{i+1}.{cl.ENDC} {cl.TITLE}{eps}{cl.ENDC} {cl.CYAN}<< {(_uploadDate[i]).text} >>{cl.ENDC}')
            return self.get_download_link(self.page_links[int(input(f'{cl.GREEN}【 Pilih Episode 】 ➤ {cl.ENDC}'))-1], url)
        except RequestException as e:
            exit(e)

    def get_download_link(self, udownload, pagelink):
        try:
            print_bar()
            _getData = req.get(udownload, headers=self.headers).text
            _bs = BeautifulSoup(_getData, 'html.parser')
            _findData = _bs.find('div',class_='download').ul
            _findAData = _findData.findAll('a')
            print(f"\n{cl.WB}{cl.UNDERLINE} {_bs.find('title').text}{cl.ENDC}{cl.ENDC}")
            for i in _findData:
                print(f"{cl.HEADER}\n\t\t\t➠ {i.find('strong').text} size : {i.find('i').text}\n{cl.ENDC}")
                for x in i.findAll('a'):
                    print('【 ▶ 】',x.text, ' : ',x['href'])
            while True:
                opsi = get_opsi()
                if opsi == '1':
                    break
                elif opsi == '2':
                    return self.get_download_page(pagelink)
                elif opsi == '3':
                    exit()
                else:
                    print('Error !!!')
        except RecursionError as e:
            exit(e)

    def get_all_download_link(self):
        """ Test """
        pass

    def clear_data(self, ignore=''):
        """ clear list ! belum tuntas"""
        if ignore == 'none':
            self.result_titles.clear()
            self.download_link.clear()
            self.download_links.clear()
            self.download_links_title.clear()
            self.page_links.clear()
        elif ignore == 'links':
            self.page_links.clear()
            self.download_links.clear()


class cl:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'
    TITLE = '\033[93m'
    WB = '\033[97m'

def main():
    print_bar()

    print(f"""   Pilih Menu

    {cl.GREEN}[*]{cl.ENDC} {cl.WB} 1.{cl.ENDC} {cl.BLUE}Ongoing{cl.ENDC}
    {cl.GREEN}[*]{cl.ENDC} {cl.WB} 2.{cl.ENDC} {cl.BLUE}Search Nime{cl.ENDC}
    {cl.GREEN}[*]{cl.ENDC} {cl.WB} 3.{cl.ENDC} {cl.BLUE}Exit{cl.ENDC}
    """)
    menu = input(f'{cl.GREEN}【 Pilih Menu 】 ➤ {cl.ENDC}')

    if menu == '1':
        Otakudesu(menu)
        mulai_lagi()
    elif menu == '2':
        Otakudesu(menu)
        mulai_lagi()
    elif menu == '3':
        exit()
    else:
        print(cl.FAIL,'\nOpps input tidak dikenali !!',cl.ENDC)
        mulai_lagi()

def mulai_lagi():
        if (input(f'{cl.GREEN}\n【 Mulai Lagi [Y/t] 】 ➤ {cl.ENDC}')).lower() == 'y':
            main()
        else:
            exit()

def opsi_kembali():
    opsi = opsi = get_opsi()
    if opsi == '1':
        pass
    elif opsi == '2':
        main()
    elif opsi == '3':
        exit()
    else:
        print("Input tidak dikenal")
        opsi_kembali()

def get_opsi():
    print("""
Menu :
1. Lanjut
2. Kembali
3. Keluar
    """)
    opsi = input('Pilih Menu > ')
    return opsi


if __name__ == "__main__":
    main()