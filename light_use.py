import subprocess

class ShellCMD(object):
    def __init__(self, icmd_ls):
        super(ShellCMD, self).__init__()
        self.icmd_ls = icmd_ls
        self.GetShells(icmd_ls)


    def GetShells(self,cmd_ls):

        for shell in cmd_ls:
            self.GetShell(shell)
        pass

    def GetShell(self,cmd):

        try:
            err = subprocess.run(cmd.split())
            # print("l_Level=",", err=",err.returncode)
        except:
            print("Помилка команди",cmd)
        pass


def main():
    icmd=[
            'gpio -g pwm 18 1024',
            'gpio -g mode 18 pwm',
            'gpio pwmc 1000',
        ]
    mcmd='gpio -g pwm 18 '

    S=ShellCMD(icmd)
    while True:
        lightLevel = float(input("Задайте рівень освітлення від 0 до 1024: "))
        lightLevel = mcmd+str(lightLevel)
        S.GetShell(lightLevel)


if __name__=="__main__":
   main()