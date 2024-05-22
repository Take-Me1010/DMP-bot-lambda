# DMP-BOT-lambda

リモートデュエルに有用なコマンドを実装しています。


## `/coin`

コインを投げます。実行すると、表か裏が出ます。

ポケカとかでも有用です。ポケモンチェック等でも活用ください。

<!-- ## `/randint num`

0 ~ num - 1 でランダムな整数を返します。

シャッフ宣言で迷ったら`/randint 1000`とかしてみては？

## `/pick options (n = 1)`

与えられた選択肢からランダムに`n`個選びます。
`n`は指定しない場合、1になります。
なお、重複して選択することはありません。

選択肢には`/pick TakeMe,canbe,udon`のように、カンマ区切りでスペースを除いて渡してください。

先攻後攻を決める際に`/pick takeme,kavaragi`などとしてみては？

## `/shuffle options`

与えられた選択肢をランダムにシャッフルして返します。

選択肢には`/pick TakeMe,canbe,udon`のように、カンマ区切りでスペースを除いて渡してください。

デュエパーティで順番を決める際に`/shuffle takeme,canbe,udon,kavaragi`などとしてみては？ -->

# 開発

Pipenv使ってます。下記は windows 前提です。
pipenv は `pip install pipenv` でインストールして、どうぞ。

```ps1
$env:PIPENV_VENV_IN_PROJECT = 1; pipenv --python 3.8
pipenv install --dev
pipenv run setup
```

.envを作っておく。

```.env
APP_ID = "YOUR_APPLICATION_ID"
SERVER_ID = "YOUR_SERVER_ID"
BOT_TOKEN = "BOT_TOKEN"
```

# 参考

- https://github.com/ker0olos/aws-lambda-discord-bot : 英語のディスコボット作成入門
- https://blog.shikoan.com/discord-bot-lambda-1/ : 日本語情報
- https://note.sarisia.cc/entry/discord-slash-commands/ : 日本語情報2
- https://github.com/keithrozario/Klayers/tree/master : 先人のLayers
  - https://api.klayers.cloud/api/v2/p3.8/layers/latest/ap-northeast-1/html : Python 3.8 の Layers。ここに PyNacl が存在するので 3.8 を選択せざるを得なかった
  - https://www.reddit.com/r/aws/comments/p1z95f/help_with_python_lambda_pynacl_module_issue : PyNacl は windows 環境でインストールしたものをデプロイしても動作しないよ、という話
