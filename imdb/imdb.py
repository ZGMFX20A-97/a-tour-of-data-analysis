import marimo

__generated_with = "0.17.7"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 実践：Netflixにおける俳優女優のimdbスコアデータの分析
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
    このデータ分析の目的は、コメディ、アクション、SFなどのさまざまなジャンルにおける俳優・女優のIMDB平均評価を整理し、各ジャンルで評価の高い作品の俳優・女優を発掘することです。

    この実習プロジェクトの目的は、次のステップで分析できるデータを得るために、データを整理する練習をすることです。
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
    データセットには、2022年7月時点でアメリカ地域で視聴可能なすべてのNetflixのテレビシリーズと映画のデータが記録されている。 このデータセットには、`titles.csv`と`credits.csv`の2つのデータテーブルが含まれている。

    titles.csv`には映画やテレビシリーズに関する情報が含まれており、作品ID、タイトル、番組の種類、説明、ジャンル、IMDB（海外のオンライン評価サイト）の評価などが含まれる。 `credits.csv`には、Netflixの映画やテレビシリーズに出演した7万人以上の監督や俳優に関する情報が含まれており、人物名、作品ID、キャラクター名、キャストタイプ（監督/俳優）などが含まれる。
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `titles.csv`カラムの定義：
    - id：作品ID。
    - title：作品タイトル。
    - show_type：番組のタイプ(映画かテレビシリーズ)。
    - description：作品の概要。
    - release_year：リリースの年。
    - age_certification：年齢認証。
    - runtime：テレビシリーズや映画の長さ。
    - genres：ジャンル。
    - production_countries：制作国。
    - seasons：テレビシリーズであれば、シーズンのことを指す。
    - imdb_id：IMDBのID。
    - imdb_score：IMDBスコア。
    - imdb_votes：IMDBの投票数。
    - tmdb_popularity：TMDBの流行度。
    - tmdb_score：TMDBスコア。

    `credits.csv`カラムの定義：
    - person_ID：人物ID。
    - id：出演した作品のID。
    - name：名前。
    - character_name：キャラクター名。
    - role：キャストタイプ(監督/俳優・女優)。
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
    raw_titles = pd.read_csv("./titles.csv")
    raw_credits = pd.read_csv("./credits.csv")
    return raw_credits, raw_titles


@app.cell
def _(raw_titles):
    raw_titles.head()
    return


@app.cell
def _(raw_credits):
    raw_credits.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## データの評価とクリーンアップ
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **クリーンアップされたデータと元のデータを区別するために、新しい変数titlesを作成し、これをraw_titlesのコピーとする。また、新しい変数creditsnにraw_creditsの変数のコピーを代入する。 以降のクリーンアップ作業は、すべてtitlesとcreditsに適用する。**
    """)
    return


@app.cell
def _(raw_credits, raw_titles):
    titles = raw_titles.copy()
    credits = raw_credits.copy()
    return credits, titles


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### データの整然度
    """)
    return


@app.cell
def _(titles):
    titles.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **先頭10行のデータを見ると、genres変数とproduction_countries変数に、分割すべき複数の値が含まれている。**

    **観察しやすいために、genres変数のいずれかの値を抽出することから始める。**
    """)
    return


@app.cell
def _(titles):
    titles['genres'][1]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **genresの表現はリストに見えるけど、実際は文字列のリストではなく文字列であり、value_counts関数で各値の出現回数を直接数えることはできない。文字列を式に変換するPythonの組み込み関数evalを使えば、リストを表す文字列をリストそのものに変換することができる。**
    """)
    return


@app.cell
def _(titles):
    titles['genres'] = titles['genres'].apply(lambda s: eval(s))
    titles['genres'][1]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **リストに変換されると、DataFrameのexplode関数を使って、そのカラムのリスト値を別々の行に分割することができる。**
    """)
    return


@app.cell
def _(titles):
    titles_1 = titles.explode('genres')
    titles_1.head(10)
    return (titles_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次に、production_countriesにも同じ操作を行う。**

    **各production_countries値は、単一のジャンルではなく一連のジャンルを表している。まず観察のために抽出する。**
    """)
    return


@app.cell
def _(titles_1):
    titles_1['production_countries'][1]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **production_countriesも同じ問題ですね**
    """)
    return


@app.cell
def _(titles_1):
    titles_1['production_countries'] = titles_1['production_countries'].apply(lambda x: eval(x))
    titles_2 = titles_1.explode('production_countries')
    titles_2['production_countries'][0]
    return (titles_2,)


@app.cell
def _(titles_2):
    titles_2.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次はcreditsを見る**
    """)
    return


@app.cell
def _(credits):
    credits.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **先頭10行のデータを見ると、creditsデータは綺麗で特に問題ない。**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### データのクリーン度
    """)
    return


@app.cell
def _(titles_2):
    titles_2.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **出力結果から、titlesデータには、合計17818の観察対象がある。tmdb_popularity、tmdb_score、imdb_votes、tmdb_popularity、tmdb_score変数にはすべて欠損値があり、後で評価およびクリーンアップする予定。**

    **さらに、release_yearは年を表し、データ型は数値ではなく日付であるべきため、データ型の変換が必要。**
    """)
    return


@app.cell
def _(pd, titles_2):
    titles_2['release_year'] = pd.to_datetime(titles_2['release_year'], format='%Y')
    titles_2['release_year']
    return


@app.cell
def _(credits):
    credits.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **出力結果から、creditsデータには合計77,801の観察対象があり、そのうちのcharacter変数には欠損値がある。**

    **さらに、person_idは人物IDを表し、データ型は数値ではなく文字列であるべきため、データ型の変換が必要。**
    """)
    return


@app.cell
def _(credits):
    credits["person_id"] = credits["person_id"].astype(str)
    credits["person_id"]
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
    **titlesデータセットでは、title、description、age_certification、production_countries、seasons、imdb_id、tmdb_popularity、tmdb_score、imdb_votes変数に欠損値がある。**

    **映画やテレビ作品のタイトル、説明、年齢認証、制作国、テレビシリーズのシーズン数、imdb_id、tmdb_popularity、tmdb_scoreeは各ジャンルにおけるIMDBスコアの高い俳優を発掘することに影響しないため、title、description、age_certification、production_countries、seasons、imdb_id、tmdb_popularity、tmdb_score、imdb_votesが欠損しているデータについて保留しても良い。**

    **しかし、imdb_scoreとgenresはこの後に行う分析の主役として関連が強く、欠損しては分析に支障をきたす。**

    **まず、見るためにimdb_scoreが欠損しているデータを抽出する。**
    """)
    return


@app.cell
def _(titles_2):
    titles_2.query('imdb_score.isnull()')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **分析に必要なコアデータであるimdb_scoreは欠損しているため、これらのデータを除去し、sum関数で除去後の列の空き値の数の合計を見る**
    """)
    return


@app.cell
def _(titles_2):
    titles_3 = titles_2.dropna(subset=['imdb_score'])
    titles_3['imdb_score'].isnull().sum()
    return (titles_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次にgenresが欠損しているデータを見つけ出す**
    """)
    return


@app.cell
def _(titles_3):
    titles_3.query('genres.isnull()')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **分析に必要なコアデータであるgenresは欠損しているため、これらのデータを除去し、sum関数で除去後の列の空き値の数の合計を見る**
    """)
    return


@app.cell
def _(titles_3):
    titles_4 = titles_3.dropna(subset=['genres'])
    titles_4['genres'].isnull().sum()
    return (titles_4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 重複データの除去
    """)
    return


@app.cell
def _(titles_4):
    titles_4.duplicated().sum()
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **genresやproduction_countries変数に一貫性のないデータが存在する可能性があり、同じジャンルを指す複数の異なる値や、同じ国を指す複数の異なる値があるかどうかを調べる。**
    """)
    return


@app.cell
def _(titles_4):
    titles_4['genres'].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **ジャンルには一貫性のないデータはなく、個々の値はすべて異なるジャンルを指している。しかしまだ空のジャンルがあり、これは有効なデータではないため削除するべき。**

    **削除後、titlesをチェックして、まだ空のジャンルがある行があるかどうかを確認する**
    """)
    return


@app.cell
def _(titles_4):
    titles_5 = titles_4.query('genres != ""')
    titles_5.query('genres == ""')
    return (titles_5,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次にproduction_countriesも同様**
    """)
    return


@app.cell
def _(titles_5):
    titles_5['production_countries'].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **国の種類が多すぎて一気に表示できないため、一時的にdisplay.max_rowsをNoneに設定することで全部表示させることができる。**
    """)
    return


@app.cell
def _(pd, titles_5):
    with pd.option_context('display.max_rows', None):
        print(titles_5['production_countries'].value_counts())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **上記の出力結果から、制作国はLebanonを除き、すべて2桁の国コードで表されていることがわかる。**

    **調べたところLebanonの国コードはLBでLBとLebanonは同じ国を示しているため統一させる必要がある。**
    """)
    return


@app.cell
def _(titles_5):
    titles_5['production_countries'] = titles_5['production_countries'].replace({'Lebanon': 'LB'})
    titles_5.query('production_countries == "Lebanon"')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Lebanonが存在しなくなった**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次はキャストタイプ**
    """)
    return


@app.cell
def _(credits):
    credits["role"] = credits["role"].astype("category")
    credits["role"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **大丈夫**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 異常値の処理
    """)
    return


@app.cell
def _(titles_5):
    titles_5.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **リリース年におかしな値が見られるが、まあいいでしょう**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### データの整理
    """)
    return


@app.cell
def _(titles_5):
    titles_5
    return


@app.cell
def _(credits):
    credits
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **今回データ分析の目的は、さまざまなジャンルの映画やテレビ作品における俳優の平均IMDBスコアを照合し、各ジャンルで評価の高い俳優を掘り出すこと。**

    **ジャンルと俳優のデータを同時に取得するために、titlesとcreditsをidをキーとしてマージする必要がある。**
    """)
    return


@app.cell
def _(credits, pd, titles_5):
    merge = pd.merge(credits, titles_5, on='id', how='inner')
    merge
    return (merge,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **データ分析の主旨は俳優を発掘することであり、監督は分析対象に含まれないためACTORタイプをフィルタリングで抽出する。**
    """)
    return


@app.cell
def _(merge):
    actor_with_titles = merge.query('role == "ACTOR"')
    return (actor_with_titles,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **各ジャンルでIMDB評価の高い俳優を掘り出すには、まずジャンルと俳優でグループ化する必要がある。**

    **俳優をグループ化する際、name変数ではなくperson_id変数を使用すること。名前はスペルミスや改名が起こりやすく、俳優名よりもperson_idの方がより正確にどの俳優であるかを反映できる。**
    """)
    return


@app.cell
def _(actor_with_titles):
    groupby_genres_and_personID = actor_with_titles.groupby(["genres","person_id"])
    return (groupby_genres_and_personID,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **グループ化した後、imdb_scoreの値を集約するだけでよいため、imdb_score変数のみ抽出しする。各俳優が出演した各ジャンルの映画・テレビの平均IMDBスコアをmean関数で計算する。**
    """)
    return


@app.cell
def _(groupby_genres_and_personID):
    imdbScore_groupby_genres_and_personID = groupby_genres_and_personID["imdb_score"].mean()
    imdbScore_groupby_genres_and_personID
    return (imdbScore_groupby_genres_and_personID,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **reset_index関数でデータを階層し、インデックスをリセットする。より見やすいDataFrameを得ることができる。**
    """)
    return


@app.cell
def _(imdbScore_groupby_genres_and_personID):
    imdbScore_groupby_genres_and_personID_df = imdbScore_groupby_genres_and_personID.reset_index()
    imdbScore_groupby_genres_and_personID_df
    return (imdbScore_groupby_genres_and_personID_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **これで、ジャンルと俳優のグループ分けに対するIMDBの評価が整理されたため、次の分析ステップに進もうと思う。**

    **例えば、各ジャンルの俳優の作品の平均評価が最も高いのは何か、最も高い評価に対応する俳優は誰かなどを調べるために、上記の結果をもう一度グループ化することができる。**

    **この結果を得るには、再度ジャンルでグループ化し、imdb_score変数を抽出してその最大値を計算する必要がある。**
    """)
    return


@app.cell
def _(imdbScore_groupby_genres_and_personID_df):
    genres_max_scores = imdbScore_groupby_genres_and_personID_df.groupby("genres")["imdb_score"].max()
    genres_max_scores
    return (genres_max_scores,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **最高スコアがわかったら、上記の結果と先ほど得たimdbScore_groupby_genres_and_personID_dfと再度結びつければ、最高スコアに対応する個々の人物IDが何かがわかる。**
    """)
    return


@app.cell
def _(genres_max_scores, imdbScore_groupby_genres_and_personID_df, pd):
    genres_max_scores_with_personID = pd.merge(imdbScore_groupby_genres_and_personID_df,genres_max_scores,on=["genres","imdb_score"])
    genres_max_scores_with_personID
    return (genres_max_scores_with_personID,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **上記の結果から、最高スコアを獲得した俳優は必ずしも1人とは限らず、同じ平均得点を持つ複数の俳優が存在する可能性があることがわかる。**

    **person_idに対応する俳優の名前を取得するには、creditsとマージする必要がある。このDataFrameには不必要なカラムがあるが、必要なのはperson_idとnameだけなためまずこの2つのカラムを抽出し、重複する行を削除する。**
    """)
    return


@app.cell
def _(credits):
    actorid_with_names = credits[["person_id","name"]].drop_duplicates()
    actorid_with_names
    return (actorid_with_names,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **次は、actorid_with_namesと先に得たgenres_max_score_with_personIDと連結し、name変数を追加して平均点が最も高い俳優の名前を表示する。**
    """)
    return


@app.cell
def _(actorid_with_names, genres_max_scores_with_personID, pd):
    genresMaxScore_with_actorName = pd.merge(actorid_with_names,genres_max_scores_with_personID,on="person_id")
    genresMaxScore_with_actorName
    return (genresMaxScore_with_actorName,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **同じジャンルをまとめてソートするためには、sort_values関数を使って結果内の行をジャンル別にソートし、reset_indexを使ってインデックスを並び替える。**

    **インデックスの並び替えが完了すると、DataFrameにインデックスカラムが追加されるため、インデックスを削除して見やすくする。**
    """)
    return


@app.cell
def _(genresMaxScore_with_actorName):
    genresMaxScore_with_actorName_1 = genresMaxScore_with_actorName.sort_values('genres').reset_index().drop('index', axis=1)
    genresMaxScore_with_actorName_1
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

