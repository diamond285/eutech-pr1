import streamlit as st
import pandas as pd
import sqlite3
from objectivities_tender import funcs, plot, plots
import openai
import json

conn = sqlite3.connect('test2.db')
f1 = pd.read_excel("index 3.xlsx")
f2 = pd.read_excel("index 4.xlsx")
t1 = pd.concat([f1, f2])

search = st.sidebar.text_input("Поиск")
cost = st.sidebar.text_input("Поиск цены по наименованию")
gpt = st.sidebar.text_input("Спроси у ChatGPT (наименование позиции)")

grouppa = st.sidebar.radio("Select group: ", set(t1[t1['Type'] != 'None']['Type']))
saved_group = grouppa


if gpt:
    openai.api_key = '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'
    ans = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": gpt + " вытащи параметры и ГОСТ"},
        ]
    )
    jns = json.loads(str(ans))
    st.header("Вывод параметров по CHAT GPT у " + gpt)
    st.write(jns['choices'][0]['message']['content'])
    d = {}
    for x in jns['choices'][0]['message']['content'].split('-', 1)[1].split('\n\n')[0][:-1].split('\n'):
        if not x: continue
        try:
            col, val = x.replace(';', '').replace('-', '')[1:].split(':', 1)
            val = val[1:]
            d[col] = val
        except Exception as e:
            st.write(str(e))
    st.table(pd.DataFrame([d]))
elif cost:
    st.header(cost)
    plot(st, cost)
elif search:
    st.subheader(f'Поиск по тексту: "{search}"')
    cursor = conn.execute(f"select * from products")
    l = []
    for x in cursor:
        l.append(x)
    l = pd.DataFrame(l)
    tmp = l[l[5].str.lower().str.contains(search.lower())]
    st.table(tmp)
else:
    st.subheader(grouppa)
    l = []
    for x in t1[t1['Type'] == grouppa].iloc:
        l.append(funcs[grouppa](x['Name']))
    df = pd.DataFrame(l)
    df = df.replace('', "Неизвестно")
    options = {}
    for x in df.drop(columns=['name']):
        options[x] = st.multiselect(
            'Выберете ' + x, set(df[x]))
    tdf = df.copy()
    for col in options:
        if not options[col]:
            continue
        sdf = []
        for x in options[col]:
            sdf.append(tdf[tdf[col] == x])
        tdf = pd.concat(sdf)
    st.write(f"Количество {len(tdf)}")
    tdf = tdf.replace('Неизвестно', '-')
    tmp = []
    for x in tdf.iloc:
        v = 0
        for i in x:
            if i == '-':
                v += 1
        tmp.append(v)
    tdf['ncol'] = tmp
    plots(st, set(tdf['name'].str.lower()))
    st.table(tdf.sort_values('ncol').drop(columns=['ncol']))