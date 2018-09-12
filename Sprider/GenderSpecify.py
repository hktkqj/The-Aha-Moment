from aip import AipFace
import base64
import os
import time
import urllib.parse


if __name__ == '__main__':
#Used Baidu API
    APP_ID = '11766662'
    API_KEY = 'V3Eo4XvelIHnBYCwjcu0AVQk'
    SECRET_KEY = 'fghsnPTVadbjF8vnvV7ykSUSPLTad3jh'
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
#End API login information

    PhotoList = os.listdir("C:\\test")
    PhotoDict = {}
    ImageType = "BASE64"
    options = {}
    options["face_type"] = "CERT"
    options["face_field"] = "age,beauty,gender"
    Noteresult = open("C:\\test\\result.txt",'w')
    Noteresult.write("Photonum     Gender  Probability    Beauty\n")
    for PhotoName in PhotoList :
        time.sleep(0.5)
        try :
            PhotoPath = open("C:\\test\\"+PhotoName,"rb")
            Base64Data = base64.b64encode(PhotoPath.read())
            Base64Data = str(Base64Data,'utf-8')
            result = client.detect(Base64Data, ImageType, options)
            print(PhotoName+':'+result['error_msg'])
            Noteresult.write(PhotoName+' '+result['result']['face_list'][0]['gender']['type']+" "+str(result['result']['face_list'][0]['gender']['probability'])+" "+str(result['result']['face_list'][0]['beauty'])+'\n')
        except :
            Noteresult.write(PhotoName + ' FAILED \n')
    Noteresult.close()