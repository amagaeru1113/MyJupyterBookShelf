#!/usr/bin/env python
# coding: utf-8

# # 03. 演習
# 
# 考え方の定着を目的として、演習問題を作って回答してみます。
# また、可能であればpytestを用いてコードの実装を行います。
# 
# 今回は初めに節の中で使用した例についてpytestでテストを書く練習をします。
# その後に演習問題を作り、回答します。
# 

# ## 同値クラステスト（同値分割/equivalence partitioning)

# ### 例

# In[1]:


get_ipython().run_cell_magic('file', 'software_testing/03/sample_func1.py', "\ndef func1(x: int) -> str:    \n    if x == 3:\n        return '3'\n    elif x == 5:\n        return '5'\n    else:\n        return 'none'")


# In[2]:


get_ipython().run_cell_magic('file', 'software_testing/03/sample_func1_test.py', "\nimport random\n\nfrom sample_func1 import func1\n\ndef test_func1_n3():\n    assert '3' == func1(3)\n\ndef test_func1_n5():\n    assert '5' == func1(5)\n    \ndef test_func1_na():\n    l = list(range(100))\n    l.remove(3)\n    l.remove(5)\n    \n    num = random.choice(l)\n    assert 'none' == func1(num)")


# In[3]:


get_ipython().system('python -m pytest software_testing/03/sample_func1_test.py')


# ## 境界値テスト（境界値分析/限界値分析/boundary value analysis)

# ### 例

# In[4]:


get_ipython().run_cell_magic('file', 'software_testing/03/sample_func2.py', "\ndef func2(x: int) -> str:    \n    if x <= 2:\n        return '2 ika'\n    elif x >= 7:\n        return '7 ijo'\n    else:\n        return 'none'")


# In[5]:


get_ipython().run_cell_magic('file', 'software_testing/03/sample_func2_test.py', "\nimport random\n\nfrom sample_func2 import func2\n\ndef test_func2_1():\n    assert '2 ika' == func2(1)\n\ndef test_func2_2():\n    assert '2 ika' == func2(2)\n    \ndef test_func2_3():\n    assert 'none' == func2(3)\n    \ndef test_func2_6():\n    assert 'none' == func2(6)\n    \ndef test_func2_7():\n    assert '7 ijo' == func2(7)\n    \ndef test_func2_8():\n    assert '7 ijo' == func2(8)")


# In[6]:


get_ipython().system('python -m pytest software_testing/03/sample_func2_test.py')


# ## 演習問題

# ### 1.　喫茶店での注文
# 
# 喫茶店でセットA、B、Cのうちどれかを選びます。
# 注文に応じて料金を出力するシステムをテストします。
# 
# - セットA: 300円
# - セットB: 500円
# - セットC: 800円
# 
# 上記のシステムのテストケースを考えます。
# また、取り扱いしていないメニューについては0円を出力します。
# 
# 
# 同値クラスは3つです。（A,B,C）
# ここでクラスを数値(A -> 0, B -> 1, C -> 2)に置き換えます。
# 必要なテストケースは以下が考えられます。
#   
# - x: 注文されたセット(A -> 0, B -> 1, C -> 2)
# - x = 'セットA' -> 300 
# - x = 'セットB' -> 500
# - x = 'セットC' -> 800
# - x = 'セットD' -> 0
# 
# より、 x = ['セットA','セットB','セットC', 'セットD']
# 期待される出力は[300, 500, 800 0]です。

# In[7]:


get_ipython().run_cell_magic('file', 'software_testing/03/exercises_1.py', "\ndef func_exe(order: str) -> int:\n\n    if order == 'セットA':\n        return 300\n    elif order == 'セットB':\n        return 500\n    elif order == 'セットC':\n        return 800\n    else:\n        return 0")


# In[8]:


get_ipython().run_cell_magic('file', 'software_testing/03/exercises_1_test.py', "\nfrom exercises_1 import func_exe\n\ndef test_exercises_1():\n    assert 300 == func_exe('セットA')\n\ndef test_exercises_2():\n    assert 500 == func_exe('セットB')\n\ndef test_exercises_3():\n    assert 800 == func_exe('セットC')\n    \ndef test_exercises_4():\n    assert 0 == func_exe('セットD')")


# In[9]:


get_ipython().system('python -m pytest software_testing/03/exercises_1_test.py')


# ### 2. 大食いチャレンジ
# 
# お寿司の大食いチャレンジの結果に応じて賞金を出力する条件分岐をテストします。
#     - 20皿以上食べた人には賞金2000円
#     - 40皿以上食べた人には賞金5000円
# 皿の枚数に応じて賞金を出力するシステムのテストケースを考えましょう。
# 
# 
# 同値クラスは2つです。（0円、2000円、5000円）
# 境界値は2つ（20皿、40皿）なので、必要なテストケースの例は次の物が考えられます。
#     
# - x : 皿の枚数
# - x < 20 -> 0円
# - x >= 20 -> 2000円
# - x >= 40 -> 5000円
# 
# より、x = [19, 20, 21, 39, 40, 41]
# 期待される出力は[0, 2000,2000, 2000, 5000,5000]です。

# In[10]:


get_ipython().run_cell_magic('file', 'software_testing/03/exercises_2.py', '\ndef func_exe(dishes: int) -> int:  \n\n    if 20 <= dishes < 40:\n        return 2000\n    elif dishes >= 40:\n        return 5000\n    else:\n        return 0')


# In[11]:


get_ipython().run_cell_magic('file', 'software_testing/03/exercises_2_test.py', '\nfrom exercises_2 import func_exe\n\ndef test_exercises_1():\n    assert 0 == func_exe(19)\n\ndef test_exercises_2():\n    assert 2000 == func_exe(20)\n    \ndef test_exercises_3():\n    assert 2000 == func_exe(21)\n    \ndef test_exercises_4():\n    assert 2000 == func_exe(39)\n\ndef test_exercises_5():\n    assert 5000 == func_exe(40)\n    \ndef test_exercises_5():\n    assert 5000 == func_exe(41)')


# In[12]:


get_ipython().system('python -m pytest software_testing/03/exercises_2_test.py')


# In[ ]:




