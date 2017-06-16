import paramiko


class DeployTemplate(object):
    def __init__(self, host, user, pwd):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.ssh_client = None

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


class Docker(DeployTemplate):
    def __init__(self, host, user, pwd):
        super(Docker, self).__init__(host, user, pwd)

    def mainLogic(self):
        stdin, stdout, stderr = self.doCmd("echo tt")
        print stdout.readlines()


class Chart(DeployTemplate):
    def __init__(self):
        super(Chart, self).__init__();

    def mainLogic(self):
        pass


class Setup(DeployTemplate):
    def __init__(self):
        super(Setup, self).__init__();

    def mainLogic(self):
        pass


def main():
    docker = Docker('192.168.56.101', 'zcsubuntu', 'zcszcszcs')
    docker.execute()

if '__name__' == '__main__':
    main()

main()