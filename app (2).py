
import streamlit as st
import yt_dlp
from PIL import Image
import requests
from io import BytesIO
import os

st.set_page_config(page_title="Music & Video Downloader", page_icon="🎧")

st.title("🎧 Music & Video Downloader")
st.markdown("Paste a YouTube URL and download video or audio, with image too!")

url = st.text_input("Enter YouTube Video URL")

# Directory to store downloads
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

if url:
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            title = info.get('title')
            thumbnail_url = info.get('thumbnail')
            st.success(f"Found: **{title}**")
            if thumbnail_url:
                response = requests.get(thumbnail_url)
                img = Image.open(BytesIO(response.content))
                st.image(img, caption="Thumbnail", use_column_width=True)

            format_choice = st.radio("Select format", ['Original Audio (.webm)', 'MP4 Video (progressive)', 'Image only'])

            if st.button("Download"):
                if format_choice == 'Original Audio (.webm)':
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(download_dir, f'{title}.webm'),
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    st.success("Audio downloaded successfully!")
                    st.audio(os.path.join(download_dir, f'{title}.webm'))

                elif format_choice == 'MP4 Video (progressive)':
                    ydl_opts = {
                        'format': '18',  # mp4 format with both audio and video (progressive)
                        'outtmpl': os.path.join(download_dir, f'{title}.mp4'),
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    st.success("Video downloaded successfully!")
                    st.video(os.path.join(download_dir, f'{title}.mp4'))

                elif format_choice == 'Image only':
                    image_path = os.path.join(download_dir, f'{title}_thumbnail.jpg')
                    img.save(image_path)
                    st.success("Thumbnail image saved!")
                    st.image(image_path, caption="Saved Thumbnail")

        except Exception as e:
            st.error(f"Error: {e}")
