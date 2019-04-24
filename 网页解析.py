# --coding:utf-8--
# Author:Clark Xu, Hang Shang
# Time:2019/3/20 16:42
# # -*- coding: utf-8 -*-
import requests
import os
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')


from bs4 import BeautifulSoup
import json

import os
current_path = sys.path[0]
if 'final_result' in os.listdir(current_path):
    os.remove('final_result')
def name_extract(soup1):
    '''
    Inputs:
        soup1 : the source code BeatifulSoup data format

    Returns:
        actor name
    '''
    tmp_info = soup1.find("h1")
    return "" if tmp_info == None else soup1.find("h1").text.split(" ")[0]

def basic_info_extract(soup1):
    '''extract personal information
    Inputs:
        soup1 : the source code BeatifulSoup data format

    Returns:
        basic info (补充)
    '''

    b = soup1.find_all("div",{"class":"info"})
    basic_info_dict = {'star': '', 'bd': '', 'bp': '', 'imdb': ''}
    if len(b) == 0:
        return ["","","",""]

    c = b[0].find("ul")
    if c == None:
        return ["", "", "", ""]

    info_text = c.find_all("li")#.text

    basic_info_list = []
    for i in range(len(info_text)):
        if info_text[i].text.replace(u" ", u"") == u"":
            continue
        info_text[i] = info_text[i].text.replace(u" ", u"").replace('\n', '')

        text_element = info_text[i].strip().split(':')
        # 获取类别
        info_class = info_text[i].split(":")[0]
        # if(d[i].text):
        if info_class == u"星座":
            basic_info_dict['star'] = info_text[i].split(":")[1]
        if info_class == u"出生日期":
            basic_info_dict['bd'] = info_text[i].split(":")[1]
        if info_class == u"出生地":
            basic_info_dict['bp'] = info_text[i].split(":")[1]
        if info_class == u"imdb编号":
            basic_info_dict['imdb'] = info_text[i].split(":")[1]


    basic_info_list.append(basic_info_dict['star'])
    basic_info_list.append(basic_info_dict['bd'])
    basic_info_list.append(basic_info_dict['bp'])
    basic_info_list.append(basic_info_dict['imdb'])

    return basic_info_list

# celebrity introduction
def intro_extract(soup1):
    '''actor information
    Inputs:
        soup1 : the source code BeatifulSoup data format

    Returns:
        actor info
    '''
    intro = soup1.find_all("div", attrs = {"id" : "intro", "class" : "mod"})
    if len(intro) == 0:
        return ""
    brief = intro[0].find_all("div", {"class": "bd"})
    return 0 if len(brief) == 0 else brief[0].text.replace(" ","").replace('\n', '').replace('\u3000',"")

def movies_extract(soup1):
    '''Recently five movies
    Inputs:
        soup1 : the source code BeatifulSoup data format

    Returns:
        five most recently movies/master work
    '''
    master_work=[]
    movie = ""
    recent = soup1.find_all("div",attrs = { "id" : "recent_movies" , "class" : "mod"})
    if len(recent) !=0:
        latest_five = recent[0].find_all("div",{"class":"bd"})
        if len(latest_five) != 0:
            b1 = latest_five[0].find("ul")
            if len(b1) != 0:
                c1 = b1.find_all("li")
                for i in range(len(c1)):
                    d1 = c1[i].find_all("div", attrs = {"class":"info"})
                    if len(d1) != 0:
                        e1 = d1[0].find_all("a")
                        if len(e1) != 0:
                            m_name = e1[0].get('title')
                            if e1[0].get('href') != None:
                                m_id = e1[0].get('href').split("/")[-2]
                            else:
                                m_id = ''
                            a_1 = {"name": m_name, "douban": m_id}
                            # j_1 = json.dumps(a_1, ensure_ascii=False)
                            master_work.append(a_1)

    best = soup1.find_all("div",attrs = {"id":"recent_movies","class":"mod"})
    if len(best) != 0:
        best_five = recent[0].find_all("div",{"class":"bd"})
        if len(best_five) != 0:
            b2=best_five[0].find("ul")
            if len(b2) != 0:
                c2=b2.find_all("li")
                for i in range(len(c2)):
                    d2 = c2[i].find_all("div",attrs = {"class":"info"})
                    if len(d2) != 0:
                        e2 = d2[0].find_all("a")
                        if len(e2) != 0:
                            m_name = e2[0].get('title')
                            if e2[0].get('href') != None:
                                m_id = e2[0].get('href').split("/")[-2]
                            else:
                                m_id=''
                            a_2 = {"name": m_name, "douban": m_id}
                            # j_1 = json.dumps(a_1, ensure_ascii=False)
                            master_work.append(a_2)

    return master_work


def extract_source(source_code):
    ''' analysis source code
    Inputs:
        the web page source code

    Returns:
        structure data

    '''
    info = []
    soup = BeautifulSoup(source_code)
    info.append(name_extract(soup))
    info = info + basic_info_extract(soup)
    info.append(intro_extract(soup))
    info.append(movies_extract(soup))
    a_1 = { "c_name" : info[0], \
            "e_name" : '',\
            "star" : info[1], \
            "birthdate" : info[2], \
            "birthplace":info[3], \
            "db_id" : info[4], \
            "intro":info[5], \
            "movie":info[6]}
    return a_1



def del_dup(list1):
    '''合并电影
    '''
    res=[]
    set1=set()
    for i in list1:
        if i['douban'] not in set1:
            set1.add(i['douban'])
            res.append(i)
    return res

def main():
    '''extract actor structure data
    '''
    path = "data/"
    file_list = set(os.listdir(path))
    count=0
    # 先解析这个文件
    with open("data/actor_info1", 'r') as f:
        each_info = f.readlines()
        for i in range(len(each_info)):
            all_info = each_info[i].split('\t')
            # print all_info
            # 获取id
            c_name = all_info[0]
            e_name = all_info[1].replace('english_name-', '')
            douban_id = all_info[2].replace('douban_id-', '')
            master_work = all_info[3].replace('master_word-', '').replace('\n', '')

            master_work_list = []

            for i in master_work.split('|x02'):
                if i != "":
                    movie_id = i.split('|x01')[0]
                    movie_name = i.split('|x01')[1]
                    m_1 = {"name": movie_name, "douban": movie_id}
                    master_work_list.append(m_1)

            if c_name == "" or douban_id not in file_list:
                continue

            with open("final_result",'a') as f1:
                file = open(path + douban_id,'r')
                source = file.read()
                final_info = extract_source(source)
                final_info["c_name"] = c_name
                final_info["e_name"] = e_name
                final_info["db_id"] = douban_id
                final_info["movie"] = del_dup(final_info["movie"]+master_work_list)


                f1.write(json.dumps(final_info, ensure_ascii=False) + "\n")


print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) , 'start'
main()
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) , 'end'






