# bangumi_and_anikore_for_anime_sales_predict
**Try to predict the BD/DVD sales of anime using data from bangumi (bangumi.tv) and anikore (anikore.jp)**

*尝试使用 bangumi（ bangumi.tv ） 和 anikore （ anikore.jp ）的数据预测动画 BD/DVD 销量*

## Data source:

bangumi data comes from https://github.com/czy0729/Bangumi-Subject.

*bangumi 的数据来自 czy0729 大佬的 json*

anikore data is scraped by myself.

*anikore 的数据是我自己爬的*

sales data is scraped from http://rankstker.net/

*销量数据来源于 http://rankstker.net/*

## What did I do

scraping, data-cleaning, merging, and some machine learning procedures.

*爬数据，清洗数据，合并，然后一些 ml 的活计*

## So I get what?

A Ridge regression model with about 0.6 R2 score, and a wordcloud (in Chinese)

*一个 R2 分数 0.6 左右的岭回归模型，以及一个中文云图*

## What did I use?

* numpy: 1.18.1
* pandas: 1.0.1
* matplotlib: 3.1.3
* sklearn: 0.22.1
* wordcloud: 1.7.0
