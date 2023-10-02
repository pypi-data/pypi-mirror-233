import os
from ShynaDatabase import Shdatabase


class ShynaCharge:

    def check_charge(self):
        try:
            dic_charge = os.popen('termux-battery-status').read()
            dic_charge = eval(dic_charge)
            charge = dic_charge['percentage']
            status = dic_charge['status']
            if int(charge) < 15 and str(status).lower() == 'discharging':
                cmd = 'termux-tts-speak "Hey! Shiv please plugin the charger. My battery is low"'
                os.popen(cmd)
            elif int(charge) > 95 and str(status).lower() == 'full':
                cmd = 'termux-tts-speak "Hey! Shiv please unplug the charger. My battery is full"'
                os.popen(cmd)
            else:
                pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    ShynaCharge().check_charge()
