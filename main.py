import pandas as pd
import re


def DeleteNone():
    data=''
    with open('game_log.tsv','r+',encoding='UTF-8') as f:
        for line in f.readlines():
            m=re.match(r'^(.*?)(None\tNone)$',line)
            if (m):
                line=m.group(1)+'None\n'
            data +=line
    with open('game_log_5c.tsv','w',encoding='UTF-8') as g:
        g.writelines(data)



def CountByDay():
    df = pd.read_table('game_log_5c.tsv',sep='\t')
    df['Event Time']=pd.to_datetime(df['Event Time'])
    data=df.set_index('Event Time')

    data=data.groupby([data.index.year,data.index.month,data.index.day]).size()
    data.to_csv('data.csv')


def WriteHTML():
    data='[\n'
    with open('data.csv','r') as f:
        for line in f.readlines():
            m=re.match(r'^(\d+),(\d+),(\d+),(\d+)$',line)
            data +='["'+m.group(1)+'-'+m.group(2)+'-'+m.group(3)+'",'+m.group(4)+'],\n'
    data +='];\n'
    out=''
    with open('template.html','r',encoding='UTF-8') as f:
        file=f.read()
        out = file.split('PutYourDataHere')[0]+data+file.split('PutYourDataHere')[1]
    
    with open('IngressCalendaHeatMap.html','w') as f:
        f.writelines(out)


if __name__=="__main__":
    DeleteNone()
    CountByDay()
    WriteHTML()