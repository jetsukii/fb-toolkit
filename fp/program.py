from fp.modul import *

class login:
    def __init__(self):
        if '.cookies' in listdir('user'):
            self.__language({'cookie':open('user/.cookies', 'r').read()})
        else:
            system('clear')
            print(p +'Silahkan Login Menggunakan Cookies Akun Facebook Anda, Pastikan Untuk Mengingat Semua Data Akun Anda Untuk Berjaga jaga Jika Akun Terkena Sesi/Kunci.')
            self.__language({'cookie':input(p +'\nCookies: '+ h)})

    def __language(self, cookies):
        with r.Session() as ses:
            page = bs(ses.get('https://mbasic.facebook.com/language', cookies=cookies).text, 'html.parser')
            for form in page.find_all('form'):
                if 'Bahasa Indonesia' in str(form):
                    payload = {}
                    for require in form('input'):
                        payload[require.get('name')] = require.get('value')
                    self.__validate(cookies, ses.post('https://mbasic.facebook.com/'+ form['action'], data=payload, cookies=cookies).text)

    def __validate(self, cookies, html):
        if 'Keluar (' in str(html):
            open('user/.cookies', 'w').write(cookies['cookie'])
            try:
                req = r.get('https://www.facebook.com/adsmanager/manage/campaigns', cookies=cookies).text
                nex = r.get('https://www.facebook.com/adsmanager/manage/campaigns?act='+ re.search('act=(.*?)&nav_source',str(req)).group(1) +'&nav_source', cookies=cookies).text
                open('user/.token', 'w').write(re.search('accessToken="(.*?)"',str(nex)).group(1))
            except Exception as e:exit(m +'Maaf Gagal Mengambil Token')
        else:
            system('rm user/.cookies')
            exit(m +'Maaf Cookies Anda Tidak Valid')

def userData():
    __cookies = {'cookie':open('user/.cookies', 'r').read()}
    html = bs(r.get('https://mbasic.facebook.com/me', cookies=__cookies).text, 'html.parser')
    __name = html.find('title').text
    log = html.find('a', string='Log Aktivitas')
    if log is None:
        exit(m +' Mungkin Akun Anda Terkena Checkpoint')
    else:
        __id = log['href'].split('/')[1]
    return __name, __id
