import marimo

__generated_with = "0.17.7"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 実践：パーマー諸島のペンギンデータの可視化
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 目標
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    このデータ分析レポートの目的は、パーマー諸島に生息するペンギンのサンプルに関連する変数を可視化し、種類、性別、生息する島などの要因と、体重、くちばしの長さと深さ、ひれの長さといったペンギンの身体的特徴との関係を探求・分析することです。
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 紹介
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    生データ`Penguins.csv`はパーマー諸島にある3つの島から収集された334のペンギン標本、およびペンギンに関連する属性データ（種名、所在島、くちばしの長さ、くちばしの深さ、ひれの長さ、体重、性別）を含む。

    `Penguins.csv`カラムの定義：
    - species：ペンギンの種類
    - island：ペンギンの所在島
    - culmen_length_mm：ペンギンくちばしの長さ（単位はmm）
    - culmen_depth_mm：ペンギンくちばしの深さ（単位はmm）
    - flipper_length_mm：ペンギンヒレの長さ（単位はmm）
    - body_mass_g：ペンギン体重（単位はg）
    - sex：ペンギン性別
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## データの読み込み
    """)
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    return np, pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **データ解析に必要なライブラリをインポートし、Pandasのread_csv関数を通して、元データファイルPenguins.csvのデータ内容をDataFrameにパースし、変数c_data(cleaned_dataの意味)に代入する。**
    """)
    return


@app.cell
def _(pd):
    raw_data = pd.read_csv("./penguins.csv")
    c_data = raw_data.copy()
    c_data.head()
    return (c_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## データの評価とクリーンアップ
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### データのクリーン度
    """)
    return


@app.cell
def _(c_data):
    c_data.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **出力結果から、データには合計344の観察対象があり、culmen_length_mm、culmen_depth_mm、flipper_length_mm、body_mass_g変数に欠損値があるが、これは後で評価し、クリーンアップする。**

    **データ型に関しては、SPECIES（ペンギンの種）、SEX（ペンギンの性別）、ISLAND（ペンギンがいる島）は、すべてカテゴリーデータであることがわかる。これらのデータ型をカテゴリーに変換する。**
    """)
    return


@app.cell
def _(c_data):
    c_data["sex"] = c_data["sex"].astype("category")
    c_data["island"] = c_data["island"].astype("category")
    c_data["species"] = c_data["species"].astype("category")
    c_data.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 欠損値の処理
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **info関数の出力から、c_dataの変数culmen_length_mm、culmen_depth_mm、flipper_length_mm、body_mass_g、sexに欠損値がある。**

    **これらの変数が欠落しているデータは、まず見るために抽出する。**
    """)
    return


@app.cell
def _(c_data):
    c_data.query("culmen_length_mm.isna()")
    return


@app.cell
def _(c_data):
    c_data.query("culmen_depth_mm.isna()")
    return


@app.cell
def _(c_data):
    c_data.query("flipper_length_mm.isna()")
    return


@app.cell
def _(c_data):
    c_data.query("body_mass_g.isna()")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **以上から、インデックス3と339のデータは、種と所属島を除くすべての変数で空であり、ペンギンの身体的属性に関連する因子を探索するための値を提供しないため、削除しても良い。**
    """)
    return


@app.cell
def _(c_data):
    c_data.drop(3, inplace=True)
    c_data.drop(339, inplace=True)
    return


@app.cell
def _(c_data):
    c_data.query("sex.isna()")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **性別変数が欠損しているデータには、分析にまだ価値を提供できる他のデータがある。**
    **Pandasは、MatplotlibやSeabornと同様に、欠損値を自動的に無視するため残しても良い**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 不整合データの処理
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **すべてのカテゴリー変数には一貫性のないデータが存在する可能性があり、異なる値が実際には同じ対象を指しているケースがあるかどうかを確認する。**
    """)
    return


@app.cell
def _(c_data):
    c_data["species"].value_counts()
    return


@app.cell
def _(c_data):
    c_data["island"].value_counts()
    return


@app.cell
def _(c_data):
    c_data["sex"].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **上記の出力から、SPECIES列とISLAND列には不整合なデータはないが、SEX列には有効な性別を表さない「.」があるため、その値をNaNに置き換える必要がある。**
    """)
    return


@app.cell
def _(c_data, np):
    c_data['sex'] = c_data['sex'].replace(".", np.nan)
    return


@app.cell
def _(c_data):
    c_data["sex"].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **変換成功**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 異常値の処理
    """)
    return


@app.cell
def _(c_data):
    c_data.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **異常値なさそう**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## データ探索
    """)
    return


@app.cell
def _(sns):
    #チャートのカラーパレットを「パステル」に設定する
    sns.set_palette("pastel")
    return


@app.cell
def _(c_data):
    c_data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 種類の割合
    """)
    return


@app.cell
def _(c_data, plt):
    species_count = c_data["species"].value_counts()
    plt.pie(species_count,autopct="%.0f%%",labels=species_count.index)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **サンプル内のペンギンのうち、Adelie種の割合が最も大きく、Gentoo種の割合が2番目に大きく、Chinstrap種の割合が約1/5で最も小さい**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 所属島の割合
    """)
    return


@app.cell
def _(c_data, plt):
    island_count = c_data["island"].value_counts()
    plt.pie(island_count,autopct="%.0f%%",labels=island_count.index)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **ペンギンの約半数はBiscoe島からのもので、次いでDream島、Torgaersen島からのサンプルは最も少ない。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 性別の割合
    """)
    return


@app.cell
def _(c_data, plt):
    sex_count = c_data["sex"].value_counts()
    plt.pie(sex_count,autopct="%.0f%%",labels=sex_count.index)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **サンプルペンギンの雌雄比は半々であり、無作為抽出の条件と一致している。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### それぞれの島に生息するペンギン種の数
    """)
    return


@app.cell
def _(c_data, plt, sns):
    sns.countplot(c_data,x="island",hue="species")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **以上から、Adelie種のペンギンの標本はbiscoe、Dream、Torgersenの3つの島すべてで存在するのに対し、Chinstrap種はDream島でしか生息しない。Gentoo種はBiscoe島でしか見つかっていないことがわかる。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### それぞれの島に生息する雌雄ペンギンの数
    """)
    return


@app.cell
def _(c_data, plt, sns):
    sns.countplot(c_data,x="island",hue="sex")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 因子間の相関関係
    """)
    return


@app.cell
def _(c_data, plt, sns):
    sns.pairplot(c_data)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **ヒストグラムから、ペンギンのサンプルのくちばしの長さ、くちばしの深さ、ヒレの長さ、体重の分布が正規分布していないことがわかる。 差のあるサンプルデータが複数セット含まれている可能性がある一方、サンプルサイズが十分大きくないことを示唆している。**

    **その他、散布図から明らかに複数のクラスターの存在がわかる、それらはペンギンの種類や性別など特定の要因に関連している可能性があるため、さらに比較して分類することができる。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 種から見る因子間の相関関係
    """)
    return


@app.cell
def _(c_data, plt, sns):
    sns.pairplot(c_data,hue="species")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **散布図上では、同種のサンプルデータは基本的にまとまっており、同種のペンギンのクチバシの長さ、クチバシの深さ、ヒレの長さ、体重の関係には類似性があることがわかる。 これらの結果は、体重とヒレの長さからペンギンの種を推定したり、ペンギンの種から体重とヒレの長さを推定したりするのに有益**
    """)
    return


@app.cell
def _(c_data, plt, sns):
    sns.pairplot(c_data,hue="species",kind="reg",plot_kws={"scatter_kws":{"alpha":0.3}})
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **線形回帰直線と組み合わせた散布図は、類似ペンギンのすべての属性データが互いに正の相関していることを示している。つまり、「くちばしが長いほどくちばしが深い」「ヒレが長いほど体重が重い」「くちばしが短いほどくちばしが浅い」「ヒレが短いほど体重が軽い」ということがわかる**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 性別から見る因子間の相関関係
    """)
    return


@app.cell
def _(c_data, plt, sns):
    sns.pairplot(c_data,hue="sex")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **サンプルを性別によって分けた結果、サンプルのオスペンギンはメスペンギンよりも各属性の値において大きいことがわかる。**
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

