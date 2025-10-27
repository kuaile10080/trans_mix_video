# 📌 Project: Translate Transcript and Merge Video

## 📝 Project Description

This Python project automates the translation of `.vtt` subtitle files using the Google Translate API. It converts the translated subtitles into `.ass` format and optionally merges them with a video file to produce a new `.mp4` video with embedded subtitles.

---

## ⚙️ Features

- Translates `.vtt` subtitle files to a target language using Google Translate.
- Converts translated subtitles to `.ass` format.
- Optionally merges the `.ass` subtitles with a video file and compresses it into a new `.mp4`.
- Configurable via a simple `config.json` file.

---

## 📁 Configuration File (`config.json`)

Example configuration:
```json
{
  "vtt_path": "./files/example.vtt",     // Path to the input VTT subtitle file
  "src": "zh",                           // Source language code
  "dst": "en",                           // Target language code
  "merge": true,                         // Whether to merge subtitles with video
  "video_path": "./files/example.mp4",   // Path to the video file (required if merge is true)
  "encoder": "libx264",                  // Video encoder (recommended to keep default)
  "quality_crf": "23"                    // Compression quality (recommended to keep default)
}
```

## 🚀 Usage

1. **Install dependencies**:
   ```bash
   pip install requests
   ```

2. **Download ffmpeg**, preferably the [Windows 64-bit GPL version](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip). Do not choose the shared build. Then, set the FFMPEG_PATH variable in main.py to the path where FFmpeg is installed.


3. **Create a `.env` file** in the project root directory and add your API key:
   ```
   APP_CODE=your_appcode_here
   ```

4. **Prepare your `config.json`** file with the required fields (see Configuration section).

5. **Run the program**:
   ```bash
   python main.py
   ```

Make sure the paths in your `config.json` are correct and that the video file exists if `merge` is set to `true`.