import random
import string
import threading

import requests

INVALID_IMG = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xa1\x00\x00\x00Q\x01\x03\x00\x00\x00\x80\rT\xec\x00\x00\x00\x06PLTE"""\xff\xff\xff^\x87 1\x00\x00\x01\xacIDATx^\xed\xd0/o\xdb@\x18\x06\xf0\xd7Q\x96\xb9\xcc6\xacn\xd5\xe5@j\x10\x90T\x01\x05\xd3t\x93n\xcb\x81HUY`@A\xa0\x9d\x91\x8d\x9d\x07\x96;\xb2\xe8\x86ZRU%\xa5\xfb\nEI\x99?\x82S4\x98\xb1\x90I\xbb\x9c\x9b\xbf3\x19h\xb7I{$\x93\x9f^=:?\xf0\xf7\xc6\xf9\x01@\x7f\xe5\xaa\x81\x02\xedeo\xce\xa34\x93\xf7\xf8\xf8f\xad\xda{{\xa6\x9a\x9e\n0\x9b\x88\x95\xfa\x1ec{\xbew\x1a\xe0\xb2\xdc\xd0\x19c\x1f\xfc\x99\xd1\x97\xa3\r\x05\xc6\x94\x0fF\x99\x84\xad\x86\x8b\xa6W\rpg\xa3\xc1\xcb\x18\xeb\xa7\x19\x9ef\xad!l\xc7\x03\\\xf0\x87\x19Px\x84p\x80\x92\x05\n\xae\xb3R\xbaV\xb0zS\xd1\x08}\xfb\x9a\xee\x1fGQ\x1de\x83\xf0\x9d0:Q\x9a\x10~\xd7\xa81)\x8f\x08U\\\x81\x89\x94\x9a`\xae<\xc2\xa4 \x0bM\x16:\x92\xfa\x15\xb2:\x8f\x8c\xceelo]\x8dKV\x85k4\xe1{Vm\xafj\x98\x06IV\xbd\xc3\xca\x08\xa1\xbeL\x0f\xcc\x1b\x08\xea\r\xc28\x9fS\xe4\xa3\xedD\xe4\xa3=M\x1c\xfb\xe5\xf1\x81\xd2\xa5\xaf\xd5Yj\xfc\x1a=\x1b:\xa8\xde\x8a\xae\xee\x0f}\xd4m[U\t\xa9\xf0\x84\x1cu\xe4m\x10jr\xc6\x85U\x07\x97\x8d.\x86\xf4\xa9.\xb1\xa5\xa2\\\xe7\xe2{[\x1f\xb0\x93\x07-\xe5*\x12\x9fk\xc28\xe4J\xacvd\xd2P\xba\xf6\xd0\x1b\x9b\x86\xb6\x83H+\x12\xe9\'\xbd\xdfmo\xadW\x86\xa2\xbc\x87?\x9d\xff\x11\xbfq\xfby|=\x1d\xbf\x10;\xaa\xc2\xeb\x8f\xe1\x17Z\xa0n\x81\x16\xde\x1e^\xaaq\xb0\xab\xe0\x16\xbe\xed9\xfc\xf3\xf9\t\x93\x80\x88\xce\xd7u"\xb2\x00\x00\x00\x00IEND\xaeB`\x82'
ID_LEN = 7


def get_html(id_url):
    url = f"https://i.imgur.com/{id_url}.png"

    headers = {
        'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200 and response.content != INVALID_IMG:
        return response.status_code, response.content
    else:
        return response.status_code, -1


def save(binary_data, img_id):
    with open(f'IMGs/{img_id}.png', 'wb') as f:
        f.write(binary_data)
    f.close()


def main():
    all_strings = string.ascii_lowercase + string.ascii_uppercase + string.digits
    while True:
        random_id = ''.join([random.choice(all_strings) for _ in range(ID_LEN)])
        video_stats = get_html(random_id)
        if random_id not in open('invalid.txt', 'r').read():
            if video_stats[1] != -1:
                print(f'VALID: https://i.imgur.com/{random_id}.png')
                save(video_stats[1], random_id)

            else:
                if video_stats[0] != 404 and video_stats[0] != 200:
                    print('Something Happened!')
                    print(f'id: {random_id} code: {video_stats[0]}')

                with open(f'invalid.txt', 'a', encoding='utf-8') as f:
                    f.writelines(f'{random_id}\n')
                f.close()

if __name__ == '__main__':
    n = int(input('Threads: '))
    threads = []
    for i in range(n):
        t = threading.Thread(target=main)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()
