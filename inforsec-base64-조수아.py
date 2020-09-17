
encode_table = [ 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U',
                 'V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v',
                 'w','x','y','z','0','1','2','3','4','5','6','7','8','9','+','/','=']


def encode(byte_Array, left):
    
    global E_output

    
    if left == 0:
        enc1 = (byte_Array[0] >> 2) & 0x3f
        enc2 = ((byte_Array[0] & 0x3) << 4) | ((byte_Array[1] & 0xf0) >> 4)
        enc3 = ((byte_Array[1] & 0xf) << 2) | ((byte_Array[2] >> 6) & 0x3)
        enc4 = byte_Array[2] & 0x3f

    elif left == 1:
        enc1 = (byte_Array[0] >> 2) & 0x3f
        enc2 = ((byte_Array[0] & 0x3) <<4) | ((0 & 0xf0) >> 4)
        enc3 = 64
        enc4 = 64

    elif left == 2:
        enc1 = byte_Array[0] >> 2 & 0x3f
        enc2 = ((byte_Array[0] & 0x3) <<4) | ((byte_Array[1] & 0xf0) >> 4)
        enc3 = ((byte_Array[1] & 15) << 2) | ((0 >> 6) & 0x3)
        enc4 = 64

    E_output += encode_table[enc1]+encode_table[enc2]+encode_table[enc3]+encode_table[enc4]
    return E_output


def decode(base_Array, left):

    global D_output

    if left == 0:
        dec1 = (base_Array[0] << 2) | (base_Array[1] >> 4)
        dec2 = ((base_Array[1] & 0x0f) << 4) | (base_Array[2] >> 2)
        dec3 = ((base_Array[2] & 0x03) << 6) | base_Array[3]
        D_output += chr(dec1) + chr(dec2) + chr(dec3)
        
    elif left == 1:
        D_output += "Can't convert!\nBase64 is encoded"
        
    elif left == 2:
        dec1 = (base_Array[0] << 2) | (base_Array[1] >> 4)
        D_output += chr(dec1)

    elif left == 3:
        dec1 = (base_Array[0] << 2) | (base_Array[1] >> 4)
        dec2 = ((base_Array[1] & 0x0f) << 4) | (base_Array[2] >> 2)
        D_output += chr(dec1)+chr(dec2)

    return D_output


    
if __name__ == "__main__":

    fp = open('C:\\Users\\sooa\\Desktop\\inforsec\\input.txt', mode ='rt', encoding='utf-8')
    asc = fp.read()
    fp.close()

    a = 0
    b = 0
    byte_Array = [ 0 for h in range(3)]
    base_Array = [ 0 for h in range(4)]
    E_output= ""
    D_output= ""
    size = len(asc)
    e_cycle = size // 3
    d_cycle = size // 4
    E_result = ''
    D_result = ''
    

    for i in range(e_cycle+1):
        if i == (e_cycle):
            if size % 3 == 1:
                byte_Array[0] = ord(asc[a])
                a += 1
                E_result = encode(byte_Array, 1)
            elif size % 3 == 2:
                for k in range(2):
                    byte_Array[k] = ord(asc[a])
                    a += 1
                E_result = encode(byte_Array,2)
            elif size % 3 == 0:
                pass
           
        else:
            for k in range(3):
                byte_Array[k] = ord(asc[a])
                a += 1
            E_result = encode(byte_Array,0)



    for i in range(d_cycle+1):
        if i == (d_cycle):
            if size % 4 == 1:
                base_Array[0] = encode_table.index(asc[b])
                b += 1
                D_result = decode(base_Array,1)
            elif size % 4 == 2:
                for k in range(2):
                    base_Array[k] = encode_table.index(asc[b])
                    b += 1
                D_result = decode(base_Array, 2)
            elif size % 4  == 3:
                for k in range(3):
                    base_Array[k] = encode_table.index(asc[b])
                    b += 1
                D_result = decode(base_Array, 3)
            elif size % 4 == 0:
                pass

        else:
            for k in range(4):
                base_Array[k] = encode_table.index(asc[b])
                b += 1
            D_result = decode(base_Array, 0)

    f = open('C:\\Users\\sooa\\Desktop\\output.txt', 'w')
    f.write('Information Security assignment #1 ASCII/Base64 32174258 모바일시스템공학과 조수아\n\n\nEncoding: '+E_result+'\n'+'Decoding: '+ D_result)
    f.close()
