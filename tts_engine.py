from gtts import gTTS
import tempfile
import hashlib
import os


# =========================
# 🧠 CACHE DIR
# =========================
CACHE_DIR = "tts_cache"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


# =========================
# 🔊 MAIN FUNCTION
# =========================
def speak_text(text, lang="en"):

    if not text:
        return None

    try:
        # 🔥 Create hash for caching
        text_hash = hashlib.md5(text.encode()).hexdigest()
        file_path = os.path.join(CACHE_DIR, f"{text_hash}.mp3")

        # ✅ If already exists → reuse
        if os.path.exists(file_path):
            return file_path

        # 🎙 Generate audio
        tts = gTTS(text=text, lang=lang)
        tts.save(file_path)

        return file_path

    except Exception as e:
        # 🛡️ FAIL SAFE (important for demo)
        return None