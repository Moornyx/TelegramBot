import youtube_dl

def get_latest_video_info(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'extractor_args': {'force_generic_extractor': True},
        'simulate': True,
        'format': 'best',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(channel_url, download=False)
        if 'entries' in info_dict:
            latest_video = info_dict['entries'][0]
            video_link = latest_video['url']
            video_title = latest_video.get('title', 'Название видео не найдено')
            return video_title, video_link
        else:
            return None, None

def main():
    channel_url = 'https://www.youtube.com/@moornyx/videos'
    latest_video_title, latest_video_link = get_latest_video_info(channel_url)
    if latest_video_title and latest_video_link:
        print('Название последнего видео:', latest_video_title)
        print('Ссылка на последнее видео:', latest_video_link)
    else:
        print('Не удалось найти последнее видео')

if __name__ == "__main__":
    main()
