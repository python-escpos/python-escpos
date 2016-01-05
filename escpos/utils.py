try:
    bytes.fromhex
    def hex2bytes(hex_string):
        return bytes.fromhex(hex_string)

except:
    def hex2bytes(hex_string):
        return hex_string.decode('hex')

