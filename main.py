
from crawl_by_username import crawl_by_username
from blacklist import Blacklist
from config import *
import pymongo

user_id_usernames = []

start = False
start_username = 'elwaslibet'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def check(username):
    global start
    if start == True:
        return
    else:
        if (username == start_username):
            start = True
    pass

# file = 'C:/Users/Administrator/Desktop/user_id_usernames.txt'


file = './user_id_usernames.txt'


def save_to_mongo(data):
    if not db[MONGO_TABLE].find(data):
        db[MONGO_TABLE].insert(data)
    else:
        print('已爬取')

if __name__ == '__main__':

    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.split('|')[1] != '----':
                user_id_usernames.append(line)
    total = len(user_id_usernames)

    # usernames = usernames[:]

    current = 1
    for user_id_username in user_id_usernames:
        data = {}
        print('total:', total, 'current:', current)
        current += 1
        user_id, username = user_id_username.split('|')
        check(username)
        if start:
            blacklist = Blacklist()
            blacklist.load_data()

            if username in blacklist.get_data():
                print(username, '黑名单')
            else:
                new_black, encoded_jsons = crawl_by_username(username)
                if len(encoded_jsons) > 0:
                    data[user_id] = encoded_jsons
                    save_to_mongo(data)
                if len(new_black.get_data()) > 0:
                    for blackname in new_black.get_data():
                        blacklist.add_blackname(username)
                    blacklist.save_data()
                    print('更新新名单')
        else:
            print('还未到开始点')


    pass