import datetime

print("input filename")
logfile=input()
file=open(logfile)
timeout={}   #サーバーアドレスごとに最初にタイムアウトした時間を保存
for line in file:
    log=line.rstrip()
    DandT,address,response=log.split(',')
    if response!='-':
        if address in timeout:
            #応答した時間
            dt1 = datetime.datetime(
            year=int(DandT[0:4]), month=int(DandT[4:6]), day=int(DandT[6:8]),
            hour=int(DandT[8:10]),minute=int(DandT[10:12]),second=int(DandT[12:14])
            )
            DandT2=timeout[address]
            #最初にタイムアウトになった時間
            dt2 = datetime.datetime(
            year=int(DandT2[0:4]), month=int(DandT2[4:6]), day=int(DandT2[6:8]),
            hour=int(DandT2[8:10]),minute=int(DandT2[10:12]),second=int(DandT2[12:14])
            )
            print(address+" "+str(dt2)+"->"+str(dt1))  #タイムアウトしてた期間を出力
            print("Failur time:"+str(dt1-dt2))  #タイムアウトしてた時間を出力
            del timeout[address]
    else:
        if address not in timeout:
            timeout[address]=DandT  #最初にタイムアウトした時間
