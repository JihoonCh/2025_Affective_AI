import csv
import pickle
import re

# train.pkl 파일 경로
file_path = "/mnt/HDD/CMU_MOSI/train.pkl"

# 파일 로드
with open(file_path, 'rb') as f:
    data = pickle.load(f)

def parse_sample_info(sample):
    # 딕셔너리 구조
    if isinstance(sample, dict):
        video_id = sample.get('video_id') or sample.get('video')
        segment = sample.get('segment')
        start = sample.get('start')
        end = sample.get('end')
    # 튜플/리스트 구조 (샘플 ID가 마지막 요소에 문자열로 포함)
    elif isinstance(sample, (tuple, list)):
        sample_id = sample[-1] if len(sample) > 0 else None
        video_id, segment = None, None
        if sample_id and isinstance(sample_id, str):
            m = re.match(r'([a-zA-Z0-9_-]+)\[(\d+)\]', sample_id)
            if m:
                video_id = m.group(1)
                segment = int(m.group(2))
        # start, end는 tuple/list에는 없을 수 있으므로 None 처리
        start, end = None, None
    else:
        video_id, segment, start, end = None, None, None, None
    return video_id, segment, start, end

# 전체 샘플에 대해 정보 추출
parsed_info = [parse_sample_info(sample) for sample in data]

# 예시: 첫 5개만 출력
for info in parsed_info[:5]:
    print(info)

with open('../mosi_segments_train.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['video_id', 'segment', 'start', 'end'])
    for row in parsed_info:
        video_id, segment, start, end = row
        # segment가 None이 아니면 1부터 시작하도록 +1
        if segment is not None:
            segment_out = segment + 1
        else:
            segment_out = ''
        writer.writerow([video_id, segment_out, start, end])