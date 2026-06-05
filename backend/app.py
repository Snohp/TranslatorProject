from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, History

import argostranslate.translate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

CORS(app)

with app.app_context():
    db.create_all()


WORDS = {
    "consumer": {
        "phonetic": "/kənˈsjuːmə(r)/",
        "pos": "noun",
        "example": "The consumer is very important.",
        "example_zh": "消费者非常重要。"
    },
    "student": {
        "phonetic": "/ˈstjuːdənt/",
        "pos": "noun",
        "example": "I am a student.",
        "example_zh": "我是学生。"
    },
    "teacher": {
        "phonetic": "/ˈtiːtʃə(r)/",
        "pos": "noun",
        "example": "My teacher is very kind.",
        "example_zh": "我的老师很友善。"
    },
    "beautiful": {
        "phonetic": "/ˈbjuːtɪfəl/",
        "pos": "adjective",
        "example": "She is beautiful.",
        "example_zh": "她很漂亮。"
    },
    "computer": {
        "phonetic": "/kəmˈpjuːtə(r)/",
        "pos": "noun",
        "example": "I use a computer every day.",
        "example_zh": "我每天使用电脑。"
    }
}


def detect_language(text):
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            return "zh"
    return "en"


def translate_text(text):

    source = detect_language(text)

    installed_languages = (
        argostranslate.translate.get_installed_languages()
    )

    if source == "zh":

        from_lang = next(
            lang for lang in installed_languages
            if lang.code == "zh"
        )

        to_lang = next(
            lang for lang in installed_languages
            if lang.code == "en"
        )

    else:

        from_lang = next(
            lang for lang in installed_languages
            if lang.code == "en"
        )

        to_lang = next(
            lang for lang in installed_languages
            if lang.code == "zh"
        )

    translation = from_lang.get_translation(
        to_lang
    )

    return translation.translate(text)


def get_word_info(word):

    word = word.lower().strip()

    if word in WORDS:
        return WORDS[word]

    return None


@app.route("/")
def home():
    return "Translator API Running"


@app.route("/translate", methods=["POST"])
def translate():

    try:

        data = request.json

        text = data.get("text", "").strip()

        if not text:

            return jsonify({
                "error": "请输入内容"
            })

        result = translate_text(text)

        word_info = None

        if len(text.split()) <= 5:
            word_info = get_word_info(text)

        history = History(
            source_text=text,
            translated_text=result
        )

        db.session.add(history)
        db.session.commit()

        return jsonify({
            "source": text,
            "result": result,
            "word_info": word_info
        })

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/history")
def history():

    records = History.query.order_by(
        History.id.desc()
    ).all()

    return jsonify([
        {
            "id": item.id,
            "source": item.source_text,
            "result": item.translated_text,
            "time": item.create_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
        for item in records
    ])


@app.route("/clear", methods=["DELETE"])
def clear():

    History.query.delete()

    db.session.commit()

    return jsonify({
        "message": "已清空"
    })


if __name__ == "__main__":
    app.run(debug=True)