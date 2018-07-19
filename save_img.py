import os
import requests
import time
import re

base_path = '/Users/ash/Desktop/用户身份识别/images/'
img_url_texts = {}

PAT = re.compile(r'queryId:"(\d*)?"', re.MULTILINE)
headers = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Host": "www.instagram.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, sdch, br",
    "accept-language": "zh-CN,zh;q=0.8",
    "X-Instragram-AJAX": "1",
    "X-Requested-With": "XMLHttpRequest",
    "Upgrade-Insecure-Requests": "1",
}

jso = {"id": "", "first": 12, "after": ""}

BASE_URL = "https://www.instagram.com"

def define_request(qq, url, headers):
    ties = 10
    while ties > 0:
        try:
            res = qq.get(url=url, headers=headers)
            if res.status_code == 200:

                return res
        except:
            ties -= 1
            time.sleep(2)
            print('倒数第%d次尝试' % ties)


def is_crawled(username):
    path = base_path + username + '.txt'
    folder = base_path + username + '/'
    # print(path)
    if os.path.exists(path) and os.path.exists(folder):
        return True
    else:
        return False


def full_dict(username):
    path = base_path + username + '.txt'

    with open(path, 'r') as f:
        lines = f.readlines()
        flag = 1
        for line in lines:
            if flag == 1:
                img_url = line
                flag *= -1
            else:
                text = line
                flag *= -1
                img_url_texts[img_url] = text

    # for key in img_url_texts.keys():
    #     print(key)
    #     print('-----', img_url_texts[key])
    # print(len(img_url_texts.keys()))





def download_img(username):
    # print('=======')
    ss = requests.session()
    temp_url = BASE_URL + '/' + username + '/'
    folder = username.replace('.', '-')

    header = {
        "Referer": temp_url,
        "Origin": "https://www.instagram.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/60.0.3112.113 Safari/537.36",
        'Connection': 'keep-alive'
    }

    # pp = define_request(ss, temp_url, header)
    # print('=====')
    # print(pp.status_code)

    img_urls = img_url_texts.keys()

    for img_url in img_urls:
        if '\n' in img_url:
            img_url = img_url[:-1]
        print(img_url)
        # res = define_request(ss, img_url, header)
        # print(res.status_code)
        # save_to_jpg(username, res)

    pass

def save_img(username):

    # print(is_crawled(username))

    if is_crawled(username):
        pass
    else:
        full_dict(username)
        download_img(username)

    pass


if __name__ == '__main__':
    save_img('Angelababyct')
    pass