import marimo

__generated_with = "0.17.7"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 実践：タイタニック号沈没事件生存者データのロジスティック回帰分析
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
    このデータ分析の目的は、タイタニック号の乗客の性別や客室クラスなどの属性に基づいて生存率のロジスティック回帰分析を行う。

    得られたモデルを使って、ダミーデータの生存率不明な乗客が生存できるかどうかを予測すること。
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
    データセットには２つのテーブルが存在する：`titianic_train.csv`と`titanic_test.csv`。

    `titianic_train.csv`は800人以上のタイタニック号乗客の生還状況と、それぞれの客室クラス、性別、年齢、同伴者・兄弟姉妹の数、同伴の両親・子供の数など、乗客に関する情報が記録されている。

    `titanic_test.csv`はモデルを立てた後に予測用の的データ。
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `titianic_train.csv`カラムの定義：
    - PassengerId：乗客ID
    - survival：生還したかどうか
       - 0	False
       - 1	True
    - pclass：客室クラス
       - 1	ファーストクラス
       - 2	セカンドクラス
       - 3  サードクラス
    - sex：性別
    - Age：年齢
    - sibsp：同乗者・兄弟姉妹の数
    - parch：同乗の両親・子供の数
    - ticket：チケット番号
    - fare：チケットの価格
    - cabin：キャビン番号
    - embarked：乗船港
       - C  シェルブール
       - Q  クイーンズタウン
       - S  サウサンプトン


    `titianic_test.csv`の変数は上記と同様，ただsurvival変数のデータはない(予測したいため)。
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
    import matplotlib.pyplot as plt
    import seaborn as sns
    return np, pd, plt, sns


@app.cell
def _(pd):
    raw_data = pd.read_csv("./titanic_train.csv")
    raw_data
    return (raw_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## データのクリーンアップ
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### データの整然度
    """)
    return


@app.cell
def _(raw_data):
    c_data = raw_data.copy()
    return (c_data,)


@app.cell
def _(c_data):
    c_data.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **先頭10行から、まあまあ綺麗なデータであることがわかる**
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
    **出力結果から、`c_data` には合計 891 個の観察対象があり、そのうち `Age`、`Cabin`、`Embarked` には欠損値があるため後で評価し、クリーンアップする。**

    **データ型については、`PassengerId` は乗客IDを表し、データ型は数値ではなく文字列であるべきなので、データ型変換が必要。**

    **また、`Survived`、`Pclass`、`Sex`、`Embarked`はすべてカテゴリーデータであることがわかっているため、データ型をCategoryに変換すればよい。**
    """)
    return


@app.cell
def _(c_data):
    c_data["PassengerId"] = c_data["PassengerId"].astype(str)
    c_data["Survived"] = c_data["Survived"].astype("category")
    c_data["Sex"] = c_data["Sex"].astype("category")
    c_data["Pclass"] = c_data["Pclass"].astype("category")
    c_data["Embarked"] = c_data["Embarked"].astype('category')
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
    **上述通り、`Age`、`Cabin`、`Embarked`に対して欠損値の処理を行う**
    """)
    return


@app.cell
def _(c_data):
    c_data[c_data["Age"].isna()]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **データ全体の約20%に相当する177個のデータで年齢変数が欠損している。 少し多いけど、他の変数にまだ分析があるため、保留してもいいかも。**

    **しかし、後で使用するロジスティック回帰関数Logitは、データ中の欠損値を許さないため欠損値は平均乗客年齢で埋めるつもり。**
    """)
    return


@app.cell
def _(c_data):
    average_age = c_data["Age"].mean()
    c_data["Age"] = c_data["Age"].fillna(average_age)
    c_data['Age'].isna().sum()
    return


@app.cell
def _(c_data):
    c_data[c_data["Cabin"].isna()]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **キャビン番号が欠損しているデータが687件、ほとんどのデータで不明であることを示している。削除したらサンプルが激減するため、保留したほうが絶対いい。**

    **さらに、キャビン番号が生存確率に影響するキー因子ではなく、欠損していてもモデリングに影響しないため、保持してもいいかと。**
    """)
    return


@app.cell
def _(c_data):
    c_data[c_data["Embarked"].isna()]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **上述と同様、保持してもモデリングに影響しないかと。保持しても良いと感じた**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 重複データの処理
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **データ変数の意味とその内容から、PassengerIdは乗客の一意な識別子であり、重複してはならないため重複する値を探す。**
    """)
    return


@app.cell
def _(c_data):
    c_data["PassengerId"].duplicated().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **ない**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 不整合データの処理
    """)
    return


@app.cell
def _(c_data):
    c_data["Survived"].value_counts()
    return


@app.cell
def _(c_data):
    c_data["Pclass"].value_counts()
    return


@app.cell
def _(c_data):
    c_data["Sex"].value_counts()
    return


@app.cell
def _(c_data):
    c_data["Embarked"].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **以上から、カテゴリ変数に不整合な表示方がない**
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
    **特に問題なさそう**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## データの整理
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **データ変数には、乗客の同乗者・兄弟姉妹の数、同乗の親・子供の数が含まれる。船内の世帯人数を計算するのに役立つ。同乗者の家族数が生還に有意に影響するかどうかに興味があるため、この値を統合して新しい変数を作成しようと思う。**
    """)
    return


@app.cell
def _(c_data):
    c_data["FamilyNum"] = c_data["SibSp"] + c_data["Parch"]
    c_data.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## データの探索
    """)
    return


@app.cell
def _(plt, sns):
    sns.set_palette("pastel")
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 生還割合
    """)
    return


@app.cell
def _(c_data, plt):
    survived_count = c_data["Survived"].value_counts()
    survived_label = survived_count.index
    plt.pie(survived_count, labels=survived_label, autopct="%.1f%%")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **円グラフを見ると、死亡した乗客は生還した乗客よりも多く、その比率は約3：2。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 乗客年齢
    """)
    return


@app.cell
def _(c_data, plt, sns):
    _figure, _axes = plt.subplots(1, 2)
    sns.histplot(c_data, x='Age', ax=_axes[0])
    sns.boxplot(c_data, y='Age', ax=_axes[1])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **乗客の大半は20代から40代だが、高齢者や幼児も少なくない。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 乗客年齢と生還状況
    """)
    return


@app.cell
def _(c_data, plt, sns):
    sns.histplot(c_data, x="Age", hue="Survived", alpha=0.4)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **搭乗者の年齢別ヒストグラムを見ると、生還者の割合が高い年齢帯は幼児グループだけで、他の年齢グループの大半は生存者よりも犠牲者の方が多い。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### チケット金額の分布
    """)
    return


@app.cell
def _(c_data, plt, sns):
    _figure, _axes = plt.subplots(1, 2, figsize=[15, 7])
    sns.histplot(c_data, x='Fare', ax=_axes[0])
    sns.boxplot(c_data, y='Fare', ax=_axes[1])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 客室クラスと生還状況
    """)
    return


@app.cell
def _(c_data, plt, sns):
    _figure, _axes = plt.subplots(1, 2)
    pclass_count = c_data['Pclass'].value_counts()
    pclass_label = pclass_count.index
    _axes[0].pie(pclass_count, labels=pclass_label)
    sns.countplot(c_data, x='Pclass', hue='Survived', ax=_axes[1])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **ヒストグラムを見ると、低い客室クラスで死亡した乗客の割合が高く、高い客室クラスで生存した乗客の割合が高いことがわかる。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 性別と生還状況
    """)
    return


@app.cell
def _(c_data, plt, sns):
    _figure, _axes = plt.subplots(1, 2)
    sex_count = c_data['Sex'].value_counts()
    sex_label = sex_count.index
    _axes[0].pie(sex_count, labels=sex_label)
    sns.countplot(c_data, x='Survived', hue='Sex', ax=_axes[1])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **生存率と性別の棒グラフを見ると、男性の死亡者割合が高く、女性の生還者割合が高い。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 乗船港と生還状況
    """)
    return


@app.cell
def _(c_data, plt, sns):
    _figure, _axes = plt.subplots(1, 2)
    embarked_count = c_data['Embarked'].value_counts()
    embarked_label = embarked_count.index
    _axes[0].pie(embarked_count, labels=embarked_label)
    sns.countplot(c_data, x='Embarked', hue='Survived', ax=_axes[1])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 同乗者数と生還状況
    """)
    return


@app.cell
def _(c_data, plt, sns):
    _figure, _axes = plt.subplots(1, 2)
    familyNum_count = c_data['FamilyNum'].value_counts()
    familyNum_label = familyNum_count.index
    _axes[0].pie(familyNum_count, labels=familyNum_label)
    sns.countplot(c_data, x='FamilyNum', hue='Survived', ax=_axes[1])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **独身乗客は死亡者割合が高い。家族連れ乗客の場合、家族数が1人から3人の場合は生存者数が死者数を上回ったが、3人以上の場合は死者数が上回る。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## データ分析
    """)
    return


@app.cell
def _():
    import statsmodels.api as sm
    return (sm,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **新しいDataFrameのtrain_dataを作成し、ロジスティック回帰分析に使用するデータとする**

    **c_dataと区別する理由として、回帰分析を実行する前にダミー変数の導入など、データの準備が必要な場合があるから。**
    """)
    return


@app.cell
def _(c_data):
    train_data = c_data.copy()
    train_data.head()
    return (train_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **説明変数として使えない因子を除去する**
    """)
    return


@app.cell
def _(train_data):
    train_data_1 = train_data.drop(['PassengerId', 'Name', 'Ticket', 'Cabin', 'Embarked'], axis=1)
    train_data_1.head()
    return (train_data_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **目的変数を説明変数から分離する**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **データにはカテゴリー変数が存在するため、直接ロジスティック回帰モデリングができない。カテゴリーに属するかどうかを示す0と1をそれぞれ導入するダミー変数が必要。**
    """)
    return


@app.cell
def _(pd, train_data_1):
    train_data_2 = pd.get_dummies(train_data_1, drop_first=True, columns=['Pclass', 'Sex'], dtype=int)
    train_data_2.head()
    return (train_data_2,)


@app.cell
def _(train_data_2):
    y = train_data_2['Survived']
    return (y,)


@app.cell
def _(train_data_2):
    X = train_data_2.drop(['Survived'], axis=1)
    X.corr()
    return (X,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **一般的に、相関係数の絶対値が0.8を超えると、共分散が強い可能性があると考えられるため、チェックの際には絶対値が0.8を超える値だけを探せばいい。**
    """)
    return


@app.cell
def _(X):
    X.corr().abs()>0.8
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **出力結果から、SibSpとFamilyNum間の相関係数の絶対値が0.8より大きいことがわかる。(FamilyNumがSibSpとParchの合計だから。)**

    **異なる変数間の相関が高すぎると数値最適化アルゴリズムが収束しなくなり、ロジスティック回帰モデルパラメータの計算結果をうまく得ることができない。**

    **よって、FamilyNumかSibSpのどちらかを削除する必要がある。同乗家族数が生存確率に影響するかどうかに興味があるため、FamilyNumを保持する。**

    **さらに、ParchとFamilyNum間にも強い相関があり、相関係数が0.78で0.8に近いため、念の為Parchも削除する。**
    """)
    return


@app.cell
def _(X):
    X_1 = X.drop(['Parch', 'SibSp'], axis=1)
    return (X_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次に、回帰方程式の切片項を定義する**
    """)
    return


@app.cell
def _(X_1, sm):
    X_2 = sm.add_constant(X_1)
    return (X_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次に、Logit関数でロジスティック回帰モデルのパラメータ値を取得し、要約情報を出力する**
    """)
    return


@app.cell
def _(X_2, sm, y):
    model = sm.Logit(y, X_2).fit()
    model.summary()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **有意区間を0.05とし、上記結果のp値は、チケット価格が乗客の生還率に有意な影響を与えないことをモデルがが示している。よって、Fare因子を除去して再構築したほうがモデルの精確率が上がると期待できる**
    """)
    return


@app.cell
def _(X_2, sm, y):
    X_3 = X_2.drop(['Fare'], axis=1)
    model_1 = sm.Logit(y, X_3).fit()
    model_1.summary()
    return (model_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **ロジスティック回帰モデルでは、以下の要因:**

    **1.年齢 2.同伴家族数 3.ファーストクラスでないこと 4.男性**

    **が増加する（または存在する）と、生還確率が低下すると予測した**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **個々の説明変数の実際の意味を理解するためには、自然定数を計算する必要がある。**
    """)
    return


@app.cell
def _(np):
    np.exp(-0.0395)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **上記の結果から、年齢が1歳増えるごとに生還確率が約4％減少することを示唆している。**
    """)
    return


@app.cell
def _(np):
    np.exp(-0.2186)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **上記の結果から、同伴家族が1人増えるごとに生還確率が約20％減少することを示唆している。**
    """)
    return


@app.cell
def _(np):
    np.exp(-1.1798)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **上記の結果から、セカンドクラスの乗客はファーストクラス乗客より生還確率が約71％低いことを示唆している。**
    """)
    return


@app.cell
def _(np):
    print(np.exp(-2.3458))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **上記の結果から、サードクラスの乗客はファーストクラス乗客より生還確率が約90％低いことを示唆している。**
    """)
    return


@app.cell
def _(np):
    np.exp(-2.7854)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **上記の結果から、男性乗客は女性乗客より生還確率が約94％低いことを示唆している。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **モデルのパラメータ値に基づき、次のように結論づける：**

    **- 若い乗客ほど生還確率が高い；**

    **- 女性乗客は男性乗客よりも生還確率が高い；**

    **- 生還確率は、高い客室クラスの乗客ほど高い；**

    **- 同伴家族の少ない乗客は、生還確率がより高い。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 考察
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **1、２番目の結論の背景には、タイタニック号沈没時に「子供と女性を優先的に救出する」という原則が関係しているかもしれない。**

    **3つ目は、ハイクラスの乗客は社会的地位や影響力のおかげで優先的に脱出できた可能性を示唆している。**

    **4つ目の理由として、同伴家族数が多い乗客は災害時に脱出することよりも家族を救出することで気を取られ、結局自分たちが脱出するチャンスを失ってしまったことがあったかもしれない。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **回帰分析モデルが出来上がったので、次は的データを投入して実際予測してみる**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 的データの読み込み
    """)
    return


@app.cell
def _(pd):
    test_data = pd.read_csv("./titanic_test.csv")
    test_data.head()
    return (test_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **前で言ったように、ロジスティック回帰モデルはデータの欠損値を許さないので、test_dataに欠損データがあるかどうかをチェックする必要がある**
    """)
    return


@app.cell
def _(test_data):
    test_data.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **出力結果から、Age、Fare、Cabinに欠損値があるとわかる。このうち、FareとCabinは、回帰モデルの説明変数ではなく、欠落していても予測に影響しないため、無視してもよい。**
    """)
    return


@app.cell
def _(test_data):
    test_data["Age"] = test_data["Age"].fillna(test_data["Age"].mean())
    test_data["Age"].isna().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次のステップは、モデル内のカテゴリ変数にダミー変数を導入すること。その前に、カテゴリ変数のタイプをCategory型に変換して、categoriesパラメータを通してモデルにすべての可能なカテゴリ値を渡す必要がある。**

    **理由としては、予測データがすべてのカテゴリ値を含むとは限らないから。ダミー変数を導入するときに、カテゴリを見逃さないように。**
    """)
    return


@app.cell
def _(pd, test_data):
    test_data["Pclass"] = pd.Categorical(test_data["Pclass"], categories=["1", "2", "3"])
    test_data["Sex"] = pd.Categorical(test_data["Sex"], categories=["female", "male"])
    test_data["Embarked"] = pd.Categorical(test_data["Embarked"], categories=["C", "Q", "S"])
    return


@app.cell
def _(pd, test_data):
    test_data_1 = pd.get_dummies(test_data, drop_first=True, columns=['Pclass', 'Sex'], dtype=int)
    test_data_1.head()
    return (test_data_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **モデルの説明変数を確認する**
    """)
    return


@app.cell
def _(model_1):
    model_1.params
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **データ整理時にFamilyNum変数を作成したので、ここでも予測データにこの変数を追加する必要がある。**
    """)
    return


@app.cell
def _(test_data_1):
    test_data_1['FamilyNum'] = test_data_1['SibSp'] + test_data_1['Parch']
    test_data_1.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次に、モデルに入力したい説明変数を渡す。説明変数は、モデルの構築時に使用した入力と同じである必要がある。**
    """)
    return


@app.cell
def _(sm, test_data_1):
    X_test = test_data_1[['Age', 'FamilyNum', 'Pclass_2', 'Pclass_3', 'Sex_male']]
    X_test = sm.add_constant(X_test)
    return (X_test,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **モデルインスタンスのpredict関数を呼び出して、生還確率の予測を行う**
    """)
    return


@app.cell
def _(X_test, model_1):
    predicted_value = model_1.predict(X_test)
    predicted_value
    return (predicted_value,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **これで`titanic_test.csv`のタイタニック号乗客の生存確率がロジスティック回帰モデルによって予測された。**

    **確率が0.5以上のものを「生還者」、0.5未満のものを「難破者」としよう。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 予測結果
    """)
    return


@app.cell
def _(predicted_value):
    predicted_value>0.5
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

