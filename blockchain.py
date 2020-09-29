import hashlib
import json
import logging
import sys
import time

import utils

MINING_DIFFICULTY = 3

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class BlockChain(object):

    def __init__(self):
        self.transcction_pool = []
        self.chain = []
        #初期を作成
        self.create_block(0, self.hash({}))

    # blockの作成
    def create_block(self, nonce, previous_hash):
        # block作成時、キーの並び順を揃えてあげる
        block = utils.sorted_dict_by_key({
            'timestamp': time.time(),
            'transactions': self.transcction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        self.chain.append(block)
        self.transcction_pool = []
        return block

    # ハッシュを作る
    def hash(self, block):
        # sortの二重チェック
        # 文字列にするときにjson.dumps(xx, sort_keys=True)とするとソートしてくれる
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    # トランザクションを作る
    def add_transaction(self, sender_blockchain_address,
                        recipient_blockchain_address, value):
        # valueは小数点がくるためfloat
        transaction = utils.sorted_dict_by_key({
            'sender_blockchain_address': sender_blockchain_address,
            'recipient_blockchain_address': recipient_blockchain_address,
            'value': float(value)
        })
        self.transcction_pool.append(transaction)
        return True

    # コンセンサスアルゴリズムの計算
    def valid_proof(self, transactions, previous_hash, nonce,
                    difficulty=MINING_DIFFICULTY):

    # ナンスの作成
    def proof_of_work(self):
        # 値が書き換わってしまうのでコピーをつかう
        transactions = self.transcction_pool.copy()
        previous_hash = self.hash(self.chain[-1])
        nonce = 0


if __name__ == '__main__':
    block_chain = BlockChain()
    # pprint(block_chain.chain)

    block_chain.add_transaction('A', 'B', 1.0)
    previous_hash = block_chain.hash(block_chain.chain[-1])
    block_chain.create_block(1, previous_hash)

    block_chain.add_transaction('C', 'D', 2.0)
    previous_hash = block_chain.hash(block_chain.chain[-1])
    block_chain.create_block(2, previous_hash)

    utils.pprint(block_chain.chain)




