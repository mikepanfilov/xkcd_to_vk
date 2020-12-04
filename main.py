import os
import random
import requests
from dotenv import load_dotenv


def get_comic_from_xkcd(comic_filename):
    page_number = random.randrange(1, 2394)
    url = f'https://xkcd.com/{page_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    picture = requests.get(comic['img'])
    with open(comic_filename, 'wb') as file:
        file.write(picture.content)
    return comic['alt']


def upload_to_vk_server(token, group_id, comic_filename):
    payload = {
        'access_token': token,
        'v': '5.126',
        'group_id': group_id
        }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']

    with open(comic_filename, 'rb') as file:
        url = upload_url
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()

    return (response.json()['photo'],
            response.json()['server'],
            response.json()['hash'])


def save_photo_to_wall(token, group_id, photo, server, hashvalue):
    payload = {
        'access_token': token,
        'v': '5.126',
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': hashvalue
        }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, params=payload)
    response.raise_for_status()
    saved_photo = response.json()['response'][0]
    return (saved_photo['owner_id'], saved_photo['id'])


def post_to_group_wall(token, group_id, owner_id, media_id, comic_title):
    payload = {
        'access_token': token,
        'v': '5.126',
        'owner_id': '-' + group_id,
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': comic_title
    }
    url = 'https://api.vk.com/method/wall.post'
    response = requests.post(url, params=payload)
    response.raise_for_status()
    print(response.json())


def main():
    load_dotenv()
    token = os.getenv('VK_TOKEN')
    group_id = os.getenv('VK_GROUP_ID')
    comic_filename = 'comic.png'
    comic_title = get_comic_from_xkcd(comic_filename)
    photo, server, hashvalue = upload_to_vk_server(token, group_id,
                                                   comic_filename)
    owner_id, media_id = save_photo_to_wall(token, group_id, photo, server,
                                            hashvalue)
    post_to_group_wall(token, group_id, owner_id, media_id, comic_title)
    os.remove(comic_filename)


if __name__ == "__main__":
    main()
