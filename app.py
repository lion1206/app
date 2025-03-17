import random
from flask import Flask, render_template
from faker import Faker
from flask import Flask, request, render_template
import re

fake = Faker()

app = Flask(__name__)
application = app

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_comments(replies=True):
    comments = []
    for i in range(random.randint(1, 3)):
        comment = { 'author': fake.name(), 'text': fake.text() }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'title': fake.sentence(),
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }

def validate_phone(phone):
    # Разрешённые символы: цифры, пробелы, круглые скобки, дефисы, точки, +
    if not re.match(r'^[\d\s\(\)\-\.\\+]+$', phone):
        return "Недопустимый ввод. В номере телефона встречаются недопустимые символы."

    # Извлекаем только цифры
    digits = re.sub(r'\D', '', phone)  

    # Проверка количества цифр
    if digits.startswith("7") or digits.startswith("8"):
        if len(digits) != 11:
            return "Недопустимый ввод. Неверное количество цифр."
    elif len(digits) != 10:
        return "Недопустимый ввод. Неверное количество цифр."

    return None  # Ошибок нет

def format_phone(digits):
    """Преобразует номер к формату 8-***-***-**-**"""
    digits = re.sub(r'\D', '', digits)  # Убираем всё, кроме цифр
    if digits.startswith("7"):
        digits = "8" + digits[1:]  # Заменяем +7 на 8

    return f"{digits[0]}-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"



posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list)

@app.route('/posts/<int:index>')
def post(index):
    p = posts_list[index]
    return render_template('post.html', title=p['title'], post=p)

@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

@app.route("/checkphone", methods=["GET", "POST"])
def checkphone():
    phone = ""
    error = None
    formatted_phone = None

    if request.method == "POST":
        phone = request.form.get("phone", "")
        error = validate_phone(phone)

        if not error:
            formatted_phone = format_phone(phone)

    return render_template("checkphone.html", phone=phone, error=error, formatted_phone=formatted_phone)


if __name__ == '__main__':
    app.run(debug=True)