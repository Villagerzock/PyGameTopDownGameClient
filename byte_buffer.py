class ByteBuffer:
    def __init__(self,data : bytes):
        self.data = data
    index = 0

    def get(self):
        value = self.data[self.index]
        self.index += 1
        return value

    def get_string(self) -> str:
        length = int.from_bytes(self.data[self.index: self.index + 4],byteorder="big")
        self.index += 4
        value = self.data[self.index: self.index + length].decode("utf-8",'replace')
        self.index += length
        return value
    def get_int(self) -> int:
        length = int.from_bytes(self.data[self.index:self.index + 4],byteorder="big", signed=True)
        self.index += 4
        return length
    def get_bool(self) -> bool:
        value = self.data[self.index]
        self.index += 1
        return value == 1