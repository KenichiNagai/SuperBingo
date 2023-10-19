# スーパービンゴシミュレータPython版

## これは何
任意の手牌に対して山をN通り生成し、チューリップをめくった結果を集計します

- super_bingo.py  シミュレータ本体
- requirements.txt    必要パッケージ
- readme.md   これ

## 使い方
Windowsの場合
1. Pythonをインストール
2. cdをsuper_bingo.pyを置いたフォルダに指定
3. コマンドは以下の通り

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


## 機能
- 牌姿指定
- 除外牌指定(華など)
- アガリ巡目指定(複数)
- スーパービンゴのみではなくパチンコにも対応
- パチンコの際の萬子の数え方に複数対応
- チューリップではなくアリスにも対応（常に非確変）
