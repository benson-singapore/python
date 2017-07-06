import pandas as pd
import json
import uuid
from datetime import *
import random

#格式化sql
def formatSql(sql,param):
    params = []
    sq = sql.split('?')
    for p in param.split(','):
        p = p.lstrip()
        params.append("'"+(p.split('(')[0])+"'" if p != 'null' else 'null')
    for i in range(len(params)):
        sq[i] = sq[i]+params[i]
    return ''.join(sq)
#json 数据格式化
def formatJson(dic1):
	json_dic2=json.dumps(dic1,sort_keys=False,indent=4,separators=(',',':'),ensure_ascii=False )
	print(json_dic2)

#excel 数据转json
def excelToJson(adr):
    excel = read_excel(adr,True)
    formatJson(formatExcel(0,excel,0))
#json 数据转excel
def jsonToExcel(adr):
    js = pd.read_json(adr);
    for n in js.index:
        print('===================')
        print(n)
        print("-------------------")
        for e in js.ix[n]['result']: 
            if(type(js.ix[n]['result']) == dict):       
                if(type(js.ix[n]['result'][e])==list):
                    print("-------------------")
                    print(e)
                    print("-=-=-=-=-=-=-=-=-=-")
                    each_json(js.ix[n]['result'][e][0])
                    print("-------------------")
                elif(type(js.ix[n]['result'][e])==dict):
                    print("-------------------")
                    print(e)
                    print("-=-=-=-=-=-=-=-=-=-")
                    each_json(js.ix[n]['result'][e],"    ")
                    print("-------------------")
                else:
                    print(e)
           
        print('===================')

#读取excel 返回 dataFrame
def read_excel(adr,flag=False):
    #excel = read_excel(adr)
    excel = pd.read_excel(adr)
    excel.fillna(value='',inplace=True)
    if(flag):
        excel[excel.columns] = excel[excel.columns].applymap(lambda x:replaceName(x)) 
    return excel

#读sql 返回 dataFrame
def read_sql(url,flag=False):
    return parsing_sql(url,flag)['df']  

# sql 字段信息打印
def print_sql(url,flag=False):
    data = parsing_sql(url,flag)
    rs = data['df']
    print('-------------------------------')
    print(data['name'])
    print('-------------------------------')
    for i in rs[0]:
        print(i)
    print('-------------------------------')
    if(rs.columns.size > 2):
        for i in rs[1]+rs[2]:
            if(i.endswith(',')):
                i = i[0:-1]
            print(i)
    else:
        for i in rs[1]:
            if(i.endswith(',')):
                i = i[0:-1]
            print(i)       
    print('-------------------------------')

#生成uuid
def getId():
    return str(uuid.uuid1()).replace('-','')

#生成当前时间
def getDate(f='%Y-%m-%d %H:%M:%S'):
    return datetime.now().strftime(f)


#######################################################################################
                            ####### private #######
#######################################################################################

#sql 数据格式化
def parsing_sql(url,flagType=False):
    arr = []
    dp = []
    name = ''
    flag = False
    p = open(url,'r')
    for e in p.readlines():
        if(e.strip()=='('):
            flag = True
        if(e.strip()==')'):
            flag = False
        if(e.find('CREATE TABLE')>=0):
            print(e)
            a = e.split('CREATE TABLE')[1].strip().split('.')
            name = a[1] if len(a)>1 else a[0]
        if(flag and e.strip()!='(' and e.find('primary') < 0 and e.find(');')<0):
            arr.append(e.strip())
    for a in arr:
        ar = []
        for i in a.split(' '):
            if(i!=''):
                ar.append(i.strip())
        dp.append(ar)
    df = pd.DataFrame(dp).fillna(value='')
    p.close()
    if(flagType):
        df[df.columns] = df[df.columns].applymap(lambda x:replaceName(x)) 
    #print(df)
    return {'name':name,'df':df}


#对excel 递归格式化 json
def formatExcel(m,excel,n):
    j_son = {}
    for i in range(m,excel.index.size):
        if(i == excel.index.size or n>excel.columns.size):
            break 
        if(excel.ix[i][n] != ''):
            if(i+1 < excel.index.size):
                if(excel.columns.size > n+1 and excel.ix[i][n+1] != ''):
                    j_son[excel.ix[i][n]] = {excel.ix[i][n+1]:''}
                    continue
                else:
                    if(excel.ix[i+1][n] == ''):
                        j_son[excel.ix[i][n]]={}
                        continue
                    else:
                        j_son[excel.ix[i][n]]= preJson(excel.ix[i][n])
                        continue
            else:
                j_son[excel.ix[i][n]]=''
                continue  
        else:
            if((excel.columns.size > n+1 and excel.ix[i][n+1] != '') or (i+1 < excel.index.size and excel.ix[i+1][n]!= '')):
                #print(j_son)
                try:
                    j_son[checkNum(excel,i,n)]
                except :
                    j_son[checkNum(excel,i,n)] = {}
                if((i+1 < excel.index.size and excel.ix[i+1][n+1]!= '')or i+1 == excel.index.size or (i+1 < excel.index.size and excel.ix[i+1][n]!= '')):
                    j_son[checkNum(excel,i,n)][excel.ix[i][n+1]] = preJson(excel.ix[i][n+1])
                continue
            else:
                if(excel.columns.size > n+2 and excel.ix[i][n+2] != ''):
                    j_son[checkNum(excel,i,n)][checkNum(excel,i,n+1)] = formatExcel(i-1,excel,n+1)[checkNum(excel,i,n+1)]
                    break
                else:
                    j_son[excel.ix[i][n]]=preJson(excel.ix[i][n])
                    continue
    return j_son

#获取父级名称
def checkNum(excel,m,n):
    try:
        if(excel.ix[m][n] != ''):
            return excel.ix[m][n]
        else:
            return checkNum(excel,m-1,n)
    except Exception:
        return checkNum(excel,excel.index.size-1,n)

#下划线名称字段取出转大写 ui_id -> uiId
def replaceName(s_,rep='_'):
    arr = s_.split(rep) if s_.find(rep)<0 else s_.lower().split(rep)
    return ''.join([arr[0]]+[i.capitalize() for i in arr[1::]])

#josn预处理
def preJson(name):
    rs = ''
    name = str(name).lower()
    if(name.find('id')>=0 or name.find('createby')>=0 or name.find('updateby')>=0):
        rs = getId()
    elif(name.find('time')>=0 or name.find('date')>=0):
        rs = getDate()
    elif(name.find('flag')>=0 or name.find('status')>=0 or name.find('type')>=0):
        rs = random.sample(list(range(0,2)),1)[0] # 在 0,1 中随意选择
    return rs

def formatUrl(url):
    json_ = {}
    if(url.find('?') >= 0):
        arr = url.split('?')[1].split('&')
        for i in arr:
            j_ = i.split('=')
            json_[j_[0]] = j_[1]
    return formatJson(json_)

def each_json(jsdata):
    for j in jsdata:
        if(type(jsdata[j]) == list):
            print("-------------------")
            print(j)
            print("-=-=-=-=-=-=-=-=-=-")
            each_json(jsdata[j][0])
            print("-------------------")
        elif(type(jsdata[j]) == dict):
            print("-------------------")
            print(j)
            print("-=-=-=-=-=-=-=-=-=-")
            each_json(jsdata[j])
            print("-------------------")
        print(str(j))