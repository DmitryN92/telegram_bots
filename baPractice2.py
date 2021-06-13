# Запускать
# в таком виде:
# C:\> python baPractice2.py -name fname -shift shift -table n_table [-s subtrahend] [--decode] [1]
# fname - полное имя файла, shift - смещение в таблице Хаффмана(обычно 29),
# n_table - номер смещения таблицы (обычно 7 в диапазоне от 0 до 7),
# subtrahend - 0 или 1 (для вычитания в ф-ии get_decode), --decode - если указано, то будет выбрано
# расшифровка файла *.jpg
# 1 - если указано, то включается трассировка

# написать версию, подходящую для работы с ботом

# ВНИМАНИЕ!
# Внимательно изучить, обратить внимание на все комментарии

import os, sys

# создаём файл для записи логов
if not os.path.exists('mylog.txt'):
    log_file = open('mylog.txt','w')
    log_file.close()

def get_bytes(fname):
    """
    Извлекает байты из jpg-файла
    и возвращает их в виде объекта bytearray
    """
    b_file = open(fname, 'rb')
    b_arr = bytearray(b_file.read())
    b_file.close()
    return b_arr

def get_idcs(b_arr):
    """
    Поиск координат (смещений), в которых начинаются таблицы Хаффмана
    """
    idcs = [] # для смещений с \xff\xc4
    for i, b in enumerate(b_arr):
        if b == 255 and b_arr[i+1] == 196:
            idcs.append(i)
    return idcs

# функции для кодирования\декодирования строки байтов
def get_encode(b_array, i, shift):
    return b_array[i+shift] - (b_array[i+shift] // 2)

def get_decode(b_array, i, shift, subtrahend=0):
    return (b_array[i+shift] * 2) - subtrahend


# для лучшей пригодности убрать значения по умолчания из shift и n_table
# заголовка функции и требовать точного ввода значений
def change_byte(b_array, fname_for_log, shift, n_table, subtrahend, mode=0, trace=0, func_enc=get_encode,
                func_dec=get_decode, get_idcs=get_idcs, log_dir=None, logfile=None):
    """
    Выполняет шифрование в байтовой строке из jpg-файла
    """
    idcs = get_idcs(b_array)  # составляем список смещений таблиц Хаффмана

    for i, b in enumerate(b_array):
        if i == idcs[n_table]:
            if trace: print(b)
            if trace: print('before:', b_array[i + shift])
            for_odd_even_test = b_array[i + shift]

            # главная операция
            b_array[i + shift] = func_enc(b_array, i, shift) if not mode else func_dec(b_array, i, shift, subtrahend)
            log_file = open('mylog.txt','a') # сохранять инфу о субтракте, шифте и н_тэйбле в этот файл
            # сохранение в журнал
            # ПОСЛЕ ТЕСТОВ У Б Р А Т Ь СОХРАНЕНИЕ shift, n_table
            if for_odd_even_test % 2:
                print('%s subtract=1 shift=%s n_table=%s' % (fname_for_log, shift, n_table), file=log_file)
            else:
                print('%s subtract=0 shift=%s n_table=%s' % (fname_for_log, shift, n_table), file=log_file)

            log_file.close() # обязательно вытолкнуть на диск и закрыть объект

            if trace: print('after', b_array[i + shift])
            # break
            break
    return b_array

if __name__ == '__main__':
    if '--decode' in sys.argv:
        # записать сюда декодирующий режим работы сценария
        mode = 1
    else:
        mode = 0

    # режим отладки по параметру --remote пока что не нужен

    # ВАЖНО! Требуется переделать так, чтоб можно было передавать все данные
    # в таком виде: C:\> python baPractice2.py -name fname -shift shift -table n_table [-s subtrahend] [--decode] [1]

    # список в словарь
    myvalues = dict()
    for i,s in enumerate(sys.argv):
        if '-' in s:
            myvalues[s] = sys.argv[i+1]

    fname = myvalues['-name']; shift = myvalues['-shift']; n_table = myvalues['-table']


     # имя файла для лога с отметками о нечётных десятичных числах в байтах jpg-файлов
    # до вычитания

    # ВАЖНО для расшифровки!
    if mode:
        subtrahend = myvalues['-s']
    else:
        subtrahend = 0

    b_arr = get_bytes(fname)  # извлекаем байты

    # ПРОАНАЛИЗИРОВАТЬ необходимость этого кода в этой версии (версия для бота в телеграм)
    trace = 1 if '1' in sys.argv else 0

    if '_new' in fname:
        fname = fname.replace('_new', '_restored')
    elif '_restored' in fname:
        fname = fname.replace('_restored', '_new')
    else:
        if '.jpg' in fname:
            fname = fname.replace('.jpg', '_new.jpg')
        else:
            fname = fname.replace('.jpeg', '_new.jpeg')

    # для сохранения информации вида "имя_фотки.jpg subtract=x shift=y n_table=z"
    # в файле .\mylog.txt
    fname_for_log = fname

    cb_arr = change_byte(b_arr, fname_for_log, shift, n_table, subtrahend=subtrahend, mode=mode, trace=trace)

    # переделать так, чтобы обработанное фото сохранялось в текущей рабочей директории
    #
    # Например, инструментами модуля os отделять простое имя от пути к нему
    # и справа добавлять обозначение текущей рабочей директории:
    # 'c:\myfolder\myphotos\photo.jpg' -> 'photo.jpg' -> fname = '.\photo.jpg'
    # (или fname = os.path.currdir + 'photo.jpg') -> f = open(fname, 'wb') -> f.write(cb_arr) -> f.close()
    fname = os.path.curdir + os.path.sep + os.path.basename(fname)
    f = open(fname, 'wb')
    f.write(cb_arr)
    f.close()