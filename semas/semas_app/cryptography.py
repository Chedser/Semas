import random
class Cryptography:

    @staticmethod
    def modify(str, key, seed):
        if not str:return
        #seed = random.randint(1000,9999)
        #key = random.randint(1000,9999)

        new_str = ""

        for i in range(len(str)):
            char_code_m = ord(str[i])^key + seed
            char = chr(char_code_m)
            new_str = new_str + char
        return new_str