from PIL import Image
import numpy as np
import getopt
import lzw
import sys


def main():
    input_filename = None
    output_filename = None
    encode = False
    img = []

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:ed')
        # -i arquivo de entrada
        # -o arquivo de saida
        # -e codificar para LZW
        # -d decodificar de LZW para o formato informado no nome do arquivo de saida
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-i':
            input_filename = arg
        elif opt == '-o':
            output_filename = arg
        elif opt == '-e':
            encode = True
        elif opt == '-d':
            encode = False

    if encode:
        try:
            img = Image.open(input_filename).convert('RGB')
        except:
            print("Erro ao abrir a imagem!")
            sys.exit(1)
        lzw.encode(img, output_filename)
    else:
        lzw.decode(input_filename, output_filename)
    



if __name__ == '__main__': main()

    
