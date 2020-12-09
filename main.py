import os
import random
import requests
from dotenv import load_dotenv

MAX_PAGES = 2394


def get_comic_from_xkcd(comic_filename):
    page_number = random.randrange(1, MAX_PAGES)
    url = f'https://xkcd.com/{page_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    if response.ok:
        response = response.json()
        picture = requests.get(response['img'])
        with open(comic_filename, 'wb') as file:
            file.write(picture.content)
        return response['alt']


def raise_vk_error(json_response):
    if 'error' in json_response:
        for pos in json_response['error']['request_params']:
            if pos['key'] == 'method':
                error_tgt = pos['value']
        error_msg = json_response['error']['error_msg']
        raise Exception(f'{error_tgt} ---> {error_msg}')


def upload_to_vk_server(token, group_id, comic_filename):
    payload = {
        'access_token': token,
        'v': '5.126',
        'group_id': group_id
        }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=payload)
    result = response.json()
    raise_vk_error(result)
    upload_url = result['response']['upload_url']

    with open(comic_filename, 'rb') as file:
        url = upload_url
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        result = response.json()

    return (result['photo'],
            result['server'],
            result['hash'])


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
    result = response.json()
    raise_vk_error(result)
    saved_photo = result['response'][0]
    return (saved_photo['owner_id'], saved_photo['id'])


def post_to_group_wall(token, group_id, owner_id, media_id, comic_title):
    payload = {
        'access_token': token,
        'v': '5.126',
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': comic_title
    }
    url = 'https://api.vk.com/method/wall.post'
    response = requests.post(url, params=payload)
    raise_vk_error(response.json())


def main():
    load_dotenv()
    token = os.getenv('VK_TOKEN')
    group_id = os.getenv('VK_GROUP_ID')
    comic_filename = 'comic.png'
    try:
        comic_title = get_comic_from_xkcd(comic_filename)
        photo, server, hashvalue = upload_to_vk_server(token, group_id,
                                                       comic_filename)
        owner_id, media_id = save_photo_to_wall(token, group_id, photo, server,
                                                hashvalue)
        post_to_group_wall(token, group_id, owner_id, media_id, comic_title)
    except Exception as error_msg:
        print(error_msg)
    finally:
        if os.path.exists(comic_filename):
            os.remove(comic_filename)


if __name__ == "__main__":
    main()
