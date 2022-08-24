def taru(k,arr):
    for i in arr:
        if i==1:
            j=k
        if i==2:
            if j%2==0:
                j=k/2
            else:
                j=(k+1)/2
        if i==3:
            if j%2==0:
                j=k/2
            else:
                j=(k+1)/2
        if i==4:
            j=0
    return j