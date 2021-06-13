"""
Значения для n_table = 7 и shift = 29.
Они выбраны на основе испытаний с двумя jpg-файлами. Можно пробовать другие значения.
mode = 1 или любое ненулевое число\mode = 0 - это аргумент со значением по умолчанию для функции change_byte().
Он является флагом для режимов кодирования\декодирования строки байтов.

ЗАДАЧА от 11.11.2020:
    сделать способ постановки в известность ф-ии get_decode() о состоянии аргумента subtrahend
    в зависимости от чётности\нечётности восстанавливаемого байта в изначальной некодированной
    строке

Тесты 11.11.2020:
    Написан режим --remote для итерирования вызовов с разными значениями shift
    для поиска удачного байта в таблицах. Требует вызывающего кода,
    использующего цикл.
    jpeg-файл из whatsapp web не поддался кодированию в таблице 5 полностью и частично в таблице 7.
    Попробовать наладить настройку делителя и увязать с этим правильное восстановление исходного
    значения.
"""

import sys, os

log_dir = r'c:\jpg_corrupt_logs'
logfile = 'odd_number_log.txt'

if not os.path.exists(log_dir):
    os.mkdir(log_dir)

if not os.path.exists(os.path.join(log_dir,logfile)):
    open(os.path.join(log_dir,logfile), 'w')

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
def change_byte(b_array, fname_log, shift, n_table, subtrahend, mode=0, trace=0, func_enc=get_encode, func_dec=get_decode, get_idcs=get_idcs, log_dir=log_dir, logfile=logfile):
    """
    Выполняет шифрование в байтовой строке из jpg-файла
    """
    idcs = get_idcs(b_array) # составляем список смещений таблиц Хаффмана
    
    for i, b in enumerate(b_array):
        if i == idcs[n_table]:
        #if b == 255 and b_arr[i+1] == 196 and b_arr[i+3] == 181 and b_arr[i+4] == 17:
            if trace: print(b)
            #for idx, bte in enumerate(b_arr[idcs[7]:idcs[7]+183]):
            #if trace: print(i, bte)
            #if bte == 122 and b_arr[(idx+i)-1] == 121:
            log_file_path = open(os.path.join(log_dir, logfile), 'a') # txt-файл для записи имён jpg-файлов с нечётным числом в байте
            if trace: print('before:', b_array[i+shift])
            for_odd_even_test = b_array[i+shift]
            
            # главная операция
            b_array[i+shift] = func_enc(b_array, i, shift) if not mode else func_dec(b_array, i, shift, subtrahend)

            # сохранение в журнал
            # ПОСЛЕ ТЕСТОВ У Б Р А Т Ь СОХРАНЕНИЕ shift, n_table
            if for_odd_even_test % 2:
                print('%s subtract=1 shift=%s n_table=%s' % (fname_log, shift, n_table), file=log_file_path)
            else:
                print('%s subtract=0 shift=%s n_table=%s' % (fname_log, shift, n_table), file=log_file_path)
                
            if trace: print('after', b_array[i+shift])
            #break
            break
    return b_array


if __name__ == '__main__':
    if '--decode' in sys.argv:
        # записать сюда декодирующий режим работы сценария
        mode = 1
    else:
        mode = 0

    # режим отладки
    # для поиска удачно кодируемого смещения
    if '--remote' in sys.argv:
        fname = sys.argv[1] # передача настроек в авторежиме
        fname_log = fname
        shift = int(sys.argv[2])
        n_table = int(sys.argv[3])
        b_arr = get_bytes(fname)
        if '_new' in fname:
            fname = fname.replace('_new', '_restored')
        elif '_restored' in fname:
            fname = fname.replace('_restored', '_new')
        else:
            if '.jpg' in fname:
                fname = fname.replace('.jpg', '_new%s.jpg' % shift)
            else:
                fname = fname.replace('.jpeg', '_new%s.jpeg' % shift)

        cb_arr = change_byte(b_arr, fname_log, shift, n_table, subtrahend=0, mode=mode, trace=0)
        open(fname, 'wb').write(cb_arr)
        os._exit(1)
        
    fname = input('Enter name of jpg-file>')
    fname_log = fname   # имя файла для лога с отметками о нечётных десятичных числах в байтах jpg-файлов
                        # до вычитания
    shift = int(input('Enter shift>'))
    n_table = int(input('Enter num of table>'))
    if mode: subtrahend = int(input('Enter subtrahend>'))
    else: subtrahend = 0
    
    b_arr = get_bytes(fname) # извлекаем байты
    
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
    
    cb_arr = change_byte(b_arr, fname_log, shift, n_table, subtrahend=subtrahend, mode=mode, trace=trace)
    open(fname, 'wb').write(cb_arr)
