import json, os, subprocess
from lib.get_translation import get_translation
from datetime import datetime

import logging
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'
)

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
FFMPEG_PATH = "lib/ffmpeg-master-latest-win64-gpl"
APP_CODE = os.getenv("APP_CODE")

# ass文件头，包含字幕格式定义等
ASS_FILE_HEAD = """[Script Info]
Title: Meeting Subtitles
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,36,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,2,1,2,40,40,40,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def read_config(path_to_config:str)->dict:
    with open(path_to_config, "r", encoding='utf-8')as fp:
        config = json.load(fp)
    if "vtt_path" not in config:
        for item in os.listdir(os.path.join(THIS_PATH,"files")):
            if item.lower().endswith(".vtt"):
                config["vtt_path"] = item
        if "vtt_path" not in config:
            raise Exception("No vtt file!")
    if "video_path" not in config:
        for item in os.listdir(os.path.join(THIS_PATH,"files")):
            if item.lower().endswith(".mp4"):
                config["video_path"] = item
        if "video_path" not in config:
            raise Exception("No video mp4 file!")
    logging.info("Read config success!")
    return config

def decode_vtt(vtt:str)->str:
    content = {
        "starts":[],
        "ends":[],
        "speakers":[],
        "texts": []
    }
    start, end, speaker, text = "", "", "", ""
    for line in vtt.split("\n"):
        if " --> " in line:
            start, end = line.split(" --> ")
            start = start.strip()
            end = end.strip()
        
        if line.startswith("<v"):
            speaker = line[3:line.find('>')]
            text += line[line.find('>')+1: line.find("</v>")]
        
        if line.endswith("</v>"):
            if not line.startswith("<v"):
                text += "\\N"
                text += line[:line.find("</v>")]
            content["starts"].append(start)
            content["ends"].append(end)
            content["speakers"].append(speaker)
            content["texts"].append(text)
            start, end, speaker, text = "", "", "", ""
    logging.info("Decode vtt success!")
    return content 

def time_format(hh_mm_ss_cs:str)->str:
    dt = datetime.strptime(hh_mm_ss_cs, "%H:%M:%S.%f")
    cs = round(dt.microsecond / 10000)
    return f"{dt.hour}:{dt.minute:02}:{dt.second:02}.{cs:02}"

def process_vtt_to_ass(config:dict):
    with open(config["vtt_path"], "r", encoding='utf-8')as fp:
        vtt_text = fp.read()
        vtt_content = decode_vtt(vtt_text)
    logging.info("Start getting translation...")
    vtt_content["translated_texts"] = get_translation(vtt_content["texts"], APP_CODE) #使用第三方封装的google translate接口，1000次/10￥
    logging.info("Get translation success!")
    ass_content_head = ASS_FILE_HEAD
    for i in range(len(vtt_content["translated_texts"])):
        start = vtt_content["starts"][i]
        end = vtt_content["ends"][i]
        speaker = vtt_content["speakers"][i]
        translated_text = vtt_content["translated_texts"][i]
        line = f"Dialogue: 0,{time_format(start)},{time_format(end)},Default,{speaker.replace(",", " ")},0,0,0,,{translated_text}\n"
        ass_content_head += line
    return ass_content_head

def process():
    config = read_config(os.path.join(THIS_PATH, "config.json"))
    ass = process_vtt_to_ass(config)
    vtt_path:str = config["vtt_path"]
    ass_path:str = vtt_path.replace(".vtt",".ass")
    with open(ass_path, "w", encoding='utf-8')as fp:
        fp.write(ass)
    video_path:str = os.path.realpath(config["video_path"])
    video_out_path = os.path.realpath(os.path.join(os.path.dirname(video_path), "[EN]" + os.path.basename(video_path)))
    ffmpeg_exe_path = os.path.realpath(os.path.join(THIS_PATH, os.path.join(FFMPEG_PATH, "bin/ffmpeg.exe")))
    cmd = [
        ffmpeg_exe_path,
        "-i", video_path,
        "-vf", f"ass={ass_path}",
        "-c:v", config["encoder"],
        "-crf", config["quality_crf"],
        "-preset", "slow",
        "-c:a", "copy",
        video_out_path
    ]
    logging.debug(cmd)
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    process()