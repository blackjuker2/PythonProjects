import subprocess
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--iface", dest="iface", help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.iface:
        parser.error("[-] Please enter an interface, use --help for more info.")
    elif not options.mac:
        parser.error("[-] Please enter an MAC address, use --help for more info.")
    return options


def macchanger(iface, mac):
    print(f"[+] Changing the MAC address for {iface} to {mac}")
    subprocess.call(["ifconfig", iface, "down"])
    subprocess.call(["ifconfig", iface, "hw", "ether", mac])
    subprocess.call(["ifconfig", iface, "up"])


def main():
    options = get_arguments()
    macchanger(options.iface, options.mac)


if __name__ == "__main__":
    main()
