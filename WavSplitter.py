from pydub import AudioSegment
import traceback
import os
import sys


def process_folder(input_folder, output_folder, segment_length):

    try:
        # Создаем выходную папку, если она не существует
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except:
        print('Error: creating new folder')
        print(traceback.format_exc())


    # Получаем список всех WAV файлов в исходной папке
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]

    for wav_file in wav_files:
        print(f'Processing: {wav_file}')

        try:
            # Загружаем аудиофайл
            audio = AudioSegment.from_wav(os.path.join(input_folder, wav_file))
        except:
            print(f'Error: loading wav file - {wav_file}')
            print(traceback.format_exc())
        
        try:
            # Разбиваем аудиофайл на сегменты
            segments = [audio[i:i+segment_length] for i in range(0, len(audio), segment_length)]
        except:
            print(f'Error: segmenting wav file - {wav_file}')
            print(traceback.format_exc())
        
        # Сохраняем сегменты в выходной папке
        for i, segment in enumerate(segments):
            output_file = os.path.join(output_folder, f'{os.path.splitext(wav_file)[0]}_{i+1}.wav')
            try:
                segment.export(output_file, format='wav')
            except:
                print(f"Error: exporting wav segment - {f'{os.path.splitext(wav_file)[0]}_{i+1}.wav'}")
                print(traceback.format_exc())

    print('Processed')

if __name__ == "__main__":
    arguments = sys.argv[1:]  # Получаем все аргументы командной строки, кроме имени скрипта

    # Здесь вы можете обрабатывать аргументы как вам необходимо
    input_folder = str('.\input')
    output_folder = str('.\out')
    segment_length = int(3000)

    if "-i" in arguments:
        input_folder_index = arguments.index('-i')
        if input_folder_index + 1 < len(arguments):
            input_folder = arguments[input_folder_index + 1]

    if "-o" in arguments:
        output_folder_index = arguments.index('-o')
        if output_folder_index + 1 < len(arguments):
            output_folder = arguments[output_folder_index + 1]
    
    if '-l' in arguments:
        segment_length_index = arguments.index('-l')
        if segment_length_index + 1 < len(arguments):
            segment_length = int(arguments[segment_length_index + 1])
    
    process_folder(input_folder, output_folder, segment_length)

