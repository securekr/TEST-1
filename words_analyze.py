from utils import remove_chars_from_text, remove_emojis, clear_user, read_conf
import nltk_analyse
import sys
from pywebio import input, config
from pywebio.output import put_html,put_text,put_image,put_collapse, put_button, put_code, clear, put_file, popup, put_table
from pywebio.input import file_upload as file
from pywebio.session import run_js
import json, re, jmespath, string, collections
from pywebio.input import input
from pywebio.pin import *

config(theme='dark',title="TelAnalysis", description="Analysing Telegram CHATS-CHANNELS-GROUPS")
put_button("Scroll Down",onclick=lambda: run_js('window.scrollTo(0, document.body.scrollHeight)'))
put_button("Close",onclick=lambda: run_js('window.close()'), color='danger')
put_html("<h1><center>Analyse of Telegram Chat<center></h1><br>")
put_input('ID')
put_button("Search ID",onclick=lambda: run_js(f'window.find({pin.ID}, true)'), color='warning')
all_tokens = []
users = []
count_messages = 0
filename = sys.argv[1]
filename = filename.split(".")[0]
filename = filename.split("/")[1]
with open(f'asset/{filename}.json', 'r', encoding='utf-8') as datas:
    data = json.load(datas)
    sf = jmespath.search('messages[*]',data)
    group_name = jmespath.search('name', data)
    for message in sf:
        try:
            user = jmespath.search('from_id', message)
            if user and user != '':
                #user = clear_user(user)
                #print(user)
                if user not in users and user is not None:
                    #user = str(user).replace(" ","").replace('"','').replace(".","").replace("꧁","")
                    try:
                        user = user.replace(" ","")
                    except:
                        put_text("error #9")
                    #print(user)
                    users.append(user)
                    
                    try:
                        exec('{}_list = []'.format(user))
                    except Exception as ex:
                        put_code(ex, user)
                        continue
        except Exception as ex:
            print(ex, 92141)
            continue
    for message in sf:
        count_messages +=1
        texts = jmespath.search('text',message)
        from_user = jmespath.search('from_id', message)
        if from_user is None:
            continue
        else:
            #from_user = clear_user(from_user)
            from_user = from_user.replace(" ","")
            #print(from_user)
        if str(type(texts)) == "<class 'str'>":
            if texts != '':
                test = str(texts).replace("\\n","").replace("\n","").strip()
                if "http" in test:
                    continue
                else:
                    try:
                        test = test.replace("\\n","").replace("\n","").replace('"',"'").strip()
                        
                        try:
                            test = remove_emojis(test)
                            
                        except:
                            test = test
                        
                    except:
                        put_text("error #1")
                    try:
                        if test is None or test == "":
                            continue
                        else:
                            exec('{}_list.append("{}")'.format(from_user,str(test)))
                            #exec('id_{}_list = []'.format(user))
                            #print('{}_list.append("{}")'.format(from_user,str(test)))
                    except Exception as ex:
                        print(ex)
                        continue
                    #count_messages +=1
        elif str(type(texts)) == "<class 'list'>":
            for textt in texts:
                try:
                    if len(textt['text']) >=1:
                        test = textt['text']
                        
                        if "http" in test:
                            continue
                        else:
                            try:
                                test = test.replace("\\n","").replace("\n","").strip()
                                try:
                                    test = remove_emojis(test)
                                except:
                                    test = test
                            except:
                                put_text("error #2")
                            try:
                                if test is None or test == "":
                                    continue
                                else:
                                    exec('{}_list.append("{}")'.format(from_user,str(test)))
                                    #print('{}_list.append("{}")'.format(from_user,str(test)))
                            except Exception as ex:
                                continue
                            #count_messages +=1
                except Exception as ex:
                    try:
                        try:
                            test = textt.replace("\\n","").replace("\n","").strip()
                            try:
                                test = remove_emojis(test)
                            except:
                                test = test
                        except:
                            put_text("error #3")
                        try:
                            if test is None or test == "":
                                continue
                            else:
                                exec('{}_list.append("{}")'.format(from_user,str(test)))
                                #print('{}_list.append("{}")'.format(from_user,str(test)))
                        except Exception as ex:
                            continue
                        #count_messages +=1
                    except:
                        put_text("error #4")
    
    
    try:
        put_table([count_messages, len(users)], header=['All used messages count','Messages from count users detected'])
    except Exception as ex:
        put_text(ex)
    
    for i,user in enumerate(users):
        #print(users)
        try:
            try:
                if user and user != "":
                    user = user.replace(" ","")
                    exec('da = {}_list'.format(user))
                    most_com = read_conf('most_com')
                    genuy, tokens = nltk_analyse.analyse(da, most_com)
                    gemy = []
                    gery = []
                    for x,y in genuy:
                        gemy.append([x,y])
                    genuy.clear()
                    for x in da:
                        gery.append([x])
                    da.clear()
                    for token in tokens:
                        all_tokens.append(token)
                    if len(gery) >=1 and len(gemy) >=1:
                        """ #put_code("*"*90)
                        put_code(f'--{i} {user}: ')
                        for j,ga in enumerate(da):
                            put_code(f'[{j}] {ga}')
                        e   lse:
                        #print(da)
                        continue
                         da = popup(user, [
                                put_html(f'<h3>{user} Сообщения:</h3>'),
                                'html: <br/>',
                                put_table([['Сообщения'], [da]]),
                                put_button(['close_popup()'], onclick=lambda _x: close_popup())
                            ])"""
                        put_collapse(user,
                        [
                        f'Messages of {user}',
                            put_table(gery
                            , header=['Messages']),
                            put_table(gemy
                            , header=['word', 'count'])],
                             open=False)


            except Exception as ex:
                put_text(f"[{user}] error #8 {ex}")
        except Exception as ex:
            put_text(f'{ex} error #6')
            continue
    most_com = read_conf('most_com')
    all_tokens,data = nltk_analyse.analyse_all(all_tokens,most_com)
    all_chat = []
    for i in all_tokens:
        try:
           all_chat.append([i[0],i[1]])
        except Exception as ex:
            put_text(f"error #7 {ex}")
            pass
    put_collapse(f'TOP words of {group_name}',[
                    put_table(all_chat
                    , header=['word']),
                    ],open=False)

    
    put_button("Close",onclick=lambda: run_js('window.close()'), color='danger')
    put_button("Scroll Up",onclick=lambda: run_js('window.scrollTo(document.body.scrollHeight, 0)'))