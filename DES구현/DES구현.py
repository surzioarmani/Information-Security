Key_array = [0 for i in range(16)] # 서브키를 저장할 배열
dKey_array = [ 0 for i in range(16)] # 복호화시 서브키를 저장할 배열
output = list()
doutput = ""
cipher_hex = list()

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

EX_table = [32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1]

P_box = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]

S_box = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 10, 3, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 14, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

shift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

PC_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

PC_2 = [14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32]


def HexTo64Bin(hexstr):
    '''
    16진수를 64bit의 2진수로 만들어준다.
    :param hexstr: 16진수로 이뤄진 string
    :return: 64 binary string
    '''
    bin64 = []

    for i in range(len(hexstr)):
        bin4 = str(bin(int(hexstr[i], 16)))[2:].rjust(4, '0')   # 4자리 오른쪽 정렬 후 빈자리는 0으로 채운다.
        bin64.append(bin4)
    return ''.join(bin64)


def permutation(permutation_t, inputB, outB):
    '''
    permutation을 진행한다.
    :param permutation_t: permutation 테이블
    :param inputB: permutation을 진행할 input binary string
    :param outB: 결과의 bit 크기 --> 결과물 배열 사이즈
    :return: permutation 진행한 결과 binary string
    '''
    outB_res = [-1] * outB  # outB 크기 만큼 배열 생성

    for i in range(len(permutation_t)):    # 테이블 크기만큼 permuation 진행
        inputB_res = permutation_t[i] - 1  # 1부터 시작하기 때문에 -1
        outB_res[i] = inputB[inputB_res]
    return ''.join(map(str, outB_res))

def Lshift(L, R, roundN):
    '''
    key generation을 진행할 때 left shift 진행 (1, 2, 9, 16)round에서는 1번, 나머지는 2번 shift
    :param L: key 왼쪽 28bit
    :param R: key 오른쪽 28bit
    :param roundN: 진행 중인 round 순서
    :return: shift 진행한 결과 key
    '''

    # shift table을 이용하여 각 round에 맞는 shift연산 횟수만큼  진행한다.
    for t in range(shift[roundN]):
        L = L[1:] + L[0]
        R = R[1:] + R[0]
    return (L, R)


def keyGenerate(key):
    '''
    subkey 16개를 pc_1, pc_2, shift를 이용하여 생성한다.
    :param key: 입력된 임의의 key 64bit
    '''

    k = HexTo64Bin(key)
    LR = permutation(PC_1, k, 56)  # PC_1으로 키 순열 진행 (64 --> 56 bit)
    mid = len(LR) // 2
    L = LR[:mid]
    R = LR[mid:]

    # 16개 서브키 만들기
    for i in range(16):
        (L, R) = Lshift(L, R, i)          # round에 맞게 shift 진행
        k = permutation(PC_2, L + R, 48)  # PC_2 진행 (56 --> 48 bit)
        Key_array[i] = k                  # subkey 16
        dKey_array[15-i] = k              # decrypt 시에는 생성된 subkey의 역순으로 진행


def xor(bit1, bit2):
    '''
    xor 연산을 bit1과 bit2로 진행한다.
    :param bit1: xor 진행할 binary string
    :param bit2: xor 진행할 binary string
    :return: xor 결과 binary string
    '''
    xor_res = []

    for i in range(len(bit1)):
        b1 = int(bit1[i])
        b2 = int(bit2[i])
        xor_bit = int(bool(b1) ^ bool(b2))   #bit씩 xor 진행
        xor_res.append(xor_bit)

    return ''.join(map(str, xor_res))


def BinToHex(binstr):
    '''
    binary string을 16진수로 변환.
    :param binstr: 변환할 binary string
    :return:  16진수로 변환된 결과 string
    '''
    hex_res1 = []

    for i in range(0, len(binstr), 4):   # 4개씩 끊어 정수로 만들고 16진수로 변환
        result = 0
        binstr_t = [x for x in reversed(binstr[i:i + 4])]

        for j in range(4):
            result += (2 ** j) * int(binstr_t[j])
        hex_res1.append('%X' % result)
    return ''.join(hex_res1)

def encrypt(key, input_hex):
    '''
    encrypt를 expansion, xor, s_box, p_box를 이용하여 진행한다.
    :param key: 임의로 설정한 64bit 키
    :param input_hex: 암호화를 진행할 16진수의 64bit input
    :return: 암호화된 16진수의 64bit의 결과
    '''
    keyGenerate(key)  # subkey인 Key_array 생성\
    input_bin = HexTo64Bin(input_hex)          # 16진수 --> 2진수
    input_ip = permutation(IP, input_bin, 64)  # IP 진행

    mid = len(input_ip) // 2
    L = input_ip[:mid]
    R = input_ip[mid:]

    # 16 round 진행
    for i in range(16):
        E = permutation(EX_table, R, 48)  # expansion 진행   (32 --> 48bit)
        X = xor(Key_array[i], E)          # key와 expansion 결과와 xor 진행

        s_res = []

        # 8그룹씩 S-box 진행  ( 6 * 8 -->  4 * 8) bit
        for n in range(8):
            start = 6 * n
            end = (6 * n) + 6
            input_s = X[start:end]
            i = int(input_s[0]) * 2 ** 1 + int(input_s[-1])
            j = int(input_s[1]) * 2 ** 3 + int(input_s[2]) * 2 ** 2 + int(input_s[3]) * 2 ** 1 + int(input_s[4])

            # s-box 계산후 오른쪽 정렬을 해서 4글자보다 작으면 0으로 채우기
            s_res.append(str(bin(S_box[n][i][j]))[2:].rjust(4, '0'))

        s_res = ''.join(s_res)

        f_res = permutation(P_box, s_res, 32)  # P_box 진행 (32 --> 32bit)
        f_res = ''.join(f_res)

        L_before = L
        L = R
        R = xor(L_before, f_res)

    RL = R + L # 마지막 라운드는 교차 없음음

   # FP 진행
    encryption_res = permutation(FP, RL, 64)
    hex_res = BinToHex(encryption_res)  # 2진수에서 16진수로 변환

    return hex_res


def decrypt(input_hex):
    input_bin = HexTo64Bin(input_hex)  # 16진수 --> 2진수
    input_ip = permutation(IP, input_bin, 64)  # IP 진행

    mid = len(input_ip) // 2
    L = input_ip[:mid]
    R = input_ip[mid:]

    # 16 round 진행
    for i in range(16):
        E = permutation(EX_table, R, 48)  # expansion 진행   (32 --> 48bit)
        X = xor(dKey_array[i], E)  # dkey와 expansion 결과와 xor 진행

        s_res = []

        # 8그룹씩 S-box 진행  ( 6 * 8 -->  4 * 8) bit
        for n in range(8):
            start = 6 * n
            end = (6 * n) + 6
            input_s = X[start:end]
            i = int(input_s[0]) * 2 ** 1 + int(input_s[-1])
            j = int(input_s[1]) * 2 ** 3 + int(input_s[2]) * 2 ** 2 + \
                int(input_s[3]) * 2 ** 1 + int(input_s[4])

            # s-box 계산후 오른쪽 정렬을 해서 4글자보다 작으면 0으로 채우기
            s_res.append(str(bin(S_box[n][i][j]))[2:].rjust(4, '0'))

        s_res = ''.join(s_res)

        f_res = permutation(P_box, s_res, 32)  # P_box 진행 (32 --> 32bit)
        f_res = ''.join(f_res)

        L_before = L
        L = R
        R = xor(L_before, f_res)

    RL = R + L  # 마지막 라운드는 교차 없음음

    # FP 진행
    encryption_res = permutation(FP, RL, 64)
    hex_res = BinToHex(encryption_res)  # 2진수에서 16진수로 변환

    return hex_res


def StrToHex(input_string):
    '''
    8byte 문자열을 16진수로 변환
    :param input_string: 8byte의 평문
    :return: 평문을 16진수로 변환한 결과 값
    '''
    hex_res = []
    for i in input_string:
        word = list(i)  # 문자열에서 문자단위로 나눔
        for k in word:  # 문자 단위마다 16진수로 변환해서 넣기
            b = hex(ord(k))[2:]
            hex_res.append(b)  # 0b 빼고 숫자만 집합시키기

    hex_res = ''.join(hex_res).rjust(16,'0')

    return ''.join(hex_res)


def HexToStr(enc):
    '''
    16진수를 ASCII로 변환한다.
    :param enc: 암호문을
    :return:
    '''
    result = []
    leng = 2
    enc = [enc[i:i+leng] for i in range(0, len(enc), leng)]

    for i in enc:
        result.append(chr(int(i,16)))
    result = ''.join(result)

    return result



def des(key, input_string):
    global ciper_hex, doutput
    '''
    num에 따라 encryption des를 진행한다.
    :param key: 임의로 주어진 64bit의 키
    :param input_string: 8byte의 des를 진행할 문자열
    '''

    input_hex = StrToHex(input_string)  # 8바이트문자열에서 16진수로
    print("[암호화]\n"+ "plaintext // 문자: "+str(input_string) + " 16진수: "+str(input_hex))
    enc = encrypt(key, input_hex)
    cipher = HexToStr(enc)

    cipher_hex.append(enc)

    print("ciphertext// 문자: " + str(cipher)+" 16진수: "+str(enc))

    output.append(str(cipher))

    dec= decrypt(enc)
    plaintext = HexToStr(dec)
    print("[복호화]\n" + "ciphertext // 문자: " + str(cipher) + " 16진수: " + str(input_hex))
    print("decrypt    // "+ "문자: "+ str(plaintext)+ " 16진수: "+ str(dec) +"\n")

    doutput += str(plaintext)

    return cipher


def block(story):  # 8바이트로 나눔
    '''
    hw2 문서의 text를 8byte씩 나누어 진행하도록 한다.
    :param story: hw2의 text
    :return: 8 바이트씩 나눈 결과
    '''
    length = 8

    for word in story:
        a = ([word[i:i + length] for i in range(0, len(word), length)])  # 8단위로 나누기
        for i in a:
            c = des(key, i)  # 8바이트씩 des시작 64bit
        output.append("\n")  #한줄이 끝나면 띄어쓰기

    return output


if __name__ == '__main__':

    key = '0000000000001000'
    f = open("C:\\Users\\sooa\\Desktop\\hw2output.txt", 'a')
    with open('C:\\Users\\sooa\\Desktop\\hw2.txt', 'rt') as file:
        story = list()
        while True:
            line = file.readline()
            if not line:
                break
            readL = line.strip('\n')
            print("txt파일의 내용: "+ str(readL))
            story.append(readL)
        print()
    en = block(story)
    print("암호 결과 : ", end = '')
    for i in range(len(output)):
        print(output[i], end='')
    print("복호화 결과 : " + doutput)

    f.write(doutput)
