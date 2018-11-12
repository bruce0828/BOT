
# coding: utf-8

# # 对流量进行分析

# In[1]:


import numpy as np
import pandas as pd
import os
import seaborn as sns
import RawData_BasicData as rb
import get_grid_volume as ggv
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# In[2]:


def read_volume(date, ctype):
    # 读取流量excel文件
    base_path = 'E:\\0BOT\\volume_B'
    with open(os.path.join(base_path,ctype+'.xlsx'),'rb') as f:
        df = pd.read_excel(f,sheetname=date)
        return df


# In[3]:


def read_grid_volume(grid, ctype='tcar'):
    # 读取流量excel文件
    base_path = 'E:\\0BOT\\volume_B'
    
    grid_volume = dict()
    for date in rb.get_dates():
        with open(os.path.join(base_path,ctype+'.xlsx'),'rb') as f:
            df = pd.read_excel(f,sheetname=date).loc[:,9:22]
            grid_volume[date] = df.loc[grid,:].values
    grid_volume = pd.DataFrame(grid_volume).T
    grid_volume.columns = range(9,23)
    return grid_volume


# In[4]:


def days(daytype):
    # 将日期分为节假日、周末、工作日
    
    all_dates = set(rb.get_dates())  # from 20170102 to 20170312, totally 70 days
    holidays = {'20170102', '20170127', '20170128', '20170129', '20170130', '20170131',                '20170201', '20170202', '20170211'}
    weekends = {'20170107', '20170108', '20170114', '20170115', '20170121', '20170122',                '20170204', '20170205', '20170211', '20170212', '20170218', '20170219',                '20170225', '20170226', '20170304', '20170305', '20170311', '20170312'}
    January = set(map(lambda s: '201701' + s.zfill(2) ,np.arange(1,32).astype(str)))
    February = set(map(lambda s: '201702' + s.zfill(2) ,np.arange(1,29).astype(str)))
    March = set(map(lambda s: '201703' + s.zfill(2) ,np.arange(1,32).astype(str)))
    spring = set(map(lambda s: '201702' + s.zfill(2) ,np.arange(1,20).astype(str)))
    last_week = set(map(lambda s: '201703' + s.zfill(2) ,np.arange(6,13).astype(str)))
    pred_days = set(map(lambda s: '201703' + s.zfill(2) ,np.arange(13,27).astype(str)))    
    
    if   daytype == 'all_dates': return all_dates
    elif daytype == 'holiday': return holidays
    elif daytype == 'weekends': return weekends
    elif daytype == 'January': return January
    elif daytype == 'February': return February
    elif daytype == 'March': return March
    elif daytype == 'spring': return spring
    elif daytype == 'last_week': return last_week
    elif daytype == 'pred_days': return pred_days


# In[5]:


def classified_days(daytype):
    # 根据rmse热力图，将70天分为4类
    all_dates = set(rb.get_dates())
    spring = {'20170126', '20170127', '20170128', '20170129', '20170130', '20170131',              '20170201', '20170202', '20170203', '20170204', '20170205'}
    spring_buffer = set(map(lambda s: '201701'+s.zfill(2), np.arange(20,26).astype(str)))
    weekend = {'20170102', '20170107', '20170108', '20170114', '20170115', '20170211', '20170212',                '20170218', '20170219', '20170225', '20170226', '20170304', '20170305', '20170311', '20170312'}   # 一共15天
    weekday = all_dates - spring - spring_buffer - weekend
    # {'20170103', '20170104', '20170105', '20170106', '20170109', '20170110', '20170111', '20170112', '20170113', '20170116', '20170117',
    #  '20170118', '20170119', '20170206', '20170207', '20170208', '20170209', '20170210', '20170213', '20170214', '20170215', '20170216',
    #  '20170217', '20170220', '20170221', '20170222', '20170223', '20170224', '20170227', '20170228', '20170301', '20170302', '20170303',
    #  '20170306', '20170307', '20170308', '20170309', '20170310'}   一共38天
    
    
    monday = list(map(lambda s: '2017'+s, ['0109','0116','0206','0213','0220','0227','0306']))
    tuesday = list(map(lambda s: '2017'+s, ['0103','0110','0117','0207','0214','0221','0228','0307']))
    wednesday = list(map(lambda s: '2017'+s,['0104','0111','0118','0208','0215','0222','0301','0308']))
    thursday = list(map(lambda s: '2017'+s,['0105','0112','0119','0209','0216','0223','0302','0309']))
    friday = list(map(lambda s: '2017'+s, ['0106','0113','0210','0217','0224','0303','0310']))
    saturday = list(map(lambda s: '2017'+s, ['0107','0114','0211','0218','0225','0304','0311']))
    sunday = list(map(lambda s: '2017'+s, ['0108','0115','0212','0219','0226','0305','0312']))
    
    if   daytype == 'spring': return spring
    elif daytype == 'spring_buffer': return spring_buffer
    elif daytype == 'weekend': return weekend
    elif daytype == 'weekday': return weekday
    elif daytype == 'monday': return monday
    elif daytype == 'tuesday': return tuesday
    elif daytype == 'wednesday': return wednesday
    elif daytype == 'thursday': return thursday
    elif daytype == 'friday': return friday
    elif daytype == 'saturday': return saturday
    elif daytype == 'sunday': return sunday


# In[6]:


def kmeans_days(daytype):
    # 根据kmeans，将70天分为4类
    all_dates = set(rb.get_dates())
    
    # holiday: 元旦、春节、元宵

    holiday = {'20170102',               '20170123', '20170124', '20170125', '20170126', '20170127', '20170128', '20170129', '20170130',                '20170131', '20170201', '20170202', '20170203', '20170204', '20170205', '20170206',               '20170211'}
    saturday = {'20170107', '20170114', '20170121', '20170218', '20170225', '20170304', '20170311'}
    sunday =   {'20170108', '20170115', '20170122', '20170212', '20170219', '20170226', '20170305', '20170312'}
    weekday = all_dates - holiday - saturday - sunday   # 共38天
    
    monday =    list(map(lambda s: '2017'+s, ['0109','0116','0213','0220','0227','0306']))
    tuesday =   list(map(lambda s: '2017'+s, ['0103','0110','0117','0207','0214','0221','0228','0307']))
    wednesday = list(map(lambda s: '2017'+s, ['0104','0111','0118','0208','0215','0222','0301','0308']))
    thursday =  list(map(lambda s: '2017'+s, ['0105','0112','0119','0209','0216','0223','0302','0309']))
    friday =    list(map(lambda s: '2017'+s, ['0106','0113','0120','0210','0217','0224','0303','0310']))
    
    if   daytype == 'holiday': return holiday
    elif daytype == 'weekday': return weekday
    elif daytype == 'saturday': return saturday
    elif daytype == 'sunday': return sunday
    elif daytype == 'monday': return monday
    elif daytype == 'tuesday': return tuesday
    elif daytype == 'wednesday': return wednesday
    elif daytype == 'thursday': return thursday
    elif daytype == 'friday': return friday


# In[7]:


def mean_volume_in_days(days,ctype='tcar'):
    # 日期days的平均流量
    init = pd.DataFrame(0,index=range(1,51),columns=range(9,24))
    for day in days:
        init += read_volume(day,ctype)
    num = len(days)
    df = init/num
    return df


# In[8]:


def rmse(volume1, volume2):
    mse = ((volume1-volume2)**2).mean().mean()
    return np.sqrt(mse)


# In[9]:


def export_figure(df,date,ctype,dpi=300,display=False,save=False):
    '''
    输出每个表格热力图
    '''

    # Create a new figure, plot into it
    title = ctype + '-' + date
    fig = plt.figure(figsize=(25,7))
    sns.heatmap(df.loc[:,9:22].T,cmap='coolwarm',annot=True)
    plt.title(title,fontsize=20)
    plt.xlabel('Grid id',fontsize=18)
    plt.ylabel('Hour',fontsize=18)
    
    if display == True:
        plt.show()
        
    if save == True:
        base_path = 'E:\\0BOT\heatmaps'
        folder = os.path.join(base_path,ctype)
        if not os.path.exists(folder):
            os.makedirs(folder)
        save_path = os.path.join(folder,title+'.png')
        fig.tight_layout()
        plt.savefig(save_path,dpi=dpi,bbox_inches='tight',pad_inches=0)
        plt.close(fig)


# In[10]:


def fangan(volume,filename):
    # 原始example格式有问题，重新生成example格式
    pred_days = set(map(lambda s: '201703' + s.zfill(2) ,np.arange(13,27).astype(str))) 
    example = []
    for day in sorted(pred_days): 
        for hour in range(9,23):
            for grid in range(51,101):
                example.append([grid,day,hour])
    plan = pd.DataFrame(example,columns=['grid_id','day','hour'])
    
    # 根据14天、14小时、50栅格流量，整理成输出文件格式
    plan['car_number'] = volume
    plan.to_csv(os.path.join('C:\\Users\\zhpy\\Desktop',filename+'.csv'),index=False)
    return plan

