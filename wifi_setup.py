import sys
import os

RC = "./boot.py"
CONFIG = "./wifi_cfg.py"

def input_choice(prompt, choices):
    while True:
        resp = input(prompt)
        if resp in choices:
            return resp

def input_get(prompt):
    return input(prompt)

def input_ssid():
    while True:
        wifi_ssid = input_get("New wifi_ssid (1-32 chars): ")
        if 1 < len(wifi_ssid) and len(wifi_ssid) < 32:
            return wifi_ssid
        else:
            print("Invalid wifi_ssid length")

def input_pasw():
    while True:
        wifi_pasw = input_get("New wifi_pasw (5-13 chars): ")
        if 5 < len(wifi_pasw) and len(wifi_pasw) < 13:
            return wifi_pasw
        else:
            print("Invalid wifi_ssid length")

def exists(fname):
    try:
        with open(fname):
            pass
        return True
    except OSError:
        return False


def get_daemon_status():
    with open(RC) as f:
        for l in f:
            if "wifi" in l:
                if l.startswith("#"):
                    return False
                return True
        return None


def change_daemon(action):
    LINES = ("import wifi", "wifi.start()")
    with open(RC) as old_f, open(RC + ".tmp", "w") as new_f:
        found = False
        for l in old_f:
            for patt in LINES:
                if patt in l:
                    found = True
                    if action and l.startswith("#"):
                        l = l[1:]
                    elif not action and not l.startswith("#"):
                        l = "#" + l
            new_f.write(l)
        if not found:
            new_f.write("\nimport wifi\nwifi.start()\n")
    # FatFs rename() is not POSIX compliant, will raise OSError if
    # dest file exists.
    os.remove(RC)
    os.rename(RC + ".tmp", RC)


def main():
    status = get_daemon_status()

    print("Network WIFI auto-start status:", "enabled" if status else "disabled")
    print("\nWould you like to (e)nable or (d)isable it running on boot?")
    print("(Empty line to quit)")
    resp = input("> ").lower()

    if resp == "e":
        resp1 = input_choice("Would you like to (s)martconfig or (n)ormal? (s/n) ", ("s", "n", ""))

        if resp1 == 's' or resp1 == '':
            with open(CONFIG, "w") as f:
                f.write("WIFI_MODE = 's'\n")

        elif resp1 == 'n':
            print("To enable WIFI, you must set ssid for it")
            ssid = input_ssid()
            print("To enable WIFI, you must set pasw for it")
            pasw = input_pasw()
            with open(CONFIG, "w") as f:
                f.write("WIFI_SSID = '%s'\n" % ssid)
                f.write("WIFI_PASW = '%s'\n" % pasw)
                f.write("WIFI_MODE = 'n'\n")

    if resp not in ("d", "e"):
        print("No further action required")
        sys.exit()

    change_daemon(resp == "e")

    print("Changes will be activated after reboot")
    resp = input_choice("Would you like to reboot now? (y/n) ", ("y", "n", ""))
    if resp == "y":
        import machine
        machine.reset()

main()
