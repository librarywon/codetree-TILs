l = []

for i in range(int(input())):
    s = input().split()
    if s[0]=="push_back":
        l.append(int(s[1])) 
    elif s[0]=="get":
        print(l[int(s[1])-1])
    elif s[0]=="size":
        print(len(l))
    elif s[0]=="pop_back":
        l.pop()