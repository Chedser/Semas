import math
import rsa
class Security:

    @staticmethod
    def get_keys():
        keys = dict()
        (publick_key, private_key) = rsa.newkeys(1024)
        keys["publick_key"] = publick_key
        keys["private_key"] = private_key
        return keys



