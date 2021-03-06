import os
import requests
from bs4 import BeautifulSoup

params = {
    'showType': '3',
    'sortId': '3'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74',
    'Cookie': '__mta=140989325.1604936058413.1613904374936.1613905420497.19; '
              '_lxsdk_cuid=175ada4c5c4c8-041e936df9cb2c-7f677c65-144000-175ada4c5c5c8; '
              'uuid_n_v=v1; uuid=EF0ABDE0740111EBB1AE3B87C7DEAC0D6A8D2D25B56E480CA7B9019391534E77; '
              '_lxsdk=EF0ABDE0740111EBB1AE3B87C7DEAC0D6A8D2D25B56E480CA7B9019391534E77; '
              '_csrf=5dd1fc58971374bca0c60d8138c4fb565bf08ccdf44b86c3a493bfe64d9869ff; '
              'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1613896013,1613904313,1613904563,1614067768; '
              '_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; '
              'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1614069452; '
              '__mta=140989325.1604936058413.1613905420497.1614069452821.20; '
              '_lxsdk_s=177cdef9ab7-b52-d1d-0a%7C%7C41'
}
BASE_URL = 'https://maoyan.com/films'


def get_html(url, offset):
    params['offset'] = offset * 30
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        html = response.text
        return html
    else:
        return False


def get_details(url, offset):
    html = get_html(url=url, offset=offset)
    soup = BeautifulSoup(html, 'lxml')
    imgs = soup.find_all(name='img', attrs={'class': 'movie-hover-img'})
    # print(imgs)
    for img in imgs:
        # print(img['src'], img['alt'])
        yield {
            'movie_name': img['alt'],
            'img_src': img['src']
        }


if __name__ == '__main__':
    # html = get_html(BASE_URL, 0)
    # print(html)
    get_details(BASE_URL, 0)



