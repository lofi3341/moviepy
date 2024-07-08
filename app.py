import streamlit as st
import moviepy.editor as mp
import tempfile

# 動画から音声を抽出する関数
def extract_audio(video_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        temp_video_path = temp_video.name
    
    clip = mp.VideoFileClip(temp_video_path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        audio_path = temp_audio.name
    clip.audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path

# 音声を挿入する関数
def insert_audio(video_file, audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        temp_video_path = temp_video.name
    
    video_clip = mp.VideoFileClip(temp_video_path)
    audio_clip = mp.AudioFileClip(audio_file)

    final_clip = video_clip.set_audio(audio_clip)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output:
        temp_output_path = temp_output.name
    final_clip.write_videofile(temp_output_path, codec='libx264', audio_codec='aac')
    return temp_output_path

# Streamlitインターフェース
st.title("動画分割・結合・音声挿入アプリ")

uploaded_file = st.file_uploader("動画ファイルをアップロード", type=["mp4", "mov", "avi"])
if uploaded_file:
    st.write("動画がアップロードされました")
    
    try:
        audio_file = extract_audio(uploaded_file)
        st.write("音声が抽出されました")

        # Reset file pointer to the beginning after reading
        uploaded_file.seek(0)

        output_file = insert_audio(uploaded_file, audio_file)
        st.write("音声が挿入されました")
        
        with open(output_file, "rb") as file:
            st.download_button(label="変換された動画をダウンロード", data=file, file_name="output.mp4", mime="video/mp4")
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        st.error("詳細なエラーメッセージはログに記録されています。")