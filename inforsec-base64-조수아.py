encode_table = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', '+', '/', '=']

# encode : Encoding ASCII Code to Base64
def encode(byte_Array, left):    # left = 문자 수, 모두 채워져 있을 경우엔 0
    global E_output  # 결과값을 저장할 변수

    # 6bit씩 분할하여 얻어낸 결과 값을 각 자리 변수에 (enc1,2,3,4) 저장
    if left == 0:    # 3문자가 모두 존재할 경우
        enc1 = (byte_Array[0] >> 2) & 0x3f
        enc2 = ((byte_Array[0] & 0x3) << 4) | ((byte_Array[1] & 0xf0) >> 4)
        enc3 = ((byte_Array[1] & 0xf) << 2) | ((byte_Array[2] >> 6) & 0x3)
        enc4 = byte_Array[2] & 0x3f

    # 모든 bit가 비어있는 자리: = (padding), 부족한 비트가 있는 자리에는 0을 채움
    elif left == 1:  # 1문자로 이루어진 경우
        enc1 = (byte_Array[0] >> 2) & 0x3f
        enc2 = ((byte_Array[0] & 0x3) << 4) | ((0 & 0xf0) >> 4)
        enc3 = 64
        enc4 = 64

    elif left == 2:  # 2문자로 이루어진 경우
        enc1 = byte_Array[0] >> 2 & 0x3f
        enc2 = ((byte_Array[0] & 0x3) << 4) | ((byte_Array[1] & 0xf0) >> 4)
        enc3 = ((byte_Array[1] & 15) << 2) | ((0 >> 6) & 0x3)
        enc4 = 64

    # encode_table을 이용하여 결과 값을 E_outuput에 저장
    E_output += encode_table[enc1] + encode_table[enc2] + encode_table[enc3] + encode_table[enc4]
    return E_output


# decode : Decoding Base64 to ASCII Code
def decode(base_Array, left):
    global D_output # 결과 값을 저장할 변수

    # 8bit씩 분할하여 얻어낸 결과 값을 각 자리 변수에 (dec1,2,3,4) 저장
    if left == 0:   # 4문자가 모두 존재할 경우
        dec1 = (base_Array[0] << 2) | (base_Array[1] >> 4)
        dec2 = ((base_Array[1] & 0x0f) << 4) | (base_Array[2] >> 2)
        dec3 = ((base_Array[2] & 0x03) << 6) | base_Array[3]
        D_output += chr(dec1) + chr(dec2) + chr(dec3)

    elif left == 1: # 1문자로 이루어진 경우 (decode 불가)
        D_output += "\nCan't convert!"

    elif left == 2: # 2문자로 이루어진 경우
        dec1 = (base_Array[0] << 2) | (base_Array[1] >> 4)
        D_output += chr(dec1)

    elif left == 3: # 3문자로 이루어진 경우
        dec1 = (base_Array[0] << 2) | (base_Array[1] >> 4)
        dec2 = ((base_Array[1] & 0x0f) << 4) | (base_Array[2] >> 2)
        D_output += chr(dec1) + chr(dec2)

    return D_output


if __name__ == "__main__":

    # a,b = 배열의 자리를 의미
    a = 0
    b = 0

    # base_Array = split base64 Code to array
    byte_Array = [0 for h in range(3)]  # split ASCII Code to 1 Byte array
    base_Array = [0 for h in range(4)]  # split base64 Code to 1 Byte array

    # 각 encoding, decoding 결과 값을 저장할 변수
    E_output = ""
    D_output = ""

    E_result = ''
    D_result = ''

    # input.txt 읽어오기 (* 전송시 올바른 주소로 바꿔야함 *)
    fp = open('C:\\Users\\sooa\\Desktopinforsec\\input.txt', mode='rt', encoding='utf-8')
    asc = fp.read()
    fp.close()

    size = len(asc)
    e_cycle = size // 3
    d_cycle = size // 4

    # encoding
    # 마지막 cycle일 때 실행, 값을 8bit씩 배열에 저장하고, 빈 자리 수에 따라 left 결정 후 encode 호출
    for i in range(e_cycle + 1):
        if i == (e_cycle):
            if size % 3 == 1:
                byte_Array[0] = ord(asc[a]) #ord를 통해 문자를 int 숫자값으로 변환
                a += 1
                E_result = encode(byte_Array, 1)
            elif size % 3 == 2:
                for k in range(2):
                    byte_Array[k] = ord(asc[a])
                    a += 1
                E_result = encode(byte_Array, 2)
            elif size % 3 == 0:
                pass

        # 마지막 cycle전까지 8bit씩 배열에 저장, left는 0으로 encode 호출
        else:
            for k in range(3):
                byte_Array[k] = ord(asc[a])
                a += 1
            E_result = encode(byte_Array, 0)

    # decoding
    # 마지막 cycle일 때 실행, 값을 6bit씩 배열에 저장하고, 빈 자리 수에 따라 left 결정 후 decode 호출
    for i in range(d_cycle + 1):
        if i == (d_cycle):
            if size % 4 == 1:
                base_Array[0] = encode_table.index(asc[b])
                b += 1
                D_result = decode(base_Array, 1)
            elif size % 4 == 2:
                for k in range(2):
                    base_Array[k] = encode_table.index(asc[b])
                    b += 1
                D_result = decode(base_Array, 2)
            elif size % 4 == 3:
                for k in range(3):
                    base_Array[k] = encode_table.index(asc[b])
                    b += 1
                D_result = decode(base_Array, 3)
            elif size % 4 == 0:
                pass

        # 마지막 cycle전까지 6bit씩 배열에 저장, left는 0으로 decode 호출
        else:
            for k in range(4):
                base_Array[k] = encode_table.index(asc[b])
                b += 1
            D_result = decode(base_Array, 0)

    # output.txt파일 만들기 (* 주소 바꿔야함 *)
    f = open('C:\\Users\\sooa\\Desktop\\output.txt', 'w')
    f.write(
        'Information Security ASCII/Base64 조수아\n\n\nEncoding: ' + E_result + '\n' + 'Decoding: ' + D_result)
    f.close()
