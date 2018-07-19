
from crawl_by_username import crawl_by_username
from blacklist import Blacklist

usernames = []

start = False
start_username = 'elwaslibet'


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


if __name__ == '__main__':

    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            username = line.strip().split('|')[1]
            usernames.append(username)
    total = len(usernames)

    # usernames = usernames[:]



    current = 1
    for username in usernames:
        print('total:', total, 'current:', current)
        current += 1
        if username != '----':

            check(username)
            if start:
                blacklist = Blacklist()
                blacklist.load_data()

                if username in blacklist.get_data():
                    print(username, '黑名单')
                else:
                    new_black = crawl_by_username(username)
                    if len(new_black.get_data()) > 0:
                        for blackname in new_black.get_data():
                            blacklist.add_blackname(username)
                        blacklist.save_data()
                        print('更新新名单')
            else:
                print('还未到开始点')


    pass