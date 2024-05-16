# Deep Cave

![Animation1_](https://github.com/N-Kazu/Deep-Cave/assets/66771601/13131697-7bd4-4699-b02f-da098a5bbd5e)

## 概要
ゲーム作成ライブラリであるlibtcodを使用したローグライクゲームです。  
自己満足のペースで更新をしています。 

## 動作環境
動作確認済み
* Windows10  

exeを実行できる環境であれば問題なく動作すると思います。  

## ダウンロード/やり方
releaseより最新バージョンをダウンロードし、gameフォルダにある「Deep Cave.exe」を起動してください。  
**ファイル構造は変えないよう、exeファイルはgameフォルダから動かさないでください**。  

## ゲーム説明
ランダムに生成されるダンジョンをアイテムや武器を駆使してより深くまで探索することがゲームの目標です。  
階層が深くなるたび難易度が上がるため、アイテムやレベルアップを駆使しながらできるだけ深くを目指しましょう！  
セーブはメニューに戻ったときにオートセーブされます。途中から始めたい場合には、メニューよりコンテニューを選択することでゲームを再開できます。

## 操作方法
基本的にはキーボードの矢印キーで上下左右に動きますが、vimキーバインドの動作を想定しています。　　

    h:← l:→ j:↓ k:↑ y:左上 u:右上 b:左下 n:右下 z:足踏み  
    
    g:拾う d:落とす i:インベントリ c:キャラクタ詳細 ESC:キャンセル/戻る/メインメニューへ  
    
    対象指定のアイテムはマウスで対象をクリックすることで使用できます。

## Special Thanks
RogueLike Development([Reddit](https://www.reddit.com/r/roguelikedev/))  

#### Algorithm
* A*([wiki](https://ja.wikipedia.org/wiki/A*))  
* Bresenham's line algorithm([wiki](https://bit.ly/30xchTm "https://ja.wikipedia.org/wiki/ブレゼンハムのアルゴリズム"))  
* Ray Casting([外部サイト](https://sites.google.com/site/jicenospam/visibilitydetermination))  
