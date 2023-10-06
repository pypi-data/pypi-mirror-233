import numpy as np
import pandas as pd
from numpy.polynomial import legendre
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import time

# 数据处理

class Data_Generator:
    def __init__(self, daily_data):

        self.raw_data = daily_data.copy()
        self.daily_data = self.get_daily_data()
        print("daily_data shape: ", self.daily_data.shape)
        self.id_encoder = self.get_id_encoder()
        print("id_encoder shape: ", self.id_encoder.classes_.shape)
        self.daily_data["id"] = self.id_encoder.transform(self.daily_data["id"]) + 1
        self.daily_data["father"] = (
            self.id_encoder.transform(self.daily_data["father"]) + 1
        )
        self.daily_data["mother"] = (
            self.id_encoder.transform(self.daily_data["mother"]) + 1
        )
        self.max_day = self.daily_data["age"].max()
        self.min_day = self.daily_data["age"].min()

    # 获得daily_data
    def get_daily_data(self):
        raw_data = self.raw_data.copy()
        # 排序
        raw_data = raw_data.sort_values(["id", "age"]).reset_index(drop=True)
        # 计算每天的增重
        raw_data["gain_weight"] = raw_data.groupby("id")["weight"].diff()
        return raw_data.reset_index(drop=True)

    # 对daily_data中每个个体的长度进行统计
    def get_id_length(self):
        id_length = self.daily_data.groupby("id").count()["age"]
        return id_length

    # 获得id_encoder
    def get_id_encoder(self):
        ids = pd.concat(
            [
                self.daily_data["id"],
                self.daily_data["father"],
                self.daily_data["mother"],
            ]
        ).unique()
        id_encoder = LabelEncoder()
        id_encoder.fit(ids)
        return id_encoder

    # 根据dataframe中的“age”，获得每条数据对应lg值
    def get_lg_df(self, input_data, degree=5):
        lg_df = input_data.copy()[["age", "id"]]
        min_day = lg_df["age"].min()
        max_day = lg_df["age"].max()
        lg_df["standared_day"] = 2 * (lg_df["age"] - min_day) / (max_day - min_day) - 1
    
        for i in range(degree + 1):
            lg_df['lg' + str(i)] = legendre.legval(lg_df['standared_day'], [0] * i + [1]) * np.sqrt((2 * i + 1) / 2)
        
        return lg_df.drop(["standared_day", "age", "id"], axis=1)

    # 根据输入数据，获得batch_df: 年-季-年龄
    def get_batch_df(self, input_data):
        batch_df = input_data[["id"]].copy()

        # 按个体号，进入时间排序
        input_data = input_data.sort_values(["id", "age"]).reset_index(drop=True).copy()
        data = (
            input_data.groupby("id")
            .first()
            .reset_index(drop=False)[["id", "enter_time", "age"]]
            .copy()
        )
        data["year"] = data["enter_time"].apply(lambda t: t.year)
        data["season"] = data["enter_time"].apply(lambda t: t.quarter)
        data["age"] = data["age"].apply(lambda t: int(t / 10))

        # 结合年份和季度，获得year-season
        data["batch"] = (
            data["year"].astype(str)
            + "-"
            + data["season"].astype(str)
            + "-"
            + data["age"].astype(str)
        )

        batch_df = batch_df.merge(data[["id", "batch"]], on="id", how="left")

        return batch_df[["batch"]]
    

    def get_dmu_data(
        self, sep=5, if_max_breed=False, if_max_sex=False, min_test_length=0
    ):
        target_columns = [
            "sex",
            "batch",
            "breed",
            "station",
            "id",
            "lg0",
            "lg1",
            "lg2",
            "lg3",
            "lg4",
            "lg5",
            "dfi",
            "dgw",
            "fcr",
        ]
        final_data = self.daily_data.copy()

        start_time = time.time()
        # 删除数据条数小于min_test_length的个体
        id_length = self.get_id_length()
        id_length = id_length[id_length >= min_test_length]
        final_data = final_data[final_data["id"].isin(id_length.index)]
        print("删除数据条数小于min_test_length的个体: ", time.time() - start_time)
        start_time = time.time()
        # 删除每个id的第一条和最后一条数据
        final_data = (
            final_data.groupby("id")
            .apply(lambda x: x.iloc[1:-1])
            .reset_index(drop=True)
        )
        print("删除每个id的第一条和最后一条数据: ", time.time() - start_time)

        feed_data = pd.DataFrame()
        feed_datas = []
        start_time = time.time()
        for id, data in final_data.groupby("id"):
            bins = int(len(data) / sep)
            groups = pd.cut(data.index, bins=bins, labels=False)
            data["group"] = groups

            new_data = data.groupby("group")[["feed_amount", "gain_weight"]].mean(
                numeric_only=False
            )

            new_data["id"] = id
            new_data["age"] = data.groupby("group").last()["age"]
            new_data["fcr"] = new_data["feed_amount"] / new_data["gain_weight"]

            feed_datas.append(new_data)
            
        feed_data = pd.concat(feed_datas, axis=0)
        
        feed_data.rename(
            columns={"feed_amount": "dfi", "gain_weight": "dgw"}, inplace=True
        )
        print("feed_data: ", time.time() - start_time)

        start_time = time.time()

        final_data = final_data.drop(["feed_amount", "gain_weight", "weight"], axis=1)
        final_data = feed_data.merge(final_data, on=["id", "age"])
        print("merge: ", time.time() - start_time)

        start_time = time.time()
        # 获得lg_df
        lg_df = self.get_lg_df(final_data)
        print("lg_df: ", time.time() - start_time)
        start_time = time.time()
        # 获得ys_df
        ys_df = self.get_batch_df(final_data)
        print("ys_df: ", time.time() - start_time)
        start_time = time.time()
        # 左右拼接数据
        final_data = pd.concat([final_data, lg_df, ys_df], axis=1)
        print("concat: ", time.time() - start_time)
        start_time = time.time()
        # 对object类型的数据进行编码
        final_data = self.recode_object_data(final_data)
        print("recode: ", time.time() - start_time)
        start_time = time.time()
        xp = final_data[["id", "father", "mother"]].copy()
        xp["year"] = 2018
        xp = xp.drop_duplicates().reset_index(drop=True)
        print("xp: ", time.time() - start_time)

        start_time = time.time()
        # 是否删除其它品种
        if if_max_breed:
            # 选择数量最多的品种
            final_data = self.get_max_breed_data(final_data)
            # 在target_columns中删除breed
            target_columns.remove("breed")
        print("if_max_breed: ", time.time() - start_time)
        start_time = time.time()

        # 是否删除其它性别
        if if_max_sex:
            # 选择数量最多的性别
            final_data = self.get_max_sex_data(final_data)
            # 在target_columns中删除sex
            target_columns.remove("sex")
        print("if_max_sex: ", time.time() - start_time)
        return final_data[target_columns].round(4), xp

    def recode_object_data(self, data):
        for col in data.columns:
            if data[col].dtype == "object":
                data[col] = LabelEncoder().fit_transform(data[col]) + 1
        return data

    def get_rep_data(
        self, sep=5, if_max_breed=False, if_max_sex=False, min_test_length=0
    ):
        final_data, xp = self.get_dmu_data(
            sep, if_max_breed, if_max_sex, min_test_length
        )
        # 删除不需要的列
        final_data = final_data.drop(["lg0", "lg1", "lg2", "lg3", "lg4", "lg5"], axis=1)
        return final_data.round(2), xp

    def get_ani_data(self, if_max_breed=False, if_max_sex=False, min_test_length=0):
        final_data, xp = self.get_dmu_data(1, if_max_breed, if_max_sex, min_test_length)

        data1 = final_data[["id", "dfi", "dgw"]].copy()

        data1 = data1.groupby("id").sum()
        data1.reset_index(inplace=True, drop=False)
        data1["fcr"] = data1["dfi"] / data1["dgw"]

        data2 = (
            final_data.drop(
                ["lg0", "lg1", "lg2", "lg3", "lg4", "lg5", "dfi", "dgw", "fcr"], axis=1
            )
            .copy()
            .drop_duplicates()
        )

        data = data1.merge(data2, on="id", how="left")
        data = data[data2.columns.tolist() + ["dfi", "dgw", "fcr"]]
        return data.round(2), xp

    def get_normal_data(self):
        data = self.daily_data.copy()
        batch_df = self.get_batch_df(data)
        data = pd.concat([data, batch_df], axis=1)
        # 按照id，年龄排序
        data = data.sort_values(["id", "age"]).reset_index(drop=True)
        # 获得每个id的数据条数
        data["count"] = data.groupby("id")["id"].transform("count")
        # 计算每个id的日均增重
        data["gain_weight"] = data["end_weight"] - data["start_weight"]
        data["dgw"] = data["gain_weight"] / data["count"]
        # 计算每个id的日均采食
        data["total_feed"] = data.groupby("id")["feed_amount"].transform("sum") / 1000
        data["dfi"] = data["total_feed"] / data["count"]
        # 计算每个id的日均饲料转化率
        data["fcr"] = data["total_feed"] / data["gain_weight"]

        data = self.recode_object_data(data)

        return (
            data.drop(
                [
                    "gain_weight",
                    "total_feed",
                    "gain_weight",
                    "count",
                    "age",
                    "feed_amount",
                    "index",
                    "birth_date",
                    "weight",
                    "enter_time",
                    "birth_weight",
                    "start_weight",
                    "end_weight",
                ],
                axis=1,
            )
            .round(2)
            .drop_duplicates()
            .reset_index(drop=True)
        )

    def get_range_normal_data_1(
        self, start, end, sep=7, start_range=2, chunk_num=5, if_max_sex=False, if_max_breed=False, if_backwards=False
    ):
        ini_start = start
        ini_end = end
        data = self.daily_data.copy()
        batch_df = self.get_batch_df(data)
        data = pd.concat([data, batch_df], axis=1)

        # 按照id，年龄排序
        data = data.sort_values(["id", "age"]).reset_index(drop=True)

        wanted_id = self.get_id_by_age_range(ini_start, ini_end)

        target_datas = []

        if if_backwards:
            start = ini_end
            end = ini_end
        else:
            start = ini_start
            end = ini_start

        for _ in range(chunk_num):
            if if_backwards:
                start = start - sep - (start_range - 1) * sep
                end = end
            else:
                start = start
                end = end + sep + (start_range - 1) * sep
            # 删除不需要的id
            target_data = data[data["id"].isin(wanted_id)].copy()
            #  只保留日龄内数据
            target_data = target_data[
                (target_data["age"] >= ini_start) & (target_data["age"] <= ini_end)
            ]
            # 获得每个id的数据条数
            target_data["count"] = target_data.groupby("id")["id"].transform("count")
            # 将开测体重换成每个id的第一条数据的体重
            target_data["start_weight"] = target_data.groupby("id")["weight"].transform(
                "first"
            )
            # 将结测体重换成每个id的最后一条数据的体重
            target_data["end_weight"] = target_data.groupby("id")["weight"].transform(
                "last"
            )
            # 计算每个id的日均增重
            target_data["gain_weight"] = (
                target_data["end_weight"] - target_data["start_weight"]
            )
            target_data["dgw"] = target_data["gain_weight"] / target_data["count"]
            # 计算每个id的日均采食
            target_data["total_feed"] = target_data.groupby("id")[
                "feed_amount"
            ].transform("sum")
            target_data["dfi"] = target_data["total_feed"] / target_data["count"]
            # 计算每个id的日均饲料转化率
            target_data["fcr"] = target_data["total_feed"] / target_data["gain_weight"]

            # 计算时间范围内的数据
            range_data = target_data[
                (target_data["age"] >= start) & (target_data["age"] <= end)
            ].copy()
            # 获得每个id的数据条数
            range_data["count"] = range_data.groupby("id")["id"].transform("count")
            # 将开测体重换成每个id的第一条数据的体重
            range_data["start_weight"] = range_data.groupby("id")["weight"].transform(
                "first"
            )
            # 将结测体重换成每个id的最后一条数据的体重
            range_data["end_weight"] = range_data.groupby("id")["weight"].transform(
                "last"
            )
            # 计算每个id的日均增重
            range_data["gain_weight"] = (
                range_data["end_weight"] - range_data["start_weight"]
            )
            range_data["range_dgw"] = range_data["gain_weight"] / range_data["count"]
            # 计算每个id的日均采食
            range_data["total_feed"] = range_data.groupby("id")[
                "feed_amount"
            ].transform("sum")
            range_data["range_dfi"] = range_data["total_feed"] / range_data["count"]
            # 计算每个id的日均饲料转化率
            range_data["range_fcr"] = (
                range_data["total_feed"] / range_data["gain_weight"]
            )
            # 只保留id, range_dgw, range_dfi, range_fcr
            range_data = (
                range_data[["id", "range_dgw", "range_dfi", "range_fcr"]]
                .drop_duplicates()
                .reset_index(drop=True)
            )

            # 将range_data与data合并
            target_data = target_data.merge(range_data, on="id", how="left")

            target_data = self.recode_object_data(target_data)
            target_data = (
                target_data.drop(
                    [
                        "gain_weight",
                        "total_feed",
                        "gain_weight",
                        "count",
                        "age",
                        "feed_amount",
                        "birth_date",
                        "weight",
                        "enter_time",
                        "birth_weight",
                        "start_weight",
                        "end_weight",
                    ],
                    axis=1,
                )
                .round(2)
                .drop_duplicates()
                .reset_index(drop=True)
            )
            # 是否删除其它品种
            if if_max_breed:
                # 选择数量最多的品种
                target_data = self.get_max_breed_data(target_data)
                # 在target_columns中删除breed
                target_data = target_data.drop(["breed"], axis=1)
            # 是否删除其它性别
            if if_max_sex:
                target_data = self.get_max_sex_data(target_data)
                # 在target_columns中删除sex
                target_data = target_data.drop(["sex"], axis=1)
            target_datas.append(target_data)

        return target_datas
    
    def get_range_normal_data_2(
        self, start, end, sep=7, chunk_num=5, if_max_sex=False, if_max_breed=False, if_backwards=False
    ):
        ini_start = start
        ini_end = end
        data = self.daily_data.copy()
        batch_df = self.get_batch_df(data)
        data = pd.concat([data, batch_df], axis=1)

        # 按照id，年龄排序
        data = data.sort_values(["id", "age"]).reset_index(drop=True)

        target_datas = []

        for _ in range(chunk_num):

            if if_backwards:
                start = start - sep
                end = end
            else:
                start = start
                end = end + sep

            wanted_id = self.get_id_by_age_range(start, end)
            # 删除不需要的id
            target_data = data[data["id"].isin(wanted_id)].copy()

            #  只保留日龄内数据
            target_data = target_data[
                (target_data["age"] >= start) & (target_data["age"] <= end)
            ]
            # 获得每个id的数据条数
            target_data["count"] = target_data.groupby("id")["id"].transform("count")
            # 将开测体重换成每个id的第一条数据的体重
            target_data["start_weight"] = target_data.groupby("id")["weight"].transform(
                "first"
            )
            # 将结测体重换成每个id的最后一条数据的体重
            target_data["end_weight"] = target_data.groupby("id")["weight"].transform(
                "last"
            )
            # 计算每个id的日均增重
            target_data["gain_weight"] = (
                target_data["end_weight"] - target_data["start_weight"]
            )
            target_data["dgw"] = target_data["gain_weight"] / target_data["count"]
            # 计算每个id的日均采食
            target_data["total_feed"] = target_data.groupby("id")[
                "feed_amount"
            ].transform("sum")
            target_data["dfi"] = target_data["total_feed"] / target_data["count"]
            # 计算每个id的日均饲料转化率
            target_data["fcr"] = target_data["total_feed"] / target_data["gain_weight"]


            # 计算时间范围内的数据
            range_data = target_data[
                (target_data["age"] >= ini_start) & (target_data["age"] <= ini_end)
            ].copy()
            # 获得每个id的数据条数
            range_data["count"] = range_data.groupby("id")["id"].transform("count")
            # 将开测体重换成每个id的第一条数据的体重
            range_data["start_weight"] = range_data.groupby("id")["weight"].transform(
                "first"
            )
            # 将结测体重换成每个id的最后一条数据的体重
            range_data["end_weight"] = range_data.groupby("id")["weight"].transform(
                "last"
            )
            # 计算每个id的日均增重
            range_data["gain_weight"] = (
                range_data["end_weight"] - range_data["start_weight"]
            )
            range_data["range_dgw"] = range_data["gain_weight"] / range_data["count"]
            # 计算每个id的日均采食
            range_data["total_feed"] = range_data.groupby("id")[
                "feed_amount"
            ].transform("sum")
            range_data["range_dfi"] = range_data["total_feed"] / range_data["count"]
            # 计算每个id的日均饲料转化率
            range_data["range_fcr"] = (
                range_data["total_feed"] / range_data["gain_weight"]
            )
            # 只保留id, range_dgw, range_dfi, range_fcr
            range_data = (
                range_data[["id", "range_dgw", "range_dfi", "range_fcr"]]
                .drop_duplicates()
                .reset_index(drop=True)
            )

            # 将range_data与data合并
            target_data = target_data.merge(range_data, on="id")

            target_data = self.recode_object_data(target_data)
            target_data = (
                target_data.drop(
                    [
                        "gain_weight",
                        "total_feed",
                        "gain_weight",
                        "count",
                        "age",
                        "feed_amount",
                        "birth_date",
                        "weight",
                        "enter_time",
                        "birth_weight",
                        "start_weight",
                        "end_weight",
                    ],
                    axis=1,
                )
                .round(2)
                .drop_duplicates()
                .reset_index(drop=True)
            )
            # 是否删除其它品种
            if if_max_breed:
                # 选择数量最多的品种
                target_data = self.get_max_breed_data(target_data)
                # 在target_columns中删除breed
                target_data = target_data.drop(["breed"], axis=1)
            # 是否删除其它性别
            if if_max_sex:
                target_data = self.get_max_sex_data(target_data)
                # 在target_columns中删除sex
                target_data = target_data.drop(["sex"], axis=1)
            target_datas.append(target_data)


        return target_datas
    
    # 生成时间区段原始数据
    def get_chunk_data(self, start_age, end_age, sep):
        data = self.get_data_by_age_range(start_age, end_age)

        batch_df = self.get_batch_df(data)
        data = pd.concat([data, batch_df], axis=1)
        data["age"] = data["age"] - start_age

        data["chunk"] = data["age"].apply(lambda t: int(t / sep))
        data["feed"] = data.groupby("id")["feed_amount"].transform("sum")
        data["gain"] = data.groupby("id")["gain_weight"].transform("sum")
        data["fcr"] = data["feed"] / data["gain"]

        data["chunk_feed"] = data.groupby(["id", "chunk"])["feed_amount"].transform(
            "sum"
        )
        data["chunk_gain"] = data.groupby(["id", "chunk"])["gain_weight"].transform(
            "sum"
        )
        data["chunk_fcr"] = data["chunk_feed"] / data["chunk_gain"]

        # 将每个个体的chunk_fcr, chunk_feed, chunk_gain放到每个个体的同一条数据中
        chunk_datas = (
            data[["id", "chunk", "chunk_fcr", "chunk_feed", "chunk_gain"]]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        chunk_datas["chunk_name_fcr"] = chunk_datas["chunk"].apply(
            lambda t: "chunk_fcr_" + str(t)
        )
        chunk_datas["chunk_name_feed"] = chunk_datas["chunk"].apply(
            lambda t: "chunk_feed_" + str(t)
        )
        chunk_datas["chunk_name_gain"] = chunk_datas["chunk"].apply(
            lambda t: "chunk_gain_" + str(t)
        )

        # print("start pivot")
        chunk_data = chunk_datas.pivot(
            index="id", columns="chunk_name_fcr", values="chunk_fcr"
        ).reset_index(drop=False)

        # 要哪些数据
        data = (
            data[
                [
                    "father",
                    "mother",
                    "birth_litter",
                    "litter_size",
                    "birth_weight",
                    "sex",
                    "batch",
                    "breed",
                    "station",
                    "id",
                    "fcr",
                ]
            ]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        data = data.merge(chunk_data, on="id", how="left")

        data = self.recode_object_data(data)
        return data

    # 生成时间区段的普通数据
    def get_chunk_normal_data(
        self, start_age, end_age, sep, if_max_breed=False, if_max_sex=False
    ):
        data = self.get_chunk_data(start_age, end_age, sep)
        # if_max_breed, 获得数量最多的breed，将其它breed的数据删除
        if if_max_breed:
            data = self.get_max_breed_data(data)
            
            # 删除breed列
            data = data.drop(["breed"], axis=1)
        # if_max_sex, 获得数量最多的sex，将其它sex的数据删除
        if if_max_sex:
            data = self.get_max_sex_data(data)
            # 删除sex列
            data = data.drop(["sex"], axis=1)
        # 将为inf的数据替换为-999
        data = data.replace([np.inf, -np.inf], -999)
        return data

    # 通过开始与结束日龄，获得合适的id
    def get_id_by_age_range(self, start_age, end_age):
        data = self.daily_data.copy()
        data["start_age"] = data.groupby("id")["age"].transform("min")
        data["end_age"] = data.groupby("id")["age"].transform("max")
        # 中位数
        data["median_age"] = data.groupby("id")["age"].transform("median")

        return list(
            data[
                (data["start_age"] <= start_age) & (data["end_age"] >= end_age)
            ].id.unique()
        )

    # 描述一下daily_data的开始日龄与结束日龄分位数情况
    def describe_daily_data_age(self):
        data = self.daily_data.copy()
        data["start_age"] = data.groupby("id")["age"].transform("min")
        data["end_age"] = data.groupby("id")["age"].transform("max")
        data["median_age"] = data.groupby("id")["age"].transform("median")
        return data[["start_age", "end_age", "median_age"]].describe()

    # 描述一下各个周龄有多少个个体
    def describe_week_age(self):
        data = self.daily_data.copy()
        # 如果该周内数据不足7天，则删除该周
        data["week_age"] = data["age"] // 7 + 1
        data = data.groupby(["id", "week_age"]).filter(lambda x: len(x) >= 7)
        # 统计每个周龄有多少个个体
        data = data.groupby("week_age")["id"].nunique().reset_index(drop=False)
        data.columns = ["week_age", "count"]
        return data

    # 通过日龄范围，从daily_data中获取数据
    # 只保留日龄内的数据，其它的都删除
    def get_data_by_age_range(self, start_age, end_age):
        ids = self.get_id_by_age_range(start_age, end_age)
        data = self.daily_data.copy()
        data = data[data["id"].isin(ids)].copy()
        data = data[(data["age"] >= start_age) & (data["age"] <= end_age)]
        data.reset_index(drop=True, inplace=True)
        return data

    def get_pedigree_data(self):
        data = self.daily_data.copy()
        data = data[["id", "father", "mother"]].drop_duplicates()
        data["year"] = 2018
        data = data.drop_duplicates().reset_index(drop=True)
        return data

    def write_dmu_data(self, data, file_name):
        data.to_csv(file_name, sep=" ", index=False, header=False)

    def get_max_breed_data(self, data):
        data = data.copy()
        # 选择数量最多的品种
        breed_count = data.groupby("breed").count()["id"]
        max_breed = breed_count.idxmax()
        data = data[data["breed"] == max_breed]
        data.reset_index(drop=True, inplace=True)
        return data

    def get_max_sex_data(self, data):
        data = data.copy()
        # 选择数量最多的性别
        sex_count = data.groupby("sex").count()["id"]
        max_sex = sex_count.idxmax()
        data = data[data["sex"] == max_sex]
        data.reset_index(drop=True, inplace=True)
        return data