import pandas as pd
import os
from scipy.stats import pearsonr


def read_sol(dir_sol):
    sol = pd.read_csv(dir_sol, header=None)[0].str.split(expand=True)
    sol.columns = sol.columns + 1
    return sol


def get_breeding_effects(dir_sol):
    sol = read_sol(dir_sol)
    breeding_effects = sol.loc[sol[1] == "4", :].loc[:, [5, 8]]
    breeding_effects = dict(
        zip(breeding_effects.iloc[:, 0], breeding_effects.iloc[:, 1])
    )
    # 将key转换为int
    breeding_effects = {int(k): float(v) for k, v in breeding_effects.items()}
    return breeding_effects


# 计算遗传力相关
def cal_bv_cor(predict: dict, data: pd.DataFrame, pedigree: pd.DataFrame):
    """计算遗传力相关系数
    Args:
        predict (dict): 预测的个体与表型的对应字典
        data (pd.DataFrame): 原始数据，用来跑动物模型，最后一行为表型
        pedigree (pd.DataFrame): 家系

        Returns:
            float: 相关系数
    """
    # 生成替换数据
    pre_data = get_replace_data(predict, data)
    # 运行
    try:
        pre_bv = cal_bv_ani(predict.keys(), pre_data, pedigree)
        ori_bv = cal_bv_ani(predict.keys(), data, pedigree)
    except:
        print("动物模型运行失败")
        return 0
    # 计算相关系数
    bv_cor = cal_cor(pre_bv, ori_bv)
    print("遗传力相关系数：", bv_cor)
    clean_dmu_files()
    return bv_cor


# 计算相关系数
def cal_cor(pre_bv: dict, ori_bv: dict) -> float:
    # 选取共同的ID
    ids = set(pre_bv.keys()) & set(ori_bv.keys())
    # 选取共同的BV
    pre_bv = {k: pre_bv[k] for k in ids}
    ori_bv = {k: ori_bv[k] for k in ids}
    # 计算相关系数
    bv_cor = pearsonr(list(pre_bv.values()), list(ori_bv.values()))[0]
    return bv_cor


# 生成替换数据
def get_replace_data(predict: dict, data):
    # 生成替换数据
    data = data.copy()
    # 表型，最后一列
    pheno = data.iloc[:, -1].copy()
    # 替换表型
    data["predict"] = data["id"].map(predict)
    data["predict"] = data["predict"].fillna(pheno)
    # 删除phenotype列
    data = data.drop(columns=[pheno.name])
    return data


# 动物模型计算遗传力
def cal_bv_ani(target_ids: list, data, pedigree) -> dict:
    # 运行
    run_ani(data, pedigree)
    # 读取结果
    breeding_effects = get_breeding_effects(write_ani_dir() + ".sol")
    # 选取目标
    bv = {k: breeding_effects[k] for k in target_ids}
    return bv


# 跑动物模型
def run_ani(data: pd.DataFrame, pedigree: pd.DataFrame):
    data.to_csv("data.txt", sep=" ", index=False, header=False)
    pedigree.to_csv("ped.txt", sep=" ", index=False, header=False)
    os.system("run_dmuai.bat " + write_ani_dir())


# 测定日模型计算遗传力
def cal_bv_tsd(target_ids: list, data, pedigree) -> pd.DataFrame:
    pass


# 跑测定日模型
def run_tsd(data, pedigree):
    data.to_csv("data.txt", sep=" ", index=False, header=False)
    pedigree.to_csv("ped.txt", sep=" ", index=False, header=False)
    os.system("run_dmuai.bat TSD")


# 删除dmu生成文件
def clean_dmu_files(excepts=[]):
    # 根据后缀删除
    d_drop = [".SOL", ".log", ".LLIK", ".lst", ".PAROUT", ".RESIDUAL", ".PAROUT_STD", "data.txt", "ped.txt"]
    for except_ in excepts:
        d_drop.remove(except_)
    for root, dirs, files in os.walk("./"):
        for file in files:
            for d in d_drop:
                if file.endswith(d):
                    os.remove(os.path.join(root, file))


# 生成动物模型的DIR文件
def write_ani_dir(DIR="AAAAAAA"):
    try:
        os.system.remove(DIR + ".DIR")
    except:
        pass
    COMMENT = "\n"
    ANALYSE = "1 1 0 1"
    DATA = "ASCII (3,1,-999) ./data.txt"
    VARIABLE_1 = "#1    2       3"
    VARIABLE_2 = "BATCH STATION ID"
    VARIABLE_3 = "#1"
    VARIABLE_4 = "PHENO"
    MODEL_1 = "1 1 0 0 0"
    MODEL_2 = "0"
    MODEL_3 = "1 0 3 1 2 3"
    MODEL_4 = "# 1个随机效应（遗传效应）"
    model_5 = "1"
    model_6 = "0"
    model_7 = "0"
    VAR_STR = "1 PED 2 ASCII ./ped.txt"
    RESIDUALS = "ASCII"
    DMUAI_1 = "10"
    DMUAI_2 = "1D-7"
    DMUAI_3 = "1D-6"
    DMUAI_4 = "1"
    DMUAI_5 = "0"
    with open(DIR + ".DIR", "w") as f:
        f.write("$COMMENT\n")
        f.write(COMMENT + "\n")
        f.write("$ANALYSE ")
        f.write(ANALYSE + "\n")
        f.write("$DATA ")
        f.write(DATA + "\n")
        f.write("$VARIABLE\n")
        f.write(VARIABLE_1 + "\n")
        f.write(VARIABLE_2 + "\n")
        f.write(VARIABLE_3 + "\n")
        f.write(VARIABLE_4 + "\n")
        f.write("$MODEL\n")
        f.write(MODEL_1 + "\n")
        f.write(MODEL_2 + "\n")
        f.write(MODEL_3 + "\n")
        f.write(MODEL_4 + "\n")
        f.write(model_5 + "\n")
        f.write(model_6 + "\n")
        f.write(model_7 + "\n")
        f.write("$VAR_STR ")
        f.write(VAR_STR + "\n")
        f.write("$RESIDUALS ")
        f.write(RESIDUALS + "\n")
        f.write("$DMUAI\n")
        f.write(DMUAI_1 + "\n")
        f.write(DMUAI_2 + "\n")
        f.write(DMUAI_3 + "\n")
        f.write(DMUAI_4 + "\n")
        f.write(DMUAI_5 + "\n")
    return DIR

# 计算遗传力
def cal_bv(dir_lst:str ) -> float:
    # 读取dir文件
    with open(dir_lst, "r") as f:
        # 出现 FINAL PARAMETERS ESTIMATED 之后
        # 出现 Covariance matrix for random effect no:            1
        pass