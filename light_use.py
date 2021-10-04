import subprocess
import csv
import datetime

class ShellCMD(object):
    def __init__(self, shell_cmd):
        super(ShellCMD, self).__init__()
        self.icmd_ls = shell_cmd[0]
        self.start_cmd=shell_cmd[1]
        self.GetShells(self.icmd_ls)

        self.logFILENAME = "example_log.csv"
        vparam=['DateTime','InputLx','DisplaylightLevel','Errors']
        self.addToFile(vparam)


    def GetShells(self,cmd_ls):

        for shell in cmd_ls:
            self.GetShell(shell)
        pass

    def GetShell(self,cmd):
        error = ''
        try:
            err = subprocess.run(cmd.split())
            
            # print("l_Level=",", err=",err.returncode)
        except:
            error="Помилка команди: "+cmd
            print(error)
        return error

    def SetLight(self,level):
        log=['','','','']
        x = datetime.datetime.now()
        
        log[0]=x.strftime("%d-%m-%Y %H:%M:%S")
        log[1]='0'
        log[2]=str(level)
        cmd=self.start_cmd+' '+log[2]
        log[3]=self.GetShell(cmd)
        self.addToFile(log)
        pass





    def addToFile(self,log):     
        try:
            with open(self.logFILENAME, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerows([log]) 
        except:
            print("Помилка запису в файл",self.logFILENAME)
        pass


def main():
    shell_cmd=[
                    ['gpio -g pwm 18 1024',
                    'gpio -g mode 18 pwm',
                    'gpio pwmc 1000'],
                    'gpio -g pwm 18 '
                ]

    Display=ShellCMD(shell_cmd)
    
    while True:
        lightLevel = float(input("Задайте рівень освітлення від 0 до 1024: "))
        Display.SetLight(lightLevel)



if __name__=="__main__":
   main()