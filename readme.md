2023/10/19
# スーパービンゴシミュレータPython版

## これは何
任意の手牌に対して山をN通り生成し、チューリップをめくった結果を集計します。  

- super_bingo.py        シミュレータ本体
- requirements.txt      必要パッケージ
- readme.md             これ

## 使い方
### Chrome等ブラウザ
PCより以下のcolab notebookを開き、最上部のパラメータ部分を編集して実行してみて下さい。  
https://colab.research.google.com/drive/1mVffPyH2XS5CTmnJ4cRUlpZkrOJLaLhs?usp=sharing  

### Windows環境の場合のコマンド等
1. Pythonをインストール
1. cdをsuper_bingo.pyを置いたフォルダに指定
1. コマンドは以下の通り

環境の作成とアクティベート(venv_bingoは任意の名前で)
```
python3 -m venv venv_bingo
.\venv_bingo\Scripts\Activate
```

必要パッケージのインストール
```
pip install -r requirements.txt
```

実行
```
python .\super_bingo.py
```

### Linux環境の場合  
そのようなつわものは自分で何とかしてください。

## 機能
- 牌姿指定
- 除外牌指定(華など)
- アガリ巡目指定(複数)
- スーパービンゴのみではなくパチンコにも対応
- パチンコの際の萬子の数え方に複数対応
- チューリップではなくアリスにも対応（常に非確変）


## お前は誰
X: kenboh_switch
