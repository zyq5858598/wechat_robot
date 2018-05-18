#!/usr/bin/env python
# coding: utf-8
#
import pprint
import re
import requests
from wxbot import *
import sql
reg=re.compile("(?=-)")
url = 'http://localhost:23501/'
api = 'wx/saveBug'
upload = 'wx/uploadFile'
projectPostfix = '项目'
countChar = 2
mysql = sql.myMysql()
class MyWXBot(WXBot):
    '''
    接受消息
    进行消息过滤处理
    调用api完成业务功能
    '''
    def handle_msg_all(self, msg):
        print(msg)
        if msg['msg_type_id'] == 3:
            project = mysql.select_project_by_gid(msg['user']['id'])
            if project is not None:
                postData = {}
                postData['creator'] = msg['content']['user']['name']
                postData['project'] = project[1]
                if msg['content']['type'] == 0:
                    data = msg['content']['data']
                    lent = reg.findall(data)
                    if len(lent) >= countChar:
                        info = data.split('-')
                        postData['isNew'] = info[0]
                        postData['title'] = info[1]
                        postData['users'] = info[2].split(',')
                        postData['detail'] = info[1]
                        if len(lent) > countChar:
                            postData['priorityLevel'] = info[3]
                            postData['seriousDegree'] = info[4]
                            postData['bugType'] = info[5]
                        result = requests.post(url + api, json=postData)
                else:
                    path = ''
                    if msg['content']['type'] == 13:
                        path = msg['content']['video']
                    if msg['content']['type'] == 4:
                        path = msg['content']['voice']
                    if msg['content']['type'] == 3:
                        path = msg['content']['img']
                    files = {'file': open(os.path.join(os.getcwd(), 'temp', path), 'rb')}
                    result = requests.post(url + upload, data=postData, files=files)
                if result is not None:
                    self.send_msg_by_uid(result.json()['msg'], msg['user']['id'])
            #self.send_msg_by_uid(u'hi', msg['user']['id'])
            #self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])

    '''
    微信群管理（成员必须是好友）
    '''
    def group_manage(self):
        msgs = mysql.select("select * from t_group order by id")
        for msg in msgs:
            members = []
            member_ids = []
            add_members = []
            if msg[2].find(',') == -1:
                members.append(msg[2])
            else:
                members = msg[2].split(',')
            for uname in members:
                uid = self.get_user_id(uname)
                if uid is not '':
                    member_ids.append(uid)
                    add_members.append({'UserName': uid})
            project = mysql.select_project_by_name(msg[1])
            if msg[3] == 1:
                group_id = self.createchartroom(add_members)
                self.update_group(group_id, msg[1])
                self.send_msg_by_uid(u'创建成功',group_id)
            elif msg[3] == 2:
                self.add_uid_to_group(','.join(member_ids), project[5])
            elif msg[3] == 3:
                for id in member_ids:
                    self.delete_uid_from_group(id, project[5])
            mysql.update("delete from t_group where id=%d" % (msg[0]))

    '''
   更新微信群id（创建时同步微信群id）
   '''
    def update_group(self, group_id, name):
        self.get_big_contact()
        self.set_group_name(group_id, name)
        mysql.update("update t_project set group_id = '%s' where name ='%s'" % (group_id, name))

    '''
   更新微信群id（每次扫码后微信群id可能会变，因此必须在扫码后重新将id同步数据库而对微信群进行管理）
   '''
    def init_group_data(self):
        for group in self.group_list:
            project = mysql.select_project_by_name(group['NickName'])
            if project is not None:
                mysql.update("update t_project set group_id = '%s' where name ='%s'" % (group['UserName'], group['NickName']))

def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png' # tty为命令行(此方法只能在Linux终端下使用)
    bot.run()



if __name__ == '__main__':
    main()