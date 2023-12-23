#libray
import streamlit as st
import pandas as pd
import xmltodict
import requests
import json
from datetime import datetime

#엑셀파일
df = pd.read_excel('your_file.xlsx')

#사용자 선택지 제공
values_1st = df['1단계'].unique().tolist()
selected_1st = st.selectbox('1단계를 선택하세요', values_1st)
values_2nd = df[df['1단계'] == selected_1st]['2단계'].unique().tolist()
selected_2nd = st.selectbox('2단계를 선택하세요', values_2nd)
values_3rd = df[(df['1단계'] == selected_1st) & (df['2단계'] == selected_2nd)]['3단계'].unique().tolist()
selected_3rd = st.selectbox('3단계를 선택하세요', values_3rd)

filtered_df = df[(df['1단계'] == selected_1st) & 
                 (df['2단계'] == selected_2nd) & 
                 (df['3단계'] == selected_3rd)]
st.write(filtered_df[['격자 X', '격자 Y']])

#날씨 조회 API
if not filtered_df.empty:
   x_value = filtered_df['격자 X'].values[0]
   y_value = filtered_df['격자 Y'].values[0]

   now = datetime.now().date()
   tonow = str(now).replace('-','')
   url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
   params ={'serviceKey' : 'your_key', 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'XML', 'base_date' : tonow, 'base_time' : '0500', 'nx' : x_value, 'ny' : y_value }
 
   response = requests.get(url, params=params)
   xmlData = response.text
   json_data = json.dumps(xmltodict.parse(xmlData), indent=4)
   dict = json.loads(json_data)

   result= []
   for item in dict["response"]["body"]["items"]["item"]:
      if item["category"] != "TMP":
        continue
    
      result.append({
               "날짜" : item["fcstDate"][:4] + "년" + item["fcstDate"][4:6] + "월" + item["fcstDate"][6:] + "일",
               "시간대" : item["fcstTime"][:2]+":"+item["fcstTime"][2:],
               "기온" : item["fcstValue"]+"℃"
               })
      
   st.write("전체예보")
   df = pd.DataFrame(result)
   st.table(df)