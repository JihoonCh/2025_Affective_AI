import pandas as pd
import os

def seconds_to_hms(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"

df = pd.read_csv('mosi_segments_test_filled.csv')

save_dir= "/mnt/HDD/CMU_MOSI/raw_data/"
for idx, row in df.iterrows():
    video_id = row['video_id']
    segment = row['segment']
    start = seconds_to_hms(row['start'])
    end = seconds_to_hms(row['end'])
    url = f"https://www.youtube.com/watch?v={video_id}"
    section = f"*{start}-{end}"
    output_name = os.path.join(save_dir, f"{video_id}_seg{segment}.mp4")
    cmd = f'yt-dlp --download-sections "{section}" "{url}" -o "{output_name}"'
    print(cmd)
    os.system(cmd)  # 실제 다운로드 실행(테스트 후 주석 해제)
