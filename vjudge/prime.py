import math
def prime(n) :
    for i1 in range(2,int(n**0.5)+1) :
        if n % i1 == 0 :
            return False
    return True

if __name__ == '__main__':
    for i in range(0,100000) :
        now =str(i)
        if prime(i) == True :
            flag = True
            for j in range(0,len(now)) :
                if flag == False :
                    break
                for k in range(j+1,len(now)+1) :
                    sp = now[j:k]
                    if prime(int(sp)) == False :
                        flag = False
                        break
            if flag == True :
                print(i,end=',')