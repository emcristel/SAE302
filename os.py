import platform
import cpuinfo
import netaddr # install with pip install netaddr
import netifaces # install with pip install netifaces

print(f"Architecture: {platform.architecture()}")
print(f"Network Name: {platform.node()}")
print(f"Operating system: {platform.platform()}")
print(f"Processor: {platform.processor()}")

my_cpuinfo = cpuinfo.get_cpu_info()
print(my_cpuinfo)


netifaces.interfaces()
adresse_ip = netifaces.ifaddresses('en0')[2][0]['addr']
netaddr_adresse_ip = netaddr.IPAddress(adresse_ip)
print(f"Mon ip est {netaddr_adresse_ip}")


def __actionOk(self):
        mess=self.text.text()
        self.message.setText(f"Bonjour {mess} !")
        try:
            if self.choix.currentText() == "OS":
                os= platform.platform()
                self.info.setText(f"Operating system: {os}")
            elif self.choix.currentText() == "CPU":
                my_cpuinfo = cpuinfo.get_cpu_info()
                self.info.setText(f"CPU: {my_cpuinfo}")
            elif self.choix.currentText() == "IP":
                netifaces.interfaces()
                adresse_ip = netifaces.ifaddresses('en0')[2][0]['addr']
                netaddr_adresse_ip = netaddr.IPAddress(adresse_ip)
                self.info.setText(f"Mon ip est {netaddr_adresse_ip}")
        except ValueError:
            QMessageBox.critical(self, "Erreur")

def __actionQuitter(self):
        QCoreApplication.exit(0)

def __actionAide(self):
        QMessageBox.information(self, "Aide","Choisissez une information du pc, de la vm que vous voullez récupérer (l'os, le nom, l'ip, ...).")

