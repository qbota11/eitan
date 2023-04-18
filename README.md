# eitan
[https://ja.mondder.com/list?id=86](https://ja.mondder.com/list?id=86 "大学受験の英単語")を作った際に使用したコード群です。
## mydb.py
量が多くて大変だったのでとりあえずデータベース（mysql）に貯めておくことになってます。
テーブルの定義が書いてあるので、テーブルを立て接続情報を書き換えてください。
## parse.py
テキストファイルを読み込んで、その中に含まれている英単語を抽出します。
## meaning.py
抽出した単語の意味を調べます。
[https://bond-lab.github.io/wnja/](https://bond-lab.github.io/wnja/ "https://bond-lab.github.io/wnja/") からwnjpn.dbをダンロードする必要があります。
## example.py
抽出した単語をもとにChatGPTに例文を作って貰います。
## translation.py
Google翻訳やDeepLのapiを使って例文を訳します。
## questions.py
上記の作業で貯め込んだデータをもとにしてCSVファイルを作ります。これを[Mondder](https://ja.mondder.com/ "Mondder")（択一式問題）にインポートすると[こんな感じのもの](https://ja.mondder.com/questions?id=423 "大学受験の英単語 英→日ver. ①")が出来上がります。
