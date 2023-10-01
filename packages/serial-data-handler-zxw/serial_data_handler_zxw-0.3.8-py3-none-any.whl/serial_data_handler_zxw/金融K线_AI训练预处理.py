"""
# File       : 金融K线_AI数据预处理.py
# Time       ：2023/9/30 19:04
# Author     ：xuewei zhang
# Email      ：jingmu_predict@qq.com
# version    ：python 3.10
# Description：
"""
from datetime import timedelta, datetime
import numpy as np
import pandas as pd
import torch
from typing import List, Tuple, Union

from serial_data_handler_zxw import 时间列_三角函数化, 生成训练数据_避开时间断点

# 开盘时间戳	开盘价	最高价	最低价	收盘价	成交量	收盘时间戳	报价币成交量	成单数	吃单方买入的基础币数量	吃单方买入的报价币数量	收盘时间
金融K线_数据头 = {"开盘时间戳": "int64", "开盘价": "float64", "最高价": "float64", "最低价": "float64",
          "收盘价": "float64", "成交量": "float64", "收盘时间戳": "int64",
          "报价币成交量": "float64", "成单数": "float64", "吃单方买入的基础币数量": "float64",
          "吃单方买入的报价币数量": "float64", "收盘时间": "datetime64[ns]"}


class 金融K线_AI数据预处理:
    mean: pd.Series = None  # 均值
    std: pd.Series = None  # 标准差
    data: pd.DataFrame = None  # 原始数据
    data_normalize: pd.DataFrame = None  # 标准化后的数据 , 只有执行 标准化() 方法后才会有值
    索引_训练集: List[Tuple[int, int, int, int]] = None  # 索引_训练集
    索引_测试集: List[Tuple[int, int, int, int]] = None  # 索引_测试集
    索引_训练与测试集: List[Tuple[int, int, int, int]] = None  # 索引_训练与测试集

    def __init__(self, csv_path, 模型input长度: int, 模型output长度: int, 训练测试集比例=0.8, dtype='float64'):
        """
        the columns of csv file are:开盘价	最高价	最低价	收盘价	成交量	报价币成交量	成单数	吃单方买入的基础币数量	吃单方买入的报价币数量	收盘时间
        """
        self.dtype = dtype
        data = pd.read_csv(csv_path, dtype={"开盘价": dtype, "最高价": dtype, "最低价": dtype,
                                            "收盘价": dtype, "成交量": dtype, "报价币成交量": dtype, "成单数": dtype,
                                            "吃单方买入的基础币数量": dtype, "吃单方买入的报价币数量": dtype})
        # to datetime
        data['收盘时间'] = pd.to_datetime(data['收盘时间'])

        # drop part of columns if it exits
        data.drop(columns=['开盘时间戳', '收盘时间戳'], inplace=True)

        # 获取训练数据与测试数据 索引
        self.索引_训练与测试集 = 生成训练数据_避开时间断点(
            data, '收盘时间', timedelta(minutes=2)
        ).数据划分_避开断点(模型input长度, 模型output长度, step=1)
        #
        self.训练测试集比例 = 训练测试集比例
        #
        self.data = data

    @staticmethod
    def help():
        说明 = """
        1. 表头严格按照以下关键字命名和排列:
        [开盘时间戳, 开盘价, 最高价, 最低价, 收盘价, 成交量, 收盘时间戳, 报价币成交量, 成单数, 吃单方买入的基础币数量, 吃单方买入的报价币数量, 收盘时间]

        2. 数据类型严格按照以下类型:
        [int64, float64, float64, float64, float64, float64, int64, float64, float64, float64, float64, datetime64[ns]]
        """
        print(说明)

    def get_训练or测试数据(self, i: int, data: pd.DataFrame, 是训练集=True) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        :param i:
        :param data: pd.DataFrame , 用于指定是标准化后的数据 还是 原始数据
        :param 是训练集:
        :return: (input, output)
        """
        if 是训练集:
            _索引 = self.索引_训练集
        else:
            _索引 = self.索引_测试集
        #
        if _索引 is None:
            self.__划分训练集和测试集()
        #
        if i >= len(self.索引_训练集):
            raise Exception(f"索引越界, {i=}, {len(_索引)=}")
        #
        return data.iloc[_索引[i][0]:_索引[i][1], :], \
            data.iloc[_索引[i][2]:_索引[i][3], :]

    def __划分训练集和测试集(self):
        训练测试集比例 = self.训练测试集比例
        训练集长度 = int(len(self.索引_训练与测试集) * 训练测试集比例)
        self.索引_训练集 = self.索引_训练与测试集[:训练集长度]
        self.索引_测试集 = self.索引_训练与测试集[训练集长度:]

    def 标准化(self, data: pd.DataFrame) -> pd.DataFrame:
        # 丢弃时间列
        data_normalize = data.loc[:, data.columns != '收盘时间']
        # 计算总体均值和标准差
        self.mean = data_normalize.mean()
        self.std = data_normalize.std()
        print(f"数据z-score正则参数: {self.mean=}, {self.std=}")
        # 标准化
        data_normalize = (data_normalize - self.mean) / self.std

        # 添加时间列, 时间列按天进行sin处理
        data_normalize['收盘时间'] = 时间列_三角函数化(
            data['收盘时间'],
            起始日期=datetime.fromisoformat('2019-01-01 00:00:00'),
            周期=timedelta(days=1))
        #
        self.data_normalize = data_normalize
        #
        return data_normalize

    def 收盘价_标准化(self, x: Union[torch.Tensor, np.ndarray, float, int]):
        return (x - self.mean["收盘价"]) / self.std["收盘价"]

    def 收盘价_逆标准化(self, x: Union[torch.Tensor, np.ndarray, float, int]):
        return x * self.std["收盘价"] + self.mean["收盘价"]

    def pd转tf(self, pd_data: pd.DataFrame) -> torch.Tensor:
        """
        将pd.DataFrame转换为tf.Tensor
        """
        # 丢弃时间列
        pd_data = pd_data.iloc[:, 1:]
        # 转换为tf.Tensor
        if self.dtype == 'float64':
            return torch.tensor(pd_data.to_numpy(), dtype=torch.float64)
        elif self.dtype == 'float32':
            return torch.tensor(pd_data.to_numpy(), dtype=torch.float32)
        else:
            raise Exception(f"不支持的数据类型, {self.dtype=}")


if __name__ == '__main__':
    csv_file = "/Volumes/AI_1505056/量化交易/币安_K线数据/BTCUSDT-1m-201909-202308.csv"
    x = 金融K线_AI数据预处理(csv_file, 100, 100)
    xn = x.标准化(x.data)
    xn.to_csv("/Volumes/AI_1505056/量化交易/币安_K线数据/BTCUSDT-1m-201909-202308_normalize.csv", index=False)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    print(x.data.head())
    print(xn.head())
