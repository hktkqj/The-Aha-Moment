from PIL import Image
import os

CharSet = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def GetChar(char) :
    if char == 255 :
        return ' '
    else :
        return CharSet[int((char/255)*len(CharSet))]

if __name__ == '__main__':
    ImageFile = Image.open("Image.jpg")
    GrayImage = ImageFile.convert('L')
    Width = GrayImage.size[0]
    Height = GrayImage.size[1]
    if Height >=300 :
        Width = int(Width * (400 / Height))
        Height = 300
        GrayImage = GrayImage.resize((Width, Height), Image.ANTIALIAS)
    else :
        Width = Width + 100
        GrayImage = GrayImage.resize((Width, Height), Image.ANTIALIAS)
    GrayImage.save("gray.jpg")
    TxtFile = open("ACSII.txt","w")
    for row in range(0,Height) :
        for line in range(0,Width) :
            pixel = GrayImage.getpixel((line,row))
            TxtFile.write(str(GetChar(pixel)))
        TxtFile.write('\n')
    os.remove("gray.jpg")