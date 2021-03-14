from dearpygui.core import *
from dearpygui.simple import *
import threading
import subprocess
import os
script_path = os.path.dirname(__file__)
BOOKMARK_PATH = script_path + r'\bookmarks.txt'
MEDIA_PATH = script_path + r'\downloads'

import webbrowser
firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
webbrowser.register('FF', None, webbrowser.BackgroundBrowser(firefox_path))
browser = webbrowser.get('FF')
def open_link(sender, url):
    '''open in browser'''
    browser.open_new(url)

def open_folder(sender, data):
    print(data)
    if data == 0:
        subprocess.Popen(['notepad',BOOKMARK_PATH])
    elif data == 1:
        subprocess.Popen(['explorer',MEDIA_PATH+r'\A'])
    else:
        subprocess.Popen(['explorer',MEDIA_PATH+r'\V'])


def youtube_dl():
    ''' download mp3'''
    link = get_value('link_input')
    if link:
        set_value('link_input','')
        set_value('status-ytdl',f'[START]{link}')

        delete_item('download :)')
        if int(get_value('format_picker')):
            method = 'mp3ripper.py'
        else:
            method = 'videoripper.py'

        p = subprocess.Popen(['python',method,link],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

        output, error = p.communicate()
        if error:
            set_value('status-ytdl',error.decode('utf-8','ignore'))
            print(error)
        else:
            set_value('status-ytdl',f'[COMPLETE]')
            if method == 'mp3ripper.py':
                open_folder(None, 1)
            else:
                open_folder(None, 2)
        add_button('download :)', parent='youtube-dl', before='status-ytdl', callback=youtube_dl_dispatcher)



def youtube_dl_dispatcher(sender, data):
    d = threading.Thread(name='daemon', target=youtube_dl, daemon=True)
    d.start()

def refreshbookmarks():
    delete_item('bookmarkgroup')
    add_group('bookmarkgroup',parent='bookmark')
    with open(BOOKMARK_PATH,'r') as fp:
        count = 0
        for line in fp:
            line = line.replace('\n','')
            if line.startswith('#'):
                add_text(" "*10+line[1:])
            else:
                name,url= line.split(', ')
                #print(name,url)
                add_button(f'{str(count)+" "+name:90}',parent='bookmarkgroup',width=280,callback=open_link,callback_data=url)
                count += 1



with window("Main Window"):
    end()

    add_window('youtube-dl',x_pos=0,y_pos=0,no_move=True,no_collapse=False,no_scrollbar=True,no_close=True,menubar=False,no_resize=True,height=600,width=206)
    add_radio_button('format_picker', items=['video','song'])
    add_input_text('link_input',width=222)
    add_button('download :)',callback=youtube_dl_dispatcher)
    add_text('status-ytdl',default_value=' ')
    end()


    add_window('bookmark',x_pos=0,y_pos=20,no_move=True,no_collapse=True,no_title_bar=True,menubar=False,no_resize=True,width=206,height=580,no_close=True)
    add_group('tool_buttons',horizontal=True,width=60)
    add_button('Refresh',callback=refreshbookmarks)
    add_button('bm.txt',callback=open_folder,callback_data=0)
    add_button('Media',callback=open_folder,callback_data=1)
    end()
    refreshbookmarks()



#show_documentation()
#show_debug()
#show_about()
#show_metrics()
#show_logger()

set_main_window_size(222,600)
set_main_window_resizable(False)
set_main_window_title(r'     ')
set_main_window_pos(0,60)
THEMES='''Classic, Light, Grey, Dark Grey, Dark, Dark 2, Cherry, Purple, Gold, Red'''.split(', ')
set_theme(THEMES[5]) # 5
start_dearpygui(primary_window="Main Window")
