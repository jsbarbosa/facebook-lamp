import json
import requests
import urllib.request as urllib2

def request(url):
    """
    sends url request
    """
    
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)

    return response.read().decode()
    
def getFacebookData(page_id, access_token):    
    """
    constructs the URL string
    """
    
    base = "https://graph.facebook.com/v2.8"
    node = "/" + page_id
    
    parameters = "?fields=taggable_friends{name}"
    url = base + node + parameters + "&access_token=%s"%access_token
    data = json.loads(request(url))
    
    return data

def main():
    with open('access_token.txt', 'r') as f:
        access_token = f.readline()

    page_id = 'me'

    friends = getFacebookData(page_id, access_token)['taggable_friends']
    friend_list = []
    
    while True:
        for friend in friends['data']: friend_list.append(friend['name'])
        try:
            friends = requests.get(friends['paging']['next']).json()
        except KeyError:
            break
    with open('friends.txt', 'a') as f:
        for friend in friend_list: print(friend, file = f)
    
if __name__ == "__main__":    
    main()