import math
from pydub import AudioSegment
import traceback
import os
import sys
from random import randrange, uniform


# output_file_count - количество файлов, в которые преобразуется входной файл голоса
# min_noise_loudness - минимальная прибавка громкости шума (может быть отрицательной)
# max_noise_loudness - максимальная прибавка громкости шума (может быть отрицательной)
def process_folder(input_folder, output_folder, output_file_count=1, min_noise_loudness=0, max_noise_loudness=0):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except:
        print('Error: creating new folder')
        print(traceback.format_exc())


    # Получить список всех wav файлов
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]

    # Наложение шума
    for i, file in enumerate(wav_files):
        print(f'Processing {i}/{len(wav_files)}: {file}')
        audio = AudioSegment.from_wav(os.path.join(input_folder, file))
        
        for i in range(output_file_count):
            db = uniform(min_noise_loudness, max_noise_loudness)
            result_audio = audio + db

            # Создание имени для нового файла (например, "file$$+5.wav")
            new_filename = f"{file}$${str(db) if db < 0 else '+' + str(db)}.wav"
            
            # Сохранение нового файла
            result_audio.export(os.path.join(output_folder, new_filename), format="wav")

    print('Processed')


if __name__ == "__main__":
    arguments = sys.argv[1:]  # Получаем все аргументы командной строки, кроме имени скрипта

    # Обрабатываем аргументы
    input_folder = str('.\input')
    output_folder = str('.\out')
    output_file_count = 1
    min_loudness = 0
    max_loudness = 0

    if '-i' in arguments:
        input_folder_index = arguments.index('-i')
        if input_folder_index + 1 < len(arguments):
            input_folder = arguments[input_folder_index + 1]

    if '-o' in arguments:
        output_folder_index = arguments.index('-o')
        if output_folder_index + 1 < len(arguments):
            output_folder = arguments[output_folder_index + 1]

    if '-c' in arguments:
        output_file_count_index = arguments.index('-t')
        if output_file_count_index + 1 < len(arguments):
            output_file_count = int(arguments[output_file_count_index + 1])
    
    if '-min' in arguments:
        min_loudness_index = arguments.index('-min')
        if min_loudness_index + 1 < len(arguments):
            min_loudness = float(arguments[min_loudness_index + 1])

    if '-max' in arguments:
        max_loudness_index = arguments.index('-max')
        if max_loudness_index + 1 < len(arguments):
            max_loudness = float(arguments[max_loudness_index + 1])

    temp = min(min_loudness, max_loudness)
    max_loudness = max(min_loudness, max_loudness)
    min_loudness = temp
    
    process_folder(input_folder=input_folder,
                   output_folder=output_folder,
                   output_file_count=output_file_count, 
                   min_noise_loudness=min_loudness, 
                   max_noise_loudness=max_loudness)