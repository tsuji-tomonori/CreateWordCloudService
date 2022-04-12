import io
import re
import os

import emoji
import pandas as pd
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud

from aws_resource import S3

STOP_WARDS = [
    "疲様",
    "了解",
    "ー"
]


def handler(event, context) -> None:
    s3 = S3()
    FONT_PATH = os.environ["FONT_PATH"]
    OUTPUT_BUCKET_NAME = os.environ["OUTPUT_BUCKET_NAME"]

    for record in event["Records"]:
        input_bucket_name = record["s3"]["bucket"]["name"]
        input_key = record["s3"]["object"]["key"]
        csv_data = s3.read_file(input_bucket_name, input_key)

        data = preprocessing(csv_data)
        wordcloud = WordCloud(
            background_color="white",
            font_path=FONT_PATH,
            width=1200,
            height=900,
            colormap="RdPu",
            stopwords=STOP_WARDS,

        ).generate(" ".join(data))
        upload_key = f"{input_key.split('.')[0]}.png"
        wordcloud.to_file("/tmp/wordcloud.png")
        with open("/tmp/wordcloud.png", "rb") as f:
            s3.upload(f, OUTPUT_BUCKET_NAME, upload_key)


def preprocessing(csv_data: str):
    df = pd.read_csv(io.StringIO(csv_data), encoding="utf-8")
    message_texts = list(
        df[df["meta_type"] == "textMessageEvent"]["message_text"])
    cleansing_data = [cleansing(text) for text in message_texts]
    result = tokenize(cleansing_data)
    return result


def remove_pure_emoji(text: str) -> str:
    return emoji.replace_emoji(text, replace='')


def remove_custom_emoji(text: str) -> str:
    return re.sub(":.*:", "", text)


def remove_not_word(text: str) -> str:
    return re.sub("[!-/:-@¥[-`{-~！～（）]", "", text)


def remove_bou(text: str) -> str:
    return re.sub("\wー+", "", text)


def replace_blank(text: str) -> str:
    return re.sub("\u3000", " ", text)


def remove_one_kana(text: str) -> str:
    return re.sub("[ぁ-ん]{1}", "", text)


def remove_w(text: str) -> str:
    patterns = ["w+", "W+", "ｗ+", "W+", "草+"]
    result = text
    for pattern in patterns:
        result = re.sub(pattern, "", result)
    return result


def cleansing(text) -> str:
    filters = [
        remove_pure_emoji,
        remove_custom_emoji,
        replace_blank,
        remove_w,
        remove_not_word,
        remove_one_kana,
        remove_bou,
    ]
    result = text
    for convert_f in filters:
        result = convert_f(result)
    return result


def tokenize(messages: list) -> list:
    t = Tokenizer()
    return [token.base_form for text in messages for token in t.tokenize(text) if token.part_of_speech.split(",")[0] in ["名詞", "形容詞"]]


def stop_word(target: list, stop_list: list) -> list:
    return [word for word in target if word not in stop_list]


def write_lst(path: str, data: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(data))
