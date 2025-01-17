import sys,logging
import os
import platform

try:
        from PySide2.QtCore import *
except ImportError:
        from PyQt5.QtCore import *
if 'PyQt5' in sys.modules:
        from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
else:
        from PySide2.QtCore import Signal, Slot


Lcdlightpath = '/sys/class/backlight/1-0045/brightness'
SSHonPath = '/lib/systemd/system/ssh.service'
SSHoffPath = '/etc/systemd/system/multi-user.target.wants/ssh.service'
#VNConPath = '/usr/lib/systemd/system/vncserver-x11-serviced.service'
#VNCoffPath = '/etc/systemd/system/multi-user.target.wants/vncserver-x11-serviced.service'

class Settting(QObject):
    # LCD Backlight
    @Slot(int)
    def Lcdlightset(self,val):
        if os.path.isfile(Lcdlightpath):
            os.system('chown pi:pi '+ Lcdlightpath)
            values = '%d'%val
            x = 'echo ' + values + ' > ' + Lcdlightpath
            os.system(x)
        else:
            logging.error("Please set the correct Lcdlight device name path")

    @Slot(result=int)
    def Lcdlightget(self):
        light = os.popen('cat ' + Lcdlightpath).readline().strip("\n")
        return int(light)

    #Camera
    @Slot()
    def Cameraon(self):
        self.Cameraoff()
        os.system("sed -i '$a start_x=1' /boot/config.txt")
        os.system("sed -i '$a gpu_mem=128' /boot/config.txt")
        logging.info("Cameraon on")
    @Slot()
    def Cameraoff(self):
        os.system('sed -i "/start_x=/d" /boot/config.txt')
        os.system('sed -i "/gpu_mem=/d" /boot/config.txt')
        logging.info("Cameraon off")

    @Slot(result=bool)
    def getCamera(self):
        camera = os.popen('grep "^start_x=1" /boot/config.txt').readline().strip("\n")
        if camera == "":
            return False
        else:
            return True

    #SSH
    @Slot()
    def SSHon(self):
        if os.path.isfile(SSHonPath):
            os.system('ln -s ' + SSHonPath + ' ' + SSHoffPath)
            logging.info("SSH ON")
        else:
            logging.error("Please set the correct SSH ON path")
    @Slot()
    def SSHoff(self):
        if os.path.isfile(SSHonPath):
            os.system('rm ' + SSHoffPath)
            logging.info("SSH OFF")
        else:
            logging.error("Please set the correct SSH OFF path")
    @Slot(result=bool)
    def getSSH(self):
        if os.path.isfile(SSHoffPath):
            return True
        else:
            return False

    #VNC
    @Slot()
    def VNCon(self):
        if 'raspberrypi4-64' in platform.uname(): 
            print("yocto not support vnc yet")
        elif 'buildroot' in platform.uname(): 
            print("buildroot not support vnc yet")
        else:
            os.system('systemctl start vncserver-x11-serviced.service')
        logging.info("VNC ON")
    @Slot()
    def VNCoff(self):
        if 'raspberrypi4-64' in platform.uname(): 
            print("yocto not support vnc yet")
        elif 'buildroot' in platform.uname(): 
            print("buildroot not support vnc yet")
        else:
            os.system('systemctl stop vncserver-x11-serviced.service')
        logging.info("VNC ON")
    @Slot(result=bool)
    def getVNC(self):
        if 'raspberrypi4-64' in platform.uname(): 
            vnc="inactive"
            print("yocto not support vnc yet")
        elif 'buildroot' in platform.uname(): 
            vnc="inactive"
            print("buildroot not support vnc yet")
        else:
            vnc = os.popen('systemctl status vncserver-x11-serviced.service | grep "active" | awk \'{print $2}\'').read().strip("\n")
        if (vnc == "active"):
            return True
        elif (vnc == "inactive"):
            return False

    #SPI
    @Slot()
    def SPIon(self):
        self.SPIoff()
        os.system("sed -i '$a dtparam=spi=on' /boot/config.txt")
        logging.info("SPI ON")
    @Slot()
    def SPIoff(self):
        os.system('sed -i "/dtparam=spi=/d" /boot/config.txt')
        logging.info("SPI OFF")
    @Slot(result=bool)
    def getSPI(self):
        spi = os.popen('grep "^dtparam=spi=on" /boot/config.txt').readline().strip("\n")
        if spi == "":
            return False
        else:
            return True

    #I2C
    @Slot()
    def I2Con(self):
        os.system('sed -i "s/.*dtparam=i2c_arm=.*$/dtparam=i2c_arm=on/g" /boot/config.txt')
        logging.info("I2C ON")
    @Slot()
    def I2Coff(self):
        os.system('sed -i "s/.*dtparam=i2c_arm=.*$/#dtparam=i2c_arm=on/g" /boot/config.txt')
        logging.info("I2C OFF")
    @Slot(result=bool)
    def getI2C(self):
        i2c = os.popen('grep "^dtparam=i2c_arm=on" /boot/config.txt').readline().strip("\n")
        if i2c == "":
            return False
        else:
            return True

    #Serial
    @Slot()
    def Serialon(self):
        self.Serialoff()
        os.system("sed -i '$a enable_uart=1' /boot/config.txt")
        logging.info("Serial ON")
    @Slot()
    def Serialoff(self):
        os.system('sed -i "/enable_uart=/d" /boot/config.txt')
        logging.info("Serial OFF")
    @Slot(result=bool)
    def getSER(self):
        ser = os.popen('grep "^enable_uart=1" /boot/config.txt').readline().strip("\n")
        if ser == "":
            return False
        else:
            return True

    #Shutdown
    @Slot()
    def Shutdown(self):
        if 'buildroot' in platform.uname(): 
            os.system('poweroff now')
        elif 'raspberrypi4-64' in platform.uname():
            os.system('poweroff')
        else:
            os.system('shutdown now')
        logging.info("R2 System Shutdown")

    #Reboot
    @Slot()
    def Rebooton(self):
        os.system('reboot')
        logging.info("R2 System Reboot")

    #Logout
    @Slot()
    def Logout(self):
        sys.exit()
