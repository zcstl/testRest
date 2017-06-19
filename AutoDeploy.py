# coding=utf-8
import paramiko
import json
import re

class DeployTemplate(object):
    def __init__(self, host, user, pwd, params):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.ssh_client = None
        self.params = params


    def initSSHConn(self):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(self.host, 22, self.user, self.pwd)
        except Exception, e:
            print('ssh %s@%s: %s' % (self.user, self.host, e))
            exit()
        self.ssh_client = ssh_client

    def doCmd(self, cmd):
        return self.ssh_client.exec_command(cmd)

    def closeSSHConn(self):
        self.ssh_client.close()

    def getCdStr(self):
        return 'cd ' + self.params.getVal('workDir')

    def generateCmd(self, cmdList):
        cmd = ''
        for tt in cmdList:
            cmd += tt + ';'
        return cmd

    def isSureRun(self, cmd):
        respon = raw_input('Sure for running ' + cmd + '? Please input y or n:  ')
        if respon == 'y':
            return True
        elif respon == 'n':
            return False
        else:
            print '***********Please input y or n***********'
            return self.isSureRun(cmd)

    def runCmdList(self, cmdList):
        try:
            cmd = self.generateCmd(cmdList)
            if self.isSureRun(cmd):
                pass
                #stdin, stdout, stderr = self.doCmd(cmd)
                #print 'The stdout is: ' , stdout.readlines()
            else:
                print 'pass this cmd: ' + cmd
        except BaseException, msg:
            print msg
            self.closeSSHConn()

    def extractIP(self, str):
        pattern = re.compile(
            r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))")
        return pattern.search(str).group()  #为空 异常

    def extractIpFromStrList(self, strList, hostName):
        pattern = re.compile(
            r"^ff.*((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))$")


    def doBefore(self):
        self.initSSHConn()

    def doAfter(self):
        self.closeSSHConn()

    def mainLogic(self):
        pass

    def execute(self):
        self.doBefore()
        self.mainLogic()
        self.doAfter()

class Environment(DeployTemplate):
    '''负责环境准备，包括文件准备，环境清理'''
    def __init__(self, host, user, pwd):
        super(Docker, self).__init__(host, user, pwd)

    def mainLogic(self):
        cmd = self.getCdStr()
        stdin, stdout, stderr = self.doCmd(cmd)
        print stdout.readlines()



class Docker(DeployTemplate):
    '''负责镜像上传'''
    def __init__(self, host, user, pwd, params):
        super(Docker, self).__init__(host, user, pwd, params)

    def mainLogic(self):
        '''
        sudo docker load -i /tmp/zcs/cpe-builder-0.3.0.tar.gz
        sudo docker tag cpe-builder:0.3.0 ip:20202/root/cpe-builder:0.3.0
        sudo docker push 100.101.58.80:20202/root/cpe-builder:0.3.0
        '''
        #imgList = ['website', 'service', 'builder', 'assembling']
        imgList = ['website', 'builder', 'service', 'assembling']
        cmdList = []
        for img in imgList:
            cmd = 'sudo docker load -i ' + self.params.getVal('imageDir') + '/'+ self.params.getVal('images-' + img + '-fileNmae')
            cmdList.append(cmd)
            cmd = 'sudo docker tag ' + self.params.getVal('images-' + img + '-name') + ' ' + self.params.getVal('images-' + img + '-tag')
            cmdList.append(cmd)
            cmd = 'sudo docker push ' + self.params.getVal('images-' + img + '-tag')
            cmdList.append(cmd)
            self.runCmdList(cmdList)
            cmdList = []


class Chart(DeployTemplate):
    '''负责chart package上传'''
    def __init__(self, host, user, pwd, params):
        super(Docker, self).__init__(host, user, pwd, params)

    def mainLogic(self):
        '''
        curl -k -X POST https://100.101.58.80:32800/v2/charts -H "Content-Type:multipart/form-data" -F content=@cpe-assembling-1.0.2.tgz -H "Domain:manage"
        '''
        #imgList = ['website', 'service', 'builder', 'assembling']
        imgList = ['website', 'builder', 'service', 'assembling']
        cmdList = []
        for img in imgList:
            cmd = 'sudo docker load -i ' + self.params.getVal('imageDir') + '/'+ self.params.getVal('images-' + img + '-fileNmae')
            cmdList.append(cmd)
            cmd = 'sudo docker tag ' + self.params.getVal('images-' + img + '-name') + ' ' + self.params.getVal('images-' + img + '-tag')
            cmdList.append(cmd)
            cmd = 'sudo docker push ' + self.params.getVal('images-' + img + '-tag')
            cmdList.append(cmd)
            self.runCmdList(cmdList)
            cmdList = []

class Setup(DeployTemplate):
    '''负责模板建立，堆栈安装'''
    def __init__(self, host, user, pwd, params):
        super(Docker, self).__init__(host, user, pwd, params)

    def mainLogic(self):
        '''
        tar -zcvf TOSCA-as-api-server-1.0.6.tgz blueprint.yaml
        '''
        #imgList = ['website', 'service', 'builder', 'assembling']
        imgList = ['website', 'builder', 'service', 'assembling']
        cmdList = []
        for img in imgList:
            cmd = 'sudo docker load -i ' + self.params.getVal('imageDir') + '/'+ self.params.getVal('images-' + img + '-fileNmae')
            cmdList.append(cmd)
            cmd = 'sudo docker tag ' + self.params.getVal('images-' + img + '-name') + ' ' + self.params.getVal('images-' + img + '-tag')
            cmdList.append(cmd)
            cmd = 'sudo docker push ' + self.params.getVal('images-' + img + '-tag')
            cmdList.append(cmd)
            self.runCmdList(cmdList)
            cmdList = []


class ParamsInterface(object):
    def getVal(self, key):
        pass
    def setVal(self, key, val):
        pass

class Params(ParamsInterface):
    '''全局参数字典'''
    def __init__(self, jsonFile):
        pass
        # self.paramsDict =self.paraseJsonFile(jsonFile)

    def getVal(self, key):
        return self.paramsDict[key]

    def setVal(self, key, val):
        self.paramsDict[key] = val

    def paraseJsonFile(self, jsonFile):
        try:
            js = json.load(file(jsonFile))
            dict = {}

            dict['workDir'] = self.pareseNodePath(js, ['workDir'])
            dict['imageDir'] = self.pareseNodePath(js, ['imageDir'])

            #docker images paras parese
            imgList = ['website', 'builder', 'service', 'assembling']
            for img in imgList:
                dict['images-' + img + '-fileNmae'] = self.pareseNodePath(js, ['images', img, 'fileName'])
                dict['images-' + img + '-name'] = self.pareseNodePath(js, ['images', img, 'name']) + ':' + self.pareseNodePath(js, ['images', img, 'tag'])
                dict['images-' + img + '-tag'] = self.pareseNodePath(js, ['omVip']) + ':' \
                                             + self.pareseNodePath(js, ['images', 'port']) \
                                             + '/' + self.pareseNodePath(js, ['images', 'user']) \
                                             + '/' + dict['images-' + img + '-name']
            #chart package
            for img in imgList:
                pass
        except ValueError, e:
            print e

        return dict

    def autoParaseJsonFile(self, jsonFile):
        try:
            js = json.load(file(jsonFile))
        except IOError:
            print 'File is not existed!'
            exit()
        tdict = {}
        path = []
        self.dfs(tdict, js.keys(), js.values(), path)
        return tdict

    def dfs(self, destDict, keys, vals, path):
        for i, key in enumerate(keys):
            val = vals[i]
            if len(path) == 0:
                if (type(val) != dict) & (type(val) != list):
                    destDict[key] = val
                else:
                    path.append(key)
                    self.dfs(destDict, val.keys(), val.values(), path)
            else:
                if (type(val) != dict) & (type(val) != list):
                    destDict['-'.join(path) + '-' + key] = val
                else:
                    path.append(key)
                    self.dfs(destDict, val.keys(), val.values(), path)
        if len(path) != 0:
            path.pop()


    def pareseNodePath(self, js, nodeList):
        for node in nodeList:
            js = js.get(node)
        return js

def main():
    try:
        # params = Params('paramsTmp.json')
        # docker = Docker('100.101.58.105', 'root', 'Huawei@123', params)
        # docker.execute()
        d = Params('test.json').autoParaseJsonFile('/Users/zhangcs/PycharmProjects/AutoDeploy/test.json')
        for i in d:
            print i, d[i]
    except BaseException, e:
        print e
        # docker.closeSSHConn()

if '__name__' == '__main__':
    main()

main()
