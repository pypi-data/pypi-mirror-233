import regex as re
from jeraconv import jeraconv
from datetime import date

def convert_hiduke_format(jd):
    min_year = 1700
    current_year = int(date.today().year)

    jd = re.sub('[\s]', '', jd)
    if '年' not in jd:
        return ''
    j2w = jeraconv.J2W()
    full_date = jd
    j_year = str(correct_year(jd))
    j_month = correct_month(jd)
    j_day = correct_day(jd)
    d_year = str(digit_year(jd))
    f_year = str(f_digi(jd))
    print(j_year, d_year, f_year, j_month, j_day)
    if (j_year):
        year = j2w.convert(j_year)
        if min_year < int(year) < current_year:
            return str(year) + '年' + j_month + j_day
        return ''
        # return f' {str(j_month)}{str(j_day)}{str(year)} '
    elif (d_year):
        # year = j2w.convert(d_year)
        if min_year < int(d_year.strip('年')) < current_year:
            return f'{str(d_year)}{str(j_month)}{str(j_day)}'
        return ''
    elif f_year:
        if min_year < int(f_year.strip('年')) < current_year:
            return f'{str(f_year)}{str(j_month)}{str(j_day)}'
        return ''
    else:
        return ''
        # if '年' in str(full_date.strip()):
        #     return str(full_date.strip())
        # else:
        #     return ''


def correct_year(jd):
    year = re.search(r'(明示|明治|大正|昭和|平成|令和|大正元|平成元|明治元)([0-9]*|[０-９]*)(年)', jd)
    if year:
        year = year.group()
    else:
        year = ''
    return str(year).strip()


def digit_year(jd):
    year = re.search(r'([0-9]{4}|[０-９]{4})[年]', jd)
    if year:
        year = year.group()
    else:
        year = ''
    return str(year).strip()


def f_digi(jd):
    year = re.search(r'([0-9]{4}|[０-９]{4})', jd)

    if year:
        year = year.group() + '年'
    else:
        year = ''
    return str(year).strip()


def correct_month(jd):
    month = re.search(r'([0-9]{1,2}|[０-９]{1,2})[月]', jd)
    if month:
        month = month.group()
    else:
        month = ''
    return str(month).strip()


def correct_day(jd):
    day = re.search(r'([0-9]{1,2}|[０-９]{1,2})[日]', jd)
    if day:
        day = day.group()
    else:
        day = ''
    return str(day).strip()

def split_end_date(colString):
    if '日' in colString:
        colString = re.split('日', colString)[0] + '日'
    elif '月' in colString:
        colString = re.split('月', colString)[0] + '月'
    elif '年' in colString:
        colString = re.split('年', colString)[0] + '年'
    return colString