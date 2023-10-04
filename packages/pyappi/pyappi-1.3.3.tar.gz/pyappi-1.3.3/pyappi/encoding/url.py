def encode_url(bin):
    result = ""

    val = 0
    valb = -6

    for c in bin:
        val = (val << 8) + c
        valb += 8

        while valb >= 0:
            result += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789[]"[(val >> valb) & 0x3F]
            valb -= 6
        

    if valb > -6:
        result += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789[]"[((val << 8) >> (valb + 8)) & 0x3F]

    while len(result) % 4:
        result += '-'

    return result
	
def decode_url(str):
    result = bytearray()

    T = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789[]"

    val = 0
    valb = -8

    for c in str:
        dx = T.find(c)

        if dx == -1:
            break

        val = (val << 6) + dx
        valb += 6

        if valb >= 0:
            result.append((val >> valb) & 0xFF)
            valb -= 8
    
    return result