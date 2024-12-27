from flask import Flask
from flask import url_for, render_template, request, redirect
import spacy
from string import punctuation
import pandas as pd


app = Flask(__name__)

df_sent = pd.DataFrame()  # все-таки тут, а не ниже (после долгих попыток втыкания куда нипопадя) нужно создать датафрейм  

@app.route('/')
def index():
    return render_template('midterm_index.html')

@app.route('/statistics', methods=['GET'])
def stat():

    global df_sent

    sent = request.args.get('user_sentence')

    # предварительно обрабатываем текст: убираем пунктуацию и цифры
    sent = (' '.join([lemma.strip(punctuation + '1234567890').lower() for lemma in sent.split()]))
    # print(sent)

    nlp_ru = spacy.load("ru_core_news_sm")
    sent_doc = nlp_ru(sent)

    # лемматизируем и определяем часть речи, создаем переменную output - список словарей разбора каждого токена
    sc_output = [{"lemma": w.lemma_, "word": w.text, "pos": w.pos_, "morph": w.morph, "syntax": w.dep_} for w in sent_doc]

    # создадим датафрейм и загрузим туда нашу выдачу и сразу посчитаем статистику
    # просто добавляются новые строчки: ссылка на документацию пандас https://pandas.pydata.org/docs/reference/api/pandas.concat.html#pandas.concat
    df_sent = pd.concat([df_sent, pd.DataFrame(sc_output)], ignore_index=True)
    statistics = df_sent.value_counts('pos').items()  # items() чтобы сразу итерировать потом https://pandas.pydata.org/docs/reference/api/pandas.Series.items.html#pandas.Series.items

    return render_template('midterm_statistics.html', statistics=statistics)

if __name__ == '__main__':
    app.run(debug=True, port=5010)