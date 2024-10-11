import pandas as pd

df_excel = pd.read_excel('test.xlsx')
df = pd.DataFrame(df_excel.head())
pop_kor = pd.read_csv('pop_kor.csv')

city_df = pd.DataFrame({
    '서대문서': ['서대문구'], '수서서': ['강남구'], '강서서': ['강서구'], '서초서': ['서초구'], '서부서': ['은평구'], 
    '중부서': ['중구'], '종로서': ['종로구'], '남대문서': ['중구'], '혜화서': ['종로구'], '용산서': ['용산구'], 
    '성북서': ['성북구'], '동대문서': ['동대문구'], '마포서': ['마포구'], '영등포서': ['영등포구'], 
    '성동서': ['성동구'], '동작서': ['동작구'], '광진서': ['광진구'], '강북서': ['강북구'], '금천서': ['금천구'], 
    '중랑서': ['중랑구'], '강남서': ['강남구'], '관악서': ['관악구'], '강동서': ['강동구'], '종암서': ['성북구'], 
    '구로서': ['구로구'], '양천서': ['양천구'], '송파서': ['송파구'], '노원서': ['노원구'], '방배서': ['서초구'], 
    '은평서': ['은평구'], '도봉서': ['도봉구']
}).transpose().reset_index()

city_df.columns = ['관서명', '구별']

df_merged = pd.merge(df_excel, city_df, on='관서명', how='left')

# df_merged['구별'] = df_merged['구별'].fillna('구없음') / pivot.drop(['구없음'])
df_merged = df_merged.dropna(subset=['구별'])

df_merged['강간검거율'] = (df_merged['강간(검거)'] / df_merged['강간(발생)']) * 100
df_merged['강도검거율'] = (df_merged['강도(검거)'] / df_merged['강도(발생)']) * 100
df_merged['살인검거율'] = (df_merged['살인(검거)'] / df_merged['살인(발생)']) * 100
df_merged['절도검거율'] = (df_merged['절도(검거)'] / df_merged['절도(발생)']) * 100
df_merged['폭력검거율'] = (df_merged['폭력(검거)'] / df_merged['폭력(발생)']) * 100
df_merged['검거율'] = (df_merged['소계(검거)'] / df_merged['소계(발생)']) * 100

pivot = pd.pivot_table(
    df_merged,
    index='구별',
    values=['강간(발생)', '강도(발생)', '살인(발생)', '절도(발생)', '폭력(발생)', 
            '강간검거율', '강도검거율', '살인검거율', '절도검거율', '폭력검거율', '검거율'],
    aggfunc='mean' 
)
pop_pivot = pop_kor.set_index('구별').join(pivot)
pop_pivot = pop_pivot.reindex(columns=['강간(발생)', '강도(발생)', '살인(발생)', '절도(발생)', '폭력(발생)', '강간검거율', '강도검거율', '살인검거율', '절도검거율'	,'폭력검거율' ,'검거율', '인구수'])
pop_pivot = pop_pivot.rename(columns={'강간(발생)':'강간', '강도(발생)':'강도', '살인(발생)':'살인', '절도(발생)':'절도', '폭력(발생)':'폭력'}) 
pop_pivot = pop_pivot.sort_values('검거율', ascending=True)
print(pop_pivot)
