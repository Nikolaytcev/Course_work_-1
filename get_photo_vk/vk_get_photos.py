# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 15:46:48 2022

@author: LocalAdmin
"""

import requests
import json
import time 
import os
from upload_ya_disk import upload_list_files



class PhotosFromVk:
    
    HOST = 'https://api.vk.com/method/'
    def __init__(self, TOKEN_vk, version):
        self.params = {
            'access_token': TOKEN_vk,
            'v': version}
        
    def __get_url_max_size_photo(self, sizes):
        height = [i['height'] for i in sizes]
        width = [i['width'] for i in sizes]
        for idx, i in enumerate(sizes):
            if i['height'] == max(height) and i['width'] == max(width):
                if max(height) != 0 and max(width) != 0:
                    return {'url': i['url'], 'height': i['height'], 'width': i['width'], 'type': i['type']}
                elif idx == len(sizes) - 1:
                    return {'url': i['url'], 'height': i['height'], 'width': i['width'], 'type': i['type']}
            
    def __write_json_file(self, data):
        os.chdir('../')
        with open('json-file.txt', 'w') as outline:
            json.dump(data, outline, indent=2)
        print('json-file.txt создан.')
    
    def get_photos_vk(self, id_vk=None):
        url = self.HOST + 'photos.get'
        photos_params = {'owner_id': id_vk,
                         'album_id': 'profile',
                         'photo_sizes': 1,
                         'extended': '1'}
        resp = requests.get(url, params={**self.params, **photos_params})
        if resp.status_code != 200:
            return resp.status_code
        else:
            resp = resp.json()
            profile_photos = []
            files_name = []
            for_writing = []
            for i in resp['response']['items']:
                name = str(i['likes']['count']) + '.jpg'
                info = self.__get_url_max_size_photo(i['sizes'])
                info_file = {}
                if name in files_name:
                    info_file['file_name'] = (name[:-4] + '_' + 
                                              time.ctime(i['date']).replace(' ', '_').replace(':', '_')) + '.jpg'
                    info_file['size'] = {'height': info['height'], 'width': info['width'], 'type': info['type']}
                    profile_photos.append({'file_name': (name[:-4] + '_' +
                                                     time.ctime(i['date']).replace(' ', '_').replace(':', '_'))+ '.jpg',
                                       'url': info['url']})
                else:
                    files_name.append(name)
                    info_file['file_name'] = name
                    info_file['size'] = {'height': info['height'], 'width': info['width'], 'type': info['type']}
                    profile_photos.append({'file_name': name,
                                       'url': info['url']})
            
                for_writing.append(info_file)
            self.__write_json_file(for_writing)
        return profile_photos
        
def main():
    TOKEN_vk = ''
    name_direction = 'Курсач' # Наименование папки в облаке
    count_photos = 5          # Количество скачиваемых фотографий
    TOKEN_yandex = ''
    id_vk = ''
    
    ph = PhotosFromVk(TOKEN_vk, '5.131')
    l = ph.get_photos_vk(id_vk)
    if l == 200:
        print(f'Ошибка {l}.')
    else:
        print('Загрузка файлов на диск:')
        upload_list_files(TOKEN_yandex, l, name_direction, count_photos)

if __name__ == '__main__':
    main()
    
    
            