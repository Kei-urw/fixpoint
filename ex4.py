import datetime

print("input filename")
logfile=input()
file=open(logfile)
print("input N")
N=int(input())
timeout={}  #サブネットごとに最初にタイムアウトした時間を保存
timeoutcnt={}  #サブネットごとに連続してタイムアウトした回数を保存
for line in file:
    log=line.rstrip()
    DandT,address,response=log.split(',')
    IP,subnet=address.split('/')  #IPアドレスとサブネットに分割
    if response!='-':
        if subnet in timeout:
            if timeoutcnt[subnet]>=N:
                dt1 = datetime.datetime(
                year=int(DandT[0:4]), month=int(DandT[4:6]), day=int(DandT[6:8]),
                hour=int(DandT[8:10]),minute=int(DandT[10:12]),second=int(DandT[12:14]),
                )
                DandT2=timeout[subnet]
                dt2 = datetime.datetime(
                year=int(DandT2[0:4]), month=int(DandT2[4:6]), day=int(DandT2[6:8]),
                hour=int(DandT2[8:10]),minute=int(DandT2[10:12]),second=int(DandT2[12:14])
                )
                print(subnet+" "+str(dt2)+"->"+str(dt1))
                print("Failur time:"+str(dt1-dt2))
            del timeout[subnet]
            del timeoutcnt[subnet]
    else:
        if subnet not in timeout:
            timeout[subnet]=DandT
            timeoutcnt[subnet]=1
        else:
            timeoutcnt[subnet]+=1
