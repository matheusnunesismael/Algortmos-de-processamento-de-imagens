from PIL import Image
import numpy as np
import sys
from struct import *

'''
    Função responsável por codificar a imagem e formato LZW
    Recebe uma entrada do tpo PIL.Image e o nome do arquivo de saída

    A imagem é convertida em formato string de valores RGB e divididos em uma string
    para cada canal, as strings são concatenadas e codificadas para formato LZW,
    o tamanho da imagem original e a string comprimida são concatenados e salvos de forma binaria em um arquivo
'''
def encode(image, output_name):
    c, l = image.size
    colorsRGB = list(image.getdata())
    R = []
    G = []
    B = []
    for color in colorsRGB:
        r = color[0]
        g = color[1]
        b = color[2]

        R.append('0'+str(r) if r < 10 else str(r))
        G.append('0'+str(g) if g < 10 else str(g))
        B.append('0'+str(b) if b < 10 else str(b))

    colors = R + G + B
    encoded = encode_array(colors)
    write_encoded_file([c, l], encoded, output_name)

'''
    Recebe uma lista de strings e retorna a versão comprimida pelo metodo LZW desta lista
'''
def encode_array(array):
    P = ''
    C = ''

    res = []
    ret = []
    dic = []

    for i in range(0, 257):
        dic.append(str(i) if i > 9 else '0'+str(i))

    for cod in array:
        C = cod
        if (P+C) in dic:
            P += C
        else:
            res += [int(dic.index(P))]
            dic += [P+C]
            P = C
    res += [int(dic.index(P))]

    return res

'''
    Recebe o tamanho da imagem, a array comprimida pelo metodo LZW e o nome do arquivo de saída
    cria o arquivo e escreve nele as informações
'''
def write_encoded_file(size, array, output_name):
    file = None
    try:
        file = open(output_name, "wb+")
    except:
        print('Erro ao criar arquivo de saida!')
        sys.exit(1)

    data = size + array

    file.write(pack('<'+str(len(data))+'I', *data))

'''
    Recebe o arquivo de entrada e de saida, decodifica o arquivo de entrada e gera o arquivo de saída

    Lê o arquivo de entrada extrai os valores de entrada e saida, decodifica o vetor de canais de cores
    e remonta a imagem original.
'''
def decode(file_name, destiny_file):
    bytes = []
    try:
        bytes = open(file_name, "rb")
    except:
        print('Erro ao abrir arquivo!')
        sys.exit(1)

    comprimento, largura = unpack('2i', bytes.read(8))

    colors = []
    colorsStr = []

    fim = False
    while not fim:
        try:
            cod = unpack('i', bytes.read(4))[0]
            colors += [int(cod)]
        except:
            fim = True

    decoded = decode_array(colors)

    R = []
    G = []
    B = []

    Rm = []
    Gm = []
    Bm = []
    idx = 0

    for i in range(3):
        for j in range((comprimento * largura)):
            c = decoded[idx]
            idx += 1
            if i == 0:
                R += [c]
            elif i == 1:
                G += [c]
            else:
                B += [c]
    arr_r = np.array(R,dtype="uint8")
    arr_g = np.array(G,dtype="uint8")
    arr_b = np.array(B,dtype="uint8")
    
    reshaper=arr_r.reshape(comprimento,largura) 
    reshapeb=arr_g.reshape(comprimento,largura)
    reshapeg=arr_b.reshape(comprimento,largura)

    imr=Image.fromarray(reshaper,mode=None)
    imb=Image.fromarray(reshapeg,mode=None)
    img=Image.fromarray(reshapeb,mode=None)
    
    imgBack = Image.merge("RGB",(imr,img,imb))
    imgBack.save(destiny_file)

'''
    Recebe uma string codificada em LZW e devolve a string decodificada
'''
def decode_array(array):
    cW = ""
    pW = ""
    P  = ""
    C  = ""

    res = []
    ret = []
    dic = []

    for i in range(0, 257):
        dic += [str(i)]

    cW = array[0]
    res += [dic[int(cW)]]

    for i in range(1, len(array)):
        pW = cW
        cW = array[i]
        if int(cW) < len(dic):
            res += dic[int(cW)].split('+')
            P = dic[int(pW)]
            C = dic[int(cW)].split('+')[0]
            dic += [P+'+'+C]
        else:
            P = dic[int(pW)]
            C = dic[int(cW)].split('+')[0]
            res += (P+C).split('+')
            dic += [P+'+'+C]

    for value in res:
        ret += [int(value)]
    
    return ret