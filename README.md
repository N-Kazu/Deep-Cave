# Deep Cave
## 概要
ゲーム作成ライブラリであるlibtcodを使用したローグライクゲームです。  
現バージョン(v0.10)では機能的な実装しか行っていないため、ゲーム性は低いです。  

## 動作環境
動作確認済み
* Windows10  

exeを実行できる環境であれば問題なく動作すると思います。  

## ダウンロード/やり方
releaseより最新バージョンをダウンロードし、gameフォルダにある「Deep Cave.exe」を起動してください。
*ファイル構造は変えないよう、exeファイルはgameフォルダから動かさないでください。  

## ゲーム説明
ランダムに生成されるダンジョンをアイテムや武器を駆使してより深くまで探索することが目的です。  
モンスターを倒し経験値を貯めてレベルアップを行い、階層が深くなるごとに難易度が上がるダンジョンを深く深く潜っていきましょう。  
セーブはメニューに戻ったときにオートセーブされます。途中から始めたい場合には、メニューよりコンテニューを選択してゲームを再開してください。

## 操作方法
基本的にはキーボードの矢印キーで上下左右に動きますが、vimキーバインドの動作を想定しています。　　

    h:← l:→ j:↓ k:↑ y:左上 u:右上 b:左下 n:右下 z:足踏み  
    
    g:拾う d:落とす i:インベントリ c:キャラクタ詳細 ESC:戻る/メニューへ

## Special Thanks
RogueLike Development([Reddit](https://www.reddit.com/r/roguelikedev/))  

#### Algorithm
* A*([wiki](https://ja.wikipedia.org/wiki/A*))  
* Bresenham's line algorithm([wiki](https://bit.ly/30xchTm "https://ja.wikipedia.org/wiki/ブレゼンハムのアルゴリズム"))  
* Ray Casting([外部サイト](https://sites.google.com/site/jicenospam/visibilitydetermination))  
