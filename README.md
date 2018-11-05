# splatnet2statink-docker



[splatnet2statink](https://github.com/frozenpandaman/splatnet2statink)をコンテナエンジン上で動作させることができます。またプログラムの開始時にソースコードを自動的に`git pull`することで常に最新版のsplatnet2statinkを実行できます。

# 使い方

## Dockerで実行

環境変数に`api_key, session_token, cookie, user_lang`を設定して、実行します。

```
$ docker run -e api_key=<your api key> \
             -e session_token=<your session token> \
             -e cookie=<your cookie> \
             -e user_lang=<your user_lang>
```

## Docker-composeで実行

上記を例に`docker-compose.yml`に事前にsplatnet2statinkを実行して得られた`config.txt`の値を設定。(取扱い注意)

```
$ docker-compose up
```

# 設定一覧

| 項目名 | 内容 | 初期値 |
| --- | -- | -- |
| api_key | stat.inkのAPI Key | "" |
| session_token | splatnet2statink動作のために取得した値 | "" |
| cookie | splatnet2statink動作のために取得した値 | "" |
| user_lang | アクセス時の言語。特に指定がなければ"en-US"にしておく | "en-US" |
| run_flags | splatnet2statink起動時のフラグ(salmon run起動時のものは編集できません) | "-r" |
| skip_update | 何かしらの値が設定されているとsplatnet2statinkの`git pull`を抑制します | false |
| skip_salmon | 何かしらの値が設定されているとSalmon Runの更新を抑制します | false |

# 定期実行のヒント

1. Google Cloud等クラウドアプリケーションで実行する 
1. 保有するサーバでcrontab等でコンテナを定期的に実行する

# ビルド済コンテナ

[DockerHub](https://cloud.docker.com/swarm/kamiyaowl/repository/docker/kamiyaowl/splatnet2statink-docker/general)