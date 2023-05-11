import re
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

f1 = pd.read_excel("100.xlsx")

def plots(st, names):
    conn = sqlite3.connect('test2.db')
    joiner = "','"
    cursor = conn.execute(f"select * from products where lower(fullname) IN ('{joiner.join([x.lower() for x in names])}')")
    l = []
    for x in cursor:
        l.append(x)
    t = pd.DataFrame(l)
    cols = ['supplier', 'filial', 'company', 'cost_purchase_order', 'finance_date', 'full_name', 'unit']
    if len(t) == 0:
        st.write("No such product")
        return
    t.columns = cols
    t['finance_date'] = pd.to_datetime(t['finance_date'], format='%Y-%m-%d')
    t = t.groupby('finance_date').mean().reset_index()
    t['period'] = pd.to_datetime(t['finance_date'].dt.strftime('%Y-%m'), format='%Y-%m')
    plt.figure(figsize=(20, 6))
    sns.lineplot(x=t['finance_date'], y=t['cost_purchase_order'])
    plt.xticks(rotation=45);
    st.pyplot(plt)
    conn.close()

def plot(st, names):
    conn = sqlite3.connect('test2.db')
    joiner = "','"
    cursor = conn.execute(f"select * from products where lower(fullname) IN ('{joiner.join(names)}')")
    l = []
    for x in cursor:
        l.append(x)
    t = pd.DataFrame(l)
    cols = ['supplier', 'filial', 'company', 'cost_purchase_order', 'finance_date', 'full_name', 'unit']
    if len(t) == 0:
        st.write("No such product")
        return
    t.columns = cols
    t = t[t['full_name'] == names]
    if t.iloc[0]['unit'] == 'кг':
        unit = st.selectbox(
            'Изменить ед. измерения',
            ('кг', 'т', 'г'))
        if unit == 'кг':
            st.dataframe(t)
        if unit == 'т':
            tmp = t.copy()
            tmp['cost_purchase_order'] = tmp['cost_purchase_order'] * 1000
            tmp['unit'] = 'т'
            st.dataframe(tmp)
            t = tmp
        if unit == 'г':
            tmp = t.copy()
            tmp['cost_purchase_order'] = tmp['cost_purchase_order'] / 1000
            tmp['unit'] = 'г'
            st.dataframe(tmp)
            t = tmp
    else:
        st.dataframe(t)
    t['finance_date'] = pd.to_datetime(t['finance_date'], format='%Y-%m-%d')
    t = t.groupby('finance_date').mean().reset_index()
    t['period'] = pd.to_datetime(t['finance_date'].dt.strftime('%Y-%m'), format='%Y-%m')
    if len(t) < 4:
        st.table(t)
    else:
        per = t.groupby('period').mean().reset_index()
        plt.figure(figsize=(20, 6))
        sns.lineplot(x=t['finance_date'],
                     y=t['cost_purchase_order'])
        sns.lineplot(x=per['period'],
                     y=per['cost_purchase_order'])
        plt.xticks(rotation=45);
        st.pyplot(plt)
    conn.close()

funcs = {}


def benz(val):
    d = {
        "name": val,
        "marka": re.findall(r'АИ[ -]?\d+', val.upper()),
        "talony": 'талон' in val.lower()
    }
    return {x: ''.join(d[x]) if type(d[x]) == list else d[x] for x in d}


funcs['БЕНЗИН'] = benz


def botinki(val):
    d = {"name": val}
    if 'зимние' in val.lower():
        d['type'] = 'зимние'
    if 'летние' in val.lower():
        d['type'] = 'летние'
    if 'женск' in val.lower():
        d['gender'] = 'женские'
    if 'мужск' in val.lower():
        d['gender'] = 'мужские'
    if 'резин' in val.lower():
        d['material'] = 'резина'
    if 'шерст' in val.lower():
        d['material'] = 'шерсть'
    if 'кирз' in val.lower():
        d['material'] = 'кирза'
    if 'кожа' in val.lower():
        d['material'] = 'кожа'
    if 'болот' in val.lower():
        d['type'] = 'болотные'
    if 'жестк' in val.lower():
        d['option'] = 'с жестким подноском'
    return {x: ''.join(d[x]) if type(d[x]) == list else d[x] for x in d}


funcs['БОТИНКИ'] = botinki


def bumaga(val):
    d = {
        "name": val,
        "size": re.findall(r'\d+[.,]?\d*[cс]?[mм]*[*xх]\d+[.,]?\d*[*xх\d]*[.,]?\d*[cс]?[mм]*', val.lower()),
        "gost": re.findall(r'ГОСТ.?[\d\-\.]+', val.upper()),
        "format": re.findall(r'([AА][\s\-]?\d) ', val.upper()),
        "mass": re.findall(r'\d+\s?г[р]?', val.lower()),
        "count": re.findall(r'\d+\s?Л', val.lower()),
    }
    rep = {'шлиф': 'шлифовальная',
           'замет': 'для заметок',
           'фальц': 'фальцованная',
           'ксер': 'для ксерокса',
           'плоттер': 'для плоттера',
           'индик': 'индикаторная',
           'инженер': 'инженерная',
           'масштаб': 'масштабно-координаторная',
           'миллиметр': 'миллиметровая',
           'наждач': 'наждачная',
           'оберт': 'оберточная',
           'офисн': 'офисная',
           'туалет': 'туалетная',
           'фильтр': 'фильтровальная'}
    d['type'] = ''
    for x in rep:
        if x in d['name'].lower():
            d['type'] = rep[x]
    return {x: ''.join(d[x]) if type(d[x]) == list else d[x] for x in d}


funcs['БУМАГА'] = bumaga


def benz(val):
    d = {
        "name": val,
        "marka": re.findall(r'АИ[ -]?\d+', val.upper()),
        "talony": 'талон' in val.lower()
    }
    return {x: ''.join(d[x]) if type(d[x]) == list else d[x] for x in d}


funcs['БЕНЗИН'] = benz


def voda(val):
    d = {
        "name": val,
        "volume": re.findall(r'[\( ](\d{1,2}[м]?\s?[ л])', val.lower()),
        "gaz": 'газир' in val.lower(),
        "pitevaya": 'пить' in val.lower()
    }
    if not d['volume']:
        d['volume'] = re.findall(r'\d{1,2}[.,]\d{0,2}[ л]', val.lower())
    if 'не газ' in val.lower() or 'негаз' in val.lower():
        d["gaz"] = False
    return {x: ''.join([x for x in d[x]]) if type(d[x]) == list else d[x] for x in d}


funcs['ВОДА'] = voda


def vikluchatel(val):
    d = {}
    d['name'] = val
    d['type'] = re.findall('(АП[\s\-]?50)', val.upper())
    if not d['type']:
        d['type'] = re.findall('(АЕ[\s\-]?\d+[\w])', val.upper())
    d['strength'] = re.findall('(\d+[,.]?\d*[AАaа])', val.upper())
    d['pluces'] = re.findall('[\(\)\- ](\d[ ]?[MmМм])', val.upper())
    d['rascipitels'] = re.findall('[\(\)\- ](\d+[ ]?I[HН])', val.upper())
    d['voltage'] = re.findall('[\(\)\- ](\d+[ ]?[ВB])', val.upper())
    return {x: ''.join([x for x in d[x]]) if type(d[x]) == list else d[x] for x in d}


funcs['ВЫКЛЮЧАТЕЛЬ'] = vikluchatel


def diztoplivo(val):
    d = {}
    d['name'] = val
    rep = {'зимн': 'зимнее',
           'летн': 'летнее'}
    d['type'] = ''
    for x in rep:
        if x in d['name'].lower():
            d['type'] = rep[x]
    d['tolon'] = 'талон' in val.lower()
    return {x: ''.join([x for x in d[x]]) if type(d[x]) == list else d[x] for x in d}


funcs['ДИЗТОПЛИВО'] = diztoplivo


def izvest(val):
    d = {}
    d['name'] = val
    rep = {'гаш': 'гашенное',
           'негаш': 'негашенное'}
    d['type'] = ''
    for x in rep:
        if x in d['name'].lower():
            d['type'] = rep[x]
    d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    return {x: ''.join([x for x in d[x]]) if type(d[x]) == list else d[x] for x in d}


funcs['ИЗВЕСТЬ'] = izvest


def cable(val):
    d = {}
    d['name'] = val
    rep = {x.lower(): x for x in set(f1[f1['title'] == 'КАБЕЛЬ']['full_name'].str.split().str[0])}
    d['type'] = ''
    for x in rep:
        if x in d['name'].lower():
            d['type'] = rep[x]
    d['size'] = re.findall(r'(\d+[*xх][\d+xх*]+)', val.lower())
    d['ozh'] = re.findall(r'ож.{0,3}([\d,.]+)', val.lower())
    d['power'] = re.findall(r'([\d,.]+)КВ', val.lower())
    return {x: ''.join([x for x in d[x]]) if type(d[x]) == list else d[x] for x in d}


funcs['КАБЕЛЬ'] = cable


def calculator(val):
    d = {}
    d['name'] = val
    d['razryadnost'] = re.findall('(\d+)\s?р', val.lower())
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['КАЛЬКУЛЯТОР'] = calculator


def costume(val):
    d = {}
    d['name'] = val
    d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['КОСТЮМ'] = costume


def kurtka(val):
    d = {}
    d['name'] = val
    rep = {'зимн': 'зимняя',
           'летн': 'летнzz'}
    d['type'] = ''
    for x in rep:
        if x in d['name'].lower():
            d['type'] = rep[x]
    d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['КУРТКА'] = kurtka


def lamp(val):
    d = {}
    d['name'] = val
    d['power'] = re.findall(r'(\d+[ ]?)ВТ', val.upper())
    if not d['power']: d['power'] = re.findall(r'ДРЛ[ -]?(\d+)', val.upper())
    if not d['power']: d['power'] = re.findall(r'(\d+[ ]?)W', val.upper())
    if not d['power']: d['power'] = re.findall(r'ДНАТ[ -]?(\d+)', val.upper())
    d['diameter'] = re.findall('[EЕ](\d+)', val.upper())
    d['voltage'] = re.findall('(\d+)[ \-]?[ВBV][ \)\(\-]', val.upper())
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['ЛАМПА'] = lamp


def costume(val):
    d = {}
    d['name'] = val
    d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['КОСТЮМ'] = costume


def lisst(val):
    d = {}
    d['name'] = val
    d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    d['size'] = re.findall(r'(\d+[*xх][\d+xх*]+)', val.lower())
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['ЛИСТ'] = lisst


def maslo(val):
    d = {}
    d['name'] = val
    d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    rep = {'турб': 'турбинное',
           'трансмисс': 'трансмиссионное',
           'моторн': 'моторное'}
    d['type'] = ''
    d['ТП'] = re.findall(r'ТП.?[\d\-\.]+', val.upper())
    for x in rep:
        if x in d['name'].lower():
            d['type'] = rep[x]
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['МАСЛО'] = maslo


def moloko(val):
    d = {}
    d['name'] = val
    d['zhir'] = re.findall(r'(\d+[,\.]*\d*%)', val.upper())
    d['volume'] = re.findall(r'(0[,\.][45]5?)', val.lower())
    if not d['volume']: d['volume'] = re.findall(r'\d+[ \-]?л', val.lower())
    if not d['volume']: d['volume'] = re.findall(r'\d+[ \-]?гр', val.lower())
    if not d['volume']: d['volume'] = re.findall(r'\d+[ \-]?мл', val.lower())
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['МОЛОКО'] = moloko


def mylo(val):
    d = {}
    d['name'] = val
    d['zhir'] = re.findall(r'(\d+[,\.]*\d*)%', val.upper())
    if not d['zhir']: d['zhir'] = re.findall(r'([76][502])', val.upper())
    d['volume'] = re.findall(r'(0[,\.][45]5?)', val.lower())
    if not d['volume']: d['volume'] = re.findall(r'\d+[ \-]?л', val.lower())
    if not d['volume']: d['volume'] = re.findall(r'\d+[ \-]?гр', val.lower())
    if not d['volume']: d['volume'] = re.findall(r'\d+[ \-]?мл', val.lower())
    rep = {'хозяй': 'хозяйственное',
           'жидко': 'жидкое',
           'туалет': 'туалетное'}
    d['type'] = ''
    for x in rep:
        if x in d['name'].lower():
            d['type'] = rep[x]
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['МЫЛО'] = mylo


def perchatki(val):
    d = {}
    d['name'] = val
    d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    rep = {'диэлектр': 'диэлектрические',
           'хлопчатобумажн': 'хлопчатобумажные',
           'латекс': 'латексные',
           'медицинс': 'медицинские',
           'резин': 'резиновые',
           'термостойкие': 'термостойкие',
           'свар': 'сварщика',
           'спилко': 'спилковые',
           'стериль': 'стерильные',
           'мультитекс': 'мультитекс'}
    d['type'] = ''
    for x in rep:
        if x in d['name'].lower():
            d['type'] = rep[x]
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['ПЕРЧАТКИ'] = perchatki


def podshipnik(val):
    d = {}
    d['name'] = val
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['ПОДШИПНИК'] = podshipnik


def rukavici(val):
    d = {}
    d['name'] = val
    d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    rep = {'диэлектр': 'диэлектрические',
           'хлопчатобумажн': 'хлопчатобумажные',
           'х/б': 'хлопчатобумажные',
           'латекс': 'латексные',
           'медицинс': 'медицинские',
           'резин': 'резиновые',
           'термостойкие': 'термостойкие',
           'свар': 'сварщика',
           'спилко': 'спилковые',
           'стериль': 'стерильные',
           'мультитекс': 'мультитекс',
           'брезент': 'c брезентовым наладонником',
           'утеплен': 'утепленные',
           'маслост': 'маслостойкие'}
    d['type'] = ''
    for x in rep:
        if x in d['name'].lower():
            d['type'] = rep[x]
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['РУКАВИЦЫ'] = rukavici


def soda(val):
    d = {}
    d['name'] = val
    d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    rep = {'каустич': 'каустическая',
           'кальцинир': 'кальцинированная'}
    d['type'] = ''
    for x in rep:
        if x in d['name'].lower():
            d['type'] = rep[x]
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['СОДА'] = soda


def sol(val):
    d = {}
    d['name'] = val
    d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    rep = {'техничес': 'техническая',
           'динатрие': 'динатриевая',
           'таблетирован': 'таблетированная',
           'гипохлорита кальция': 'гипохлорита кальция',
           'мора': 'соль Мора'}
    d['type'] = ''
    for x in rep:
        if x in d['name'].lower():
            d['type'] = rep[x]
    return {x: ''.join([x for x in d[x][:1]]) if type(d[x]) == list else d[x] for x in d}


funcs['СОЛЬ'] = sol


def truba(val):
    d = {}
    d['name'] = val
    d['size'] = re.findall(r'(\d+\s?[*xх]\s?[\d+xх*]+)', val.lower())
    d['diameter'] = re.findall(r'[dдØф][\s\.\-]?(\d+[.,]?\d+)', val.lower())
    d['material'] = re.findall(r'[ \(\)][cс][tт].?[0-9а-яА-Яa-zA-Z]+', val.lower())
    d['gost'] = re.findall(r'[ -?]ТУ.?[\d\-\.A-ZА-Я]+', val.upper())
    if not d['gost']: d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    return {x: ''.join([x for x in d[x]]) if type(d[x]) == list else d[x] for x in d}


funcs['ТРУБА'] = truba


def udolok(val):
    d = {}
    d['name'] = val
    d['size'] = ''.join(re.findall(r'(\d+\s?[*xх]\s?[\d+xх*]+)', val.lower()))
    if d['size']:
        d['size'] = d['size'].replace('x', '*').replace('х', '*').replace(' ', '*')
        l = sorted([int(x) for x in d['size'].split('*')])
        if l[0] < l[1]:
            l.append(l.pop(0))
        d['size'] = '*'.join([str(x) for x in l])
    d['material'] = re.findall(r'[ \(\)][cс][tт].?[0-9а-яА-Яa-zA-Z]+', val.lower())
    d['gost'] = re.findall(r'[ -?]ТУ.?[\d\-\.A-ZА-Я]+', val.upper())
    if not d['gost']: d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    return {x: ''.join([x for x in d[x]]) if type(d[x]) == list else d[x] for x in d}


funcs['УГОЛОК'] = udolok


def shar(val):
    d = {}
    d['name'] = val
    d['diameter'] = re.findall(r'[dдØф][\s\.\-]?[\s]?(\d+[.,]?\d+)', val.lower())
    d['gost'] = re.findall(r'[ -?]ТУ.?[\d\-\.A-ZА-Я]+', val.upper())
    if not d['gost']: d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    return {x: ''.join([x for x in d[x]]) if type(d[x]) == list else d[x] for x in d}


funcs['ШАР'] = shar


def electrod(val):
    d = {}
    d['name'] = val
    d['diameter'] = re.findall(r'[dдØф][\=\s\.\-]?[\s]?\d+[.,]?\d*', val.lower())
    d['gost'] = re.findall(r'[ -?]ТУ.?[\d\-\.A-ZА-Я]+', val.upper())
    if not d['gost']: d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    return {x: ''.join([x for x in d[x]]) if type(d[x]) == list else d[x] for x in d}


funcs['ЭЛЕКТРОД'] = electrod


def emal(val):
    d = {}
    d['name'] = val
    d['type'] = re.findall(r'НЦ.?[\d\-\.]+', val.upper())
    if not d['type']: d['type'] = re.findall(r'ПФ.?[\d\-\.]+', val.upper())
    if not d['type']: d['type'] = re.findall(r'ХВ.?[\d\-\.]*', val.upper())
    d['gost'] = re.findall(r'ГОСТ.?[\d\-\.]+', val.upper())
    # d['asd'] = val.upper()\
    #               .replace(''.join([x for x in d['type']]), '')\
    #               .replace(''.join([x for x in d['gost']]), '')\
    #               .replace('ЭМАЛЬ', '').replace(';', '').strip()
    d['color'] = re.findall(r'[а-я]+ий', val.lower())
    if not d['color']: d['color'] = re.findall(r'[а-я]+ая', val.lower())
    if not d['color']: d['color'] = re.findall(r'[а-я]+яя', val.lower())
    if not d['color']: d['color'] = re.findall(r'[а-я]+ый', val.lower())
    return {x: ', '.join([x for x in d[x]]) if type(d[x]) == list else d[x] for x in d}


funcs['ЭМАЛЬ'] = emal
