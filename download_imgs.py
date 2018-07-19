import requests
import re
import os
import shutil
import time
import random

base_path = '/Users/ash/Desktop/用户身份识别/images/'
img_url_texts = {}
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
    file_txt = base_path + username + '.txt'
    if os.path.exists(file_txt):
        return True
    else:
        return False


def is_downloaded(username):
    file_txt = base_path + username + '.txt'
    folder = base_path + username + '/'
    if os.path.exists(file_txt) and os.path.exists(folder):
        return True
    else:
        return False


def create_folder(username):
    folder = base_path + username + '/'
    if not os.path.exists(folder):
        os.mkdir(folder)


def delete_folder(username):
    folder = base_path + username + '/'
    # os.rmdir(folder)
    if os.path.exists(folder):
        shutil.rmtree(folder)


def load_data(username):
    img_url_texts.clear()
    if is_crawled(username):
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
        pass
    else:
        print('user:', username, '还未获取图片链接')
        pass


def save_as_jpg(username, filename, res):
    path = base_path + username + '/'
    file = path + filename + '.jpg'
    with open(file, 'wb') as f:
        f.write(res.content)


def get_res(ss, url, header):
    res = define_request(ss, url, header)
    return res


def exist_jpg(username, filename):
    file = base_path + username + '/' + filename + '.jpg'
    if os.path.exists(file):
        return True
    else:
        return False


def download_imgs(username):

    create_folder(username)

    ss = requests.session()
    temp_url = BASE_URL + '/' + username + '/'
    header = {
        "Referer": temp_url,
        "Origin": "https://www.instagram.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/60.0.3112.113 Safari/537.36",
        'Connection': 'keep-alive'
    }
    pp = define_request(ss, temp_url, header)

    img_urls = img_url_texts.keys()
    count = 0
    for img_url in img_urls:
        if '\n' in img_url:
            img_url = img_url[:-1]
        filename = img_url[-15:-4]
        if not exist_jpg(username, filename):
            res = get_res(ss, img_url, header)
            save_as_jpg(username, filename, res)
            count += 1

        if count % 100 == random.randrange(20, 50):  # 请求超过20-50次，就重置一下session，防止被远程服务器关闭
            ss.close()
            ss = requests.session()
            pp = define_request(ss, temp_url, header)



if __name__ == '__main__':

    # create_folder('asdf')
    # delete_folder('asdf')
    # load_data('Angelababyct')
    # for key in img_url_texts.keys():
    #     print(key)
    #     print('----', img_url_texts[key])
    save_as_jpg('Ang', 'aaa', None)
    pass