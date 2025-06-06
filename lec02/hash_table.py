import random, sys, time

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################

# Hash function. keyを整数値(index)に変換
#
# |key|: string "Alice"
# Return value: a hash value "510"
def calculate_hash(key):
    assert type(key) == str # keyがstr型なのを確認する
    # Note: This is not a good hash function. Do you see why?
    # 衝突が起こりやすい。ハッシュ値が同じになりやすい。("abc", "cba")
    # 改善：順序を考慮する。1*a + 2*b + 3*c
    hash = 0
    for i, c in enumerate(key):
        hash += ord(c)* (i+1)
    return hash


# n以上の最小の素数を求める関数
def get_prime(n):
    def bool_prime(x): # 素数判定する関数
        if x<=1:
            return False
        for i in range(2, int(x ** 0.5)+1):
            if x%i == 0:
                return False
        return True
    
    while True:
        if bool_prime(n):
            return n
        n += 1


# An item object that represents one key - value pair in the hash table.
# ("Alice", 510, ("Elica", 510)/[])
class Item:
    # |key|: The key of the item. The key must be a string. "Alice"
    # |value|: The value of the item. "510"
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


# The main data structure of the hash table that stores key - value pairs. 
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size. # 素数だと衝突しにくい
# |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is |hash|.
# |self.item_count|: The total number of items in the hash table. # ユーザーの数?ハッシュテーブルに含まれる要素の数
class HashTable:

    # Initialize the hash table.
    def __init__(self):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size # [None, None, ...]
        self.item_count = 0

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|: The key of the item. "Alice"
    # |value|: The value of the item. "510"
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.
    def put(self, key, value):
        assert type(key) == str
        if self.item_count > self.bucket_size * 0.7: # # 要素数がテーブルサイズの70%を上回ったら
            self.resize(self.bucket_size * 2)
        self.check_size() # Note: Don't remove this code.
        
        bucket_index = calculate_hash(key) % self.bucket_size # 510%97(=25)
        item = self.buckets[bucket_index] # buckets[25]にある最初のItemを取得(リストの先頭)
        while item:
            if item.key == key: # すでに同じキーが存在したら
                item.value = value
                return False
            item = item.next
        new_item = Item(key, value, self.buckets[bucket_index]) # 新しいItemオブジェクトを作る(nextには今の先頭Itemを設定)
        self.buckets[bucket_index] = new_item # 新しいItemを先頭に追加
        self.item_count += 1
        return True
    

    # Get an item from the hash table.
    #
    # |key|: The key.
    # Return value: If the item is found, (the value of the item, True) is
    #               returned. Otherwise, (None, False) is returned.
    def get(self, key):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    # Delete an item from the hash table.
    #
    # |key|: The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        assert type(key) == str
        #self.check_size()
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        prev = None
        while item:
            if item.key == key:
                if prev:
                    prev.next = item.next # 前のノードを次のノードに繋げる
                else: # keyが先頭にあった時
                    self.buckets[bucket_index] = item.next  # 先頭のItemを削除
                self.item_count -= 1
                if self.bucket_size > 19 and self.item_count < self.bucket_size * 0.3: # 要素数がテーブルサイズの30%を下回ったら
                    self.resize(max(19, self.bucket_size // 2))  # 最小サイズ19に制限, 19かsize//2か大きい方を選択
                self.check_size()
                return True
            prev = item
            item = item.next
        return False

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count

    # Check that the hash table has a "reasonable" bucket size.
    # The bucket size is judged "reasonable" if it is smaller than 100 or
    # the buckets are 30% or more used.
    #
    # Note: Don't change this function.
    def check_size(self):
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)
    

    # 再ハッシュ関数
    # ハッシュテーブルを拡大縮小する
    # 新しいハッシュテーブルに要素を再配置する
    def resize(self, new_size):
        new_size = get_prime(new_size)
        old_buckets = self.buckets
        self.bucket_size = new_size
        self.buckets = [None] * new_size

        for old_item in old_buckets:
            while old_item:
                new_index = calculate_hash(old_item.key) % new_size
                new_item = Item(old_item.key, old_item.value, self.buckets[new_index]) # nextには今の先頭Itemを設定
                self.buckets[new_index] = new_item
                old_item = old_item.next



    #if self.bucket_size*0.7 < self.item_count: # 要素数がテーブルサイズの70%を上回ったら
    #    self.bucket_size *= 2
    #elif self.bucket_size*0.3 > self.item_count: # 要素数がテーブルサイズの30%を下回ったら
    #    self.bucket_size //= 2





# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    #functional_test()
    performance_test()
