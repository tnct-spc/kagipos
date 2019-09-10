# kagipos
kagisys-possys統合環境

## 注意
これは現在の"仕様"について記したものである  
もし、ここに書いてあることと違う現象があったとしたら、それはバグなので、すぐにissueを立てること

## 本番環境での初回起動時にやること
```bash
docker exec -it kagipos_django_1 /bin/bash
```
これでコンテナの中に入るので
```bash
python manage.py createsuperuser
```
を実行して管理者を作る

## デプロイ方法
```bash
docker-compose restart
```
単なる`git pull`だけでも反映される可能性がある
これで反映されなかったり、エラーがでる場合は、コンテナに入って
```bash
python manage.py makemigration
python manage.py migrate --run-syncdb
```
とすればうまくいく・・・かもしれない
models.pyを書き換えた場合 migrate 関連は必須で、コンフリクトする場合も多いので頑張ろう

```bash
docker-compose down
docker-compose up
```
も使える

## APIについて
APIは、単体APIとREST-APIに分けてある

### 単体API
`アプリ名/api/`の下に置いてあり、全て筐体アカウントからしかアクセスできないようになっている  
最初、筐体アカウントは存在しない  
`username`で判別しているので、`kagisys`と`possys`のユーザーを作っておくこと  
また、基本的に`GET`しか受け付けてないので、パラメータは全部URLに含める

### REST-API
REST-fullなAPIで、`api/アプリ名/`の下に置いてある  
ログインしていれば誰でもアクセスできる

### アクセス方法
全てのAPIはセッションかトークンでアクセスできる  
トークン取得APIは`api/auth/`で、`POST`で`username`と`password`を投げると`token`がJSON形式で帰ってくる
