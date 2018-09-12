import os
import  shutil
if __name__ == '__main__':
    Datalist = open("C:\\test\\result.txt","r")
    All_Data_Str = Datalist.read()
    All_Data_Str = All_Data_Str.split('\n')
    All_Data_Str.remove(All_Data_Str[0])
    for student in All_Data_Str :
        Now_Student = student.split(' ')
        print(Now_Student)
        if len(Now_Student) == 1 :
            break
        if Now_Student[1] == 'FAILED' :
            shutil.copy('C:\\test\\'+Now_Student[0],'C:\\test\\fail')
        else :
            Photo_Name = Now_Student[0]
            Gender = Now_Student[1]
            Probability = float(Now_Student[2])
            Beauty = float(Now_Student[3])
            if Gender == 'male' :
                shutil.copy('C:\\test\\'+Photo_Name,'C:\\test\\male\\(%s)' % (str(Beauty))+Photo_Name)
            else :
                shutil.copy('C:\\test\\'+Photo_Name,'C:\\test\\female\\(%s)' % (str(Beauty))+Photo_Name)