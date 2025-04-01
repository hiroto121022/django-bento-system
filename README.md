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
* お休み登録→クールを選択

![Image](https://github.com/user-attachments/assets/46e60411-ef87-459c-9b48-a48f1c7045de)

* 選択したクールの自分の注文状況が表示される

![Image](https://github.com/user-attachments/assets/f1e00114-eed0-4089-80b7-1e8f7b5b787d)

* 日付の下の`◯` or `✕`のボタンをクリックすると`◯`と`✕`が反転する、変更のメッセージが表示される

![Image](https://github.com/user-attachments/assets/6f5882a0-d6f6-4bbd-8d7f-6deb0c23c4ae)

* そのクールすべて注文なしも可能

![Image](https://github.com/user-attachments/assets/86f9646c-a0f7-4f2d-8900-47e24d6e08ec)

* そのクールすべて注文はデフォルト、ボタンでも可能
  
![Image](https://github.com/user-attachments/assets/5199d166-9bc1-41d4-9713-074afc28cba7)

### 注文数・支払金額確認
* 支払金額→クール選択

![Image](https://github.com/user-attachments/assets/390fccae-acbc-4017-a791-148e2fc3a149)

* そのクールの自分の注文個数と合計金額が表示される

![Image](https://github.com/user-attachments/assets/912feeae-c0bc-4e54-89e1-7e249fc0be24)

### 電話・献立表
* メニュー選択 店舗に電話、献立表、今日のお弁当の数を確認できる

![Image](https://github.com/user-attachments/assets/eee89cde-2e94-4651-94f5-58ffb10a831e)

* お店の情報

![Image](https://github.com/user-attachments/assets/f4003b7f-a9de-4730-bf25-38b1440bf374)

* 献立表→何月の献立表か選択

![Image](https://github.com/user-attachments/assets/6ec375ee-1c25-4459-80d8-0c0eec24f5d2)

* 献立表が画像で送られる

![Image](https://github.com/user-attachments/assets/e096f5e9-cf2d-48da-82f4-ea3692c78f55)

* 今日のお弁当の数

![Image](https://github.com/user-attachments/assets/062f47e8-a815-4144-811c-071bf1950d05)
