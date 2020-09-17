

encode_table = [ 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U',
                 'V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v',
                 'w','x','y','z','0','1','2','3','4','5','6','7','8','9','+','/','=']


a = 0

def encode(ch, left):
    
    global output

    
    if left == 0:
        enc1 = (ch[0] >> 2) & 0x3f
        enc2 = ((ch[0] & 0x3) << 4) | ((ch[1] & 0xf0) >> 4)
        enc3 = ((ch[1] & 0xf) << 2) | ((ch[2] >> 6) & 0x3)
        enc4 = ch[2] & 0x3f

    elif left == 1:
        enc1 = (ch[0] >> 2) & 0x3f
        enc2 = ((ch[0] & 0x3) <<4) | ((0 & 0xf0) >> 4)
        enc3 = 64
        enc4 = 64

    elif left == 2:
        enc1 = ch[0] >> 2 & 0x3f
        enc2 = ((ch[0] & 0x3) <<4) | ((ch[1] & 0xf0) >> 4)
        enc3 = ((ch[1] & 15) << 2) | ((0 >> 6) & 0x3)
        enc4 = 64


    output += encode_table[enc1]+encode_table[enc2]+encode_table[enc3]+encode_table[enc4]
    return output





  
if __name__ == "__main__":

    fp = open('C:\\Users\\sooa\\Desktop\\inforsec\\input.txt', mode ='rt', encoding='utf-8')
    asc = fp.read()
    fp.close()
    f = open('C:\\Users\\sooa\\Desktop\\inforsec\\output.txt', mode ='wt')

    ch = [ 0 for h in range(3)]
    output= ""
    size = len(asc)
    cycle = size // 3
    result = ''
    bytes(4)


    for i in range(cycle+1):
        if i == (cycle):
            if size % 3 == 1:
                ch[0] = ord(asc[a])
                a += 1
                result = encode(ch, 1)
            elif size % 3 == 2:
                for k in range(2):
                    ch[k] = ord(asc[a])
                    a += 1
                result = encode(ch,2)
            elif size % 3 == 0:
                pass
           
        else:
            for k in range(3):
                ch[k] = ord(asc[a])
                a += 1
            result = encode(ch,0)

    print(result)

    f.write(result)

       


        
            
    

