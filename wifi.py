
import network

wlan = network.WLAN(network.STA_IF)

def close():
    wlan.active(False)

def start(delay = 10):
    try:
        import wifi_cfg
        
        close()

        if wifi_cfg.WIFI_MODE == 's':
            print("Started wifi in smartconfig mode")
            print(network.smartconfig())
        elif wifi_cfg.WIFI_MODE == 'n':
            print("Started wifi in normal mode")
            wlan.active(True)
            wlan.connect(wifi_cfg.WIFI_SSID, wifi_cfg.WIFI_PASW)
        print(delay, 'secends waiting network connected......')
        
        import utime
        last_time = utime.time()
        while (utime.time() < last_time + delay):
            if(wlan.isconnected()):
                break
                
        if(wlan.isconnected() is False):
            print("wifi connect fail, check wifi_cfg.py or run 'import wifi_setup', please")
            close()
    except:
        print("wifi is not configured, run 'import wifi_setup'")

