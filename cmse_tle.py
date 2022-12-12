import requests
from lxml import etree
from datetime import datetime,timedelta

t0 = datetime.fromisoformat('2022-02-11')
t1 = datetime.now()
(t1-t0).days

css_tle = requests.session()
css_url = 'http://www.cmse.gov.cn/was5/web/search'

params = {
    'channelid': '228160',
    'docreltime': '2022.02.11',
}

tle_data=[]
for i in range((t1-t0).days):
    t = t0+timedelta(days=i)
    params['docreltime'] = t.strftime('%Y.%m.%d')
    exception = ''
    for _ in range(5):
        try:
            r_tle = css_tle.get(css_url, params=params, timeout=10).text
            break
        except Exception as err:
            print('Retry!')
            exception = err
    if exception:
        print(exception)
    else:
        if '48274U' in r_tle:
            tle_html = etree.HTML(r_tle)
            for tle_html in tle_html.xpath("//font"): 
                tle_data.append(tle_html.text.replace('\xa0',' '))
        else:
            print(params['docreltime'], r_tle)

with open('cmse_css_tle.txt', 'w') as fp:
    for tle in tle_data:
        fp.write(f'{tle}\n')
