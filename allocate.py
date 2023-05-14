data = open("system.img", "wb")

val = (0).to_bytes(1, 'little') * (16 << 20)

val = bytes(val)

data.write(val)

data.close()