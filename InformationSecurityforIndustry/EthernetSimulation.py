import os

class EthernetData(object) :
    def __init__(self,OriginalAdd,DestinationAdd,TransportData):
        if '-' in OriginalAdd :
            OriginalAdd = ''.join(OriginalAdd.split('-'))
        elif ':' in OriginalAdd :
            OriginalAdd = ''.join(OriginalAdd.split(':'))
        if '-' in DestinationAdd :
            DestinationAdd = ''.join(DestinationAdd.split('-'))
        elif ':' in DestinationAdd :
            DestinationAdd = ''.join(DestinationAdd.split(':'))
        self.__OriginalAddress = OriginalAdd
        self.__DestinationAddress = DestinationAdd
        self.__Data = TransportData

    def Encode(self,s1):
        return ''.join([bin(ord(ch)).replace('0b','') for ch in s1])

    def PartI(self):
        headerI  = '10101010'
        headerII = '10101011'
        Combine = hex(int(headerI,2))*7+hex(int(headerII,2))
        return Combine


    def PartII(self):
        BinMAC1 = self.Encode(self.__OriginalAddress)
        if len(BinMAC1) >= 48 :
            return BinMAC1[0:48]
        else :
            return '0'*(48-len(BinMAC1))+BinMAC1

    def PartIII(self):
        BinMAC2 = self.Encode(self.__DestinationAddress)
        if len(BinMAC2) >= 48:
            return BinMAC2[0:48]
        else:
            return '0' * (48 - len(BinMAC2)) + BinMAC2

    def PartIV(self):
        return '0' * (16 - len(bin(self.__Data))+2) + bin(self.__Data)[2:]

    def PartV(self):
        return '101010101010101000000011'

    def PartVI(self):
        return bin(self.__Data)[2:]

    def PartVII(self):
        return '00000000' * 4

    def Total(self):
        return self.PartI()+self.PartII()+self.PartIII()+self.PartIV()+self.PartV()+self.PartVI()+self.PartVII()

if __name__ == '__main__':
    c = EthernetData('58:FB:84:8C:22:11','58-FB-84-8C-22-11',23)
    print(c.PartI())
    print(c.Total())
