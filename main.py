import sys
sys.path.append('../..')
from bot import bot, commandlist, commandPluginsList, webreloadPlugins

class basic(bot):
    def printConfig(self):
        uid = self.se.get('user_id')
        gid = self.se.get('group_id')
        settings = self.groupSettings or self.getConfig(self.uuid, 'qn', gid, self.sql_config)[0]
        
        message = '[CQ:face,id=151] 本群机器人配置：'
        for i in self.settingName:
            if int(i.get('isHide')) == 1:
                continue
            
            message += '\n[CQ:face,id=161] '+str(i.get('name'))+'：'+str(i.get('description'))+'\n     值：'+str(settings.get(i.get('description')))
            if i.get('other') != '':
                message += '\n     描述：'+str(i.get('other'))
        message += '\n\n[CQ:face,id=189] 请使用 set 指令修改配置\n例如：set recallFlag===0 即为设置取消防撤回功能'
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
                self.send('[CQ:face,id=189] 错误截获\n{0}'.format(e))
                
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
                self.send('[CQ:face,id=189] 指令帮助\n[CQ:face,id=161] 指令内容：'+str(i.get('content'))+'\n[CQ:face,id=161] 指令用法：'+str(i.get('usage'))+'\n[CQ:face,id=161] 指令解释：'+str(i.get('description'))+'\n[CQ:face,id=161] 指令权限：'+promisetext+'\n[CQ:face,id=161] 指令分类：'+str(i.get('mode')))
                return 
        self.send('没有这个指令呢qwq')
        
    def cd(self):
        uid = self.se.get('user_id')
        gid = self.se.get('group_id')
        
        message = '[CQ:face,id=151]{0}-菜单'.format(self.botSettings.get('name'))
        for i in commandlist:
            message += '\n[CQ:face,id=161] '+i.get('content')+'\n用法：'+i.get('usage')+'\n解释：'+i.get('description')+'\n权限：'
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
                    message += '\n[CQ:face,id=60] '+str(i.get('name'))
                    num += 1
                else:
                    message += '   '+str(i.get('name'))+' [CQ:face,id=60]'
                    num = 1
            
            # if findObject('path', i.get('cwd'), pluginsList).get('num') != -1:
                # message += '\n[CQ:face,id=189] '+str(i.get('name'))
        
        message += '\n[CQ:face,id=161] 发送上面的选项名 （注意大小写）即可查看对应的详细指令列表\n在使用指令时尖括号(<>)和方括号分别表示必须的项和可选的项，使用指令时不需要带有这些括号！'
        message += '\n\n{0} POWERED BY PIGBOTFRAMEWORK'.format(self.botSettings.get('name'))
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
            self.send('[CQ:face,id=161] 更改成功！')
        else:
            self.send('[CQ:face,id=171] 该指令禁止更改权限或该指令不存在！')