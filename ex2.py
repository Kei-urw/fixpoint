import datetime

print("input filename")
logfile=input()
file=open(logfile)
print("input N")
N=int(input())
timeout={}  #サーバーアドレスごとに最初にタイムアウトした時間を保存
timeoutcnt={}  #サーバーアドレスごとに連続してタイムアウトした回数を保存
for line in file:
    log=line.rstrip()
    DandT,address,response=log.split(',')
    if response!='-':
        if address in timeout:
            if timeoutcnt[address]>=N:  #連続タイムアウト回数がN回を超えてたらタイムアウトしていた期間を出力
                dt1 = datetime.datetime(
                year=int(DandT[0:4]), month=int(DandT[4:6]), day=int(DandT[6:8]),
                hour=int(DandT[8:10]),minute=int(DandT[10:12]),second=int(DandT[12:14]),
                )
                DandT2=timeout[address]
                dt2 = datetime.datetime(
                year=int(DandT2[0:4]), month=int(DandT2[4:6]), day=int(DandT2[6:8]),
                hour=int(DandT2[8:10]),minute=int(DandT2[10:12]),second=int(DandT2[12:14])
                )
                print(address+" "+str(dt2)+"->"+str(dt1))
                print("Failur time:"+str(dt1-dt2))
            del timeout[address]  #最初にタイムアウトした時間を削除
            del timeoutcnt[address]  #連続してタイムアウトした回数を削除
    else:
        if address not in timeout:
            timeout[address]=DandT
            timeoutcnt[address]=1
        else:
            timeoutcnt[address]+=1  #連続してタイムアウトした回数を更新
