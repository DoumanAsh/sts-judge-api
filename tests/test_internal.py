from internal import lang
from internal.core import ST

def test_lang_detection():
    assert lang.detect("猫好き") == "ja"
    assert lang.detect("Я люблю котят") == "ru"

def test_similarity():
    model = ST("Gameselo/STS-multilingual-mpnet-base-v2")
    result = model.determine_similarity("I like cat", ["I love cat", "猫好き", "я люблю котят"])
    assert result == [[0.85, 0.91, 0.85]]
    result = model.determine_similarity("ありうがとう", ["誠にありがとうございます", "あんがとう", "ありがとうございます", "おおきに"])
    assert result == [[0.68, 0.89, 0.72, 0.76]]
