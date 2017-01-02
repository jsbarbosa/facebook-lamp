#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  facebook-friends.py
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

import json
import datetime
import requests
import numpy as np
import matplotlib.pyplot as plt
import urllib.request as urllib2

def request(url):
    """
    sends url request
    """
    
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True

        except Exception as e:
            print("Error %s: on %s %s" %(e, url, datetime.datetime.now()))

    return response.read().decode()
    
def getFacebookData(page_id, access_token):    
    """
    constructs the URL string
    """
    
    base = "https://graph.facebook.com/v2.8"
    node = "/" + page_id
    
    parameters = "?fields=posts{comments{from},reactions{name},sharedposts}"
    url = base + node + parameters + "&access_token=%s"%access_token
    data = json.loads(request(url))
    
    return data
    
def counter(users_likes, users_comments, posts):
    """
    counts the number of reactions and comments per user
    """
    
    for post in posts['data']:
        try: 
            reactions = post['reactions']
            while True:
                for reaction in reactions['data']:
                    name = reaction['name']
                    if name in users_likes: users_likes[name] += 1
                    else: users_likes[name] = 1
                try: reactions = requests.get(reactions['paging']['next']).json()
                except KeyError: break
        except KeyError:
            pass
        
        try:
            comments = post['comments']
            while True:
                for comment in comments['data']:
                    name = comment['from']['name']
                    if name in users_comments: users_comments[name] += 1
                    else: users_comments[name] = 1
                try: comments = comments.get(comments['paging']['next']).json()
                except: break
        except KeyError:
            pass
    return users_likes, users_comments
    
def unifier(users_likes, users_comments):
    """
    unifies and sorts the data
    """
    for name in users_likes:
        if not name in users_comments:
            users_comments[name] = 0

    for name in users_comments:
        if not name in users_likes:
            users_likes[name] = 0

    values = np.zeros((len(users_likes), 2))
    names = []

    for (i, name) in enumerate(users_likes):
        names.append(name)
        values[i] = [users_likes[name], users_comments[name]]

    pos = np.argsort(np.sum(values, axis = 1))
    return np.array(names)[pos], values[pos]

def plotter(names, values, fontsize = 8, alpha = 0.7, lw = 0, name = "Complete.pdf"):
    """
    plots the bar plot
    """
    N = len(names)
    x_axes = np.arange(N)
    max_y = np.sum(values[-1])
    delta = max_y/25

    fig, ax = plt.subplots(figsize=(N/4, 12))   
    rects1 = ax.bar(x_axes, values[:, 0], color = 'blue', alpha = alpha, align='center', lw = lw
                    , label = "Reactions")
    rects2 = ax.bar(x_axes, values[:, 1], color = 'red', alpha = alpha, align='center', lw = lw
                    , bottom = values[:, 0], label = "Comments")
     
    for (rect1, rect2) in zip(rects1, rects2):
        h1 = rect1.get_height()
        h2 = rect2.get_height()
        x = rect1.get_x() + rect1.get_width()/2.
        if h1 - delta > 0:
            ax.text(x, h1 - delta, "%d"%int(h1), ha = "center", va = "bottom", fontsize = fontsize)
        if h2 + h1 - delta > h1:
            ax.text(x, h2 + h1 - delta, "%d"%int(h2), ha = "center", va = "bottom", fontsize = fontsize)
        ax.text(x, h2 + h1 + delta, "%d"%(int(h2+h1)), color = "r", ha = "center", va = "bottom", fontsize = fontsize)
    
    ax.set_xlim(0, N)
    ax.yaxis.grid(True)
    ax.set_xticks(x_axes)  
    ax.set_ylim(0, max_y*1.2)
    plt.legend(loc="upper left")
    
    ax.set_xticklabels(names, fontsize = fontsize, rotation=90)
    plt.tight_layout()
    plt.savefig("Complete.png", dpi = 300)#,name)

def main():
    with open('access_token.txt', 'r') as f:
        access_token = f.readline()

    page_id = 'me'
    users_likes = {}
    users_comments = {}

    status = getFacebookData(page_id, access_token)['posts']

    i = 0
    while True:
        users_likes, users_comments = counter(users_likes, users_comments, status)
        try:
            status = requests.get(status['paging']['next']).json()
        except KeyError:
            break
        i += 1
        print("Current: %d"%(i*20))
        
    print("Unifying...")
    names, values = unifier(users_likes, users_comments)
    print("Plotting...")
    plotter(names, values)
    
if __name__ == "__main__":    
    main()



