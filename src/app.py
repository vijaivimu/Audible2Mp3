import streamlit as st
import subprocess
import os
import json
from dotenv import load_dotenv

load_dotenv()
ACTIVATION_BYTES = os.getenv("ACTIVATION_BYTES")

def extract_chapters(aax_file):
    result = subprocess.run([
        "ffprobe",
        "-activation_bytes", ACTIVATION_BYTES,
        "-print_format", "json",
        "-show_chapters",
        "-i", aax_file
    ], capture_output=True, text=True)

    return json.loads(result.stdout).get("chapters", [])

def convert_chapter(aax_file, start, end, title, index, output_dir):
    output_file = os.path.join(output_dir, f"{index:02d}_{title}.mp3")
    cmd = [
        "ffmpeg",
        "-activation_bytes", ACTIVATION_BYTES,
        "-i", aax_file,
        "-ss", str(start),
        "-to", str(end),
        "-c:a", "libmp3lame",
        "-b:a", "64k",
        "-y",
        output_file
    ]
    subprocess.run(cmd, check=True)
    return output_file

st.title("AAX to MP3 Splitter (Chapter-wise)")

aax_file_path = st.text_input("Enter full path to your .aax file")

if aax_file_path and st.button("Split by Chapters"):
    if not os.path.exists(aax_file_path):
        st.error("File not found!")
    else:
        with st.spinner("Extracting chapters..."):
            chapters = extract_chapters(aax_file_path)
        
        if not chapters:
            st.warning("No chapters found in the AAX file.")
        else:
            output_dir = os.path.splitext(aax_file_path)[0] + "_chapters"
            os.makedirs(output_dir, exist_ok=True)

            with st.spinner("Splitting..."):
                for i, chapter in enumerate(chapters):
                    start = float(chapter['start_time'])
                    end = float(chapter['end_time'])
                    title = chapter.get('tags', {}).get('title', f"chapter_{i+1}").replace(" ", "_")
                    try:
                        convert_chapter(aax_file_path, start, end, title, i+1, output_dir)
                    except subprocess.CalledProcessError:
                        st.error(f"Error converting chapter {title}")
            
            st.success(f"Chapters saved in: {output_dir}")