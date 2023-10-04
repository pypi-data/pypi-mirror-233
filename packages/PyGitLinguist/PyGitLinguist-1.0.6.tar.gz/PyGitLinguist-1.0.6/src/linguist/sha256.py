import hashlib
from linguist.tokenizer import Tokenizer, Token


class SHA256:
    @staticmethod
    def hexdigest(obj):
        digest = hashlib.sha256()

        def update(obj):
            if isinstance(obj, (str, int, bool, type(None))):
                digest.update(str(type(obj)).encode('utf-8'))
                digest.update(str(obj).encode('utf-8'))
            elif isinstance(obj, Token):
                digest.update(str(type(obj)).encode('utf-8'))
                digest.update(str(obj).encode('utf-8'))
            elif isinstance(obj, list):
                digest.update(str(type(obj)).encode('utf-8'))
                for e in obj:
                    update(e)
            elif isinstance(obj, dict):
                digest.update(str(type(obj)).encode('utf-8'))
                try:
                    for key, value in obj.items():
                        if isinstance(key, Token):
                            key = str(key)
                        if not isinstance(key, (str, int, bool, type(None))):
                            key = str(key)
                        if isinstance(value, dict):
                            digest.update(key.encode('utf-8'))
                            for k, v in value.items():
                                update(k)
                                update(v)
                        elif isinstance(value, Token):
                            digest.update(str(key).encode('utf-8'))
                            update(str(value))
                        else:
                            update(key)
                            update(value)
                except Exception as e:
                    print(f"Error hashing dict: {e} - {obj}")
            elif isinstance(obj, tuple):
                digest.update(str(type(obj)).encode('utf-8'))
                for e in obj:
                    update(e)
            else:
                raise TypeError("can't convert {} into String".format(repr(obj)))

        update(obj)
        return digest.hexdigest()
