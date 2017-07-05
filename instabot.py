import requests,urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

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
            print 'Caption is : %s' % (caption)
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
            print 'Caption is : %s' % (caption)
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print 'Image is downloaded'
        else:
            print 'Post does not exist'
    else:
        print 'Status code other than 200 recieved'


#Function to get the ID of the recent post of a user by username

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s' % (user_id,APP_ACCESS_TOKEN))
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'No recent post of the user'
            exit()
    else:
        print 'Status code other than 200 recieved!!!'
        exit()



#Function to like post of a user

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)

    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {'access_token': APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url,payload).json()

    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!!!'
    else:
        print 'Your like was Unsuccessful...Please try again!!!'


#Function to make a comment on the recent post of the user

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input('Enter comment:')
    payload = {'access_token': APP_ACCESS_TOKEN, 'text' : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.get(request_url,payload).json()

    if make_comment['meta']['code'] == 200:
        print 'Successfully added a new comment'
    else:
        print 'Unable to add comment....Try again!!!'


#function to delete negative comments

def delete_negative_comments(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] ==200:
        if len(comment_info['data']):
            for x in range(0,len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiments.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id,comment_id,APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url)

                    if delete_info['meta']['code'] == 200:
                        print 'Negative comment successfully deleted'
                    else:
                        print 'Unable to delete comment'
                else:
                    print 'No negative comment'
        else:
            print 'There are no existing comments on the post'
    else:
        print 'Status code other than 200 recieved'


#Function to start instabot

def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'What do you wanna do???'
        print 'Here are your options:'
        print '1.Get your own details\n'
        print '2.Get details of a user by username\n'
        print '3.Get your own recent post\n'
        print '4.Get recent post of a user by username'
        print '5.Like the recent post of a user'
        print '6.Make a comment on the recent post of a user'
        print '7.Delete the negative comments on the post'
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
        elif choice == '5':
            insta_username = raw_input("Enter the name of the user: ")
            like_a_post(insta_username)
        elif choice == '6':
            insta_username = raw_input("Enter the name of the user: ")
            post_a_comment(insta_username)
        elif choice == '7':
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comments(insta_username)
        elif choice == 'e':
            exit()
        else:
            print "You have not entered a correct choice"

start_bot()