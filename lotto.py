import requests
import pandas as pd

# 먼저 기존 CSV 파일을 불러오기 (만약 파일이 없으면 새롭게 생성 후 저장)
try:
    lotto_df = pd.read_csv('lotto_numbers.csv', index_col=0, encoding='utf-8-sig')
except FileNotFoundError:
    lotto_df = pd.DataFrame()
    lotto_df.to_csv('lotto_numbers.csv', encoding='utf-8-sig')




# 1회차부터 1126회차까지 반복
for drwNo in range(0,1126):
    url = f"http://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}"
    response = requests.get(url)
    
    # 데이터를 저장할 빈 리스트 생성
    draw_dates = []
    winning_numbers = {
        '1st': [],
        '2nd': [],
        '3rd': [],
        '4th': [],
        '5th': [],
        '6th': [],
        'bonus': [],
        'firstPrzwnerCo': [],  #1등 당첨 인원
        'firstWinamnt' :[], # 1등 상금액
        'totSellamnt' : [] # 총 상금액     
        }


    if response.status_code == 200:
        data = response.json()
        
        # 회차 추가
        draw_dates.append(data['drwNoDate'])
        
        # 당첨번호 추가
        winning_numbers['1st'].append(data['drwtNo1'])
        winning_numbers['2nd'].append(data['drwtNo2'])
        winning_numbers['3rd'].append(data['drwtNo3'])
        winning_numbers['4th'].append(data['drwtNo4'])
        winning_numbers['5th'].append(data['drwtNo5'])
        winning_numbers['6th'].append(data['drwtNo6'])
        winning_numbers['bonus'].append(data['bnusNo'])
        winning_numbers['firstPrzwnerCo'].append(data['firstPrzwnerCo'])
        winning_numbers['firstWinamnt'].append(data['firstWinamnt'])
        winning_numbers['totSellamnt'].append(data['totSellamnt'])
        
        # 새로운 데이터 프레임 생성
        new_data = pd.DataFrame(winning_numbers, index=draw_dates)
        lotto_df = pd.concat([lotto_df, new_data])

        # CSV 파일로 저장
        lotto_df.to_csv('lotto_numbers.csv', encoding='utf-8-sig')

        print(f"{drwNo}회차 데이터 수집 완료")
        
    else:
        print(f"{drwNo}회차 데이터 요청 실패")
