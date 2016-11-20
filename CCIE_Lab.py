try:
    import paramiko
    import os
    from scp import SCPClient
    import time
    import getpass

except:
    print("try to install the needed modules with PiP (python installer program/"
          "you are probably missing paramiko, scp or getpass")
    #os.system("c:\Python34\Scripts\pip.exe install paramiko")


def f_menu():
    print("Option 1: lab1 advanced.foundation.labs")
    print("Option 2: lab2 advanced.practice.labs (full lab)")
    print("Option 3: lab3 advanced.technology.labs")
    print("Option 4: lab4 advanced.troubleshooting.labs")
    return int(input("please select an script to run : (number)"))

def path(option):
    cnt = 0
    lst = []

    pth = "c:/Learning/Cisco/CCIE/INE-CCIEv5-R&S/Books/lab_cfgs/"

    if option == 1:
        files = os.path.join(pth, "advanced.foundation.labs/foundation.lab.1/")
    if option == 2:
        files = os.path.join(pth, "advanced.practice.labs/rsv5.full.scale.lab.1.initial/")

    if option == 3:
        files = os.path.join(pth, "advanced.technology.labs")

        for x in os.listdir(files):
            print("lab Choice %s  %s" % (str(cnt), x))
            lst.append(x)
            cnt += 1
        sub = int(input("please choice you're lab number"))
        print(lst)
        files = os.path.join(pth, "advanced.technology.labs/%s/" % lst[sub])

    if option == 4:
        files = os.path.join(pth, "advanced.troubleshooting.labs")

        for x in os.listdir(files):
            print("lab_sub_choice" + x)

        sub = input()
        files = os.path.join(pth, "advanced.troubleshooting.labs")
    return files


def upload_cfg(option):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()

    routers = {"R1": "10.200.0.1"}#, "R2": "10.200.0.1" , "R3": "10.200.0.1" ,"R4": "10.200.0.1", "R5": "10.200.0.1",
               #"R6": "10.200.0.1", "R7": "10.200.0.1", "R8": "10.200.0.1", "R9": "10.200.0.1", "R10": "10.200.0.1"}

    for x in routers:

        #open ssh session for SCP usage.
        ssh.connect(routers[x], username='admin', password='cisco', look_for_keys=False, allow_agent=False)
        files = option + x.lower() + ".txt"
        scp = SCPClient(ssh.get_transport())

        scp.put(files, "flash:upload.txt")
        ssh.close()

        #Open new session for ssh commands the Get_transport will not allow extra commands.
        ssh.connect(routers[x], username='admin', password='cisco', look_for_keys=False, allow_agent=False)
        session = ssh.invoke_shell()

        output = session.recv(65535)
        print(output)

        session.send("copy flash:upload.txt running\n")
        time.sleep(1)
        session.send("\n")

        output = session.recv(65535)
        print(output)

        ssh.close()


if __name__ == '__main__':
   menu = f_menu()
   pth = path(menu)
   upload_cfg(pth)

