# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:29:09 2020

@author: josep
"""

from pandas import DataFrame
import fbchat
import fbchat.models as models
from time import sleep

credentials = ('ejnislam18@gmail.com','Jello123!')

class Chat_api_augmented:
    def __init__(self, credentials):
        self.__client = fbchat.Client(*credentials)
        self.__client_url = None
    
    def client_id(self):
        return self.__client.uid
    
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

    def read_last_n_messages_uid(self, uid, n):
        return self.__client.fetchThreadMessages(uid, limit=n)

    # Read the last n messages from a conversation.
    def read_last_n_messages(self, thing_name, n):
        thing_with_names = self.__find_friend_with_name(thing_name)
        if len(thing_with_names) >1:
            raise AssertionError('Too many friends with name:', thing_name)
            return (thing_name, ['NO.','BAD.', 'U have',' 2+ things',' with that',' name'])
        friend = thing_with_names[0]
        return (friend.first_name + ' ' + friend.last_name,self.__client.fetchThreadMessages(friend.uid, limit=n))
        
    def logout(self):
        self.__client.logout()
        
# The purpose of this class is to keep users active so we don't have to constantly
# Search for them, and push differences associated with users out to facebook.
class Facebook_to_Pandas_and_Back:
    def __init__(self, credentials, names=[]):
        self._client = Chat_api_augmented(credentials)
        self.load_names(names)
    
    # Add all the users 
    # make a self._users = {name: userThread} dictionary object to handle
    # User message interaction
    def load_names(self, names): # Reload names every time
        self._users = {}
        for name in names:
            try:
                friends = self._client.find_friend_with_name(name)
                if len(friends) > 1:
                    print('too many friends with name: ' + name)
                    raise AssertionError('too many friend with name: ' + name)
                self._users[name] = friends[0]
            except AssertionError:
                pass
    
    '''
    Reads last n messages between all loaded users
    Takes:
        n = number of messages between people to display
    Returns:
        dictionary in {user: [WHOSENTIT, message_text]} format
    '''
    # Read the last n messages between loaded users (labelled client-other)
    def read_last_messages(self, n):
        last_messages = dict()
        for name, thread in self._users.items():
            messages = self._client.read_last_n_messages_uid(thread.uid, n)
            content_author_pairs = [[message.author, message.text
                                     ] for message in messages]
            # First pass: Label who sent each message
            for index, pair in enumerate(content_author_pairs):
                if pair[0] == self._client.client_id():
                    content_author_pairs[index] = ['CLIENT'] + pair[1]
                else:
                    content_author_pairs[index] = ['OTHER'] + pair[1]

            last_messages[name] = content_author_pairs
        return last_messages
            
    '''
    posts given new messages to facebook.
    Takes: 
        new_msg_dataframe: Pandas dataframe in {userName: [msg1out, msg2out, ..., msgNout]}
                            format. 
    Returns:
        boolean success of the message posting.
    '''
    def post_given_messages(self, new_msg_dataframe):        
        active_user_threads = self._users.keys()
        assert len(active_user_threads) == len(new_msg_dataframe.loc[0]), \
        "Cannot post " + str(len(new_msg_dataframe.loc[0])) + \
        " convo threads to " + str(len(active_user_threads)) + ". Load names again?"
        
        for name in new_msg_dataframe.loc[0]:
            if name in active_user_threads:
                thread = self._users[name]
                for new_msg_out in new_msg_dataframe[name]:
                    try:
                        self._client.send_message_to_person_uid(thread.uid, new_msg_out)
                    except:
                        return False
        return True # We at least attempted to send all the messages. 

'''
HELPER FUNCTIONS
'''

'''
Returns a list of new client message texts to send to facebook
Takes:
    The old list of client message texts from past push to google sheet
    The returned client messages texts from the google sheet 
Returns:
    list of new client message texts to send to facebook
'''
def get_new_client_messages_out(past_client_msgs, current_client_msgs):
    # Since the current client msgs are the ones that are changing, 
    # we know if we backtrack the client messages until we encounter 
    # past client messages, we have exposed all the new client messages
    if len(past_client_msgs) == len(current_client_msgs): # The length must be different if new msg because the user interaction field is longer tha nthe return field
        return []
    
    new_but_backwards = []
    backtrack_index = -1
    last_past_client_msg = past_client_msgs[-1]
    last_current_client_msg = current_client_msgs[backtrack_index]
    while last_current_client_msg != last_past_client_msg:
        new_but_backwards.append(last_current_client_msg)
        backtrack_index -= 1
    return new_but_backwards[::-1]

def get_client_messages_from_google_sheet(all_messages):
    return all_messages[::4]

'''
Gets message data from the google sheet we're working on in 
    dataFrame = {userName: [CLIENTMSG, "", OTHERMSG, "", CLIENTMSG, ...,
                                "", CLIENTMSG/OTHERMSG]} format
'''
def get_data_from_google_sheet():
    return DataFrame()

'''
Sends message data to the google sheet we're working on in 
    dataFrame = {userName: [CLIENTMSG, "", OTHERMSG, "", CLIENTMSG, ...,
                                "", CLIENTMSG/OTHERMSG]} format
'''
def send_data_to_google_sheet(message_data):
    succeeded = True
    return succeeded

'''
Gets message data from facebook in
    dataFrame = {userName: [CLIENTMSG, OTHERMSG, CLIENTMSG, ..., 
                            CLIENTMSG/OTHERMSG]} format
'''
def get_messages_from_facebook():
    return DataFrame()

'''
Sends message data to facebook in
    dataFrame = {userName: [CLIENTMSG, CLIENTMSG, ..., CLIENTMSG]} format
'''
def send_messages_to_facebook(dataFrame_messages_to_send_to_facebook):
    
    
    succeeded = True
    return succeeded

'''
Processes message data from google sheet format to facebook message format
and sends message data out to facebook
'''
def get_messages_from_google_sheet_and_send_to_facebook(original_sheet):
    '''
    google_sheets_data = {userName: [CLIENTMSG, "", OTHERMSG, "", CLIENTMSG, ...,
                                "", CLIENTMSG/OTHERMSG]} format'''
    google_sheets_data = get_data_from_google_sheet()
    
    '''
    Sends message data to facebook in
    dataFrame = {userName: [CLIENTMSG, CLIENTMSG, ..., CLIENTMSG]} format
    '''
    facebook_sending_data = dict()
    # I'm just going to add all the new client messages the facebook_sending_data
    # if there is a new user. I will just delete the new user from the google sheets data
    # after I add them to the facebook_sending_data and proceed through the
    # rest of the data normally after that.
    old_names = original_sheet.iloc[0]
    for name in list(google_sheets_data.iloc[0]): #Check to see if there is a new user
        if name not in old_names: # Then there is a new user. Add all the new client messages to the user and delete the new user from the google sheets data
            facebook_sending_data[name] = get_client_messages_from_google_sheet(google_sheets_data[name])
            #for clientMsgIndex in range(0, len(google_sheets_data[name]), 4):
            #    facebook_sending_data[name].append()
        google_sheets_data.drop(columns=[name])
    
    # If a user has been removed, the user's connection will be refreshed away
    # automatically.ju
    for userName in google_sheets_data.iloc[0]:
        facebook_sending_data[userName] = [] # only gonna send back the new messages
        new_msgs = get_new_client_messages_out(get_client_messages_from_google_sheet(original_sheet[userName]),
                                               get_client_messages_from_google_sheet(google_sheets_data[userName])) # This gives back the new messages
        facebook_sending_data[userName] = new_msgs
    send_messages_to_facebook(DataFrame(facebook_sending_data))

'''
Processes message data from facebook message format to google sheets format
and sends message data out to google sheets
'''
def get_messages_from_facebook_and_send_to_google_sheet():
    pass

'''
Cycles information between facebook and google sheets
'''
def cycle_messages_between_facebook_and_google_sheet():
    get_messages_from_facebook_and_send_to_google_sheet()
    get_messages_from_google_sheet_and_send_to_facebook()
    
def main():
    pass
    
'''
class Facebook_AND_Pandas_MSG_HANDLER:
    def __init__(self, dataFrame, credentials):
        self._dataFrame = dataFrame
        self._previous_DataFrame_Instance = self._dataFrame.copy(deep = True)
        
        self._chat_augmented_api = Chat_api_augmented(credentials)
        self._active_friend_conversations = {} # A dict of {name: user-Thread objects} from facebook api. Comes from dataframe when initialized.
        
    # Detect differences between the current dataframe and the new dataframe instance
    # Store differences in a new update instance
    # Update old dataframe object to new dataframe instance
    # 
    def __update_internal_reps(self, new_dataFrame_instance):
        # Declare differences dataframe
        # make
        # 
        #differences = dict(zip(TO_DELETE_NAMES, 
        #                       [[''] for dummy in range(len(TO_DELETE_NAMES))]))
        # Detect Major differences
            # Users have been added or removed
            #If we added a new user to the dataframe, note that difference.
            
            
            difference_in_num_users = (len(new_dataFrame_instance.loc[0]) - 
                                       len(self._dataFrame.loc[0]))
            if difference_in_num_users > 0: # user has been added. 
                pass
            elif difference_in_num_users < 0: # user has been deleted 
                pass
        # Detect minor differences:
            # Message differences
    def push_data_to_facebook(self):
        pass
    def pull_data_from_facebook(self):
        pass
'''

# b=0 case
'''
dataframe_placeholder = {'':[],
                         '':[],
                         ...
                         '':[],
                         'Name1':['S1','','R1','','S2','','R2',...]
                         'Name2':['S1','','R1','','S2','','R2',...]
                         ...
                         'NameN':['S1','','R1','','S2','','R2',...]}

dataframe_placeholder = {'':[],
                         '':[],
                         ...
                         '':[],
                         '':['','',...,'Name1', 'S1','','R1','','S2','','R2',...]
                         '':['','',...,'Name2','S1','','R1','','S2','','R2',...]
                         ...
                         '':['','',...,'NameN','S1','','R1','','S2','','R2',...]}
'''

TO_DELETE_NAMES = ['Dipesh Poudel','Joseph Islam','Ali', 'Ana Verulidze']
'''
longest_message = 0
vertical_offset = 0
horizontal_offset = 0
max_len = vertical_offset + longest_message


dataframe_placeholder = {}
for column in range(horizontal_offset):
    dataframe_placeholder[' ' * column] = [] + ['']*max_len
    
for index, name in enumerate(names):
    if vertical_offset == 0:
        dataframe_placeholder[name] = ['']*max_len
    else:
        dataframe_placeholder[' ' * (column + index + 1)] = ['']
'''

dataframe_placeholder = dict(zip(TO_DELETE_NAMES, [[''] for dummy in range(len(TO_DELETE_NAMES))]))
dataFrame = DataFrame(dataframe_placeholder)

# Second pass: Put empty response between client-client responses
# or other-other responses

# Third pass

#augmented = Chat_api_augmented(credentials)
#print(augmented.read_last_n_messages('Dipesh', 10))
#augmented.logout()
