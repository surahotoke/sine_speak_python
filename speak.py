import numpy as np
import sounddevice as sd

# 音声データ（dB, Hz）
phonemes = {
    'あ': [[-39, 106], [-41, 212], [-41, 318], [-47, 424], [-45, 530], [-41, 636], [-36, 742], [-35, 848], [-46, 954], [-45, 1060], [-49, 1166], [-43, 1272], [-51, 1378], [-61, 1484], [-68, 1590], [-74, 1802], [-77, 1908], [-75, 2014], [-72, 2650], [-71, 2756], [-80, 2862], [-74, 3286]],
    'い': [[-39, 106], [-44, 212], [-38, 318], [-64, 424], [-65, 530], [-80, 636], [-81, 742], [-78, 848], [-80, 1060], [-81, 2332], [-75, 2438], [-75, 2544], [-79, 2650], [-82, 2756], [-75, 3498], [-77, 3604]],
    'う': [[-39, 106], [-46, 212], [-38, 318], [-44, 424], [-58, 530], [-78, 636], [-68, 742], [-73, 848], [-66, 954], [-69, 1060], [-71, 1166], [-69, 1272], [-62, 1378], [-65, 1484], [-75, 1590], [-78, 1696], [-76, 2438], [-70, 2544], [-81, 3750]],
    'え': [[-39, 106], [-43, 212], [-43, 318], [-40, 424], [-45, 530], [-56, 636], [-54, 742], [-62, 848], [-66, 954], [-66, 1060], [-71, 1166], [-73, 1272], [-72, 1378], [-71, 1484], [-74, 1590], [-74, 1696], [-76, 1802], [-72, 1908], [-68, 2014], [-66, 2120], [-64, 2226], [-56, 2332], [-64, 2438], [-64, 2544], [-66, 2650], [-63, 2756], [-64, 2862], [-62, 2968]],
    'お': [[-39, 106], [-46, 212], [-42, 318], [-39, 424], [-45, 530], [-54, 636], [-49, 742], [-47, 848], [-51, 954], [-69, 1060], [-71, 1166], [-76, 1272], [-77, 1378], [-76, 1484], [-79, 2544], [-72, 2650]],
    'ん': [[-39, 106], [-41, 214], [-43, 323], [-47, 431], [-64, 533], [-65, 641], [-67, 743], [-70, 851], [-72, 958], [-70, 1066], [-73, 1174], [-76, 1281], [-70, 1400], [-68, 1486], [-71, 1593], [-79, 1701], [-83, 1809], [-78, 1916], [-77, 2024], [-75, 2132], [-79, 2239], [-80, 2347], [-75, 2455], [-79, 2562]]
}
# 合成音ルール
compound_phonemes = {
    'な': ['ん', 'あ'],
    'に': ['ん', 'い'],
    'ぬ': ['ん', 'う'],
    'ね': ['ん', 'え'],
    'の': ['ん', 'お'],
    'や': ['い', 'あ'],
    'ゆ': ['い', 'う'],
    'よ': ['い', 'お'],
    'わ': ['う', 'あ'],
    'を': ['う', 'お'],
    'いぇ': ['い', 'え'],
    'うぃ': ['う', 'い'],
    'うぇ': ['う', 'え'],
    'にゃ': ['に', 'や'],
    'にゅ': ['に', 'ゆ'],
    'にぇ': ['に', 'え'],
    'にょ': ['に', 'よ'],
}
alphabet_list = {
    'a': 'えー',
    'e': 'いー',
    'i': 'あい',
    'n': 'えぬ',
    'o': 'おー',
    'u': 'ゆー',
    'y': 'わい',
    'A': 'えー',
    'E': 'いー',
    'I': 'あい',
    'N': 'えぬ',
    'O': 'おー',
    'U': 'ゆー',
    'Y': 'わい',
    ',': '、',
    '.': '。',
    ' ': 'っ'
}
word_replace_list = {
    'an': 'あん',
    'eye': 'あい',
    'in': 'いん',
    'now': 'なう',
    'nan': 'なん',
    'knee': 'にー',
    'no': 'のー',
    'know': 'のー',
    'none': 'なん',
    'on': 'おん',
    'yeah': 'やー',
    'you': 'ゆー',
    'yen': 'いぇん',
    'war': 'うぉー',
    ', ': '、',
    '. ': '。'
}
kana_list = {
    'ア': 'あ',
    'イ': 'い',
    'ウ': 'う',
    'エ': 'え',
    'オ': 'お',
    'ナ': 'な',
    'ニ': 'に',
    'ヌ': 'ぬ',
    'ネ': 'ね',
    'ノ': 'の',
    'ヤ': 'や',
    'ユ': 'ゆ',
    'ヨ': 'よ',
    'ワ': 'わ',
    'ヲ': 'を',
    'ン': 'ん',
    'ィ': 'ぃ',
    'ェ': 'ぇ',
    'ャ': 'ゃ',
    'ュ': 'ゅ',
    'ョ': 'ょ',
    'ッ': 'っ'
}
kanji_list = {
    '阿': 'あ',
    '亜': 'あ',
    '合': 'あ',
    '会': 'あ',
    '愛': 'あい',
    '青': 'あお',
    '蒼': 'あお',
    '穴': 'あな',
    '兄': 'あに',
    '姉': 'あね',
    '鮎': 'あゆ',
    '泡': 'あわ',
    '案': 'あん',
    '庵': 'あん',
    '胃': 'い',
    '伊': 'い',
    '井': 'い',
    '意': 'い',
    '医': 'い',
    '委': 'い',
    '位': 'い',
    '威': 'い',
    '居': 'い',
    '言': 'い',
    '家': 'いえ',
    '否': 'いな',
    '犬': 'いぬ',
    '戌': 'いぬ',
    '稲': 'いね',
    '嫌': 'いや',
    '岩': 'いわ',
    '祝': 'いわ',
    '院': 'いん',
    '印': 'いん',
    '淫': 'いん',
    '韻': 'いん',
    '員': 'いん',
    '隠': 'いん',
    '卯': 'う',
    '上': 'うえ',
    '畝': 'うね',
    '運': 'うん',
    '絵': 'え',
    '江': 'え',
    '英': 'えい',
    '栄': 'えい',
    '永': 'えい',
    '円': 'えん',
    '炎': 'えん',
    '園': 'えん',
    '尾': 'お',
    '御': 'お',
    '王': 'おう',
    '欧': 'おう',
    '多': 'おお',
    '鬼': 'おに',
    '斧': 'おの',
    '親': 'おや',
    '恩': 'おん',
    '女': 'おんな',
    '名': 'な',
    '奈': 'な',
    '萎': 'な',
    '内': 'ない',
    '苗': 'なえ',
    '尚': 'なお',
    '七': 'なな',
    '縄': 'なわ',
    '何': 'なん',
    '二': 'に',
    '荷': 'に',
    '煮': 'に',
    '贄': 'にえ',
    '匂':'にお',
    '庭': 'にわ',
    '忍': 'にん',
    '妊': 'にん',
    '縫': 'ぬ',
    '塗': 'ぬ',
    '鵺': 'ぬえ',
    '布': 'ぬの',
    '値': 'ね',
    '音': 'ね',
    '寝': 'ね',
    '根': 'ね',
    '寧': 'ねい',
    '姐': 'ねえ',
    '年': 'ねん',
    '念': 'ねん',
    '野': 'の',
    '乗': 'の',
    '呑': 'の',
    '飲': 'の',
    '脳': 'のう',
    '能': 'のう',
    '農': 'のう',
    '納': 'のう',
    '矢': 'や',
    '屋': 'や',
    '八': 'や',
    '焼': 'や',
    '揶': 'や',
    '柔': 'やわ',
    '軟': 'やわ',
    '湯': 'ゆ',
    '喩': 'ゆ',
    '油': 'ゆ',
    '唯': 'ゆい',
    '優': 'ゆう',
    '夕': 'ゆう',
    '悠': 'ゆう',
    '故': 'ゆえ',
    '世': 'よ',
    '良': 'よ',
    '余': 'よ',
    '夜': 'よ',
    '与': 'よ',
    '酔': 'よ',
    '用': 'よう',
    '要': 'よう',
    '陽': 'よう',
    '洋': 'よう',
    '曜': 'よう',
    '弱': 'よわ',
    '齢': 'よわい',
    '四': 'よん',
    '和': 'わ',
    '話': 'わ',
    '倭': 'わ',
    '罠': 'わな',
    '鰐': 'わに',
    '湾': 'わん',
    '椀': 'わん'
}
replace_list = {**alphabet_list, **kana_list, **kanji_list}
# 単独音 + 合成音 + 記号 + 漢字
available_char = set(phonemes.keys()) | set(compound_phonemes.keys()) | {'ー', 'っ', '、', '。'} | set(replace_list.keys() | set(word_replace_list.keys()))
# ソートする
available_char = " | ".join(sorted(available_char))

def shift_frequencies(data, key_shift):
    ratio = 2 ** (key_shift / 12)
    return [[db, freq * ratio] for db, freq in data]
# dB → 振幅変換
def db_to_amplitude(db):
    return 10 ** (db / 20)
def adjust_duration(duration, key_shift=0):
    pitch_ratio = 106 * 2 ** (key_shift / 12)
    return round(pitch_ratio * duration) / pitch_ratio
# 音声生成
def synthesize_sound(data, duration, key_shift=0):
    data = shift_frequencies(data, key_shift)
    t = np.linspace(0, adjust_duration(duration, key_shift), int(48000 * adjust_duration(duration, key_shift)), endpoint=False)
    signal = np.zeros_like(t)
    for db, freq in data:
        amp = db_to_amplitude(db)
        tone = amp * np.sin(2 * np.pi * freq * t)
        signal += tone
    return signal / np.max(np.abs(signal))
# 再起フレーズ分け
def resolve_phoneme_parts(char):
    if char in phonemes:
        return [char]
    elif char in compound_phonemes:
        parts = []
        for p in compound_phonemes[char]:
            parts.extend(resolve_phoneme_parts(p))
        # 重複除去（順序保持）
        return list(dict.fromkeys(parts))
    else:
        return []
# メイン関数
def speak_kana(text, key_shift=0):
    signals = []
    i = 0
    last_vowel = None
    while i < len(text):
        if text[i] in pause_map:
            silence = np.zeros(int(48000 * pause_map[text[i]]))
            signals.append(silence)
            i += 1
        elif text[i] == "ー" and last_vowel:
            sig = synthesize_sound(last_vowel, prolong_duration, key_shift)
            signals.append(sig)
            i += 1
        else:
            silence = np.zeros(int(48000 * normal_duration))
            signals.append(silence)
            matched = False
            # 最大2文字の合成音をチェック
            for length in [2, 1]:
                if i + length <= len(text):
                    part = text[i:i+length]
                    parts = resolve_phoneme_parts(part)
                    if parts:
                        for j, p in enumerate(parts):
                            duration = conso_duration if j < len(parts) - 1 else full_duration - j * conso_duration
                            sig = synthesize_sound(phonemes[p], duration, key_shift)
                            signals.append(sig)
                        last_vowel = phonemes[parts[-1]]
                        i += length
                        matched = True
                        break
            if not matched:
                print(f"⚠️ 未対応の文字: 「{text[i]}」")
                i += 1

    if signals:
        full_signal = np.concatenate(signals)
        sd.play(full_signal)
        sd.wait()
    else:
        print("⚠️ 有効な音が含まれていません。")
# 文字列をひら仮名に変換する関数
def to_kana(text):
    result = ''
    i = 0
    while i < len(text):
        matched = False
        for length in [4, 3, 2]:
            if i + length <= len(text) and text[i:i+length] in word_replace_list:
                result += word_replace_list[text[i:i+length]]
                i += length
                matched = True
                break
        if not matched:
            if text[i] in replace_list:
                result += replace_list[text[i]]
            else:
                result += text[i]
            i += 1
    return result
# 漢字対応版speak関数
def speak(text, key_shift=0):
    kana_text = to_kana(text)
    print("\n\n使用可能な文字：\n"+available_char+"\n\n")
    print(f"🗣️ 原文　　: {text}")
    print(f"🗣️ 読み仮名: {kana_text}\n")
    speak_kana(kana_text, key_shift)
# 設定（単位：秒）
normal_duration = 0.03
full_duration = 0.14
conso_duration = 0.05
prolong_duration = 0.16
pause_map = {
    'っ': 0.12,
    '、': 0.3,
    '。': 0.6,
}
speak("yeah, あーーーーーーニュニュニュ、イッヌイッヌ。あの女の姉の犬や兄のニャンニャン、青いねー。あの絵、何円なの。I no nan you.", 2)