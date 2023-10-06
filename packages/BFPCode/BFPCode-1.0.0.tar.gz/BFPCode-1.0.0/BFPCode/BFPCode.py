def bfc(code, inl=128):
    try:
        bf = list(code)
        l = inl
        if type(inl) == int:
            l = [0] * inl
        l = list(l)
        p = 0
        i = 0
        stack = []  # 用于跟踪括号的栈
        while i < len(code):
            if bf[i] == ">":
                if p < len(l):
                    p += 1

            elif bf[i] == "<":
                if p > 0:
                    p -= 1

            elif bf[i] == "+":
                if l[p] < 128:
                    l[p] += 1

            elif bf[i] == "-":
                if l[p] > 0:
                    l[p] -= 1

            elif bf[i] == ".":
                print(chr(l[p]), end="")

            elif bf[i] == ",":
                l[p] = ord(input())

            elif bf[i] == "[":
                if l[p] == 0:
                    qz = 1
                    while qz > 0:
                        i += 1
                        if bf[i] == "[":
                            qz += 1
                        elif bf[i] == "]":
                            qz -= 1
                else:
                    stack.append(i)

            elif bf[i] == "]":
                if l[p] != 0:
                    i = stack[-1]
                else:
                    stack.pop()
            
            elif bf[i] == "~":
                return l

            i += 1
    except :
        return
