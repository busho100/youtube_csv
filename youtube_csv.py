import requests
import pandas as pd
import config  # 設定ファイルをインポート

# 設定ファイルからAPIキーを取得
api_key = config.YOUTUBE_API_KEY
search_query = '燻製料理'  # ここに検索したいキーワードを入力してください。
max_results = 50  # 最大取得結果数

# YouTube Data APIで動画IDを検索
search_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={search_query}&maxResults={max_results}&key={api_key}'
search_response = requests.get(search_url)
search_results = search_response.json()

# 動画IDのリストを作成
video_ids = ','.join([item['id']['videoId'] for item in search_results.get('items', [])])

# 各動画の詳細情報（評価数や再生回数を含む）を取得
video_details_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_ids}&key={api_key}'
video_details_response = requests.get(video_details_url)
video_details = video_details_response.json()

# 各動画の情報をリストに格納
video_data = []
for video in video_details.get('items', []):
    title = video['snippet']['title']
    view_count = int(video['statistics'].get('viewCount', 0))  # 再生回数を整数に変換
    like_count = int(video['statistics'].get('likeCount', 0))  # 高評価数を整数に変換
    published_at = video['snippet']['publishedAt']
    video_url = f'https://www.youtube.com/watch?v={video["id"]}'
    
    # サムネイルURLの取得、存在しない場合は空欄
    thumbnail_url = video['snippet']['thumbnails'].get('default', {}).get('url', '')

    video_data.append([title, view_count, like_count, published_at, video_url, thumbnail_url])

# データフレームを作成し、高評価数の多い順に並べ替え
df = pd.DataFrame(video_data, columns=['動画タイトル', '再生回数', '高評価数', '投稿日', 'URL', 'サムネイルURL'])
df = df.sort_values(by='高評価数', ascending=False)

# 並べ替えたデータをCSVとして保存
df.to_csv('youtube_videos_with_ratings_and_thumbnails_sorted.csv', index=False, encoding='utf-8-sig')

print("高評価数の多い順に並べ替えた動画情報がCSVファイルに保存されました。")
