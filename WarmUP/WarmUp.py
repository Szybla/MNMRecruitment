
def fun(str):
    str = str.lower()
    l = ['', '']
    for i in range(len(str)):
        if(i%2==0):
            l[0] = l[0] + str[i].lower()
            l[1] = l[1] + str[i].upper()

        else:
            l[0] = l[0] + str[i].upper()
            l[1] = l[1] + str[i].lower()
    return l
print(f"WarmUp.a: {fun('abcdef')}")

def function(str):
    str = str.lower()
    d = {}
    for i in str:
        if i not in d:
            d[i] = 1
        else:
            d[i] = d[i] + 1
    n = 0
    for i in d:
        if d[i]>1:
            n=n+1
    return n

print(f"WarmUp.b ABBA: {function('ABBA')}")
print(f"WarmUp.b aBcbA: {function('aBcbA')}")
print(f"WarmUp.b RhabarbArka: {function('RhabarbArka')}")