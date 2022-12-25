# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 20:08:22 2022

@author: LocalAdmin
"""
import requests
from tqdm import tqdm

class YaUploader:
    
    HOST = 'https://cloud-api.yandex.net/'
    
    def __init__(self, token: str):
        self.token = token
        
    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
            }
    
    def create_directory(self, file_path):
        url = self.HOST + 'v1/disk/resources'
        res = requests.put(f'{url}?path={file_path}', headers=self._get_headers())
        return res.status_code
    
    def upload(self, file_url, file_name, name_dir):
        url = self.HOST + 'v1/disk/resources/upload/'
        params = {'path': f'/{name_dir}/{file_name}', 'url': file_url}
        resp = requests.post(url, headers=self._get_headers(), params=params)
        return resp.status_code
       
          
def upload_list_files(token, pictures, name_dir='Курсач', count_photos=5):
    uploader = YaUploader(token)
    res_dir = uploader.create_directory(name_dir)
    if res_dir == 201 or res_dir == 409:
        if len(pictures) >= count_photos:
            i = count_photos
        else:
            i = len(pictures)
        
        for i in tqdm(range(i)):
            uploader.upload(pictures[i]['url'], pictures[i]['file_name'], name_dir)
        print('\nФайлы загружены!')
    else:
        print('Файлы не загружены.')

    
    

    
    
    
    
   