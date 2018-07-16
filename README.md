# splatnet2statink-docker

[https://github.com/frozenpandaman/splatnet2statink](https://github.com/frozenpandaman/splatnet2statink)

上記アプリケーションをコンテナエンジン上で動作させる。

# 使い方

## 実行時に指定

1. `docker-compose.yml`に事前にsplatnet2statinkを実行して得られた`config.txt`の値を設定。

1. `$ docker-compose up`

## コンテナを自分でビルドする場合

`Dockerfile`はプロジェクトフォルダごとコンテナ内にコピーします。この際にconfig.txtをコンテナ内に移動させることで環境変数無しで実行できます。

1. `.dockerignore`から`config.txt`を削除

1. splatnet2statinkで得られた`config.txt`を府rジェクトルートに配置

1. `docker-compose build`

1. `docker-compose up`