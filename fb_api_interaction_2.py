# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:29:09 2020

@author: josep
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pandas import DataFrame, Series
from df2gspread import df2gspread as d2g
from google.oauth2 import service_account
import fbchat
import fbchat.models as models
from time import sleep
from gspread_formatting import cellFormat, textFormat, format_cell_range, color
credentials = ('ejnislam18@gmail.com','Jello123!')

class Sheets_api_simplified:
    def __init__(self, credentials):

        scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
        gc = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(credentials, scope))
        self._sheet = gc.open("outreach_app").sheet1


    def set_cell_background_color(self, cell_id, color_):

        fmt = cellFormat(
            backgroundColor=color(*color_),
        textFormat=textFormat(bold=False, foregroundColor=color(0,0,0)),
        horizontalAlignment='CENTER')
        format_cell_range(self._wks, cell_id + ':' + cell_id, fmt)

    def set_cell_text_color(self, cell_id, color_):
        pass
    def align_cell(self, cell_id, alignment='CENTER'):
        pass

    def get_cell_color(self, cell_id):
        # Returns cell color
        cell_color_format = get_effective_format(self._sheet, cell_id)
        return cell_color_format.backgroundColor
        # Returns cell color
        pass
    def get_cell_text(self, cell_id):
        cell_text_format = get_effective_format(self._sheet, cell_id)
        return cell_color_format.textColor
        pass
    def toggle_borders(self, cell_id):
        border_toggle = get_effective_format(self._sheet, cell_id)
        return toggle_borders
        pass
    def set_cell_text(self, cell_id, text):
        pass
    def get_all_records(self):
        return self._wks.get_all_records()
    def remove_column(self):
        pass

class Sheets_api_augmented:
    ALPHA = 'ABCDEFGHIJLMNOPQRSTUVWXYZ'
    MAX_CONVO_DISPLAY_LENGTH = 40
    def __init__(self, credentials):
        self._client = Sheets_api_simplified()

    '''
    Creates new thread for name on Google Sheet with texts conversation
    with name in cell pos ([Letter][Number] format) and texts below.
    '''
    def place_new_thread(self, name, conversation, pos):
        col = Sheets_api_augmented.ALPHA.index(pos[0])
        row = int(pos[1])
        for ind, line in enumerate(conversation):
            new_pos = col + str(row + ind)
            self._client.set_cell_text(new_pos, line)
            if not ind % 4:
                self._client.set_cell_text_color(new_pos, (0,0,0))
            else:
                self._client.set_cell_text_color(new_pos, (0,0,1))

    def remove_thread(self, pos):
        col = Sheets_api_augmented.ALPHA.index(pos[0])
        self._client.remove_column(col)
        '''row = int(pos[1])
        for ind in range(1, 50):
            new_pos = col + str(row + ind)
            self._client.set_cell_background_color(new_pos, (1,1,1))
            self._client.set_cell_text(new_pos) = ''
            self.'''

    '''
    Gets thread with name at pos
    Takes:
        Google sheets pos in [ColumnLetter][RowNumber] format
    Returns:
        (CTRL NUM, conversation body)
        CTRL = 1 if this is a new member
        CTRL = -1 if this is a delete-me member
        CTRL = 0 if this is just an ordinary exchange.
    '''
    def get_thread(self, pos):
        col = pos[0]
        row = int(pos[1])
        name = self._client.get_cell_text(pos)
        color = self._client.get_cell_color(pos)
        messages = []
        for num in range(Sheets_api_augmented.MAX_CONVO_DISPLAY_LENGTH):
            new_pos = col + str(ind + (num + 1))
            messages.append(self._client.get_cell_text(new_pos))

        CTRL = 0 # if defaukt
        if color == 'green': # pick your green
            CTRL = 1
        elif color == 'RED':
            CTRL = -1
        return (CTRL, messages)
    def get_name(self, pos):
        return self._client.get_cell_text(pos)

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
        return (friend.first_name + ' ' + friend.last_name,self.__client.fetchThreadMessages(friend.uid, limit=n)[::-1]) # RECENT CHANGE COME BACK TO ME IF SOEMTING BREAKS

    def logout(self):
        self.__client.logout()

class Sheets_to_Pandas_and_Back:
    ALPHA = 'ABCDEFGHIJLMNOPQRSTUVWXYZ'
    def __init__(self, credentials, names=[], starting_row = 1):

        self._starting_row = starting_row
        self._client = Sheets_api_augmented(credentials)
        self.load_names(names)

    # Gives each user a new spot and binds their name accordingly.
    def load_names(self, names):
        names += ['new']
        row = self._starting_row
        self._users = dict()
        for ind, name in enumerate(names):
            self._users[name] = Sheets_to_Pandas_and_Back.ALPHA[ind+1] + str(row)
        return load_names

    def send_data_to_sheets(self, messages): # This is where new users are added and old users are removed.
        old_names = [user[0] for user in self._users]
        for name in messages.columns:
            if name in old_names:
                self._client.place_new_thread(name, messages[name], self._users[name])
            else:
                self._client.remove_thread(self._users[name]) # There's some excess functionality here... THat's okay...

    # Get all the messages currently registered
    def retrieve_data_from_sheets(self):
        messages = {}
        for user in self._users:
            thread = self._client.get_thread(user[1])
            if thread[0] == 0:
                messages[thread[0]] = thread[1]
            elif thread[0] == 1:# If there's a new user, reflect that there is a new user!
                messages[thread[0]] = thread[1]
                name = self._client.get_name(user.pos) # Make the new user occupy the old new user spot.
                self._users[name] = self._users['new'] # Make the new user placeholder occupy a now shifted over by one spot.
                self._users['new'] = Sheets_to_Pandas_and_Back.ALPHA[len(self._users)+1] + str(self._starting_row)
            else:
                self._client.remove_thread(self._users[name]) # just remove the thread from the sheet and keep going.
                pass # Don't store data for people we're not going to be keeping around. Delete them from the excel sheet after this tick.
        return messages

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
                elif len(friends) == 1:
                    self._users[name] = friends[0]
                else:
                    print('No friends found with name: ' + name)
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
                    content_author_pairs[index] = ['CLIENT'] + [pair[1]]
                else:
                    content_author_pairs[index] = ['OTHER'] + [pair[1]]

            last_messages[name] = content_author_pairs
        return last_messages

    '''
    posts given new messages to facebook.
    Will not post Null messages to facebook. Null messages are those that are ''
    Takes:
        new_msg_dataframe: Pandas dataframe in {userName: [msg1out, msg2out, ..., msgNout]}
                            format.
    Returns:
        boolean success of the message posting.
    '''
    def post_given_messages(self, new_msg_dataframe):
        active_user_threads = list(self._users.keys())
        assert len(active_user_threads) == len(new_msg_dataframe.columns), \
        "Cannot post " + str(len(new_msg_dataframe.columns)) + \
        " convo threads to " + str(len(active_user_threads)) + ". Load names again?"

        for name in new_msg_dataframe.columns:
            if name in active_user_threads:
                thread = self._users[name]
                for new_msg_out in new_msg_dataframe[name]:
                    try:
                        if new_msg_out == '':
                            continue
                        self._client.send_message_to_person_uid(thread.uid, new_msg_out)
                    except:
                        return False
        return True # We at least attempted to send all the messages.
    def logout(self):
        self._client.logout()
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
        last_current_client_msg = current_client_msgs[backtrack_index]
    return new_but_backwards[::-1]

def make_dictionary_into_rectangle_array(dictionary, filler=''):
    return DataFrame(dict([ (name,Series(messages)) for name,messages in dictionary.items() ])).fillna(filler)

def get_client_messages_from_google_sheet(all_messages):
    return all_messages[::4]


'''
API INTERACTION FUNCTIONS
'''

'''
Gets message data from the google sheet we're working on in
    dataFrame = {userName: [CLIENTMSG, "", OTHERMSG, "", CLIENTMSG, ...,
                                "", CLIENTMSG/OTHERMSG]} format
'''
def get_data_from_google_sheet(Google_sheet_to_Pandas):
    return Google_sheet_to_Pandas.retrieve_data_from_Sheets()

'''
Sends message data to the google sheet we're working on in
    dataFrame = {userName: [CLIENTMSG, "", OTHERMSG, "", CLIENTMSG, ...,
                                "", CLIENTMSG/OTHERMSG]} format
'''
def send_data_to_google_sheet(Pandas_to_Google_Sheet, messages_DF):
    try:
        Pandas_to_Google_Sheet.send_data_to_sheets(messages_DF)
    except AssertionError:
        pass
    return True

'''
Gets message data from facebook in
    dataFrame = {userName: [CLIENTMSG, OTHERMSG, CLIENTMSG, ...,
                            CLIENTMSG/OTHERMSG]} format
'''
def get_messages_from_facebook(facebook_to_pandas, n):
    return facebook_to_pandas.read_last_messages(n)

'''
Sends message data to facebook in
    dataFrame = {userName: [CLIENTMSG, CLIENTMSG, ..., CLIENTMSG]} format
'''
def send_messages_to_facebook(pandas_to_facebook,
                              dataFrame_messages_to_send_to_facebook):
    # messagesData = dict(zip(names, [['hello','test1'],['YUCK'],['BAAAAAH'],['']]))
    # messages = DataFrame(dict([ (name,Series(messages)) for name,messages in messagesData.items() ])).fillna('')

    try:
        pandas_to_facebook.post_given_messages(dataFrame_messages_to_send_to_facebook)
    except AssertionError:
        pandas_to_facebook.load_names(dataFrame_messages_to_send_to_facebook.columns)
        pandas_to_facebook.post_given_messages(dataFrame_messages_to_send_to_facebook)
    succeeded = True
    return succeeded

'''
Processes message data from google sheet format to facebook message format
and sends message data out to facebook
'''
def get_messages_from_google_sheet_and_send_to_facebook(pandas_to_facebook, Google_sheet_to_Pandas, original_sheet):
    '''get_messages_from_google_sheet_and_send_to_facebook
    google_sheets_data = {userName: [CLIENTMSG, "", OTHERMSG, "", CLIENTMSG, ...,
                                "", CLIENTMSG/OTHERMSG]} format'''
    google_sheets_data = get_data_from_google_sheet()

    # DUMMY TO BE REMOVED LATER
    dummy_return_sheet = {'Ali':['c1','','o1','','c2','','o2'],
                   'Dipesh':['c1','','o1','','c2','','o2','','c3','','','','c4']}
    google_sheets_data = make_dictionary_into_rectangle_array(dummy_return_sheet)
    # END DUMMY SECTION

    '''
    Sends message data to facebook in
    dataFrame = {userName: [CLIENTMSG, CLIENTMSG, ..., CLIENTMSG]} format
    '''
    facebook_sending_data = dict()
    # I'm just going to add all the new client messages the facebook_sending_data
    # if there is a new user. I will just delete the new user from the google sheets data
    # after I add them to the facebook_sending_data and proceed through the
    # rest of the data normally after that.
    old_names = list(original_sheet.columns)
    for name in list(google_sheets_data.columns): #Check to see if there is a new user
        if name not in old_names: # Then there is a new user. Add all the new client messages to the user and delete the new user from the google sheets data
            facebook_sending_data[name] = get_client_messages_from_google_sheet(google_sheets_data[name])
            #for clientMsgIndex in range(0, len(google_sheets_data[name]), 4):
            #    facebook_sending_data[name].append()
            google_sheets_data = google_sheets_data.drop(columns=[name])

    # If a user has been removed, the user's connection will be refreshed away
    # automatically.ju
    for userName in google_sheets_data.columns:
        facebook_sending_data[userName] = [] # only gonna send back the new messages
        new_msgs = get_new_client_messages_out(get_client_messages_from_google_sheet(list(original_sheet[userName])),
                                               get_client_messages_from_google_sheet(list(google_sheets_data[userName]))) # This gives back the new messages
        facebook_sending_data[userName] = new_msgs
    print(make_dictionary_into_rectangle_array(facebook_sending_data))
    send_messages_to_facebook(pandas_to_facebook, make_dictionary_into_rectangle_array(facebook_sending_data))
'''
Processes message data from facebook message format to google sheets format
and sends message data out to google sheets
'''
def get_messages_from_facebook_and_send_to_google_sheet(facebook_to_pandas, pandas_to_Google_Sheets, max_messages_to_display = 10):
    # There will no active chat changes between facebook and google sheets.
    # Thus, we only have to change the format between the facebook format
    # and the google sheets format.
    # Get the facebook conversations in a rectangular pandas dataframe format
    facebook_conversations = facebook_to_pandas.read_last_messages(max_messages_to_display)

    send_to_google_sheets = {}
    for name in facebook_conversations.columns:
        # Second Pass: Make sure the messages alternate in CLIENT, OTHER, ... CLIENT form.
        for index in range(len(facebook_conversations[name]) - 1):
            if facebook_conversations[name][index][0]==facebook_conversations[name][index+1][1]:
                if facebook_conversations[name][index][0] == 'CLIENT':
                    facebook_conversations[name].insert(index, ('OTHER', ""))
                else:
                    facebook_conversations[name].insert(index, ('CLIENT', ""))
        # Third pass: Make sure the number of messages is still <= the max
        if len(facebook_conversations[name]) > 10:
            extra_length = len(facebook_conversations[name]) - 10
            facebook_conversations[name] = facebook_conversations[name][extra_length:]
        # Fourth pass: Make sure the client is leading the messages.
        if facebook_conversations[name][0] == 'OTHER':
            facebook_conversations[name] = facebook_conversations[name][1:]

        # Fifth pass Remove labels
        for indx, message in enumerate(facebook_conversations[name]):
            facebook_conversations[indx] = facebook_conversations[indx][1]

        # Sixth pass: Add the proper spacing between each message
        i = len(facebook_conversations[name]) # Go from the back to the front and insert in between each entity.
        while i > 0:
            facebook_conversations[name].insert(i, '')
            i -= 1
        # Chill. Now our data is formatted correctly.
    # now, we can frameify it and send it off to the google sheet.
    formatted_conversation = make_dictionary_into_rectangle_array(facebook_conversations)
    # Send these facebook conversations to the google sheet. There won't be any friend conflicts at this time.
    send_data_to_google_sheet(pandas_to_Google_Sheets, formatted_conversation)
    # And this should make the end of this function!

'''
Cycles information between facebook and google sheets
'''
def cycle_messages_between_facebook_and_google_sheet():
    get_messages_from_google_sheet_and_send_to_facebook()
    current_sheet_instance = get_messages_from_facebook_and_send_to_google_sheet()
    return current_sheet_instance

def main():
    fb_credentials = ('a','b')#(Useremail, password)
    gs_credentials = ('a','b')
    facebook_to_pandas_and_back = Facebook_to_Pandas_and_Back(fb_credentials)
    pandas_to_google_sheet_and_back = Pandas_to_Google_Sheet_and_Back(gs_credentials)

    current_original_sheet_instance = cycle_messages_between_facebook_and_google_sheet(facebook_to_pandas_and_back, pandas_to_google_sheet_and_back)

def testing_function():
    names = ['Ali','Dipesh','Ana','Joseph']
    credentials = ('ejnislam18@gmail.com','Jello123!')
    facebook_to_pandas_and_back = Facebook_to_Pandas_and_Back(credentials)
    facebook_to_pandas_and_back.load_names(names)

    messagesData = dict(zip(names, [['hello','test1'],['YUCK'],['BAAAAAH'],['']]))
    messages = DataFrame(dict([ (name,Series(messages)) for name,messages in messagesData.items() ])).fillna('')

    facebook_to_pandas_and_back.post_given_messages(messages)

    last_messages = facebook_to_pandas_and_back.read_last_messages(10)
    print(last_messages)
    facebook_to_pandas_and_back.logout()
    return last_messages, messages

def testing_bigger_functions():
    names = ['Ali','Dipesh','Ana','Joseph']
    credentials = ('ejnislam18@gmail.com','Jello123!')
    facebook_to_pandas_and_back = Facebook_to_Pandas_and_Back(credentials)
    facebook_to_pandas_and_back.load_names(names)

    messagesData = dict(zip(names, [['hello','test1'],['YUCK'],['BAAAAAH'],['']]))
    send_messages_to_facebook(facebook_to_pandas_and_back,
                              make_dictionary_into_rectangle_array(messagesData))
    last_messages = get_messages_from_facebook(facebook_to_pandas_and_back, 1)
    facebook_to_pandas_and_back.logout()
    return last_messages

def testing_biggest_functions():
    '''get_messages_from_google_sheet_and_send_to_facebook
    google_sheets_data = {userName: [CLIENTMSG, "", OTHERMSG, "", CLIENTMSG, ...,
                                "", CLIENTMSG/OTHERMSG]} format'''

    dummy_original_sheet = {'Ali':['c1','','o1','','c2','','o2'],
                   'Dipesh':['c1','','o1','','c2','','o2'],
                   'Ana':['c1','','o1','','c2','','o2']}
    #dummy_return_sheet = {'Ali':['c1','','o1','','c2','','o2'],
    #               'Dipesh':['c1','','o1','','c2','','o2','','c3','','','','c4'],
    #               'Ana':['c1','','o1','','c2','','o2','','c3']
    #               'Joseph':['c1','']}
    dummy_original_sheet = make_dictionary_into_rectangle_array(dummy_original_sheet)

    names = ['Ali','Dipesh','Ana','Joseph']
    credentials = ('ejnislam18@gmail.com','Jello123!')
    facebook_to_pandas_and_back = Facebook_to_Pandas_and_Back(credentials)
    facebook_to_pandas_and_back.load_names(names)

    get_messages_from_google_sheet_and_send_to_facebook(facebook_to_pandas_and_back, dummy_original_sheet, )
#last_messages = testing_biggest_functions()
