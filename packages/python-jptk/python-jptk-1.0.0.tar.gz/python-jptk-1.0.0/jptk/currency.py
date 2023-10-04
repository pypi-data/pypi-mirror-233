import regex as re
import pandas as pd

def convert_kanji_to_numbers(kanji):
    if pd.isna(kanji):
        return ''
    kanji = re.findall(r'[0-9|０-９]|一兆|十億|一億|千万|百万|十万|兆|億|万|千|百|十|円', str(kanji))
    UNITS = {
        '円': 1,
        '十': 10,
        '百': 100,
        '千': 1000
    }

    MULTIPLES = {
        '万': 10000,
        '億': 100000000,
        '兆': 1000000000000
    }

    SUB_SET = {
        '十万': 100000,
        '百万': 1000000,
        '千万': 10000000,
        '一億': 100000000,
        '十億': 1000000000,
        '一兆': 10000000000,
    }
    digit = ''
    total = []
    for index, kan in enumerate(kanji):
        if kan.isdigit():
            digit += str(kan)
        elif kan == '円':
            if digit != "":
                total.append(float(digit))
                digit = ''
            break
        else:
            if kan in UNITS.keys():
                if kanji[index + 1] == '円':
                    total.append(float(digit or 1) * int(UNITS[kan]))
                else:
                    total.append(float(digit or 1) * int(UNITS[kan]) * MULTIPLES['万'])
                digit = ''
            elif kan in MULTIPLES.keys():
                total.append(float(digit or 1) * MULTIPLES[kan])
                digit = ''
            elif kan in SUB_SET:
                total.append(float(digit or 1) * SUB_SET[kan])
                digit = ''
            else:
                digit = ''
                continue
    if total is not None:
        if len(digit) != 0:
            return "{:,}".format(int(float(digit)))
        return "{:,}".format(int(sum(total)))
    else:
        return ''