
# coding: utf-8

# In[2]:


import pandas as pd
import os
import datetime


# In[3]:


def read_raw_csv(path,ctype):
    # 打开原始的csv文件
    with open(path) as f:
        if ctype == 'ecar':
            return pd.read_csv(f,dtype={'system_mode':str})
        elif ctype == 'rcar':
            return pd.read_csv(f)


# In[7]:


def get_dates():
    # 获得所有数据的日期
    base_path = 'E:\\0BOT\BOT智能汽车技术挑战赛初赛数据集'
    ctype = 'ecar'
    files = os.listdir(os.path.join(base_path, ctype))
    dates = set(map(lambda x: x.split('_')[3],files))
    dates = sorted(list(dates))
    return dates


# In[20]:


def combine_samedate_files(date, ctype):
    # 对同一日期的文件进行合并.原始所有日期被分为3个
    base_path = 'E:\\0BOT\BOT智能汽车技术挑战赛初赛数据集'
    d0 = read_raw_csv(os.path.join(base_path,ctype,'BOT_data_' + ctype + ('_' + date)*2 + '_part0.csv'), ctype)
    d1 = read_raw_csv(os.path.join(base_path,ctype,'BOT_data_' + ctype + ('_' + date)*2 + '_part1.csv'), ctype)
    d2 = read_raw_csv(os.path.join(base_path,ctype,'BOT_data_' + ctype + ('_' + date)*2 + '_part2.csv'), ctype)   
    d = pd.concat([d0,d1,d2],axis=0,ignore_index=True)
    
    # 根据经纬度筛选
    lb = (121.315-0.005*3, 31.15-0.005*3)  # left_bottom
    rt = (121.775+0.005*3, 31.315+0.005*3)   # right_top 
    df = d[(d.lon>=lb[0]) & (d.lon<=rt[0]) & (d.lat>=lb[1]) & (d.lat<=rt[1])]
    return df


# In[9]:


def save_split_file(date_folder, ctype, df):
    # 一天数据中可能包含其他日期数据
    datetimes = df.date_time.unique()
    dates = map(lambda x: x.split(' ')[0], datetimes)
    dates = sorted(set(dates))
    
    # 新建文件夹
    folder = os.path.join('E:\\0BOT','new',ctype,date_folder)
    if not os.path.exists(folder):     #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(folder)
        
    for date in dates:
        file = df[df.date_time.str.contains(date)]
        file.to_csv(os.path.join('E:\\0BOT','new',ctype,date_folder,date+'.csv'),index=False)


# In[10]:


def filter_files(date, ctype):
    # 在所有子目录中搜索与日期对应的文件
    # 输入date='20170102
    
    # 所有的子文件列表
    file_path = 'E:\\0BOT\\new'
    path_list = []
    for eachdate in get_dates():
        folder_path = os.path.join(file_path,ctype,eachdate)
        folders = os.listdir(folder_path)
        for file in folders:
            path_list.append(os.path.join(file_path,ctype,eachdate,file))
    
    # 筛选
    filter_file = []
    target_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
    for file in path_list:
        if target_date in file:
            filter_file.append(file)
            
    return filter_file


# In[21]:


def combine_filter_files(date, ctype):
    # 对筛选出来的文件路径，读出、合并
    filter_file = filter_files(date, ctype)
    
    if ctype == 'ecar':
        cols = 'car_id,date_time,lat,lon,work_mode,mileage,speed,avg_fuel_consumption,system_mode'.split(',')
    elif ctype == 'rcar':
        cols = 'car_id,date_time,lat,lon,power_mode,mileage,speed,fuel_consumption'.split(',')
    
    df = pd.DataFrame(columns=cols)
    for file in filter_file:
        dfile = read_raw_csv(file,ctype)
        df = pd.concat([df,dfile],axis=0,ignore_index=True)
        
    df.drop_duplicates(inplace=True)
    return df


# In[12]:


def save_filter_files(df):
    # 新建文件夹
    folder = os.path.join('E:\\0BOT','basefile',ctype)
    if not os.path.exists(folder):     #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(folder)
    df.to_csv(os.path.join('E:\\0BOT','basefile',ctype,date+'.csv'),index=False)


# In[ ]:


if __name__ == '__main__':
    
    # 对原始文件按日期拆分（可能一个文件包含多个日期）
    base_path = 'E:\\0BOT\BOT智能汽车技术挑战赛初赛数据集'
    
    for ctype in ['ecar','rcar']:
        for date in get_dates():
            car = combine_samedate_files(date, ctype)
            save_split_file(date, ctype, car)
            print(ctype,date)
    print('file split finished!')
    
    # 对拆分的文件进行合并
    for ctype in ['ecar','rcar']:
        for date in get_dates():
            df = combine_filter_files(date, ctype)
            save_filter_files(df)
            print(ctype,date)
    print('files combine finished!')


# In[ ]:


# # test1
# ctype = 'ecar'
# date = '20170306'
# car = combine_samedate_files(date, ctype)
# save_file(date, ctype, car)


# In[23]:


# # test2
# ctype = 'rcar'
# for date in get_dates():
#     df = combine_filter_files(date, ctype)
#     save_filter_files(df)
#     print(ctype,date)
# print('files combine finished!')

