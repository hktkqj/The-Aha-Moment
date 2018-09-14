# !/usr/bin/python
# -*- coding : UTF-8 -*-
# File name : SCADA server.py
class EthernetData(object) :
    def __init__(self, OriginalAdd, DestinationAdd, TransportData):
        if '-' in OriginalAdd:
            OriginalAdd = ''.join(OriginalAdd.split('-'))
        elif ':' in OriginalAdd:
            OriginalAdd = ''.join(OriginalAdd.split(':'))
        if '-' in DestinationAdd:
            DestinationAdd = ''.join(DestinationAdd.split('-'))
        elif ':' in DestinationAdd:
            DestinationAdd = ''.join(DestinationAdd.split(':'))
        OriginalAdd = OriginalAdd.upper()
        DestinationAdd = DestinationAdd.upper()
        self.__OriginalAddress = OriginalAdd
        self.__DestinationAddress = DestinationAdd
        self.__Data = TransportData

    def Change(self,char):
        if ord('0')<=ord(char)<=ord('9') :
            return str(bin(ord(char)-ord('0')))
        else :
            return str(bin(ord(char)-ord('A')+10))

    def Encode(self,s1):
        return ''.join([self.Change(ch).replace('0b','').zfill(4) for ch in s1])

    def PartI(self):
        headerI  = '10101010'
        headerII = '10101011'
        Combine = hex(int(headerI,2))*7+hex(int(headerII,2))
        Combine = Combine.upper()
        return ''.join([self.Change(ch).replace('0b','') for ch in Combine.replace('0X','')])

    def PartII(self):
        BinMAC1 = self.Encode(self.__OriginalAddress)
        if len(BinMAC1) >= 48 :
            return BinMAC1[0:49]
        else :
            return BinMAC1.zfill(48)

    def PartIII(self):
        BinMAC2 = self.Encode(self.__DestinationAddress)
        if len(BinMAC2) >= 48:
            return BinMAC2[0:49]
        else:
            return BinMAC2.zfill(48)

    def PartV(self):
        return '101010101010101000000011'

    def PartVI(self):
        return bin(self.__Data)[2:]

    def PartIV(self):
        return bin(len(bin(self.__Data)[2:])).replace('0b','').zfill(16)

    def PartVII(self):
        return '00000000' * 4

    def Total(self):
        return self.PartI()+self.PartII()+self.PartIII()+self.PartIV()+self.PartV()+self.PartVI()+self.PartVII()

class EthernetDataDecoder(object) :
    def __init__(self,Ethernetdata):
        for i in range(0,len(Ethernetdata)) :
            if Ethernetdata[i] == Ethernetdata[i+1] :
                self.__DataStart = i + 2
                break
        self.__AvailableData = Ethernetdata[self.__DataStart:]

    def OriginAddress(self):
        return self.__AvailableData[0:48]

    def HexOriginAddress(self):
        HexRes = ''
        for i in range(0,48,4) :
            HexRes = HexRes + hex(int(self.__AvailableData[i:i+4],2)).replace('0x','')
        return HexRes.upper()

    def DestinationAddress(self):
        return self.__AvailableData[48:96]

    def HexDestinationAddress(self):
        HexRes = ''
        for i in range(48,96,4) :
            HexRes = HexRes + hex(int(self.__AvailableData[i:i+4],2)).replace('0x','')
        return HexRes.upper()

    def DataLength(self):
        self.__BinDataLen = self.__AvailableData[96:112]
        return int(self.__BinDataLen.lstrip('0'),2)

    def BinData(self):
        return self.__AvailableData[136:136+self.DataLength()]

    def DecData(self):
        return int(self.BinData(),2)


    def PrintDetails(self):
        print("Ori Addr="+self.HexOriginAddress()+", Dest Addr="+self.HexDestinationAddress()+", Data Len="+str(self.DataLength())+", Data="+self.BinData()+", Result="+str(self.DecData()))



if __name__ == '__main__':
    c = EthernetData('58:FB:84:8C:22:11','5A-FB-84-8C-22-10',23)
    '''
    print(c.PartI())
    print(c.PartII())
    print(c.PartIII())
    print(c.PartIV())
    print(c.PartV())
    print(c.PartVI())
    print(c.PartVII())
    print(c.Total())
    print(EthernetDataDecoder(c.Total()).OriginAddress())
    print(EthernetDataDecoder(c.Total()).DestinationAddress())
    print(EthernetDataDecoder(c.Total()).DataLength())
    print(EthernetDataDecoder(c.Total()).HexOriginAddress())
    print(EthernetDataDecoder(c.Total()).HexDestinationAddress())
    print(EthernetDataDecoder(c.Total()).Data())
    '''


