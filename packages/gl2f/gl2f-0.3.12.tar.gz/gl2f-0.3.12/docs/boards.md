# リストの作り方

サブコマンド `cat, dl, ls, open, search` は、対象となるリストや表示の整形を指示する必要があります（[コマンドの説明](./commands.md)）。
リストの指定はページの種類（ブログ、ニュース、ラジオ等）と、さらに必要なグループまたはメンバーを与えて行います。
またページとは別に、 `today` とすると全てのページの24時間以内の更新をリストします。

```sh
# Girls2 のブログを開く
gl2f open blogs/girls2

# 杉浦優來のラジオを開く
gl2f open radio/yura

# GL2 family のニュースを開く
gl2f open news/family

# 24時間以内の更新を開く
gl2f open today
```


## 引数

ページの種類によって、指定できるメンバー名などは変わります。


### `today` 24時間以内の更新

日記、ニュース、ラジオ、Gtube、commercial movie、またイベント期間中は特設ページをチェックし、24時間以内の更新を返します。

24時間以内の更新を全てリストとして表示する
```sh
gl2f ls today
```

### `blogs` 日記

日記のリスト ( https://girls2-fc.jp/page/blogs 等 ) を取得します。
指定できるのはグループ名 `girls2, loveky2, lucky2`, メンバーの下の名前のアルファベット小文字 `yuzuha, momoka, misaki, ...`, また当日の更新を取得する `today` です。

今日投稿されたブログを全て開く
```sh
gl2f open -a blogs/today
```

### `news` ニュース

ニュースのリスト ( https://girls2-fc.jp/page/familyNews 等 ) を取得します。
指定できるのはグループ名 `girls2, lovely2, lucky2, mirage2` と、Girls2 + Lucky2 の `family` です。

GL2 family のニュース本文を表示する。
```sh
gl2f cat news/family
```

### `radio` ラジオ

ラジオのリスト ( https://girls2-fc.jp/page/lucky2radio 等 ) を取得します。
指定できるのはグループ名 `girls2, loveky2, lucky2`, メンバーの下の名前のアルファベット小文字 `yuzuha, momoka, misaki, ...` です。

比嘉優和のラジオをブラウザで開く
```sh
gl2f open radio/yuwa
```

### `gtube` Gtube

Gtube ( https://girls2-fc.jp/page/gtube ) を取得します。
`gtube` を省略できるメインコマンドはありません。

Gtube をブラウザで開く
```sh
gl2f open gtube
```


### `cm` commercial movie

commercial movie ( https://girls2-fc.jp/page/commercialmovie/ ) を取得します。
`gtube` を省略できるメインコマンドはありません。

commercial movie をブラウザで開く
```sh
gl2f ls cm
```

### fm

ファンミーティングのフォトギャラリーを取得します。

引数
* `lucky2-2023` https://girls2-fc.jp/page/L2FanMeetingPG2
* `girls2-2022` https://girls2-fc.jp/page/G2fcmeetingpg
* `lucky2-2022` https://girls2-fc.jp/page/L2fcmeetingpg

Girls2 ファンミーティング2022 の画像をリストする
```sh
gl2f ls fm/girls2-2022
```


### その他

そのほか、過去のページの取得方法については[こちら](./other_boards.md)


## オプション

リストを作るために共通して以下のオプションがあります。

* `-n, --number` 読み込み数の指定。1~99 の範囲です。
* `-p, --page` ページの指定。
* `--group` グループの指定。ブログで、莉愛と優來のときに `--group lovley2` とすることで lovely2 時代の記事を取りに行きます。
* `--order <オプション>` ソートの指定。 公開日 `reservedAt` と記事タイトル `name` のどちらかについて、昇順 `asc`と降順 `desc` を指定します。デフォルトは `reservedAt:desc` で、更新日の新しいものから並べます。

山口莉愛 の lovely2 の頃のブログを開く
```sh
gl2f open blogs/rina --group lovely2
```

lovely2 のブログを20件一覧表示する
```sh
gl2f ls blogs/lovely2 -n 20
```

Lucky2 のニュースの最新6番目から10番目を一覧表示する (1ページあたり5件の2ページ目)
```sh
gl2f ls news/lucky2 -n 5 -p 2
```

原田都愛のブログをタイトル降順で30件を一覧表示する
```sh
gl2f ls blogs/toa --order name:desc -n 30
```

### リストの整形

また、表示方法を制御するために以下のオプションがあります。

* `-f, --format` リストのフォーマット指定。以下の要素を `:` で区切って与えます。デフォルトはサブコマンドによって異なります。
	* `author` 著者名。
	* `title` 記事タイトル。
	* `url` URL。
	* `date-p` 記事が公開された日時。
	* `date-c` 記事がアップロードされた日時。
	* `index` リスト上での番号を振ります。
	* `br` 改行。
	* `id` 記事のID。ダウンロードするフォルダ名などに使っているので、調べたいときに使えます。
	* `media` 記事に含まれる画像と動画の数。画像が5、動画が1あるときは`i05 v1` のように出力されます。
	* `page` ページ名
* `-d, --date` フォーマット指定を指定して記事の公開日時を左側に表示します。デフォルトは月/日(`%m/%d`)。書式については[こちら](https://docs.python.org/ja/3/library/datetime.html#strftime-strptime-behavior)
* `--break-urls` URLを改行して表示します。 `-f` で `url -> br:url` と置き換えることと同じです。
* `--enum` リストに番号を振ります。 `-f` に `index` を含めることと同じです。


Girls2 のニュースを公開日の早いものから10件一覧表示する。公開年月日も表示する
```sh
gl2f ls news/girls2 --order reservedAt:asc -d '%Y/%m/%d'
```

lovely2 スタッフのブログを、投稿日と公開日とともに一覧表示する。日時は秒まで表示する。
```sh
gl2f ls blogs/lovely2staff -f author:date-p:date-c:title:url -d '%m/%d %H:%M:%S'
```

今日の更新をページ名を含め表示する
```sh
gl2f ls today -f page:author:title
```
