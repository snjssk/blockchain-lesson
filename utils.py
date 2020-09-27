import collections
import hashlib

def sorted_dict_by_key(unsorted):
    return collections.OrderedDict(
        sorted(unsorted.items(), key=lambda d:d[0]))

# 文字列に対して同じハッシュを生成する
# あくまでハッシュから文字列を推測できないようにするのが目的
# print(hashlib.sha256('test'.encode()).hexdigest())
# print(hashlib.sha256('test'.encode()).hexdigest())

# 辞書型の場合、中身は同じでも並び順によってハッシュが異なってしまう
# obj1 = {'a': 1, 'b': 2}
# obj2 = {'b': 2, 'a': 1}
# print(hashlib.sha256(str(obj1).encode()).hexdigest())
# print(hashlib.sha256(str(obj2).encode()).hexdigest())

# 順番を保持するメソッド
# obj1 = collections.OrderedDict(sorted(obj1.items(), key=lambda d:d[0]))
# obj2 = collections.OrderedDict(sorted(obj2.items(), key=lambda d:d[0]))
# print(hashlib.sha256(str(obj1).encode()).hexdigest())
# print(hashlib.sha256(str(obj2).encode()).hexdigest())