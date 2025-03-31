# django-bento-system
弁当の購入数及び合計金額をLINE Official Accountで管理するシステム

## 使用技術
* Docker
* Django
* Nginx
* MySQL
* LINE Messaging API

## 作成時間
* 10時間

## できること
* ユーザーの登録をLINEのUserIDを通して行う。
* 各々の弁当の購入数、金額を把握することができる。
* 合計の数を把握できるので、電話注文の際に助かる。
* その日の弁当の数が分かるので、注文ミスに即日気づくことができる。

## 使い方

### メニュー
![Image](https://github.com/user-attachments/assets/1ab15991-e7a8-4308-8ed9-b4aff5750903)

### お弁当お休み登録
* クールを選択

![Image](https://github.com/user-attachments/assets/58a340a2-3074-4c07-815d-9cc6a7818a91)

* 選択したクールの自分の注文状況が表示される

![Image](https://github.com/user-attachments/assets/e35ea57d-2238-444e-bb6d-acf23d29b053)

* 日付の下の`◯` or `✕`のボタンをクリックすると`◯`と`✕`が反転する、変更のメッセージが表示される

![Image](https://github.com/user-attachments/assets/e55c1efd-4879-4bd6-94f9-31f9e321c7e2)

* そのクールすべて注文なしも可能

![Image](https://github.com/user-attachments/assets/0002767c-0923-4e8a-bd46-f2ca46f2d1f6)

* そのクールすべて注文はデフォルト、ボタンでも可能
  
![Image](https://github.com/user-attachments/assets/2355e6c1-e0b6-4ce0-af5f-90b55e501bb9)

### 注文数・支払金額確認
* クール選択

![Image](https://github.com/user-attachments/assets/f8405feb-87ba-499a-bbaf-6c675e70f4c2)

* そのクールの自分の注文個数と合計金額が表示される

![Image](https://github.com/user-attachments/assets/d9a3d785-0aea-4dec-8a23-4189ce749263)

### 電話・献立表
* メニュー選択 店舗に電話、献立表、今日のお弁当の数を確認できる

![Image](https://github.com/user-attachments/assets/a0799361-d461-4ace-84db-cd67deda5810)

* お店の情報

![Image](https://github.com/user-attachments/assets/71599694-8b44-4bfd-9c0b-35ceffe2cefd)

* 献立表→何月の献立表か選択

![Image](https://github.com/user-attachments/assets/feaad363-5cd1-4d4d-a4d9-326d052dda2d)

* 献立表が画像で送られる

![Image](https://github.com/user-attachments/assets/1fc40ef3-f579-49a5-92b7-3de3c561632c)

* 今日のお弁当の数

![Image](https://github.com/user-attachments/assets/78caca34-370b-4f27-b642-dc2b38057547)
