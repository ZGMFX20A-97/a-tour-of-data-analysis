import marimo

__generated_with = "0.17.7"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 実践：イギリスECサイトの市場販売データ
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
    このデータ分析の目的は、市場販売データに基づいて、売れ行きの良い製品を発掘し、より効果的なマーケティング戦略を策定して収益を向上させることです。

    この実践プロジェクトの目的は、データのクリーン度と整然度を評価する練習を行い、評価結果に基づいてデータをクリーニングし、次の分析に使用できるデータを得ることです。
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
    カラムの定義：
    - `InvoiceNo`: インボイス番号。6桁。取引を識別するための一意の番号。“c”で始まる場合、取引が取り消されたことを示す。
    - `StockCode`: 商品コード。5桁。商品を表す一意の商品コード。
    - `Description`: 商品名。
    - `Quantity`: 取引の商品数量。
    - `InvoiceDate`: 請求書が発行された日時。つまり取引が行われた日時。
    - `UnitPrice`: 商品単価。単位はポンド（£）。
    - `CustomerID`: カスタマーID。5桁。カスタマーに関する一意のID。
    - `Country`: 国名。カスタマー所在の国名。
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
    return (pd,)


@app.cell
def _(pd):
    raw_data = pd.read_csv("./e_commerce.csv")
    raw_data.head()
    return (raw_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## データの整理
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### データの整然度
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **ランダムに10個を取り出して観察する**
    """)
    return


@app.cell
def _(raw_data):
    raw_data.sample(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### データのクリーン度
    """)
    return


@app.cell
def _(raw_data):
    raw_data.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **出力結果からすると、DescriptionとCustomerIDには欠損値が存在する。
    かつ、InvoiceDateはDate型であるはず、CustomerIDはfloatではなくStringであるべき**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 欠損値
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Descriptionの欠損データを抽出する**
    """)
    return


@app.cell
def _(raw_data):
    raw_data[raw_data["Description"].isnull()]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **1454個欠損しているデータを発見、これらのデータの中でUnitPriceが一見全部0になっているが、**

    **念の為UnitPriceが0でない欠損データが存在するかを検証する**
    """)
    return


@app.cell
def _(raw_data):
    raw_data[(raw_data["Description"].isnull()) & (raw_data["UnitPrice"]!=0)]
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
    **CustomerIDが欠損しているデータを抽出する**
    """)
    return


@app.cell
def _(raw_data):
    raw_data[(raw_data["CustomerID"].isnull())]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **結構存在するけど分析には支障をきたさないので残す**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 重複データ
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **InvoiceNo、StockCode、CustomerIDは全部一意であるが、一回の取引で違う商品が存在することもあるためInvoiceNoは重複しても良い。**

    **違う取引で同じ商品を購入された場合を考慮して、StockNoの重複も許せる。同じ顧客が複数回の購入もできるため、CustomerIDの重複も許容できる**

    **よって、重複データの処理はスキップしても良い**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 不整合データの処理
    """)
    return


@app.cell
def _(raw_data):
    raw_data["Country"].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Countryデータからわかるのは、「USA」「United States」がアメリカのことを示し、「UK」「U.K.」「United Kingdom」がイギリスを示している**

    **これらの表示方法を統一するべき**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 異常値の処理
    """)
    return


@app.cell
def _(raw_data):
    raw_data.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **QuantityとUnitPriceに負数が存在する。処理が必要**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quanityが負数であるデータの抽出**
    """)
    return


@app.cell
def _(raw_data):
    raw_data[raw_data["Quantity"]<0]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **結果を見ると、Quantityが負数になっているデータは、InvoiceNoが「C」で始まっている(つまり取引が取り消された)模様**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **取り消されたデータをさらに抽出すると**
    """)
    return


@app.cell
def _(raw_data):
    raw_data[(raw_data["Quantity"]<0) & (raw_data["InvoiceNo"].str[0]!="C")]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **推測が間違った。取り消したトレードのQuantityが全部負数になっているわけではない　1336/10624**

    **ただ、UnitPriceの値も気になる。InvoiceNoの先頭がCじゃなく、かつQuantityが負数のデータのUnitPriceは必ず0である可能性は？**
    """)
    return


@app.cell
def _(raw_data):
    raw_data[(raw_data["Quantity"]<0) & (raw_data["InvoiceNo"].str[0]!="C") & (raw_data["UnitPrice"]!=0)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **結論：**

    **Quantityが0である場合**

    **1.InvoiceNoはCから始まる**

    **2.UnitPriceは0**

    **これらは有効なデータではなく、分析の邪魔になってしまうため整理が必要**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次はUnitpriceが負数のデータを抽出する**
    """)
    return


@app.cell
def _(raw_data):
    raw_data[raw_data["UnitPrice"]<0]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **二つ存在、消す**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## データの処理
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **読み込みデータにそのまま操作せず、コピーを作って処理を行う**
    """)
    return


@app.cell
def _(raw_data):
    data = raw_data.copy()
    data.head()
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **まずInvoiceDateをfloat型からdatetime型へ変換する**
    """)
    return


@app.cell
def _(data, pd):
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
    data["InvoiceDate"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次はCustomerIDをfloat型からstringに変換する**
    """)
    return


@app.cell
def _(data):
    data["CustomerID"] = data["CustomerID"].astype(str)
    data["CustomerID"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **元のデータがfloat型だったため、末尾に.0がついている。IDに.0は不必要なため切り取る**
    """)
    return


@app.cell
def _(data):
    data["CustomerID"] = data["CustomerID"].str.slice(0,-2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Descriptionが欠損しているデータをドロップする**
    """)
    return


@app.cell
def _(data):
    data.dropna(subset=["Description"],inplace=True)
    return


@app.cell
def _(data):
    data["Description"].isnull().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Country変数の「USA」を「United States」に変換する**
    """)
    return


@app.cell
def _(data):
    data["Country"] = data["Country"].replace({"USA":"United States"})
    return


@app.cell
def _(data):
    len(data[data["Country"]=="USA"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Country変数の「UK」と「U.K.」を「United States」に変換する**
    """)
    return


@app.cell
def _(data):
    data["Country"] = data["Country"].replace({"UK":"United Kingdom","U.K.":"United Kingdom"})
    return


@app.cell
def _(data):
    print(len(data[data["Country"]=="UK"]))
    print(len(data[data["Country"]=="U.K."]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quantityが負数のデータをドロップ**
    """)
    return


@app.cell
def _(data):
    data_1 = data[data['Quantity'] >= 0]
    return (data_1,)


@app.cell
def _(data_1):
    len(data_1[data_1['Quantity'] < 0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **UnitPriceが負数のデータをドロップ**
    """)
    return


@app.cell
def _(data_1):
    data_2 = data_1[data_1['UnitPrice'] >= 0]
    return (data_2,)


@app.cell
def _(data_2):
    len(data_2[data_2['UnitPrice'] < 0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 整理したデータを保存する(完了)
    """)
    return


@app.cell
def _(data_2):
    data_2.to_csv('e_commerce_cleaned.csv', index=False)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

