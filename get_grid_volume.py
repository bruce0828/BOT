
# coding: utf-8

# # 获取预测栅格流量

# In[ ]:


import numpy as np
import pandas as pd
import os
import datetime
import RawData_BasicData as rb


# In[ ]:


def get_hour(df):
    df.date_time = df.date_time.apply(pd.to_datetime)
    df.sort_values('date_time',inplace=True)
    df['hour'] = df.date_time.apply(lambda dt: dt.hour)
    return df


# In[ ]:


def parse_grid():
    grid = {}
    with open('E:\\0BOT\\BOT智能汽车技术赛的初赛A榜测试信息.csv') as f:
        for line in f.readlines()[1:]:
            l = line.rstrip().split(',')
            grid[int(l[0])] = np.append(np.array(l[1].split('~')).astype(float),np.array(l[2].split('~')).astype(float))
        f.close()
    return grid


# In[ ]:


def get_matrix_grid():
    # 将矩形分成多个小栅格
    lb = (121.315-0.005*3, 31.15-0.005*3)  # left_bottom
    rt = (121.775+0.005*3, 31.315+0.005*3)   # right_top 
    
    lons = np.arange(lb[0],rt[0],0.005)
    lats = np.arange(lb[1],rt[1],0.005)
    
    matrix = {}
    id = 0
    for i in range(len(lats)-1):
        for j in range(len(lons)-1):
            matrix[id] = np.array([lats[i],lats[i+1],lons[j],lons[j+1]])
            id += 1
    return matrix


# In[ ]:


def get_pred_grid_volume(df,start_hour=9,end_hour=23,gtype='pred'):
    # 预测grid矩阵
    df = get_hour(df)
    df = df[(df.hour>=start_hour) & (df.hour<=end_hour)]
    
    # 预测的栅格：（1）固定的50；（2）整个矩形框内所有栅格
    if gtype == 'pred':
        grid = parse_grid()
    elif gtype == 'matrix':
        grid = get_matrix_grid()
    
    m = end_hour - start_hour + 1
    n = len(grid)
    res = np.zeros((m,n))

    for hour,group in df.groupby('hour'):
        for key in grid.keys():
            df_hour = group[(group.lat>=grid[key][0]) & (group.lat<=grid[key][1]) & (group.lon>=grid[key][2]) & (group.lon<=grid[key][3])]
            num = df_hour.car_id.nunique()
            res[hour-start_hour,key-1] = num

    res = pd.DataFrame(res).T
    res = res.astype(int)
    res.columns = range(start_hour,end_hour+1)
    res.index = range(1,n+1)

    return res


# In[ ]:


def output_total_volume(date,out='tcar',start_hour=9,end_hour=23,gtype='pred'):
    # 输出某天总的grid volume
    base_path = 'E:\\0BOT\\basefile'
    
    if out == 'ecar':
        ecar = rb.read_raw_csv(os.path.join(base_path,'ecar',date+'.csv'),'ecar')
        volume = get_pred_grid_volume(ecar,start_hour,end_hour,gtype)
    elif out == 'rcar':
        rcar = rb.read_raw_csv(os.path.join(base_path,'rcar',date+'.csv'),'rcar')
        volume = get_pred_grid_volume(rcar,start_hour,end_hour,gtype)
    elif out == 'tcar':
        ecar = rb.read_raw_csv(os.path.join(base_path,'ecar',date+'.csv'),'ecar')
        e_volume = get_pred_grid_volume(ecar,start_hour,end_hour,gtype)
        rcar = rb.read_raw_csv(os.path.join(base_path,'rcar',date+'.csv'),'rcar')
        r_volume = get_pred_grid_volume(rcar,start_hour,end_hour,gtype)
        volume = e_volume + r_volume
    else: print('Please check the out parameter.')
        
    return volume


# In[ ]:


def outputs(volume_panel,out='tcar'):
    # 生成文件
    base_path = 'E:\\0BOT\\volume'
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    volume_panel.to_excel(os.path.join(base_path,out+'.xlsx'))


# In[ ]:


if __name__ == '__main__':
    for out in ['ecar','rcar','tcar']:
        volume = {}
        for date in rb.get_dates():
            volume[date] = output_total_volume(date,out)
        outfile = pd.Panel(volume)
        outputs(outfile,out)
        print(out,date)


# In[ ]:


# # test1
# date = '20170306'
# res = output_total_volume(date,out='tcar',start_hour=9,end_hour=12,gtype='matrix')
# res

