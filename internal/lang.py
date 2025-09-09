import langdetect
from langdetect import DetectorFactory
# Ensure stable output
DetectorFactory.seed = 0

def detect(text: str) -> str:
    print(langdetect.detect_langs(text))
    return langdetect.detect(text)
