#!/usr/bin/env python
# coding: utf-8

# # A comprehensive beginner’s guide to create a Time Series Forecast (with Codes in Python and R)

# ## リンク
# 
# [サイトページ](https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/)
# 
# [web魚拓](https://megalodon.jp/2020-1009-0951-57/https://www.analyticsvidhya.com:443/blog/2016/02/time-series-forecasting-codes-python/)
# 
# ## 概要
# 
# - 時系列予測を作成する手順を学びます。
# - Dickey-Fuller検定とARIMA (Autoregressive, moving average)モデルにも焦点を当てています。
# - pythonでの実装と同様に、理論的な概念を学びます。
# 

# ## 序文
# 時系列（Time Series、以降TS）は、データサイエンスの世界ではあまり知られていないスキルの一つと考えられています。私は時系列問題を解決するための基本的な手順を学ぶために旅に出ましたが、ここではあなたと同じことを共有しています。これらは間違いなく、あなたが取り上げる任意の将来のプロジェクトでまともなモデルを取得するのに役立ちます
# 
# この記事を読む前に、[A Complete Tutorial on Time Series Modeling in R](https://www.analyticsvidhya.com/blog/2015/12/complete-tutorial-time-series-modeling/)を読んで、[無料のTime Series Forecastingコース](http://courses.analyticsvidhya.com/courses/creating-time-series-forecast-using-python?utm_source=blog&utm_medium=TimeSeriesForecastComprehensivearticle)を受講することを強くお勧めします。これは基本的な概念に焦点を当てており、私はPythonのコードと一緒に問題を解決する際にこれらの概念をエンドツーエンドで使用することに焦点を当てています。Rでの時系列のための多くのリソースは存在しますが、[Pythonのためのリソース](http://courses.analyticsvidhya.com/courses/introduction-to-data-science-2?utm_source=blog&utm_medium=TimeSeriesForecastComprehensivearticle)は非常に少ないので、この記事ではPythonを使用します。
# 
# 
# 私たちの旅は、次のようなステップを経ることになるでしょう。
# 
# 1. 時系列を特別なものにしているのは何か？
# 2. pandasでの時系列の読み込みと処理
# 3. 時系列の定常性を確認するには？
# 4. 時系列の定常性を確認するには？
# 5. 時系列を予測する
# 
# 
# ## 1.何が時系列を特徴付けるか？
# 
# その名が示すように、TSは一定の時間間隔で収集されたデータ点の集合です。これらは、将来を予測したり、他の形式の分析を行うために、長期的な傾向を決定するために分析されます。しかし、TSは通常の回帰問題と何が違うのでしょうか？次の2つのことがあります。
# 
# 
# 1. **時間依存性**：したがって、観測者が独立しているという線形回帰モデルの基本的な仮定は、このケースでは保持されない。
# 
# 2. **季節性**：増加または減少傾向とともに、ほとんどのTSは、ある種の季節性傾向、すなわち、特定の時間枠に固有の変動を持っています。たとえば、ウールのジャケットの販売が時間の経過とともに変化するのを見ると、冬の季節には必ずより高い販売価格もしくは販売量が見られるでしょう。
# 
# TSには固有の特徴があるため、TSの分析には様々なステップがあります。これらについては以下で詳しく説明します。まず、PythonでTSオブジェクトを読み込むことから始めましょう。ここでは人気のある[AirPassengers](https://www.analyticsvidhya.com/wp-content/uploads/2016/02/AirPassengers.csv)のデータセットを使用します。
# 
# この記事の目的は、一般的にTSで使用される様々なテクニックに慣れることであることに注意してください。ここで考えた例は説明のためのものであり、私は幅広いトピックをカバーすることに焦点を当て、あまり正確な予測はしません。
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 

# ## 2. pandasで時系列の読み込みと処理
# 
# pandasには TSオブジェクトを扱うための専用ライブラリがあり、特に datatime64[ns] クラスは時間情報を保存し、いくつかの操作を高速に実行できるようにしてくれます。まずは必要なライブラリを起動してみましょう。
# データは1949年１月〜1960年12月までの月毎の飛行機の乗客数のデータセットであるAirport Passengersです。

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings


warnings.simplefilter('ignore')


# In[2]:


# さて、データセットをロードして、いくつかの初期の行と列のデータ型を見てみましょう。
data_path = './data/AirPassengers.csv'
data = pd.read_csv(data_path)
print ('\n Data Types:')
print (data.dtypes)
print ('\n Data Shape:')
print (data.shape)
print ('\n Data Head:')
print (data.head())


# In[3]:


# データには、特定の月とその月に旅行した乗客の数が含まれています。データを時系列として読み込むためには, read_csvコマンドに特別な引数を渡す必要があります.
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
data = pd.read_csv(data_path, parse_dates=['Month'], index_col='Month',date_parser=dateparse)
print ('\n Parsed Data:')
print (data.head())


# 引数を一つずつ理解していきましょう。
# 
# - **parse_dates**：これは日付と時刻の情報を格納するカラムを指定します。上で言ったように、カラム名は'Month'です。
# 
# - **index_col**：TSデータにPandasを使用する際の重要な考え方は、インデックスが日付時間情報を表す変数でなければならないということです。そのため、この引数は'Month'カラムをインデックスとして使用するようにpandasに指示します。
# 
# - **date_parser**:これは入力文字列をdatetime変数に変換する関数を指定します。デフォルトでは、pandasは'YYYY-MM-DD HH:MM:SS'形式でデータを読み込みます。もしデータがこのフォーマットでない場合は、フォーマットを手動で定義しなければなりません。この目的のために、ここで定義されているdataparse関数に似たものを使用することができます。
# 
# これで、データのインデックスがTimeオブジェクト、列が#Passengersであることがわかります。次のコマンドでインデックスのデータ型を照合することができます。

# In[4]:


data.index


# indexのデータ型dtype='datetime[ns]' となっていることに注目してください。
# 個人的な好みとして、私はTSを使用するたびに列の名前を参照するのを防ぐために、列をSeriesオブジェクトに変換します。
# 

# In[5]:


ts = data['#Passengers']
ts.head()


# 先に進む前に、TSデータのインデックス作成のテクニックについて説明します。まず、Seriesオブジェクトで特定の値を選択することから始めましょう。これは以下の2つの方法で行うことができます。
# 
# 

# In[6]:


#1. 特定のindexを文字列で指定します。
print(ts['1949-01-01'])

#2. datetime ライブラリをインポートして 'datetime' 関数を使用します。
from datetime import datetime
print(ts[datetime(1949,1,1)])


# どちらも、以前の出力からも確認できる値'112'を返すことになります。1949年5月までのすべてのデータが欲しいとします。これには2つの方法があります。
# 

# In[7]:


#1. 範囲を指定します:
ts['1949-01-01':'1949-05-01']

#2. ':' を使用して始端から指定日までを指定します:
ts[:'1949-05-01']


# ここで注意すべき点が2つあります。
# 
# 1. 数値インデキシングとは異なり、ここでは終了インデックスが含まれています。例えば、リストにa[:5]というインデックスを付けた場合、インデックス-[0,1,2,3,4]の値を返すことになります。しかし、ここではインデックス '1949-05-01' が出力に含まれています。
# 
# 2. インデックスをソートしないと範囲が機能しません。インデックスをランダムにシャッフルした場合、これは動作しません。
# 
# 別の例として、1949年のすべての値が必要な場合を考えてみましょう。これは次のようにすることができます。

# In[8]:


ts['1949']


# 月の部分が省略されています。同様に、特定の月のすべての日の場合は、日の部分を省略することができます。
# 
# さて、TSを分析する上で移動することができます。

# ## 3. どのようにして時系列の定常性を判定するか？
# 
# 平均や分散などの統計的特性が時間の経過とともに一定である場合、TSは定常であると言われています。しかし、なぜそれが重要なのでしょうか？ほとんどのTSモデルは、TSが定常であるという前提で動作します。直感的には、あるTSがある時間内に特定の振る舞いをしている場合、将来的にも同じ振る舞いをする確率が非常に高いということがわかります。また、定常系列に関連する理論は、非定常系列に比べて成熟しており、実装が容易です。
# 
# 定常性は非常に厳しい基準で定義されています。しかし、実用的な目的のためには、次のような統計的特性が一定であれば、その系列は定常であると仮定することができます。
# 
# 1. 平均が一定
# 2. 分散が一定
# 3. 自己共分散が時間に依存しない
# 
# [この記事](https://www.analyticsvidhya.com/blog/2015/12/complete-tutorial-time-series-modeling/)で明確に定義されているので、詳細は省きます。それでは、定常性をテストする方法に移りましょう。まず第一に、データを簡単にプロットして視覚的に分析することです。データは以下のコマンドでプロットすることができます。
# 
# 

# In[9]:


fig, axes = plt.subplots(figsize=(9,6))
plt.plot(ts);


# データには季節的な変動もありますが、全体的に増加傾向にあることは明らかです。しかし、必ずしもそのような視覚的な推論ができるとは限りません（後ほどそのようなケースを見てみましょう）。そこで、より正式には、以下のような方法で定常性を確認することができます。
# 
# 1. ローリング統計を可視化します。移動平均や移動分散をプロットして、それが時間とともに変化するかどうかを見ることができます。移動平均/分散とは、任意の瞬間't'において、昨年の平均/分散、すなわち過去12ヶ月の平均/分散を取ることを意味します。つまりはこれも視覚的なテクニックです。
# 
# 
# 2. ディッキー・フラー検定. これは、定常性をチェックするための統計的検定の1つです。ここでは、帰無仮説は、TSが非定常であるということです。検定結果は，検定統計量と信頼度の差の臨界値で構成される．検定統計量」が「臨界値」よりも小さければ、帰無仮説を棄却し、系列が定常であると言えます。詳細は[こちらの記事](https://www.analyticsvidhya.com/blog/2015/12/complete-tutorial-time-series-modeling/)を参照してください。

# この時点では、これらの概念はあまり直感的には聞こえないかもしれません。参照先の記事を読むことをお勧めします。理論的な統計学に興味があるのであれば、**Brockwell and DavisのIntroduction to Time Series and Forecasting**を参照してください。この本は少し統計学的な内容が多いですが、行間を読むスキルがあれば、概念を理解して統計学に触れることができます。
# 
# 静止性のチェックに戻りますが、我々はDickey-Fuller検定の結果と一緒にローリング統計量のプロットを多く使用するでしょう。平均に近い単位を保つために、分散の代わりに標準偏差をプロットしたことに注意してください。

# In[10]:


import statsmodels
from statsmodels.tsa.stattools import adfuller


def test_stationarity(ts):
    
    # ローリング統計の決定
    rolmean = pd.rolling_mean(ts, window=12)
    rolstd = pd.rolling_std(ts, window=12)
    
    # ローリング統計のプロット
    arig = plt.plot(ts, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    
    # ディッキーフラー検定
    print('Results of Dickey-Fuller Test')
    dftest = adfuller(ts, autolog='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)


# In[12]:





# In[ ]:




