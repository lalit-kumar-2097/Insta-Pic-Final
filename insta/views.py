import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
from django.conf import settings


#insta_loader imports:
import instaloader
import pandas as pd
from datetime import datetime
import hashlib
import os
import csv
import wget
import re

from django.utils.html import format_html, mark_safe

def convert_string_to_html_element(html_string):
    return mark_safe(format_html(html_string))



if not settings.configured:
    settings.configure()


def get_MD5(str):
    with open(str, 'rb') as f:
        data = f.read()
        md5hash = hashlib.md5(data).hexdigest()
    new_name = F'{md5hash}.jpg'
    print(new_name)
    return(new_name)


def display_images(request):
    if request.method == 'POST':
        # get image URLs from the POST request
        image_urls = request.POST.get('image_urls').split(',')
        print(image_urls)
        # fetch the images from the URLs
        images = []
        for url in image_urls:
            response = requests.get(url)
            image = response.content
            images.append(image)                    
        # images = b'images'
        # return the images as a JSON response
        return JsonResponse({'images': b'images'.decode('utf-8')}, safe=False)
    # render the initial template
    return render(request, 'index.html')


L = instaloader.Instaloader(download_videos=False)
SINCE = datetime(1990, 5, 10)
df = pd.DataFrame(columns=["post_id","type","MD5","URL"])
print(df)
# username = 'ashwathama532'
# password = 'hive@1234'
# L.login(username, password)

def instapic(request):
    if request.method == 'POST':
        post_ids = request.POST.get('instapic')
        post_ids = post_ids.strip()
        post_ids = post_ids.split(",")
        list_dict = []
        print(len(list_dict))
        for post_id in post_ids:
            image = 0
            video = 0
            print("\n  \n "+post_id)
            post = instaloader.Post.from_shortcode(L.context, shortcode= post_id)
            temp_json = {"post_id": post_id, "COUNT": [], "DATA": []}
            if post.typename == 'GraphImage':
                wget.download(post.url, out = 'resources/insta/resources/temp.jpg')
                MD5 = get_MD5('resources/insta/resources/temp.jpg').replace('.jpg','')
                new_name = 'resources/insta/resources/'+get_MD5('resources/insta/resources/temp.jpg')
                os.rename('resources/insta/resources/temp.jpg',new_name)
                element = '<img src="'+new_name+'" alt = ""></img>'
                element = convert_string_to_html_element(element)
                #file_entries, post_id, type= 'Image', MD5, URL = post.url, file_loc = new_name                
                temp_dict = {
                                "post_id": post_id,
                                "Type": "Image",
                                "MD5": MD5,
                                "URL": post.url,
                                'File': new_name,
                                'Element': element
                             }
                image+=1
                temp_json["DATA"].append(temp_dict)
            if post.typename == 'GraphSidecar':
                for node in post.get_sidecar_nodes():
                    if node.is_video == True:
                        video+=1
                        print("It's a video")
                        wget.download(node.video_url, out = 'resources/insta/resources/temp.mp4')
                        MD5 = get_MD5('resources/insta/resources/temp.mp4').replace('.jpg','')
                        new_name = 'resources/insta/resources/'+MD5+".mp4"
                        os.rename('resources/insta/resources/temp.mp4',new_name)
                        element = '<video src="'+new_name+'" controls></video>'
                        element = convert_string_to_html_element(element)
                        #file_entries, post_id, type= 'Image', MD5, URL = post.url, file_loc = new_name                
                        temp_dict = {
                                        "post_id": post_id,
                                        "Type": "Video",
                                        "MD5": MD5,
                                        "URL": node.video_url,
                                        'File': new_name,
                                        'Element': element
                                    }
                        temp_json["DATA"].append(temp_dict)
                    else:
                        print("It's a pic")
                        image+=1
                        wget.download(node.display_url, out = 'resources/insta/resources/temp.jpg')
                        MD5 = get_MD5('resources/insta/resources/temp.jpg').replace('.jpg','')
                        new_name = 'resources/insta/resources/'+get_MD5('resources/insta/resources/temp.jpg')
                        os.rename('resources/insta/resources/temp.jpg',new_name)
                        element = '<img src="'+new_name+'" alt = ""></img>'
                        element = convert_string_to_html_element(element)
                        #file_entries, post_id, type= 'Image', MD5, URL = post.url, file_loc = new_name                
                        temp_dict = {
                                        "post_id": post_id,
                                        "Type": "Image",
                                        "MD5": MD5,
                                        "URL": node.display_url,
                                        'File': new_name,
                                        'Element': element
                                    }
                        temp_json["DATA"].append(temp_dict)
            if post.is_video == True:
                video+=1
                wget.download(post.video_url, out = 'resources/insta/resources/temp.mp4')
                MD5 = get_MD5('resources/insta/resources/temp.mp4').replace('.jpg','')
                new_name = 'resources/insta/resources/'+MD5+".mp4"
                os.rename('resources/insta/resources/temp.mp4',new_name)
                element = '<video src="'+new_name+'" controls></video>'
                element = convert_string_to_html_element(element)
                #file_entries, post_id, type= 'Image', MD5, URL = post.url, file_loc = new_name                
                temp_dict = {
                                "post_id": post_id,
                                "Type": "Video",
                                "MD5": MD5,
                                "URL": post.url,
                                'File': new_name,
                                'Element': element
                             }
                temp_json["DATA"].append(temp_dict)  
            count_list = {"images": image,"videos": video}
            temp_json['COUNT'].append(count_list)       
            list_dict.append(temp_json)
            print(post_id)
            print(count_list)
        print(list_dict)
        data = {'data': list_dict}
        return render(request, 'my_json_page1.html',data)
    else:
        return render(request, "instapic.html")     


















