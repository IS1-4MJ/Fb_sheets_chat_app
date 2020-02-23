# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 13:49:42 2020

@author: josep
"""

import fbchat
import fbchat.models as models
from time import sleep

# User log in credentials
credentials = (user_email, password)
groupName = 'Meeeeeeeet Some Balls'

# Create an emulated facebook client instance
#client = fbchat.Client(*credentials)

# Whenever the client fails to log in or is logged out,
# Use this.
#if not client.isLoggedIn():
#    client.login(*credentials)


class Chat_api_augmented:
    def __init__(self, credentials):
        self.__client = fbchat.Client(*credentials)
        self.__client_url = None
    def send_blast_message_to_group(self, group, message):
        # NOT WORKING. TODO: FIX
        for uid in group.participants:
            users = self.__client(*self.__client.searchForUsers())  
            for user in users:
                sleep(.1)
                print(user.first_name)
            self.send_message_to_person_uid(uid, message)
    
    def send_message_to_person_uid(self, uid, message):
        self.__client.send(models.Message(text=message), thread_id = uid,
                      thread_type = models.ThreadType.USER)
    def send_message_to_person(self, user, message):
        self.__client.send(models.Message(text=message), thread_id = user.uid,
                      thread_type = models.ThreadType.USER)
        
    def find_friend_with_name(self, friend_name):
        users = self.__client.searchForUsers(friend_name)
        friends = []
        for user in users:
            if user.is_friend:
                friends.append(user)
        return friends
    
    def find_groups_with_participation(self, groupName):
        # NOT WORKING. TODO: FIX
        groups = self.__client.searchForGroups(groupName)
        participating_groups = []
        for group in groups:
            if self.__client.uid in group.participants:
                participating_groups.append(group)
        return participating_groups
    
    def logout(self):
        self.__client.logout()
        
augmented = Chat_api_augmented(credentials)
friends = augmented.find_friend_with_name('Ana Verulidze')
sleep(.5)
for friend in friends:
    print(friend.uid)
    augmented.send_message_to_person(friend, 'Wanna meat me in the back for some balls?')
sleep(.5)


groups = augmented.find_groups_with_participation(groupName)
for group in groups:
    augmented.send_blast_message_to_group(group, 'YOOOOOOOLOOOOOOO')
augmented.logout()



'''
                
        
    

# Find a group specified by group name
group = fbchat.searchForGroups(groupName)
# And make sure the user is in the group


# Use this whenever the client must be logged out.
client.logout()
'''
