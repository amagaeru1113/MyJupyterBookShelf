#!/usr/bin/env python
# coding: utf-8

# # Content with notebooks
# 
# また、Jupyter Notebooksを使ってコンテンツを作成することもできます。つまり、コードブロックとその出力を本に含めることができます。
# 
# ## Markdown + notebooks
# 
# マークダウンなので、画像やHTMLなどを投稿に埋め込むことができます!
# 
# ![](https://myst-parser.readthedocs.io/en/latest/_static/logo.png)
# 
# また、数学も記述（$add_{math}$）できます。
# 
# $$
# math^{blocks}
# $$
# 
# とか
# 
# $$
# \begin{aligned}
# \mbox{mean} la_{tex} \\ \\
# math blocks
# \end{aligned}
# $$
# 
# しかし、ダラーマークの書き方については注意してください。
# But make sure you \$Escape \$your \$dollar signs \$you want to keep!
# 
# ## MyST markdown
# 
# MyST markdownはJupyterノートブックでも動作します。
# MyST markdownの詳細については、[the MyST guide in Jupyter Book](https://jupyterbook.org/content/myst.html)をチェックするか、
# [the MyST markdown documentation](https://myst-parser.readthedocs.io/en/latest/)を参照してください。
# 
# 
# ## Code blocks and outputs
# 
# Jupyter Bookは、あなたのコードブロックと出力をあなたのブックにも埋め込みます。
# 例えば、以下に Matplotlib のサンプルコードを示します。

# In[1]:


from matplotlib import rcParams, cycler
import matplotlib.pyplot as plt
import numpy as np
plt.ion()


# In[2]:


# Fixing random state for reproducibility
np.random.seed(19680801)

N = 10
data = [np.logspace(0, 1, 100) + np.random.randn(100) + ii for ii in range(N)]
data = np.array(data).T
cmap = plt.cm.coolwarm
rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, N)))


from matplotlib.lines import Line2D
custom_lines = [Line2D([0], [0], color=cmap(0.), lw=4),
                Line2D([0], [0], color=cmap(.5), lw=4),
                Line2D([0], [0], color=cmap(1.), lw=4)]

fig, ax = plt.subplots(figsize=(10, 5))
lines = ax.plot(data)
ax.legend(custom_lines, ['Cold', 'Medium', 'Hot']);


# ブックでできることは、出力 (インタラクティブな出力を含むなど) 以外にもたくさんあります。これについての詳細は、[the Jupyter Book documentation](https://executablebooks.github.io/cli/start/overview.html)を参照してください。

# In[ ]:




