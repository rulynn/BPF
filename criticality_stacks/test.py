
def getVMThread():
    VMThread = {}
    with open('out_stack.log', 'r') as f:
        jstack = f.readlines()
    for i in range(0, len(jstack)):
        if jstack[i][0] == "\"":
            x = jstack[i].split("\"")
            idx = jstack[i].find("nid")
            nid = ""
            for j in range(idx+6, len(jstack[i])):
                if jstack[i][j] == ' ':
                    break
                nid += jstack[i][j]
            nid_int = int(nid.upper(), 16)
            VMThread[nid_int] = x[1]
            print(x[1], nid_int)
    return VMThread

getVMThread()