import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df_train  = pd.read_csv("dataset.csv")

trian_corr = df_train.corr() #計算相關係數
plt.subplots(figsize=(10, 10))  # 設置長寬尺寸大小
sns.heatmap(trian_corr, annot=True, vmax=1, cmap="Blues")

