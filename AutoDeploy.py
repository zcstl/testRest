import paramiko


class DeployTemplate():
    def __init__(self, host, user, pwd):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.ssh_client = None

    def initConn(self):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(self.host, 22, self.user, self.pwd)
        except Exception, e:
            print('ssh %s@%s: %s' % (self.user, self.host, e))
            exit()
        self.ssh_client = ssh_client



    def doBefore(self):
        self.initConn()

    def doAfter(self):
        pass

    def mainLogic(self):
        pass

    def execute(self):
        self.doBefore();
        self.mainLogic();
        self.doAfter();


class Docker(DeployTemplate):
    def __init__(self):
        super(Docker, self).__init__();

    def mainLogic(self):
        pass


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
    pass

if '__name__' == '__main__':
    main()