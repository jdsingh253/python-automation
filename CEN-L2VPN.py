# Importing modules
import paramiko as pmk, time, getpass, sys, os, pandas as pd

def start():
    print('\n')
    print('*********************************************')
    print('*                                           *')
    print('*              CEN L2VPN TOOL               *')
    print('*                                           *')
    print('*********************************************')
    print('\n')

# SSH conncection for CEN Server
def server_login():
    print('* Connecting to CEN Server')
    print('\n')
    ssh_server = pmk.SSHClient()
    # Allowing the machine to trust the server
    ssh_server.set_missing_host_key_policy(pmk.AutoAddPolicy())
    try:
        ssh_server.connect(hostname='10.227.244.80', port='22', username='prov', password='Airtel@123')
        global ssh
        ssh = ssh_server.invoke_shell()
        print('* Server Logged In')
        time.sleep(5)
        ssh.send("\n")
    except:
        print("* Unable to login server")
        rst = input("Do you want to continue [Y/N] ? ",).lower()
        if rst == 'y':
            main()
        else:
            print('\n')
            print("* The program will now exit.")
            time.sleep(5)
            sys.exit()

# Empty entry for delay in CEN server
def emptyentry():
    i = 0 #pylint: disable=unused-variable
    for i in range(3):
        ssh.send("\n")
        time.sleep(0.5)

# Input for Router IP & credentials
def rtr_login_inp():
    global rtr_ip, rtr_usr, rtr_pswd
    print("Kindly enter the Router IP & credentials.")
    rtr_ip = input("Router IP: ",)
    rtr_usr = input("Username: ",)
    rtr_pswd = getpass.getpass("Password: ")
    return rtr_ip, rtr_usr, rtr_pswd


# SSH connection for CEN Router and l2vpn up command
def xconnect_up(rtr_ip, rtr_usr, rtr_pswd):
    ssh.send('ssh ' + rtr_ip + " " +rtr_usr)
    ssh.send("\n")
    time.sleep(5)
    ssh.send(rtr_pswd)
    ssh.send("\n")
    time.sleep(5)
    ssh.send("terminal length 0")
    ssh.send("\n")
    time.sleep(5)
    print('\n')
    print('* {} >> show l2vpn xconnect state up'.format(rtr_ip))
    ssh.send("show l2vpn xconnect state up")
    ssh.send("\n")
    time.sleep(30)
    output1 = ssh.recv(9999999999).decode()
    time.sleep(10)
    print('* Done')
    output2 = output1.splitlines()
    data=[]
    final=[]
    os.chdir('C:\\Users\\B0214902\\Desktop')
    for i in output2:
        if i=='----------------------------------------------------------------------------------------':
            final.append(data)
            data=[]
        else:
            b=i.split(' ')
            for j in b:
                if j != '':
                    data.append(j)
    df1=pd.DataFrame(final)
    df1.to_csv("xconnect_up.csv")

# SSH connection for CEN Router and l2vpn down command
def xconnect_down(rtr_ip, rtr_usr, rtr_pswd):
    ssh.send('ssh ' + rtr_ip + " " +rtr_usr)
    ssh.send("\n")
    time.sleep(5)
    ssh.send(rtr_pswd)
    ssh.send("\n")
    time.sleep(5)
    ssh.send("terminal length 0")
    ssh.send("\n")
    time.sleep(5)
    print('\n')
    print('* {} >> show l2vpn xconnect state down'.format(rtr_ip))
    ssh.send("show l2vpn xconnect state down")
    ssh.send("\n")
    time.sleep(30)
    output1 = ssh.recv(9999999999).decode()
    time.sleep(10)
    print('* Done')
    output2 = output1.splitlines()
    data=[]
    final=[]
    os.chdir('C:\\Users\\B0214902\\Desktop')
    for i in output2:
        if i=='----------------------------------------------------------------------------------------':
            final.append(data)
            data=[]
        else:
            b=i.split(' ')
            for j in b:
                if j != '':
                    data.append(j)
    df2=pd.DataFrame(final)
    df2.to_csv("xconnect_down.csv")

# SSH connection for CEN Router and l2vpn unresolved command
def xconnect_unr(rtr_ip, rtr_usr, rtr_pswd):
    ssh.send('ssh ' + rtr_ip + " " +rtr_usr)
    ssh.send("\n")
    time.sleep(5)
    ssh.send(rtr_pswd)
    ssh.send("\n")
    time.sleep(5)
    ssh.send("terminal length 0")
    ssh.send("\n")
    time.sleep(5)
    print('\n')
    print('* {} >> show l2vpn xconnect state unresolved'.format(rtr_ip))
    ssh.send("show l2vpn xconnect state unresolved")
    ssh.send("\n")
    time.sleep(30)
    output1 = ssh.recv(9999999999).decode()
    time.sleep(10)
    print('* Done')
    output2 = output1.splitlines()
    data=[]
    final=[]
    os.chdir('C:\\Users\\B0214902\\Desktop')
    for i in output2:
        if i=='----------------------------------------------------------------------------------------':
            final.append(data)
            data=[]
        else:
            b=i.split(' ')
            for j in b:
                if j != '':
                    data.append(j)
    df3=pd.DataFrame(final)
    df3.to_csv("xconnect_unr.csv")

# Logout the CEN Server
def stop():
    ssh.send("\n")
    ssh.send("exit")
    ssh.send("\n")
    time.sleep(3)
    ssh.send("exit")
    ssh.send("\n")
    time.sleep(3)

# Generation of csv file
def report():
    os.chdir('C:\\Users\\B0214902\\Desktop')
    df1=pd.read_csv("xconnect_up.csv")
    df2=pd.read_csv("xconnect_down.csv")
    df3=pd.read_csv("xconnect_unr.csv")
    df1 = df1.iloc[1:]
    df2 = df2.iloc[1:]
    df3 = df3.iloc[1:]
    df1 = df1[['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14']]
    df2 = df2[['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14']]
    df3 = df3[['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14']]
    df4=pd.concat([df1,df2,df3], ignore_index=True)
    df4.to_csv("All_xconnect.csv")
    print("\n")
    print("* The report is generated and available at your desktop.")
    print("\n")
    rst = input("Do you want to continue [Y/N] ? ",).lower()
    if rst == 'y':
        main()
    else:
        print('\n')
        print("* The program will now exit.")
        time.sleep(5)
        sys.exit()


def main():
    start()
    server_login()
    emptyentry()
    rtr_login_inp()
    xconnect_up(rtr_ip, rtr_usr, rtr_pswd)
    xconnect_down(rtr_ip, rtr_usr, rtr_pswd)
    xconnect_unr(rtr_ip, rtr_usr, rtr_pswd)
    stop()
    report()

if __name__ == "__main__":
    main()
