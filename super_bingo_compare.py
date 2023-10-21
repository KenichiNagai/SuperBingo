'''
設定部分
'''

# 手牌の牌姿を指定: 凡例: 19m456p789s / 東西南北白發中 or 1~7z / 花 or 華 or x
TEHAI = '234789p123678s477z'

# 除外する牌を指定: 凡例: 19m456p789s / 東西南北白發中 or 1~7z / 花 or 華 or x
EXECLUDE_TILE = 'xxxx'

# 一発、三倍満、AOPなどによるストック数(転落保障回数)
V_STOCK = 0

# 試行回数
TRY_NUM = 10000

# 何巡目のシミュレーションを表示するか(半角数字をカンマ区切りで指定)
TURN_LIST = [6, 15]

# True:スーパービンゴ / False:萬子入り
SUPER_BINGO = False

# 何枚区切りで結果表示するか
TIP_WIDTH = 5

# 萬子の数え方 / QUASAR:通常の数え方 / YUNYUN2:萬子2枚乗り / YUNYUN3:萬子3枚乗り
# SUPER_BINGOがTrueのとき無視されます
MANZU_COUNT = 'QUASAR'
# MANZU_COUNT = 'YUNYUN3'
# MANZU_COUNT = 'YUNYUN2'

# True:チューリップ / False:アリス      # アリスの場合,常に非確変
TULIP = True


'''
コード部分
'''
import random
import re
import matplotlib.pyplot as plt
import pandas as pd
# import tqdm.notebook
from tqdm import tqdm
from collections import Counter


class tile_deck():
    tile_deck = []

    def __init__(self, super_bingo = True):
        self.tile_deck = []
        self.tile_deck = self.make_tile_deck(super_bingo)

    # 牌山を生成する
    def make_tile_deck(self, super_bingo):
        tile_name_list = []
        if super_bingo:
            tile_name_list.append(f"7p")
            tile_name_list.append(f"7s")
        else:
            tile_name_list.append(f"1m")
            tile_name_list.append(f"9m")

        for i in range(1, 10):
            tile_name_list.append(f"{i}p")
            tile_name_list.append(f"{i}s")
        for i in range(1, 8):
            tile_name_list.append(f"{i}z") # 東南西北白發中
        tile_name_list.append(f"x") # 華

        for tile_name in tile_name_list:
            for i in range(4):
                self.tile_deck.append(tile_name)
        random.shuffle(self.tile_deck)
        return self.tile_deck

    def shuffle_tile_deck(self):
        random.shuffle(self.tile_deck)

    # 牌山から牌を引く
    def draw_tile(self):
        return self.tile_deck.pop()

    # 牌山から牌を除外
    def remove_tile(self, tile_name):
        self.tile_deck.remove(tile_name)

    # 牌山から手牌を除外
    def remove_tehai(self, tehai_list):
        for tile_name in tehai_list:
            self.tile_deck.remove(tile_name)


# 手牌　str -> list
def make_tile_list(tehai_input = ''):
    # 正規表現で検索
    manzu = re.search(r'\d+m', tehai_input)
    pinzu = re.search(r'\d+p', tehai_input)
    souzu = re.search(r'\d+s', tehai_input)
    zihai = re.search(r'\d+z', tehai_input)

    def replace_input_str(input_str):
        if input_str is not None:
            input_str = input_str.group()
            input_str = input_str.replace('m', '')
            input_str = input_str.replace('p', '')
            input_str = input_str.replace('s', '')
            input_str = input_str.replace('z', '')
        else:
            input_str = []
        return input_str

    manzu = replace_input_str(manzu)
    pinzu = replace_input_str(pinzu)
    souzu = replace_input_str(souzu)
    zihai = replace_input_str(zihai)

    tehai_input = list(tehai_input)

    tehai_list = []
    # 手牌をリストに格納
    for i in manzu:
        tehai_list.append(f'{i}m')
    for i in pinzu:
        tehai_list.append(f'{i}p')
    for i in souzu:
        tehai_list.append(f'{i}s')
    for i in zihai:
        tehai_list.append(f'{i}z')


    while '東' in tehai_input:
        tehai_list.append('1z')
        tehai_input.remove('東')
    while '南' in tehai_input:
        tehai_list.append('2z')
        tehai_input.remove('南')
    while '西' in tehai_input:
        tehai_list.append('3z')
        tehai_input.remove('西')
    while '北' in tehai_input:
        tehai_list.append('4z')
        tehai_input.remove('北')
    while '白' in tehai_input:
        tehai_list.append('5z')
        tehai_input.remove('白')
    while '發' in tehai_input:
        tehai_list.append('6z')
        tehai_input.remove('發')
    while '中' in tehai_input:
        tehai_list.append('7z')
        tehai_input.remove('中')
    while 'x' in tehai_input:
        tehai_list.append('x')
        tehai_input.remove('x')
    while '花' in tehai_input:
        tehai_list.append('x')
        tehai_input.remove('花')
    while '華' in tehai_input:
        tehai_list.append('x')
        tehai_input.remove('華')

    return tehai_list


def handle_agari(tile_deck_instance, tehai_list = []):
    global TULIP

    all_haiyama_num = len(tile_deck_instance.tile_deck)

    total_tip_count_a = 0
    total_tip_count_t = 0
    renchan = 0
    tip_count_dict_a = {}
    tip_count_dict_t = {}


    v_alice = 1
    v_tulip = 1
    while(1):
        all_haiyama_num = len(tile_deck_instance.tile_deck)
        if all_haiyama_num > 0:
            draw_hai1 = tile_deck_instance.draw_tile()
        else:
            break
        
        TULIP = False
        tip_count_a = count_tip(draw_hai1, tehai_list)
        TULIP = True
        tip_count_t = count_tip(draw_hai1, tehai_list)

        if tip_count_a == 0:
            v_alice = 0
        if tip_count_t == 0:
            v_tulip = 0

        if v_alice > 0:
            total_tip_count_a += tip_count_a
        if v_tulip > 0:
            total_tip_count_t += tip_count_t

        renchan += 1
        if v_alice > 0:
            tip_count_dict_a[renchan] = total_tip_count_a
        if v_tulip > 0:
            tip_count_dict_t[renchan] = total_tip_count_t


    # 0連荘のとき　空の辞書を返す
    # n連荘のとき　n連荘のときのチップ枚数を辞書で返す
    return tip_count_dict_a, tip_count_dict_t


def count_tip(draw_hai, tehai_list):
    count_num = 0
    nori_hai = calc_norihai(draw_hai)
    for nori in nori_hai:
        for tehai in tehai_list:
            if nori == tehai:
                count_num += 1

    # print(f'{draw_hai}, {nori_hai}, {tehai_list}, {count_num}')
    return count_num


def calc_norihai(draw_hai):
    nori_hai = []
    if TULIP:
        if draw_hai[-1] in ['p', 's']:
            if int(draw_hai[0])-1 == 0:
                n1 = f'9{draw_hai[-1]}'
            else:
                n1 = f'{int(draw_hai[0])-1}{draw_hai[-1]}'

            n2 = f'{int(draw_hai[0])}{draw_hai[-1]}'

            if int(draw_hai[0])+1 == 10:
                n3 = f'1{draw_hai[-1]}'
            else:
                n3 = f'{int(draw_hai[0])+1}{draw_hai[-1]}'

            nori_hai = [n1, n2, n3]

        elif draw_hai[-1] == 'm':
            if MANZU_COUNT == 'QUASAR':
                if draw_hai == '1m':
                    nori_hai = ['9m', '9m', '1m']
                if draw_hai == '9m':
                    nori_hai = ['9m', '1m', '1m']
            if MANZU_COUNT == 'YUNYUN2':
                    nori_hai = ['1m', '1m', '9m', '9m']
            if MANZU_COUNT == 'YUNYUN3':
                    nori_hai = ['1m', '1m', '1m', '9m', '9m', '9m']


        elif draw_hai[-1] == 'z' and draw_hai[0] in ['1', '2', '3', '4']:
            if draw_hai == '1z':
                nori_hai = ['4z', '1z', '2z']
            elif draw_hai == '2z':
                nori_hai = ['1z', '2z', '3z']
            elif draw_hai == '3z':
                nori_hai = ['2z', '3z', '4z']
            elif draw_hai == '4z':
                nori_hai = ['3z', '4z', '1z']


        elif draw_hai[-1] == 'z' and draw_hai[0] in ['5', '6', '7']:
                nori_hai = ['5z', '6z', '7z']

        elif draw_hai[-1] == 'x':
            nori_hai = ['x', 'x', 'x']

        return nori_hai

    else:
        return [draw_hai]




def main(tehai_input):
    global TULIP

    # tehai_input = TEHAI
    tehai_list = make_tile_list(tehai_input)

    try:
        execlude_tile = EXECLUDE_TILE
        execlude_tile_list = make_tile_list(execlude_tile)
    except:
        print('除外牌指定なし')
        execlude_tile_list = []

    tip_num_dict = {}
    renchan_num_dict = {}
    counters = {}
    result_dfs = []
    max_graph = 0


    for turn in TURN_LIST:
        tip_num_dict[str(turn)+'a'] = []
        tip_num_dict[str(turn)+'t'] = []
        renchan_num_dict[str(turn)+'a'] = []
        renchan_num_dict[str(turn)+'t'] = []
    for _ in tqdm(range(TRY_NUM), leave=False):
        tile_deck_instance = tile_deck(super_bingo = SUPER_BINGO)
        tile_deck_instance.remove_tehai(tehai_list)
        tile_deck_instance.remove_tehai(execlude_tile_list)
        tile_deck_instance.shuffle_tile_deck()

        tip_count_dict_a , tip_count_dict_t = handle_agari(tile_deck_instance, tehai_list)

        for turn in TURN_LIST:

            # t巡目における最大連荘数 = int(62 - t*3) [枚]
            max_renchan_num = int( (62 - turn*3) )
            for i in range(max_renchan_num):
                # 0枚の場合
                if len(tip_count_dict_a) == 0:
                    tip_num_dict[str(turn)+'a'].append(0)
                    renchan_num_dict[str(turn)+'a'].append(0)
                # 1枚以上の場合、考えうる最大連荘数から順に探索
                if max_renchan_num - i in tip_count_dict_a:
                    tip_num_dict[str(turn)+'a'].append(tip_count_dict_a[max_renchan_num - i])
                    renchan_num_dict[str(turn)+'a'].append(max_renchan_num - i)
                    break
            for i in range(max_renchan_num):
                if len(tip_count_dict_t) == 0:
                    tip_num_dict[str(turn)+'t'].append(0)
                    renchan_num_dict[str(turn)+'t'].append(0)
                    break
                if max_renchan_num - i in tip_count_dict_t:
                    tip_num_dict[str(turn)+'t'].append(tip_count_dict_t[max_renchan_num - i])
                    renchan_num_dict[str(turn)+'t'].append(max_renchan_num - i)
                    break

            # print(tip_num_dict[turn])


    for turn in TURN_LIST:

        tip_num_dict[str(turn)+'a'].sort()
        tip_num_dict[str(turn)+'t'].sort()
        counters[str(turn)+'a'] = Counter(tip_num_dict[str(turn)+'a'])
        counters[str(turn)+'t'] = Counter(tip_num_dict[str(turn)+'t'])
        max_graph = max(max(tip_num_dict[str(turn)+'t']), max_graph)

    keys = list(counters.keys())
    for key in keys:
        for i in range(0, max_graph):
            if i not in counters[key]:
                counters[key][i] = 0
        counters[key] = dict(sorted(counters[key].items()))
        # plt.plot(list(counters[key].keys()), [count / sum(counters[key].values()) * 100 for count in counters[key].values()], label=f'turn:{key}', marker='', linestyle='-', linewidth=1)

        # テーブル表示の処理
        pd.options.display.float_format = '{:.3f}'.format
        data = {'tip num': [], 'freq': []}

        data['tip num'].append("0　　")
        data['freq'].append(counters[key][0])

        for i in range(1, max_graph+1, TIP_WIDTH):
            group = f"{i}-　(%)　"
            group_data = [value for value in range(i, i+TIP_WIDTH) if value in counters[key]]
            if i == max_graph:
                group_data = [value for value in range(i, i+99999) if value in counters[key]]

            freq = sum(counters[key].get(value, 0) for value in group_data)
            data['tip num'].append(group)
            data['freq'].append(freq)

        df = pd.DataFrame(data)

        tip_average = sum(tip_num_dict[key]) / TRY_NUM
        renchan_average = sum(renchan_num_dict[key]) / TRY_NUM +1
        df['freq%'] = df['freq'] / TRY_NUM * 100
        df.rename(columns={'freq%': f'turn:{key}'}, inplace=True)

        df = df.set_index('tip num')
        df.loc['平均 (枚)'] = round(tip_average, 3)
        # df.loc['ren'] = round(renchan_average, 1)
        df.loc['継続　(%)'] = round(100 - 100/renchan_average, 3)
        
        df.loc['最大 (枚)'] = max(tip_num_dict[key])
        df.drop('freq', axis=1, inplace=True)
        result_dfs.append(df)

    df_result = pd.concat(result_dfs, axis=1)

    # グラフの装飾
    # plt.xlabel('tip num')
    # plt.ylabel('freq (%)')
    if SUPER_BINGO:
        title = 'SUPER_BINGO'
    else:
        title = 'TULIP & ALICE'
    title_ex = f'{title} / {tehai_input} \n TRY:{TRY_NUM} / V_STOCK:{V_STOCK} / EXECLUDE:{EXECLUDE_TILE}' 
    # plt.title(f'{title} / {tehai_input} \n TRY:{TRY_NUM} / V_STOCK:{V_STOCK} / EXECLUDE:{EXECLUDE_TILE}')
    # plt.legend()  # 凡例を表示


    print(tehai_input)
    print(df_result)


    # グラフを表示
    # plt.show()


if __name__ == "__main__":
    main('234789p123678s477z')
    main('123456789p12344s4z')
