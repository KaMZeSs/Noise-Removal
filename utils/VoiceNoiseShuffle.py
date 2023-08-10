import math
from pydub import AudioSegment
import traceback
import os
import sys
from random import randrange, uniform


# output_file_count - количество файлов, в которые преобразуется входной файл голоса
# min_noise_loudness - минимальная прибавка громкости шума (может быть отрицательной)
# max_noise_loudness - максимальная прибавка громкости шума (может быть отрицательной)
def process_folder(input_voice_folder, input_noise_folder, output_folder, output_file_count=1, min_noise_loudness=0, max_noise_loudness=0):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except:
        print('Error: creating new folder')
        print(traceback.format_exc())


    # Получить список всех wav файлов
    voice_wav_files = [f for f in os.listdir(input_voice_folder) if f.endswith('.wav')]
    noise_wav_files = [f for f in os.listdir(input_noise_folder) if f.endswith('.wav')]

    # Наложение шума
    for i, voice_file in enumerate(voice_wav_files):
        print(f'Processing {i}/{len(voice_wav_files)}: {voice_file}')
        voice_audio = AudioSegment.from_wav(os.path.join(input_voice_folder, voice_file))
        
        for i in range(output_file_count):
            noise_file = noise_wav_files[randrange(0, len(noise_wav_files)-1)]
            noise_audio = AudioSegment.from_wav(os.path.join(input_noise_folder, noise_file)) + uniform(min_noise_loudness, max_noise_loudness)
            result_audio = voice_audio.overlay(noise_audio)
            
             # Создание имя для нового файла (например, "voicefile#noice.wav")
            new_filename = f"{voice_file}#{os.path.splitext(noise_file)[0]}.wav"
            
            # Сохранение нового файла
            result_audio.export(os.path.join(output_folder, new_filename), format="wav")

    print('Processed')


if __name__ == "__main__":
    arguments = sys.argv[1:]  # Получаем все аргументы командной строки, кроме имени скрипта

    # Обрабатываем аргументы
    input_voice_folder = str('.\input')
    input_noise_folder = str('.\input')
    output_folder = str('.\out')
    target_length = int(3000)
    output_file_count = 1
    min_loudness = 0
    max_loudness = 0

    if '-iv' in arguments:
        input_voice_folder_index = arguments.index('-iv')
        if input_voice_folder_index + 1 < len(arguments):
            input_voice_folder = arguments[input_voice_folder_index + 1]
    
    if '-in' in arguments:
        input_noise_folder_index = arguments.index('-in')
        if input_noise_folder_index + 1 < len(arguments):
            input_noise_folder = arguments[input_noise_folder_index + 1]

    if '-o' in arguments:
        output_folder_index = arguments.index('-o')
        if output_folder_index + 1 < len(arguments):
            output_folder = arguments[output_folder_index + 1]
    
    if '-t' in arguments:
        target_length_index = arguments.index('-t')
        if target_length_index + 1 < len(arguments):
            target_length = arguments[target_length_index + 1]

    if '-c' in arguments:
        output_file_count_index = arguments.index('-t')
        if output_file_count_index + 1 < len(arguments):
            output_file_count = int(arguments[target_length_index + 1])
    
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
    
    process_folder(input_voice_folder=input_voice_folder, input_noise_folder=input_noise_folder, 
                   output_folder=output_folder, target_length=target_length, 
                   output_file_count=output_file_count, 
                   min_noise_loudness=min_loudness, max_noise_loudness=max_loudness)