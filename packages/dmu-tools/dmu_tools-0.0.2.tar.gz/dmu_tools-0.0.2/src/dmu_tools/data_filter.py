import pandas as pd
import numpy as np
from multiprocessing import Pool

# 用第一种方法筛选采食数据，并记录每种错误的数量
def get_feed_data_filter_1(raw_data):
    # 将数据按照id——enter_time排序
    raw_data = raw_data.sort_values(by=['id', 'enter_time'])
    # 删除每个id的第一条和最后一条数据
    raw_data = raw_data.groupby('id').apply(
        lambda x: x.iloc[1:-1]).reset_index(drop=True)
    # 存储各种错误的数量
    error_num = {}
    error_index = []
    # FIV-low:每次采食量<-20g的数据
    error_num['FIV-low'] = len(
        raw_data[raw_data['feed_amount'] < -20])
    error_index.extend(raw_data[raw_data['feed_amount'] < -20].index)
    # FIV-high:每次采食量>2000g的数据
    error_num['FIV-high'] = len(
        raw_data[raw_data['feed_amount'] > 2000])
    error_index.extend(raw_data[raw_data['feed_amount'] > 2000].index)
    # FIV-0:每次采食量=0的数据
    error_num['FIV-0'] = len(raw_data[raw_data['feed_amount'] == 0])
    error_index.extend(raw_data[raw_data['feed_amount'] == 0].index)
    # OTV-low:每次采食时间<0的数据
    error_num['OTV-low'] = len(
        raw_data[raw_data['feed_time'] < 0])
    error_index.extend(raw_data[raw_data['feed_time'] < 0].index)
    # OTV-high:每次采食时间>3600s的数据
    error_num['OTV-high'] = len(
        raw_data[raw_data['feed_time'] > 3600])
    error_index.extend(raw_data[raw_data['feed_time'] > 3600].index)
    # FRV-High-FIV-low:每次采食率>500g/min且 0g<每次采食量<50g的数据
    error_num['FRV-High-FIV-low'] = len(raw_data[((raw_data['feed_amount'] > 0) & (
        raw_data['feed_amount'] < 50) & (raw_data['feed_time'] < 6))])
    error_index.extend(raw_data[((raw_data['feed_amount'] > 0) & (
        raw_data['feed_amount'] < 50) & (raw_data['feed_time'] < 6))].index)
    # FRV-high-strict:每次采食率>100g/min & 每次采食量≥50g或者每次采食量＜-20g
    error_num['FRV-high-strict'] = len(raw_data[((raw_data['feed_amount'] >= 50) | (
        raw_data['feed_amount'] < -20)) & (raw_data['feed_time'] < (50/(100/60)))])
    error_index.extend(raw_data[((raw_data['feed_amount'] >= 50) | (
        raw_data['feed_amount'] < -20)) & (raw_data['feed_time'] < (50/(100/60)))].index)
    # FRV-high:每次采食率>170g/min & 每次采食量≥50g或者每次采食量＜-20g的数据
    error_num['FRV-high'] = len(raw_data[((raw_data['feed_amount'] >= 50) | (
        raw_data['feed_amount'] < -20)) & (raw_data['feed_time'] < (50/(170/60)))])
    error_index.extend(raw_data[((raw_data['feed_amount'] >= 50) | (
        raw_data['feed_amount'] < -20)) & (raw_data['feed_time'] < (50/(170/60)))].index)
    # FRV-0:每次采食率=0g/min & 采食时间>500s
    error_num['FRV-0'] = len(raw_data[((raw_data['feed_amount']
                                        == 0) & (raw_data['feed_time'] > 500))])
    error_index.extend(raw_data[((raw_data['feed_amount']
                                == 0) & (raw_data['feed_time'] > 500))].index)
    # FRV-low:每次采食率!=0g/min & 采食率<2g/min
    error_num['FRV-low'] = len(raw_data[((raw_data['feed_amount'] != 0) & (
        (raw_data['feed_amount'] / raw_data['feed_time'])*60 < 2))])
    error_index.extend(raw_data[((raw_data['feed_amount'] != 0) & (
        (raw_data['feed_amount'] / raw_data['feed_time'])*60 < 2))].index)
    # all:所有错误的数据
    error_num['all'] = len(raw_data[((raw_data['feed_amount'] < -20) | (raw_data['feed_amount'] > 2000) | (raw_data['feed_amount'] == 0) | (raw_data['feed_time'] < 0) | (raw_data['feed_time'] > 3600) | ((raw_data['feed_amount'] > 0) & (raw_data['feed_amount'] < 50) & (raw_data['feed_time'] < 6))
                                    | ((raw_data['feed_amount'] >= 50) & (raw_data['feed_time'] < 6)) | ((raw_data['feed_amount'] >= 50) & (raw_data['feed_time'] < 6)) | ((raw_data['feed_amount'] == 0) & (raw_data['feed_time'] > 500)) | ((raw_data['feed_amount'] != 0) & (raw_data['feed_time'] < 2)))])
    # 返回筛选后的数据
    return raw_data.drop(error_index)

# 用第二种方法筛选采食数据，并记录每种错误的数量
def get_feed_data_filter_2(raw_data):
    # 需要的数据：id,enter_time,exit_time,feed_amount,feed_time,weight,birth_date
    # 单位：feed_amount:g,feed_time:s

    # 计算FRV = feed rate value (feed amount / feed time)，g/min
    raw_data['FRV'] = raw_data['feed_amount'] / raw_data['feed_time'] * 60
    # 计算FRV的上下限
    FRV_up = raw_data['FRV'].quantile(0.75) + \
        1.5*(raw_data['FRV'].quantile(0.75) -
             raw_data['FRV'].quantile(0.25))
    FRV_down = raw_data['FRV'].quantile(0.25) - \
        1.5*(raw_data['FRV'].quantile(0.75) -
             raw_data['FRV'].quantile(0.25))
    # 计算OTV的上下限
    OTV_up = raw_data['feed_time'].quantile(0.75) + \
        1.5*(raw_data['feed_time'].quantile(0.75) -
             raw_data['feed_time'].quantile(0.25))
    OTV_down = raw_data['feed_time'].quantile(0.25) - \
        1.5*(raw_data['feed_time'].quantile(0.75) -
             raw_data['feed_time'].quantile(0.25))
    # 计算前向体重差 LWD = leading weight difference (weight of following visit − weight of present visit)
    raw_data['LWD'] = raw_data.groupby(
        'id')['weight'].shift(-1) - raw_data['weight']
    # 计算LWD的上下限
    LWD_up = raw_data['LWD'].quantile(0.75) + \
        1.5*(raw_data['LWD'].quantile(0.75) -
             raw_data['LWD'].quantile(0.25))
    LWD_down = raw_data['LWD'].quantile(0.25) - \
        1.5*(raw_data['LWD'].quantile(0.75) -
             raw_data['LWD'].quantile(0.25))
    # 计算后向体重差 FWD = following weight difference (weight of present visit − weight of preceding visit)
    raw_data['FWD'] = raw_data['weight'] - \
        raw_data.groupby('id')['weight'].shift(1)
    # 计算FWD的上下限
    FWD_up = raw_data['FWD'].quantile(0.75) + \
        1.5*(raw_data['FWD'].quantile(0.75) -
             raw_data['FWD'].quantile(0.25))
    FWD_down = raw_data['FWD'].quantile(0.25) - \
        1.5*(raw_data['FWD'].quantile(0.75) -
             raw_data['FWD'].quantile(0.25))
    # 计算前向时间差 LTD = leading time difference (entrance time of following visit − exit time of present visit)
    raw_data['LTD'] = raw_data.groupby(
        'id')['enter_time'].shift(-1) - raw_data['exit_time']
    raw_data['LTD'] = raw_data['LTD'].apply(lambda x: x.total_seconds())
    # 计算LTD的上下限
    LTD_up = raw_data['LTD'].quantile(0.75) + \
        1.5*(raw_data['LTD'].quantile(0.75) -
             raw_data['LTD'].quantile(0.25))
    LTD_down = raw_data['LTD'].quantile(0.25) - \
        1.5*(raw_data['LTD'].quantile(0.75) -
             raw_data['LTD'].quantile(0.25))
    # 计算后向时间差 FTD = following time difference (entrance time of present visit − exit time of preceding visit)
    raw_data['FTD'] = raw_data['enter_time'] - \
        raw_data.groupby('id')['exit_time'].shift(1)
    raw_data['FTD'] = raw_data['FTD'].apply(lambda x: x.total_seconds())
    # 计算FTD的上下限
    FTD_up = raw_data['FTD'].quantile(0.75) + \
        1.5*(raw_data['FTD'].quantile(0.75) -
             raw_data['FTD'].quantile(0.25))
    FTD_down = raw_data['FTD'].quantile(0.25) - \
        1.5*(raw_data['FTD'].quantile(0.75) -
             raw_data['FTD'].quantile(0.25))
    

    error_num = {}
    error_index = []
    # error1: 所有进出站数据中，每次采食量FIV<-20g的数据
    error1 = raw_data[raw_data['feed_amount'] < -20]
    error_index.extend(error1.index)
    error_num['error1'] = len(error1)
    # error2: 所有进出站数据中，每次采食量FIV>2000g的数据
    error2 = raw_data[raw_data['feed_amount'] > 2000]
    error_index.extend(error2.index)
    error_num['error2'] = len(error2)
    # error3: 采食时间OTV=0的数据中，|FIV|>20g的数据
    error3 = raw_data[(raw_data['feed_time'] == 0) &
                      (abs(raw_data['feed_amount']) > 20)]
    error_index.extend(error3.index)
    error_num['error3'] = len(error3)
    # error4: 所有进出站数据中，采食时间OTV<0s的数据
    error4 = raw_data[raw_data['feed_time'] < 0]
    error_index.extend(error4.index)
    error_num['error4'] = len(error4)
    # error5: 所有进出站数据中，采食时间OTV>OTV_up的数据
    error5 = raw_data[raw_data['feed_time'] > OTV_up]
    error_index.extend(error5.index)
    error_num['error5'] = len(error5)
    # error6: 0g<FIV<50g的数据中，采食速率FRV>500g/min的数据
    error6 = raw_data[(raw_data['feed_amount'] > 0) & (
        raw_data['feed_amount'] < 50) & (raw_data['FRV'] > 500)]
    error_index.extend(error6.index)
    error_num['error6'] = len(error6)
    # error7: FIV>50g的数据中，采食速率FRV>110g/min的数据
    error7 = raw_data[(raw_data['feed_amount'] > 50) & (
        raw_data['FRV'] > 110)]
    error_index.extend(error7.index)
    error_num['error7'] = len(error7)
    # error8: FIV>50g的数据中，采食速率FRV>FRV_up的数据
    error8 = raw_data[(raw_data['feed_amount'] > 50) & (
        raw_data['FRV'] > FRV_up)]
    error_index.extend(error8.index)
    error_num['error8'] = len(error8)
    # error9: FRV=0g/min的数据中，OTV>OTV_up的数据
    error9 = raw_data[(raw_data['feed_amount'] == 0)
                      & (raw_data['feed_time'] > OTV_up)]
    error_index.extend(error9.index)
    error_num['error9'] = len(error9)
    # error10: FRV!=0g/min的数据中，|FRV|<2g/min的数据
    error10 = raw_data[(raw_data['feed_amount'] != 0)
                       & (abs(raw_data['FRV']) < 2)]
    error_index.extend(error10.index)
    error_num['error10'] = len(error10)
    # error11: LWD<LWD_down的数据
    error11 = raw_data[raw_data['LWD'] < LWD_down]
    error_index.extend(error11.index)
    error_num['error11'] = len(error11)
    # error12: LWD>LWD_up的数据
    error12 = raw_data[raw_data['LWD'] > LWD_up]
    error_index.extend(error12.index)
    error_num['error12'] = len(error12)
    # error13: FWD<FWD_down的数据
    error13 = raw_data[raw_data['FWD'] < FWD_down]
    error_index.extend(error13.index)
    error_num['error13'] = len(error13)
    # error14: FWD>FWD_up的数据
    error14 = raw_data[raw_data['FWD'] > FWD_up]
    error_index.extend(error14.index)
    error_num['error14'] = len(error14)
    # error15: LTD<0s的数据
    error15 = raw_data[raw_data['LTD'] < 0]
    error_index.extend(error15.index)
    error_num['error15'] = len(error15)
    # error16: FTD<0s的数据
    error16 = raw_data[raw_data['FTD'] < 0]
    error_index.extend(error16.index)
    error_num['error16'] = len(error16)
    result = raw_data.drop(error_index)
    # all:所有错误的数据
    error_num['all'] = len(raw_data) - len(result)
    return result

# 就不筛了。按原来的步骤！
def get_feed_data_filter_3(raw_data):
    # 需要的数据：id,enter_time,exit_time,feed_amount,feed_time,weight,birth_date
    # 单位：feed_amount:g,feed_time:s

    # 计算FRV = feed rate value (feed amount / feed time)，g/min
    raw_data['FRV'] = raw_data['feed_amount'] / raw_data['feed_time'] * 60

    # 计算前向体重差 LWD = leading weight difference (weight of following visit − weight of present visit)
    raw_data['LWD'] = raw_data.groupby(
        'id')['weight'].shift(-1) - raw_data['weight']

    # 计算后向体重差 FWD = following weight difference (weight of present visit − weight of preceding visit)
    raw_data['FWD'] = raw_data['weight'] - \
        raw_data.groupby('id')['weight'].shift(1)

    # 计算前向时间差 LTD = leading time difference (entrance time of following visit − exit time of present visit)
    raw_data['LTD'] = raw_data.groupby(
        'id')['enter_time'].shift(-1) - raw_data['exit_time']
    raw_data['LTD'] = raw_data['LTD'].apply(lambda x: x.total_seconds())

    # 计算后向时间差 FTD = following time difference (entrance time of present visit − exit time of preceding visit)
    raw_data['FTD'] = raw_data['enter_time'] - \
        raw_data.groupby('id')['exit_time'].shift(1)
    raw_data['FTD'] = raw_data['FTD'].apply(lambda x: x.total_seconds())

    result = raw_data
    return result

def weight_filter(raw_data: pd.DataFrame):
    # 按id分组
    groups = raw_data.groupby('id')
    # 多进程筛选
    result = paralleize_dataframe(groups, apply_filt_group)
    return result

def filt_weight(group):
    """
    用于筛选体重数据
    n_std: 残差的标准差的倍数
    """
    group = group.copy()
    group.sort_values(by=['age'], inplace=True)
    # start_weight和weight不是一个单位欸
    group.at[group.index[0], 'weight'] = group.at[group.index[0], 'start_weight']
    group.at[group.index[-1], 'weight'] = group.at[group.index[-1], 'end_weight']
    # 只用开始和结束体重用于构建线性模型
    model = np.polyfit(group['age'].iloc[[0, -1]], group['weight'].iloc[[0, -1]], 1)
    # 计算残差
    group['residual'] = group['weight'] - (model[0]*group['age'] + model[1])

    # 计算残差的标准差
    std = group['residual'].std()
    # 将weight中超过残差绝对值三个标准差的数据改为nan
    group.loc[abs(group['residual']) > 3*std, 'weight'] = np.nan
    # 增加一列，记录这处是否改成了nan
    group['weight_is_nan'] = group['weight'].isna()
    # 增加一列，记录std
    group['std'] = std
    # 用移动平均法填充
    group['weight'] = group['weight'].fillna(
        group['weight'].rolling(5, min_periods=1).mean())
    return group

def apply_filt_group(group):
    return filt_weight(group)

def paralleize_dataframe(df_grouped, func):
    df_split = [group for name, group in df_grouped]
    pool = Pool(16)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    df.drop(columns=['weight_is_nan', 'residual', 'std'], inplace=True)
    return df

def get_data(raw_data, filter_method=2):
    # 需要的数据：id,enter_time,exit_time,feed_amount,feed_time,weight,birth_date
    # 单位：feed_amount:g,feed_time:s
    uneed_columns = ['FTD', 'LTD', 'FWD', 'LWD', 'FRV', 'exit_time', 'feed_time']
    data = raw_data.copy()
    data['enter_time'] = pd.to_datetime(data['enter_time'])
    data['exit_time'] = pd.to_datetime(data['exit_time'])
    data['birth_date'] = pd.to_datetime(data['birth_date'])

    data['age'] = data['enter_time'] - data['birth_date']
    data['age'] = data['age'].dt.total_seconds()
    
    data = weight_filter(data)

    data['age'] = data['enter_time'] - data['birth_date']
    data['age'] = data['age'].dt.days

    final_data = data.copy()

    # 筛选采食数据
    if filter_method == 1:
        data = get_feed_data_filter_1(data)
    elif filter_method == 2:
        data = get_feed_data_filter_2(data)
    elif filter_method == 3:
        data = get_feed_data_filter_3(data)

    # 按id和date排序
    final_data = data.sort_values(by=['id', 'age'])

    # 将体重的零值填充为前后5次体重的平均值
    final_data['weight'] = final_data.groupby('id', group_keys=False)['weight'].apply(
        lambda x: x.replace(0, np.nan).fillna(method='ffill').fillna(method='bfill'))
    
    # 如果数据所有体重均值 > 1000g，那么将体重单位转换为kg
    if final_data['weight'].mean() > 1000:
        final_data['weight'] = final_data['weight'] / 1000
    if final_data['start_weight'].mean() > 1000:
        final_data['start_weight'] = final_data['start_weight'] / 1000
    if final_data['end_weight'].mean() > 1000:
        final_data['end_weight'] = final_data['end_weight'] / 1000

    # 如果数据所有采食均值 > 100g，那么将采食单位转换为kg
    if final_data['feed_amount'].mean() > 10:
        final_data['feed_amount'] = final_data['feed_amount'] / 1000

    # 如果有uneed_columns中的列，那么删除
    for column in uneed_columns:
        if column in final_data.columns:
            final_data = final_data.drop(columns=[column])

    # 改最小enter_time
    final_data['enter_time'] = final_data.groupby('id')['enter_time'].transform('min')
    # 求出每天的采食总量
    final_data['feed_amount'] = final_data.groupby(['id', 'age'])['feed_amount'].transform('sum')
    # 求出每天的平均体重
    final_data['weight'] = final_data.groupby(['id', 'age'])['weight'].transform('mean')

    # 删除重复的数据
    final_data.drop_duplicates(inplace=True)

    # 将第一条体重改成start_weight
    final_data.loc[final_data.groupby('id').head(1).index, 'weight'] = final_data['start_weight']
    # 将最后一条体重改成end_weight
    final_data.loc[final_data.groupby('id').tail(1).index, 'weight'] = final_data['end_weight']

    final_data.reset_index(drop=True, inplace=True)

    return final_data