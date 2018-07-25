from download_imgs import *

def get_user_id_names():
    with open('./user_id_usernames.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        user_id_names = [line.strip().split('|') for line in lines]
    return user_id_names


if __name__ == '__main__':
    user_id_names = get_user_id_names()
    start_point = 63
    total = len(user_id_names)
    cur = start_point

    for user_id, username in user_id_names[start_point:]:
        print('total:', total, 'current:', cur)

        if username != '----':
            print('正在爬取', username)
            start(user_id, username)
        cur += 1
    pass