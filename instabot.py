import requests,urllib

APP_ACCESS_TOKEN = '1424263315.eea5f47.b72ecf57f66646a38a5e0e81e3747d48'
BASE_URL = 'https://api.instagram.com/v1/'


#Fumction to get your own info

def self_info():
    request_url = (BASE_URL+"users/self/?access_token=%s")%(APP_ACCESS_TOKEN)
    print 'GET request url: %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


#function to get id of a user by username

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


#Function to get the information about user by username

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


#Function to get your recent post

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print 'your image has been downloaded'
            caption = own_media['data'][0]['caption']['text']
            print caption
        else:
            print 'Post does not exit!!'
    else:
        print 'Status code other than 200 recieved!!!'


#function to get the recent post of a user by username

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist...Please enter a valid username!!!'
        exit()
    request_url = (BASE_URL+'users/%s/media/recent/?access_token=%s') % (user_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            caption = user_media['data'][0]['caption']['text']
            print caption
        else:
            print 'Post does not exist'
    else:
        print 'Status code other than 200 recieved'





#Function to start instabot

def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print '1.Get your own details\n'
        print '2.Get details of a user by username\n'
        print '3.Get your own recent post\n'
        print '4.Get recent post of a user by username'
        print 'e.Exit'

        choice = raw_input("Enter you choice: ")
        if choice == '1':
            self_info()
        elif choice == '2':
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == '3':
            get_own_post()
        elif choice == '4':
            insta_username = raw_input("Enter the name of the user: ")
            get_user_post(insta_username)
        elif choice == 'e':
            exit()
        else:
            print "You have not entered a correct choice"

start_bot()