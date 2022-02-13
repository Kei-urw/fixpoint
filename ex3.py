import datetime

print("input filename")
logfile=input()
file=open(logfile)
print("input N")
N=int(input())
print("input m t")
m,t=map(int,input().split())
timeout={}  #サーバーアドレスごとに最初にタイムアウトした時間を保存
timeoutcnt={}  #サーバーアドレスごとに連続してタイムアウトした回数を保存
responsetime={}  #サーバーごとの応答時間をリストで保存
responsecnt={}  #サーバーアドレスごとの応答回数を保存
DandTinfo={}   #サーバーごとの時間情報をリストで保存
for line in file:
    log=line.rstrip()
    DandT,address,response=log.split(',')
    if response!='-':
        if address in timeout:
            if timeoutcnt[address]>=N:
                dt1 = datetime.datetime(
                year=int(DandT[0:4]), month=int(DandT[4:6]), day=int(DandT[6:8]),
                hour=int(DandT[8:10]),minute=int(DandT[10:12]),second=int(DandT[12:14])
                )
                DandT2=timeout[address]
                dt2 = datetime.datetime(
                year=int(DandT2[0:4]), month=int(DandT2[4:6]), day=int(DandT2[6:8]),
                hour=int(DandT2[8:10]),minute=int(DandT2[10:12]),second=int(DandT2[12:14])
                )
                print("Server down "+address+" "+str(dt2)+"->"+str(dt1))
                print("Failur time:"+str(dt1-dt2))
            del timeout[address]
            del timeoutcnt[address]
    else:
        if address not in timeout:
            timeout[address]=DandT
            timeoutcnt[address]=1
        else:
            timeoutcnt[address]+=1

    #ここから過負荷測定
    if response!='-':
        if address not in responsetime:
            responsetime[address]=[int(response)]  #サーバーアドレスごとに応答時間をリストで保存
            responsecnt[address]=1  #サーバーアドレスごとの応答回数を更新
            DandTinfo[address]=[DandT]  #サーバーごとの時間情報をリストで保存
        else:
            responselist=responsetime[address]
            responselist.append(int(response))
            responsetime[address]=responselist  #サーバーアドレスごとに応答時間をリストで保存
            responsecnt[address]+=1  #サーバーアドレスごとの応答回数を更新
            DandTlist=DandTinfo[address]
            DandTlist.append(DandT)
            DandTinfo[address]=DandTlist  #サーバーごとの時間情報をリストで保存
        if responsecnt[address]>=m:  #応答回数がmを超えた時
            responselist=responsetime[address]
            waittime=sum(responselist[-m:])  #直近m回分の応答時間の合計
            DandTlist=DandTinfo[address]
            if waittime/m<t:  #直近m回の応答時間の平均値がt未満だった時
                if responsecnt[address]!=m:  #記録してたのがm回よりも多かった時は過負荷だった期間が存在するためその期間を出力
                    DandT1=DandTlist[-2]  #過負荷だった期間の最後
                    DandT2=DandTlist[0]  #過負荷だった期間の最初
                    dt1 = datetime.datetime(
                    year=int(DandT1[0:4]), month=int(DandT1[4:6]), day=int(DandT1[6:8]),
                    hour=int(DandT1[8:10]),minute=int(DandT1[10:12]),second=int(DandT1[12:14])
                    )
                    dt2 = datetime.datetime(
                    year=int(DandT2[0:4]), month=int(DandT2[4:6]), day=int(DandT2[6:8]),
                    hour=int(DandT2[8:10]),minute=int(DandT2[10:12]),second=int(DandT2[12:14])
                    )
                    print("Overload "+address+" "+str(dt2)+"->"+str(dt1))
                    print("Failur time:"+str(dt1-dt2))
                responsetime[address]=responselist[-(m-1):]  #直近のm-1回分の応答時間を保存
                responsecnt[address]=m-1  #応答回数を直近m-1回分にする
                DandTinfo[address]=DandTlist[-(m-1):]  #直近m-1回分の時間情報を保存
