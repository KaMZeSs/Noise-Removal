from pydub import AudioSegment
import traceback
import os
import sys

def process_folder(input_folder, output_folder, output_format, bit_rate):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except:
        print('Error: creating new folder')
        print(traceback.format_exc())


    # Get all files from input folder
    files = os.listdir(input_folder)

    for file in files:
        print(f'Processing: {file}')

        try:
            # Load audio file
            audio = AudioSegment.from_file(os.path.join(input_folder, file))
            audio.frame_rate = bit_rate
        except:
            print(f'Error: loading file - {file}')
            print(traceback.format_exc())
            continue
        
        output_file = os.path.join(output_folder, f'{os.path.splitext(file)[0]}.{output_format}')

        try:
            audio.export(output_file, format=output_format, bitrate=bit_rate)
        except:
            print(f"Error: exporting wav segment - {f'{os.path.splitext(file)[0]}.{output_format}'}")
            print(traceback.format_exc())

    print('Processed')


if __name__ == "__main__":
    arguments = sys.argv[1:]  # Получаем все аргументы командной строки, кроме имени скрипта

    # Обрабатываем аргументы
    input_folder = str('.\input')
    output_folder = str('.\out')

    output_format = str('wav')
    frame_rate = int(44100)

    if '-i' in arguments:
        input_folder_index = arguments.index('-i')
        if input_folder_index + 1 < len(arguments):
            input_folder = arguments[input_folder_index + 1]

    if '-o' in arguments:
        output_folder_index = arguments.index('-o')
        if output_folder_index + 1 < len(arguments):
            output_folder = arguments[output_folder_index + 1]
    
    if '-f' in arguments:
        output_format_index = arguments.index('-o')
        if output_format_index + 1 < len(arguments):
            output_format = arguments[output_format_index + 1]

    if '-r' in arguments:
        output_frame_rate_index = arguments.index('-o')
        if output_frame_rate_index + 1 < len(arguments):
            frame_rate = int(arguments[output_frame_rate_index + 1])

    
    process_folder(input_folder, output_folder, output_format, frame_rate)