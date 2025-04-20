import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

ACTIVATION_BYTES = os.getenv("ACTIVATION_BYTES")

def convert_aax_to_mp3(input_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_folder, f"{file_name}.mp3")

    command = [
        "ffmpeg",
        "-activation_bytes", ACTIVATION_BYTES,
        "-i", input_path,
        "-c:a", "libmp3lame",
        "-b:a", "64k",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        return f"Conversion successful: {output_path}"
    except subprocess.CalledProcessError as e:
        return f"Error: {str(e)}"