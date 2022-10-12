import sys, time, traceback, datetime, random
sys.path.append('../..')
from bot import bot, commandlist, commandPluginsList
from fabot import reloadPlugins, yamldata
import nsfw.classify_nsfw as nsfw

class basic(bot):
    def printConfig(self):
        uid = self.se.get('user_id')
        gid = self.se.get('group_id')
        settings = self.groupSettings or self.getConfig(self.uuid, 'qn', gid, self.sql_config)[0]
        
        message = '[CQ:face,id=151] 本群机器人配置：'
        for i in self.settingName:
            if int(i.get('isHide')) == 1:
                continue
            
            message += '\n[CQ:face,id=54] '+str(i.get('name'))+'：[|'+str(i.get('description'))+'|]\n     值：[|'+str(settings.get(i.get('description')))+'|]'
            if i.get('other') != '':
                message += '\n     描述：'+str(i.get('other'))
        message += '\n\n[CQ:face,id=189] [|请使用 set 指令修改配置|]\n[|例如：set recallFlag===0 即为设置取消防撤回功能|]'
        self.send(message)
        
    def runFunc(self):
        uid = self.se.get('user_id')
        gid = self.se.get('group_id')
        message = self.message
        
        if 'runFunc(' in message:
            self.send('[CQ:face,id=189] 递归警告：禁止在runFunc中调用自己！')
        else:
            try:
                exec(message)
            except Exception as e:
                msg = traceback.format_exc()
                self.send('[CQ:face,id=189] 错误截获\n{0}'.format(msg))
                
    def replyPM(self):
        uid = self.se.get('user_id')
        gid = self.se.get('group_id')
        message = self.message
        uuid = self.uuid
        
        message1 = message.split('|')
        userid = message1[0]
        messageid = message1[1]
        message = message1[2]
        self.SendOld(userid, '[CQ:reply,id='+str(messageid)+'] '+message)
        self.SendOld(uid, '[CQ:face,id=151] 回复成功！')
        
    def commandhelp(self):
        uid = self.se.get('user_id')
        gid = self.se.get('group_id')
        message = self.message
        
        for i in commandlist:
            content = i.get('content').rstrip()
            if message==content:
                if i.get('promise') == 'admin' or i.get('promise') == 'ao':
                    promisetext = '管理员'
                elif i.get('promise') == 'owner':
                    promisetext = '我的主人'
                elif i.get('promise') == 'anyone':
                    promisetext = '任何人'
                elif i.get('promise') == 'ro':
                    promisetext = '真正的主人'
                elif i.get('promise') == 'xzy':
                    promisetext = '最高管理员'
                self.send('[CQ:face,id=189] 指令帮助\n[CQ:face,id=54] 指令内容：'+str(i.get('content'))+'\n[CQ:face,id=54] 指令用法：'+str(i.get('usage'))+'\n[CQ:face,id=54] 指令解释：'+str(i.get('description'))+'\n[CQ:face,id=54] 指令权限：'+promisetext+'\n[CQ:face,id=54] 指令分类：'+str(i.get('mode')))
                return 
        self.send('没有这个指令呢qwq')
        
    def cd(self):
        uid = self.se.get('user_id')
        gid = self.se.get('group_id')
        
        message = '[CQ:face,id=151]{0}-菜单'.format(self.botSettings.get('name'))
        for i in commandlist:
            message += '\n[CQ:face,id=54] '+i.get('content')+'\n用法：'+i.get('usage')+'\n解释：'+i.get('description')+'\n权限：'
            if i.get('promise') == 'admin' or i.get('promise') == 'ao':
                message += '管理员'
            elif i.get('promise') == 'owner':
                message += '我的主人'
            elif i.get('promise') == 'anyone':
                message += '任何人'
            elif i.get('promise') == 'ro':
                message += '真正的主人'
            elif i.get('promise') == 'xzy':
                message += '最高管理员'
        message += '\n\n{0} POWERED BY PIGBOTFRAMEWORK'.format(self.botSettings.get('name'))
        
        '''
        SendOld(uid, message)
        SendOld(uid, '[CQ:face,id=151] 已私聊发送！', gid)
        '''
        self.send(message)
    
    def cd2(self):
        uid = self.se.get('user_id')
        gid = self.se.get('group_id')
        
        self.chushihuacd()
        message = '[CQ:face,id=151]{0}-菜单'.format(self.botSettings.get('name'))
        num = 1
        for i in self.commandmode:
            if self.findObject('path', i.get('cwd'), self.pluginsList).get('num') != -1 or i.get('cwd')=='':
                if num < 2:
                    message += '\n[CQ:face,id=60] [|{0}|]'.format(i.get('name'))
                    num += 1
                else:
                    message += '   [|{0}|] [CQ:face,id=60]'.format(i.get('name'))
                    num = 1
            
            # if findObject('path', i.get('cwd'), pluginsList).get('num') != -1:
                # message += '\n[CQ:face,id=189] '+str(i.get('name'))
        
        message += '\n[CQ:face,id=54] 发送上面的选项名（注意大小写，不包括[]中括号）即可查看对应的详细指令列表\n在使用指令时尖括号(<>)和方括号分别表示必须的项和可选的项，使用指令时不需要带有这些括号！'
        message += '\n\n[ {0} POWERED BY PIGBOTFRAMEWORK ]'.format(self.botSettings.get('name'))
        self.send(message)
        
    def changePromise(self):
        uuid = self.uuid
        gid = self.se.get('group_id')
        promise = self.message.split(' ')[1]
        command = self.message.split(' ')[0]
        
        defaultPromise = None
        for l in self.pluginsList:
            if commandPluginsList.get(l.get('path')) == None:
                continue
            for i in commandPluginsList.get(l.get('path')):
                if command.lstrip().rstrip() == i.get('content').lstrip().rstrip():
                    defaultPromise = i.get('promise')
        
        if defaultPromise != None and defaultPromise != promise and defaultPromise != 'owner' and defaultPromise != 'ro' and defaultPromise != 'xzy':
            commandCustom = self.selectx('SELECT * FROM `botPromise` WHERE `uuid`="{0}" and `gid`={1} and `command`="{2}"'.format(uuid, gid, command))
            if commandCustom:
                self.commonx('UPDATE `botPromise` SET `promise`="{0}" WHERE `id`={1}'.format(promise, commandCustom[0].get('id')))
            else:
                self.commonx('INSERT INTO `botPromise` (`uuid`,`gid`,`command`,`promise`) VALUES ("{0}", {1}, "{2}", "{3}")'.format(uuid, gid, command, promise))
            self.send('[CQ:face,id=54] 更改成功！')
        else:
            self.send('[CQ:face,id=171] 该指令禁止更改权限或该指令不存在！')
            
    def requestListener(self):
        se = self.se
        botSettings = self.botSettings
        uid = se.get('user_id')
        settings = self.groupSettings
        gid = se.get('group_id')
        
        if se.get('request_type') == 'group':
            if se.get('sub_type') == 'invite' and botSettings.get('autoAcceptGroup') and self.isGlobalBanned == None:
                # 邀请机器人加群
                print('group invite')
                return '{"approve":true}'
            elif uid == yamldata.get('chat').get('owner'):
                # 最高管理员一律同意
                print('group invite')
                return '{"approve":true}'
            elif settings.get('autoAcceptGroup') != 0 and se.get('sub_type') == 'add':
                # 有人要加群
                print('group add')
                if self.isGlobalBanned == None:
                    return '{"approve":true}'
                else:
                    self.SendOld(botSettings.get('owner'), '[CQ:face,id=151] 已禁止用户'+str(uid)+'加群\n原因：'+self.isGlobalBanned.get('reason'), gid)
                
            elif settings.get('autoAcceptGroup') == 0:
                self.send('[CQ:face,id=151] 管理员快来，有人要加群！')
                
        elif se.get('request_type') == 'friend' and botSettings.get('autoAcceptFriend'):
            print('friend')
            if self.isGlobalBanned == None:
                return '{"approve":true}'
            else:
                self.SendOld(botSettings.get('owner'), '[CQ:face,id=151] 已禁止用户'+str(uid)+'加好友\n原因：'+ob.get('reason'), gid)
                self.SendOld(botSettings.get('second_owner'), '[CQ:face,id=151] 已禁止用户'+str(uid)+'加好友\n原因：'+ob.get('reason'), gid)
                
    def noticeListener(self):
        userCoin = self.userCoin
        se = self.se
        gid = se.get('group_id')
        cid = se.get('channel_id')
        uid = se.get('user_id')
        message = se.get('message')
        settings = self.groupSettings
        uuid = self.uuid
        botSettings = self.botSettings
        
        if se.get('notice_type') == 'group_ban' and se.get('user_id') == se.get('self_id'):
            # 禁言机器人
            # checkBan(meta_data)
            pass
        
        elif se.get('notice_type') == 'group_recall' and settings.get('recallFlag') != 0 and se.get('operator_id') != botSettings.get('myselfqn') and se.get('user_id') != botSettings.get('myselfqn'):
            # 消息防撤回
            data = self.CallApi('get_msg', {"message_id":se.get('message_id')})
            if self.weijinWhileFunc(data.get('data').get('message')) == False and 'http' not in data.get('data').get('message'):
                self.send('[CQ:face,id=54] 消息防撤回\n[CQ:at,qq='+str(se.get('operator_id'))+'] 撤回了 [CQ:at,qq='+str(se.get('user_id'))+'] 发送的一条消息\n撤回的消息内容：'+str(data.get('data').get('message')))
            else:
                self.send('[CQ:at,qq='+str(se.get('operator_id'))+'] 撤回了 [CQ:at,qq='+str(se.get('user_id'))+'] 发送的一条不可见人的消息')
            
        elif se.get('notice_type') == 'notify':
            # 戳机器人
            if se.get('sub_type') == 'poke' and se.get('target_id') == botSettings.get('myselfqn'):
                if random.randint(0, 2) == 1:
                    self.send('[CQ:at,qq='+str(se.get('user_id'))+'] 我爱你，別戳了！')
                else:
                    self.send('[CQ:at,qq='+str(se.get('user_id'))+'] 不要再戳我啦！')
                
        elif se.get('notice_type') == 'group_increase':
            # 有人进群
            if settings.get('increase') != 0:
                self.send('[CQ:at,qq='+str(se.get('user_id'))+'] '+str(settings.get('increase_notice')))
            if settings.get('increase_verify') != 0:
                self.increaseVerify()
            
        elif se.get('notice_type') == 'group_decrease' and settings.get('decrease') != 0:
            # 有人退群
            if se.get('sub_type') == 'leave':
                self.send('成员 '+str(se.get('user_id'))+' 主动离开了本群。')
            elif 'kick' in se.get('sub_type'):
                self.send('成员 '+str(se.get('user_id'))+' 被 [CQ:at,qq='+str(se.get('operator_id'))+'] 踢出了本群。')
        
        elif se.get('notice_type') == 'essence':
            # 精华消息
            if se.get('sub_type') == 'add' and settings.get('delete_es') != 0:
                self.CallApi('delete_essence_msg', {'message_id':se.get('message_id')})
                self.send('已自动撤回成员[CQ:at,qq={0}]设置的精华消息'.format(se.get('sender_id')))
            elif se.get('sub_type') == 'delete' and se.get('operator_id') != botSettings.get('myselfqn'):
                data = self.CallApi('get_msg', {"message_id":se.get('message_id')})
                self.send('很不幸，[CQ:at,qq={0}]撤回了一个精华消息\n消息内容：{1}'.format(se.get('operator_id'), data.get('data').get('message')))
    
    def increaseVerifyCommand(self):
        uid = self.se.get('user_id')
        gid = self.se.get('group_id')
        for i in range(len(increaseVerifyList)):
            if increaseVerifyList[i].get('uid') == uid and increaseVerifyList[i].get('gid') == gid:
                if increaseVerifyList[i].get('pswd') == self.message:
                    increaseVerifyList[i]['pswd'] = None
                else:
                    self.send('你这验证码太假了！')
                break
    
    def increaseVerify(self):
        uid = self.se.get('user_id')
        gid = self.se.get('group_id')
        pswd = self.generate_code(4)
        limit = self.groupSettings.get('increase_verify')
        increaseVerifyList.append({"uid":uid,"gid":gid,"pswd":pswd})
        self.send('[CQ:at,qq={0}]\n请在{1}秒内发送指令“人机验证 {2}”\n注意中间有空格！'.format(uid, limit, pswd))
        l = 0
        for i in range(len(increaseVerifyList)):
            if increaseVerifyList[i].get('uid') == uid and increaseVerifyList[i].get('gid') == gid:
                l = i
                break
        while limit >= 0:
            if increaseVerifyList[l].get('pswd') == None:
                increaseVerifyList[l]["pswd"] = "continue"
                self.send('[CQ:at,qq={0}] 恭喜，验证通过！'.format(uid))
                increaseVerifyList.pop(l)
                return
            limit -= 1
            time.sleep(1)
        self.send('[CQ:at,qq={0}] 到时间啦，飞机票一张！'.format(uid))
        self.CallApi('set_group_kick', {'group_id':gid,'user_id':uid})
        increaseVerifyList.remove(l)
    
    def getVerifyStatus(self):
        for i in range(len(increaseVerifyList)):
            if increaseVerifyList[i].get('uid') == self.se.get('user_id') and increaseVerifyList[i].get('gid') == self.se.get('group_id'):
                if increaseVerifyList[l]["pswd"] == "continue":
                    return False
                return True
        return False
    
    def pythonTime(self):
        self.send(time.ctime())
    
    def pornCheckFunc(self):
        self.send(nsfw.main("/pbf/resources/porn.png"))

increaseVerifyList = []