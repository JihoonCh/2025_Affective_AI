import pandas as pd

# 1. 내 파일(비어있는 start, end)
df1 = pd.read_csv('mosi_segments_train.csv')

# 2. 메타데이터 파일(모든 정보가 있는 파일)
df2 = pd.read_csv("/home/ivpl-d27/jhchoi/MISA/CMU_MOSI_p2fa.csv")  # 파일명에 맞게 수정
df2 = df2.dropna(subset=['segment'])
df2['segment'] = df2['segment'].astype(int)

# 혹시 segment가 문자열이면 정수로 변환 (매칭 오류 방지)
df1['segment'] = df1['segment'].astype(int)
df2['segment'] = df2['segment'].astype(int)

# 3. video_id, segment 기준으로 merge
merged = pd.merge(df1, df2[['video_id', 'segment', 'start', 'end']],
                  on=['video_id', 'segment'], how='left', suffixes=('', '_meta'))

# 4. start, end 컬럼 업데이트 (df2에서 가져온 값으로 채우기)
# 만약 df1의 start, end가 비어있으면 df2의 값을 사용
merged['start'] = merged['start_meta']
merged['end'] = merged['end_meta']
merged = merged.drop(columns=['start_meta', 'end_meta'])

# 5. 저장
merged.to_csv('mosi_segments_train_filled.csv', index=False)
print(merged.head())
