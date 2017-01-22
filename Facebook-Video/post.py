#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  facebook-post.py
#  
#  Copyright 2016 Juan Barbosa <juan@Lenovo-U410>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import facebook
import requests
from datetime import datetime

def main():
    with open('access_token.txt', 'r') as f:
        access_token = f.readline()
    
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    message = """print('Hello world!'), uploaded at %s

Gracias por todo padre
"""%time

    url = 'https://graph-video.facebook.com/me/videos?access_token=' + access_token
    path = "wood.mp4"
    files = {'file':open(path,'rb')}
    payload = {'name': 'Blender Video', 'description': message}

    answer = requests.post(url, files=files, data=payload).text
    print(answer)

if __name__ == "__main__":
    main()
