import streamlit as st
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
ACTIVATION_BYTES = os.getenv("ACTIVATION_BYTES")

st.title("Audible AAX to MP3 Converter")

aax_file_path = st.text_input("Enter full path to your .aax file")

if aax_file_path and st.button("Convert to MP3"):
    if not os.path.exists(aax_file_path):
        st.error("File not found!")
    else:
        base_dir = os.path.dirname(aax_file_path)
        base_name = os.path.splitext(os.path.basename(aax_file_path))[0]
        output_path = os.path.join(base_dir, f"{base_name}.mp3")

        try:
            command = [
                "ffmpeg",
                "-activation_bytes", ACTIVATION_BYTES,
                "-i", aax_file_path,
                "-c:a", "libmp3lame",
                "-b:a", "64k",
                output_path
            ]
            subprocess.run(command, check=True)

            st.success(f"Converted to MP3: {output_path}")
        except subprocess.CalledProcessError as e:
            st.error(f"Conversion failed: {e}")