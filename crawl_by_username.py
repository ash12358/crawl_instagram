import os
import re
import requests
import json
from lxml import etree
from urllib import parse

from utils import ctx

from blacklist import Blacklist

new_black = None
global_url = None

# base_path = '/Users/ash/Desktop/用户身份识别/images/'
# base_path = 'C:/Users/Administrator/Desktop/images/'
base_path = './images/'

img_url_texts = {}
# 更换用户数据字典
encoded_jsons = []
user_info = {}
PAT = re.compile(r'queryId:"(.+?)",', re.MULTILINE)
headers = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0",
    "Host": "www.instagram.com",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, sdch, br",
    "accept-language": "zh-CN,zh;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "Upgrade-Insecure-Requests": "1",
}

jso = {"id": "", "first": 12, "after": ""}

BASE_URL = "https://www.instagram.com"

NEXT_URL = 'https://www.instagram.com/graphql/query/?query_hash={0}&variables={1}'


# def reOpen(qq):
#     qq = requests.session()
#     temp_url = global_url
#     headers.update({'Referer': temp_url})
#     # res = qq.get(url=temp_url, headers=headers)
#
#     res = define_request(qq, temp_url, headers)
#     print('reopen ', res.status_code)
#     return qq

def define_request(qq, url, headers):
    ties = 10
    while ties > 0:
        try:
            res = qq.get(url=url, headers=headers, timeout=5)
            if res.status_code == 200:
                res.encoding = "utf-8"
                return res
        except:
            ties -= 1
            print('倒数第%d次尝试' % ties)
#             if (ties == 5 or ties == 1):
#                 qq = reOpen(qq)


def crawl_next(qq, html, query_id_url, rhx_gis, id, username):
    print('下一页')

    edges = html["user"]["edge_owner_to_timeline_media"]["edges"]
    end_cursor = \
        html["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
    has_next = \
        html["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]

    extract_from_edges(edges)

    # query_content = qq.get(BASE_URL + query_id_url[1])
    query_content = define_request(qq, BASE_URL + query_id_url[1], None)
    query_id_list = PAT.findall(query_content.text)

    jso["id"] = id
    jso["first"] = 12
    jso["after"] = end_cursor
    # 注意了这处dumps默认会出都自动在，逗号和冒号后面添加空格，导致了格式不符合
    text = json.dumps(jso, separators=(',', ':'))
    xhr_code = "{0}:{1}".format(rhx_gis, text)
    # print(xhr_code)
    # for query_hash in query_id_list:
    # query_hash = "472f257a40c653c64c666ce877d59d2b"
    query_hash = query_id_list[2]
    url = NEXT_URL.format(query_hash, parse.quote(text))
    # print(url)
    gis = ctx.call("get_gis", xhr_code)
    # 就是缺少了这个GIS参数
    headers.setdefault("X-Instagram-GIS", gis)
    headers.update({"X-Instagram-GIS": gis})

    # res = qq.get(url=url, headers=headers)
    res = define_request(qq, url, headers)

    try:
        html = json.loads(res.content.decode(), encoding='utf-8')

        if has_next and len(img_url_texts.keys()) < 200:
            crawl_next(qq, html['data'], query_id_url, rhx_gis, id, username)
        else:
            print('has_next', has_next)
            print('len,', len(img_url_texts.keys()))
            if len(img_url_texts.keys()) == 0:
                new_black.add_blackname(username)
    except:
        print('encoding error --------------')
        pass


def convert_text_to_a_line(text):
    texts = text.split('\n')
    text = ''
    for te in texts:
        text += te.strip()
        if len(te.strip()) > 0:
            text += ' '
    text = text[:-1]
    return text

def extract_from_edges(edges):

    # print('提取图片')
    # for edge in edges:
    #     if edge['node']['is_video'] == False:
    #         img_url = edge["node"]["display_url"]
    #         # img_url = convert_text_to_a_line(img_url)
    #         edges_for_text = edge['node']['edge_media_to_caption']['edges']
    #         text = ''
    #         if edges_for_text and len(edges_for_text) > 0:
    #             text = edges_for_text[0]['node']['text']
    #             text = convert_text_to_a_line(text)
    #         if len(img_url_texts.keys()) < 200:
    #             img_url_texts[img_url] = text
    #
    #         # print('phtot, save')
    #     else:
    #         # print('video, pass')
    #         pass

    # 直接将json数据保存下来
    encoded_json = json.dumps(edges)
    encoded_jsons.append(encoded_json)

    pass

def crawl_first(username):
    print('进入主页')
    qq = requests.session()
    query = username
    temp_url = BASE_URL + '/' + query + '/'
    global_url = temp_url
    headers.update({'Referer': temp_url})
    # res = qq.get(url=temp_url, headers=headers)

    print('请求res')
    res = define_request(qq, temp_url, headers)
    print(res.status_code)

    html = etree.HTML(res.content.decode())
    all_a_tags = html.xpath('//script[@type="text/javascript"]/text()')  # 图片数据源
    query_id_url = html.xpath('//script[@type="text/javascript"]/@src')  # query_id 作为内容加载

    js_data = None
    rhx_gis = None
    for a_tag in all_a_tags:
        if 'window._sharedData' in str(a_tag.strip()) and 'window._sharedData)' not in str(a_tag.strip()):
            data = a_tag.split('= {')[1][:-1]  # 获取json数据块
            try:
                js_data = json.loads('{' + data, encoding='utf-8')
                rhx_gis = js_data["rhx_gis"]
                id = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]
                edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"][
                    "edges"]
                extract_from_edges(edges)
                crawl_next(qq, js_data["entry_data"]["ProfilePage"][0]["graphql"], query_id_url, rhx_gis, id, username)
            except:
                print('encoding error ---------------')
                pass
    qq.close()

    pass


def is_crawled(username):
    path = base_path + username + '.txt'
    # print(path)
    if os.path.exists(path):
        return True
    else:
        return False



def save_to_txt(username):
    # if len(img_url_texts.keys()) > 0:
    #     path = base_path + username + '.txt'
    #     print('保存的路径：', path)
    #     try:
    #         with open(path, 'wb+') as f:
    #             for key in img_url_texts.keys():
    #                 f.write((key + '\n').encode('utf-8'))
    #                 # f.write(img_url_texts[key] + '\n')
    #                 f.write((img_url_texts[key] + '\n').encode('utf-8'))
    #         print('保存完毕')
    #     except:
    #         os.remove(path)

    # 保存到mongodb中，或是保存成txt

    pass


def crawl_by_username(username):
    global new_black
    new_black = Blacklist()
    if is_crawled(username):
        print(username, '已爬取')
        pass
    else:
        print('开始爬取', username)
        img_url_texts.clear()
        crawl_first(username)
        # save_to_txt(username)
        # 现在不保存到txt中，而是保存到mongodb中，所以需要将该用户的信息按照字典格式返回

        pass

    return new_black, encoded_jsons
    pass



if __name__ == '__main__':
    crawl_by_username('eric_r_miller')
    for key in img_url_texts.keys():
        print(key)
        print('------', img_url_texts[key])
    pass