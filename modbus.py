# Title : modbus.py
# Description : Interface simplifiée pour liaision Modbus
# Detail :
#     - Ce module est dédié aux cours de supervision
#     - Il se peut qu'il ne fonctionne pas hors de ce cadre
#
# Author : Pierre Chatelain
# Date : 22 mars 2024
#

try: 
    from pymodbus.client import ModbusTcpClient
except:
    print()
    print("Pour utiliser pymodbus, il faut d'abord l'installer :")
    print(">> python -m pip install pymodbus")
    print()

class Modbus:
    def __init__(self,adresse="127.0.0.1",port=9502):
        self.client = ModbusTcpClient(adresse,port)
        self.client.connect()
        
    def ecrireBit(self,adresse,valeur):
        adresse = adresse - 1
        self.client.write_coils(adresse,valeur)
        
    def lireBit(self,adresse):
        adresse = adresse - 1
        resultat = self.client.read_coils(adresse,count=1)
        return resultat.getBit(0)
        
    def lireOctet(self,adresse):
        adresse = adresse - 1
        resultat = self.client.read_coils(adresse,count=8).bits
        puissance = 1
        res = 0
        for i in range(8):
            if resultat[i]:
                res = res + puissance
            puissance = puissance * 2
        return res
        
    def lireMot(self,adresse):
        adresse = adresse - 1
        resultat = self.client.read_coils(adresse,count=16).bits
        puissance = 1
        res = 0
        for i in range(16):
            if resultat[i]:
                res = res + puissance
            puissance = puissance * 2
        return res
        
    def ecrireRegistre(self,adresse,valeur):
        adresse = adresse - 1
        self.client.write_register(adresse,valeur)
        
    def lireRegistre(self,adresse):
        adresse = adresse - 1
        resultat = self.client.read_input_registers(adresse,count=1)
        return resultat.getRegister(0)
        
    def lireRegistreEntree(self,adresse):
        adresse = adresse - 1
        resultat = self.client.read_input_registers(adresse,count=1)
        return resultat.getRegister(0)

    def close(self):
        self.client.close()