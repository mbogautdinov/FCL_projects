```python
# Текст должен быть предварительно обработан: знаки переноса строк (LF или CRLF) заменены на '\par', все знаки препинания должны быть отделены от любого токена справа и слева 1 пробелом, текст приведен к lowercase.
# Ключи словаря и, соответственно, первое значение внутри массива - значения ключа должны быть изменены в соответствии текстом.
# Поиск имен героев можно попробовать осуществить на natasha.github.io, с использованием других открытых библиотек или вручную.
# Проверьте, одинаковое ли тире в коде и в вашем тексте.
# Диалогом считается подряд идущие строки, начинающиеся с тире, а также строка, оканчивающаяся на двоеточие, перед первой строкой, начинающеся с тире, 
# а также 1 абзац, содержащий не более двух точек, внутри строк, начинающихся с тире.


text = input().split()
paragraph = []
paragraph.append([])
k = 0
for item in text:  # создаем список из абзацев, то есть предложений, начинающихся с новой строки, и следующих за ними в том же абзаце
    if item != '\\par':
        paragraph[k].extend([item])
    else:
        paragraph.append([])
        k += 1
while [] in paragraph:
    paragraph.remove([])
dialogue =  [[]]  # список - собиратор диалогов
d_d = 0  # обычный счетчик, работает внутри списка dialogue
passed = []  # список, в который забрасываются уже обработанные внутри цикла абзацы, по которым уже не нужно проходиться
for p in range(len(paragraph)):  # глобально здесь мы ищем именно диалоги
    if p in passed:
        passed.remove(p)
    elif paragraph[p][0] == '—':
        dialogue[d_d].extend(paragraph[p])  # добавляем тут как раз-таки предложение 
        passed.clear()
        if paragraph[p - 1][-1] == ':':  # случай, когда последнее предложение абзаца перед диалогом заканчивается на двоеточие 
            dialogue[d_d].extend(paragraph[p - 1])
        next = 1
        while paragraph[p + next][0] == '—' or paragraph[p + 1 + next][0] == '—':
            if paragraph[p + next][0] == '—':  # Случай, когда реплика идет за репликой
                dialogue[d_d].extend(paragraph[p + next])
            elif paragraph[p + 1 + next][0] == '—' and paragraph[p + 1].count('.') < 3:  # Случай, когда абзац занимает одно-два предложения внутри диалога
                dialogue[d_d].extend(paragraph[p + next])
                dialogue[d_d].extend(paragraph[p + 1 + next])
            next += 1
            passed.append(p + next)
        dialogue.append([])
        d_d += 1
while [] in dialogue:
    dialogue.remove([])
# Этот список геров подходит для книги "Маленькие тролли и большое наводнение", героев для остальных книг ищи в автомат_тексты_и_герои
win_char = {'Муми-тролль': ['тролл'],  # здесь мы создаем ключи = имена героев, значения = массивы, в которых первое значение - часть имени героя, по которой осуществляется поиск
            'Муми-мама': ['мам'],
            'Бельчонок': ['бельчон'],
            'Снусмумрик': ['снусмумрик'],
            'Хемуль': ['хемул'],
            'Зверек': ['звер'],
             'Малышка Мю': ['малышк'],
             'Туу-тикки': ['тикки'],
             'Мюмла': ['мюмл'],
             'Морра': ['морр'],  
             'Хатифнатты': ['хатифнатт'],
             'Юнк': ['юнк'],
             'Саломея': ['саломе'],
             'Филифьонка': ['филифьонк'],
             'Хомса': ['хомс'],
             'Муми-папа': ['пап'],
             'Снорк': ['снорк']}
final = win_char.copy()
for dial in dialogue:  # глобально хотим посмотреть, кто с кем говорил
    dia = []
    for key in win_char:  # здесь мы собираем всех участников диалога с повторениями
        for d in dial:
            if win_char[key][0] in d:
                if win_char[key][0] == 'мам' and dial[dial.index(d) + 1] == 'Муми-тролля':  # здесь мы убираем штуку, когда у нас что-то типа "мама Муми-тролля", чтобы сам Муми-тролль не считался
                    dial[dial.index(d) + 1] = 'hahhhahaha'
                elif win_char[key][0] == 'пап' and dial[dial.index(d) + 1] == 'Муми-тролля':
                    dial[dial.index(d) + 1] = 'hahhhahaha'
            if win_char[key][0] in d:
                if ':' == dial[-1] and dial.index(dial[-1]) - dial.index[d] < 16:  # тут как раз берем то имя персонажа, которое встретилось в предложении, заканчивающемся на двоеточие
                    dia.append(key)
                context_d_dial = []  # здесь мы набираем контекст возле слова d: 6 слева, 3 справа токенов
                con = dial.index(d)
                for p in range(len(dial) - 1 - dial.index(d)):
                    if p > 3:
                        break
                    context_d_dial.append(dial[con])
                    con += 1
                k = 0
                for p in range(dial.index(d) - 1, 0, -1):
                    if k > 6:
                        break
                    context_d_dial.append(dial[p])
                    k += 1
                if context_d_dial.count('—') > 1 or (context_d_dial.count('—') > 0 and context_d_dial.count('.') > 0):  # здесь мы смотрим: если справа и слева есть либо два тире, либо и точка, и тире, то берем такого персонажа
                    dia.append(key)
    for name in dia:
        while dia.count(name) != 1:
            dia.remove(name)
    for key in win_char:
        for name in dia:
            if name == key:
                dia_copy = dia.copy()
                dia_copy.remove(name)
                for n in dia_copy:
                    win_char[key].extend([n])
for key in win_char:
    for f_key in final:
        num = win_char[key].count(f_key)
        final[f_key].extend((key, num))
        final[f_key] = final[f_key][-(len(win_char) * 2):]
print('\n\n\n')
for f_key in final:
    print(f_key, final.get(f_key), end='\n\n\n')  # Это вывод всего
