import numpy as np
import pandas as pd
import csv
import json
import matplotlib.pyplot as plt
import matplotlib
from sklearn.linear_model import LinearRegression
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
matplotlib.rcParams['axes.unicode_minus'] = False
def task1(days):
    print("task1")
    df=pd.read_csv("COVID_19-2020-12-all.csv",encoding="utf-8")
    increased=[]#全球总计新增人数
    total=[]#全球总计累计确诊人数
    cure=[]#全球总计累计治愈人数
    dead=[]#全球总计累计死亡人数

    for day in days:#对于每天计算总和并加到对应数组末尾
        increased.append(df[df['day']==day]['increased'].sum())
        total.append(df[df['day']==day]['total'].sum())
        cure.append(df[df['day']==day]['cure'].sum())
        dead.append(df[df['day']==day]['dead'].sum())

    data={'day':days,'increased':increased,'total':total,'cure':cure,'dead':dead}
    df1=pd.DataFrame(data)#data转换成dataframe
    print(df1)

    x = [i for i in range(15)]
    y = []
    columns = ['increased', 'total', 'cure', 'dead']#用于确认每个子图的y轴数据列标签
    # 每个子图的标题
    title=['全球每日新增人数变化曲线','全球累计确诊人数变化曲线','全球累计治愈人数变化曲线','全球累计死亡人数变化曲线']
    style=['b-o','g-o','r-o','c-o']#每个子图的风格
    plt.figure(figsize=(20, 12))#画布大小
    plt.style.use('bmh')#绘图风格
    for i in range(1, 5):
        plt.subplot(2, 2, i)#子图划分
        y = df1[columns[i - 1]].values.tolist()#每个子图对应的y数据
        plt.plot(days, y, style[i-1])#绘制趋势图
        plt.title(title[i-1])#添加标题
        plt.xlabel("日期")#x轴标签
        plt.ylabel("人数")#y轴标签
        plt.legend(title, loc='upper left')#图例
        for a, b in zip(x, y):
            plt.text(a+0.2, b, '%d' % b, ha='left', va='center', fontsize=10, rotation=0)#数据展示
    plt.show()


def task2():
    print("task2")
    #累计确诊排名前20的国家 看最后一天12月15号的数据即可
    df=pd.read_csv("COVID_19-2020-12-15.csv",encoding="utf-8")
    df=df.sort_values(by=["total"],ascending=False)#根据确诊总数升序排序
    df=df.iloc[range(0,20)]#取前20的数据

    plt.barh(range(20),df['total'],height=0.5,alpha=0.8)#横着的直方图
    plt.yticks(range(20), df['country'])#刻度
    plt.xlabel("累计确诊人数")
    plt.ylabel("国家")
    plt.title("累计确诊排名前20的国家")
    for x, y in enumerate(df['total']):
        plt.text(y + 0.2, x - 0.1, '%s' % y)
    plt.show()



def task3():
    print("task3")
    df = pd.read_csv("COVID_19-2020-12-all.csv", encoding="utf-8")
    _sum = df.groupby(by=['country'])['increased'].sum()#计算每个国家15天increased总和
    df1=pd.DataFrame(_sum)
    df1 = df1.sort_values(by=['increased'], ascending=False)#对increased升序排列
    df1.to_csv("temp.csv")#输出成temp.csv
    df1=pd.read_csv("temp.csv",encoding="utf-8",nrows=10)#只取前10行的数据 代表前10的数据
    countrys=df1['country'].tolist()
    print(countrys)
    colors = ['darkblue','darkgoldenrod','darkcyan','darkkhaki','darkgreen','darkgray'
        ,'darkred','darksalmon','darkseagreen','darkturquoise']
    for i in range(10):
        df2=df[df['country']==countrys[i]]
        y=df2['increased'].tolist()
        plt.plot(days,y,color=colors[i],label=countrys[i],linestyle="-",marker=".")
        plt.legend(loc="upper right")
    plt.title("每日新增确诊数累计排名前10个国家的每日新增确诊数据的曲线图")
    plt.xlabel("日期")
    plt.ylabel("新增人数")
    plt.show()



def task4():
    #累计确诊人数占总人口比例排名前20的国家
    print("task4")
    #每个国家总人口数据
    with open("country_text.json","r", encoding="UTF-8") as f:
        load_dict = json.load(f)
    df=pd.read_csv("COVID_19-2020-12-15.csv",encoding="utf-8")

    rate=[]
    country=[]
    population=[]
    total=[]
    for i in range(df['total'].size):
        for j in load_dict:
            if(j['country']==df['country'][i]):#疫情数据中有一个钻石号公主游轮 不属于 国家 在这里进行筛选
                rating=df['total'][i]/j['population']#计算比例
                country.append(df['country'][i])#将国家名加入数组
                total.append(df['total'][i])#将确诊总数加入数组
                population.append(j['population'])#将总人数加入数组
                rate.append(rating)#将rating加入数组
    data={'country':country,'total':total,'population':population,'rate':rate}#生成字典
    df=pd.DataFrame(data)#字典转dataframe
    df=df.sort_values(by=["rate"],ascending=False)#根据rate排序
    df=df.iloc[range(0, 20)]#前20
    print(df)
    #plt.figure(figsize=(10,8))
    plt.barh(range(20), df['rate'], height=0.5, alpha=0.8)#画横直方图
    plt.yticks(range(20), df['country'])
    plt.xlabel("确诊人数占总人口比例")
    plt.ylabel("国家")
    plt.title("累计确诊人数占总人口比例排名前20的国家")
    for x, y in enumerate(df['rate']):
        plt.text(y + 0.001, x - 0.1, '%f' % y)
    plt.show()
    plt.pie(df['rate'], labels=df['country'], labeldistance=1.1, autopct="%1.1f%%", shadow=True,
            startangle=0, pctdistance=0.6)
    plt.show()

def task5():
    #死亡率（累计死亡人数/累计确诊人数）最低的10个国家
    print("task5")
    df=pd.read_csv("COVID_19-2020-12-15.csv",encoding="utf-8")
    df1 = df[df['dead']!=0]#将死亡数为0的国家剔除
    df1['rate']=df1['dead']/df1['total']#计算死亡率并添加新列
    df1 = df1.sort_values(by=['rate'])#根据死亡率升序排序
    df1=df1.iloc[range(0,10)]#取死亡率最低的10个国家
    print(df1)
    country = df1['country'].tolist()
    rates = df1['rate'].tolist()
    print(country)
    print(rates)
    plt.barh(country, rates, height=0.5,alpha=0.8,)#绘制横方图
    plt.xlabel("死亡率")
    plt.ylabel("国家")
    plt.title("死亡率（累计死亡人数/累计确诊人数）最低的10个国家")
    for a, b in zip(rates, country):
        plt.text(a, b, '%f' % a, ha='left', va='center', fontsize=13)#设置数据展示
    plt.show()


def task6():
    #各个国家的累计确诊人数比例
    print("task6")
    df = pd.read_csv("COVID_19-2020-12-15.csv", encoding="utf-8")
    df1=df[df['total']>=1000000]#大于1000000的国家正常展示
    df2=df[df['total']<=1000000]#小于1000000的国家合并成others
    others=df2['total'].sum()

    count=df1['total'].tolist()
    count.append(others)
    labels=df1['country'].tolist()
    labels.append("others")

    plt.title("各个国家的累计确诊人数比例")
    plt.pie(count, labels=labels, labeldistance=1.1, autopct="%1.1f%%", shadow=True,
            startangle=0, pctdistance=0.6)
    plt.show()

def task7():
    #展示全球各个国家累计确诊人数的箱型图，要有平均值
    print("task7")
    df = pd.read_csv("COVID_19-2020-12-15.csv", encoding="utf-8")
    f = df.boxplot(column=['total'], meanline=True, showmeans=True, vert=True, return_type='dict')  # 修改True的设置

    plt.title("累计确诊人数箱型图")
    for mean in f['means']:
        mean.set(color='r', linewidth=2)#平均值

    # 添加文本注释
    ax = df.boxplot(column=['total'], meanline=True, showmeans=True, vert=True)  # 修改True的设置
    ax.text(1.1, df['total'].mean(), df['total'].mean())
    ax.text(1.1, df['total'].median(), df['total'].median())
    ax.text(0.9, df['total'].quantile(0.25), df['total'].quantile(0.25))
    ax.text(0.9, df['total'].quantile(0.75), df['total'].quantile(0.75))

    plt.show()

def task8():
    print("task8")
    #治愈率最高和最低的十个国家
    df = pd.read_csv("COVID_19-2020-12-15.csv", encoding="utf-8")
    df1 = df[df['cure'] != 0]  # 将治愈数为0的国家剔除
    df1['rate'] = df1['cure'] / df1['total']  # 计算治愈率率并添加新列
    #最高
    df1 = df1.sort_values(by=['rate'],ascending=False)  # 根据治愈率降序排序
    df2= df1.sort_values(by=['rate'])# 根据治愈率升序排序
    df1 = df1.iloc[range(0, 10)]  # 取治愈率最高的10个国家
    print(df1)
    country = df1['country'].tolist()
    rates = df1['rate'].tolist()
    print(country)
    print(rates)
    plt.barh(country, rates, height=0.5, alpha=0.8, )  # 绘制横方图
    plt.xlabel("治愈率")
    plt.ylabel("国家")
    plt.title("治愈率最高的10个国家")
    for a, b in zip(rates, country):
        plt.text(a, b, '%f' % a, ha='left', va='center', fontsize=13)  # 设置数据展示
    plt.show()

    #最低
    df2 = df2.iloc[range(0, 10)]  # 取治愈率最高的10个国家
    print(df2)
    country = df2['country'].tolist()
    rates = df2['rate'].tolist()
    print(country)
    print(rates)
    plt.barh(country, rates, height=0.5, alpha=0.8, )  # 绘制横方图
    plt.xlabel("治愈率")
    plt.ylabel("国家")
    plt.title("治愈率最低的10个国家")
    for a, b in zip(rates, country):
        plt.text(a, b, '%f' % a, ha='left', va='center', fontsize=13)  # 设置数据展示
    plt.show()

    df=pd.read_csv("COVID_19-2020-12-all.csv",encoding="utf-8")
    df=df.sort_values(by=['increased'],ascending=False)#排序
    df=df.iloc[range(0,10)]#取前十

    plt.bar(df['day'],df['increased'])
    plt.title("15天内新增人数最多的前十数据对应的天数和新增人数")
    plt.xlabel("日期")
    plt.ylabel("新增人数")
    plt.legend(df['country'],loc="upper right")

    for a, b in zip(df['day'], df['increased']):
        plt.text(a, b+100, '%s' % b, ha='left', va='center', fontsize=13)  # 设置数据展示

    plt.show()
    print(df)

def Efficiency():
    df = pd.read_csv("COVID_19-2020-12-15.csv", encoding="utf-8")
    with open("country_text.json", "r", encoding="UTF-8") as f:
        load_dict = json.load(f)
    population_rate = []
    cure_rate=[]#治愈率
    dead_rate=[]#死亡率
    country = []#国家
    population = []#人口
    total = []#累计确诊
    efficiency=[]#效率
    for i in range(df['total'].size):
        for j in load_dict:
            if (j['country'] == df['country'][i]):  # 疫情数据中有一个钻石号公主游轮 不属于 国家 在这里进行筛选
                country.append(df['country'][i])  # 将国家名加入数组
                total.append(df['total'][i])  # 将确诊总数加入数组
                population.append(j['population'])  # 将总人数加入数组
                rate1=df['total'][i] / j['population']#确诊占总人口率
                rate2=df['cure'][i] / df['total'][i]#治愈率
                rate3=df['dead'][i]/df['total'][i]#死亡率
                population_rate.append(rate1)  # 将rating加入数组
                cure_rate.append(rate2)
                dead_rate.append(rate3)
                efficiency.append((rate2-rate3)/rate1)#效率计算
    data = {'country': country, 'total': total, 'population': population, 'population_rate': population_rate
            ,'cure_rate':cure_rate,'dead_rate':dead_rate,'efficiency':efficiency}  # 生成字典
    df = pd.DataFrame(data)  # 字典转dataframe
    # 最高
    df1 = df.sort_values(by=['efficiency'], ascending=False)  # 根据efficiency降序排序
    df1 = df1.iloc[range(0, 10)]  # 取efficiency最高的10个国家
    df1.to_csv("test.csv")
    print(df1)
    country = df1['country'].tolist()
    rates = df1['efficiency'].tolist()
    print(country)
    print(rates)
    plt.barh(country, rates, height=0.5, alpha=0.8, )  # 绘制横方图
    plt.xlabel("效率")
    plt.ylabel("国家")
    plt.title("效率最高的10个国家")
    for a, b in zip(rates, country):
        plt.text(a, b, '%f' % a, ha='left', va='center', fontsize=13)  # 设置数据展示
    plt.show()

def do_prediction():
    df = pd.read_csv("COVID_19-2020-12-all.csv", encoding="utf-8")
    _sum = df.groupby(by=['day'])['total'].sum()  # 每日全球确诊人数
    df1 = pd.DataFrame(_sum)
    df1.to_csv("globalTotal.csv")
    df2 = pd.read_csv("globalTotal.csv", encoding="utf-8")

    xArr = list(range(1, 11))#代表前十天
    yArr = df2['total'].iloc[range(0, 10)].tolist()#取前十天的累计确诊数据
    _xArr = list(range(1, 16))#代表总计十五天
    _yArr = df2['total'].tolist()#十五天的累计确诊数据
    liner = LinearRegression()#线性模型实例
    liner.fit(np.reshape(xArr,(-1,1)),np.reshape(yArr,(-1,1)))#根据前十天的数据搭建线性回归模型
    y_pred = liner.predict(np.reshape(_xArr, (-1, 1)))#根据模型对15天的进行预测


    differ=[]
    plt.figure(figsize=(5, 5))
    plt.scatter(_xArr, _yArr)
    plt.plot(xArr,y_pred[:10],color="r")#前十天预测结果实线展示
    plt.plot(list(range(10,16)), y_pred[9:], color="r",linestyle="-.")#后五天预测结果虚线表示
    for i in range(10,15):
        differ.append({'day':'12-'+str(i+1),'total':_yArr[i],'pred_total':y_pred[i].tolist()[0]
                          ,'differ':(y_pred[i]-_yArr[i]).tolist()[0]})#差值数组
        plt.quiver(_xArr[i],_yArr[i],0,y_pred[i]-_yArr[i],color='g',
                   angles='xy', scale_units='xy', scale=1, width=0.005)#绘制箭头
    df=pd.DataFrame(differ)#字典转dataframe
    df.to_csv("differ.csv")
    with open('differ.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(differ, ensure_ascii=False))#输出成json文件
    plt.xticks(_xArr)
    plt.xlabel("日期")
    plt.ylabel("全球累计确诊人数")
    plt.title("利用前10天数据做后5天的预测")
    plt.legend(["累计确诊人数"],loc="upper left")
    plt.show()


if __name__ == '__main__':
    #在每个表第一列添加日期进行标识，将15天的表合成一张大表
    days = []
    df = pd.read_csv("COVID_19-2020-12-01.csv")
    df.insert(0, 'day', ['12-01'] * 186)
    df.to_csv("COVID_19-2020-12-all.csv", index=False)
    days.append('12-01')
    for i in range(2,16):
        if(i<10):
            filename="COVID_19-2020-12-0"+str(i)+".csv"
            df = pd.read_csv(filename)
            df.insert(0, 'day', ['12-0' + str(i)] * 186)
            days.append('12-0' + str(i))
        else:
            filename="COVID_19-2020-12-"+str(i)+".csv"
            df = pd.read_csv(filename)
            df.insert(0, 'day', ['12-' + str(i)] * 186)
            days.append('12-' + str(i))
        df.to_csv("COVID_19-2020-12-all.csv",index=False,header=False,mode="a+")
    task1(days)
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    task8()
    Efficiency()
    do_prediction()
