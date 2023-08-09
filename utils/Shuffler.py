import math
from pydub import AudioSegment
import traceback
import os
import sys

def make_length_multiple(segment, target_length):
    current_length = len(segment)
    num_repeats = -(-target_length // current_length)  # Round up division
    return segment * num_repeats


def process_folder(input_folder, output_folder, target_length):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except:
        print('Error: creating new folder')
        print(traceback.format_exc())


   # Получите список всех wav файлов в папке
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]

    # Пройдитесь по парам файлов и наложите их друг на друга
    for i in range(len(wav_files)):
        for j in range(i + 1, len(wav_files)):
            file1 = AudioSegment.from_wav(os.path.join(input_folder, wav_files[i]))
            file2 = AudioSegment.from_wav(os.path.join(input_folder, wav_files[j]))
            
            # Сделать длины кратными целевой длине
            max_length = max(len(file1), len(file2))
            new_len = math.ceil(max_length / target_length) * target_length

            silent = AudioSegment.silent(duration=new_len, frame_rate=file1.frame_rate).set_channels(2)
            silent = silent.overlay(file1, loop=True).overlay(file2, loop=True)
            
            # Создайте имя для нового файла (например, "1_2.wav")
            new_filename = f"{os.path.splitext(wav_files[i])[0]}_{os.path.splitext(wav_files[j])[0]}.wav"
            
            # Сохраните новый файл
            silent.export(os.path.join(output_folder, new_filename), format="wav")

    print('Processed')


if __name__ == "__main__":
    arguments = sys.argv[1:]  # Получаем все аргументы командной строки, кроме имени скрипта

    # Обрабатываем аргументы
    input_folder = str('.\input')
    output_folder = str('.\out')
    target_length = int(3000)

    if '-i' in arguments:
        input_folder_index = arguments.index('-i')
        if input_folder_index + 1 < len(arguments):
            input_folder = arguments[input_folder_index + 1]

    if '-o' in arguments:
        output_folder_index = arguments.index('-o')
        if output_folder_index + 1 < len(arguments):
            output_folder = arguments[output_folder_index + 1]
    
    if '-t' in arguments:
        target_length_index = arguments.index('-t')
        if target_length_index + 1 < len(arguments):
            target_length = arguments[target_length_index + 1]

    
    process_folder(input_folder, output_folder, target_length)