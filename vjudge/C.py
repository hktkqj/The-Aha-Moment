def sum(n) :
    if n==0 :
        return 0
    ans = add = 0
    i = 1
    while i<=n :
        add = n // (n//i)
        ans = ans + (i+add)*(add-i+1)//2*(n//i)
        i = add + 1
    return ans

if __name__ == '__main__':
    str = input()
    a = int(str.split(' ')[0])
    b = int(str.split(' ')[1])
    print("%d\n" % (sum(b)-sum(a-1)))