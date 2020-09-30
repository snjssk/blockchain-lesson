import hashlib
import json
import logging
import sys
import time

import utils

MINING_DIFFICULTY = 3
MINING_SENDER = 'THE BLOCK CHAIN'
MINING_REWARD = 0.1

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

class BlockChain(object):

    def __init__(self, blockchain_address):
        self.transaction_pool = []
        self.chain = []
        #初期を作成
        self.create_block(0, self.hash({}))
        self.blockchain_address = blockchain_address

    # blockの作成
    def create_block(self, nonce, previous_hash):
        # block作成時、キーの並び順を揃えてあげる
        block = utils.sorted_dict_by_key({
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        self.chain.append(block)
        self.transaction_pool = []
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
        self.transaction_pool.append(transaction)
        return True

    # コンセンサスアルゴリズムの計算
    def valid_proof(self, transactions, previous_hash, nonce,
                    difficulty=MINING_DIFFICULTY):
        # ブロックをつくって
        guess_block = utils.sorted_dict_by_key({
            'transactions': transactions,
            'previous_hash': previous_hash,
            'nonce': nonce
        })
        # ハッシュを作って
        guess_hash = self.hash(guess_block)
        # 判定をする
        return guess_hash[:difficulty] == '0'*difficulty

    # ナンスの作成
    def proof_of_work(self):
        # 値が書き換わってしまうのでコピーをつかう
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash(self.chain[-1])
        nonce = 0
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce

    # マイニング
    def mining(self):
        self.add_transaction(
            sender_blockchain_address=MINING_SENDER,
            recipient_blockchain_address=self.blockchain_address,
            value=MINING_REWARD)
        nonce = self.proof_of_work()
        previous_hash = self.hash(self.chain[-1])
        self.create_block(nonce, previous_hash)
        logging.info({'action': 'minig', 'status': 'success'})
        return True


if __name__ == '__main__':
    my_blockchain_address = 'my_blockchain_address'
    block_chain = BlockChain(blockchain_address=my_blockchain_address)
    # pprint(block_chain.chain)

    block_chain.add_transaction('A', 'B', 1.0)
    block_chain.mining()
    # previous_hash = block_chain.hash(block_chain.chain[-1])
    # nonce = block_chain.proof_of_work()
    # block_chain.create_block(nonce, previous_hash)

    block_chain.add_transaction('C', 'D', 2.0)
    block_chain.mining()
    # previous_hash = block_chain.hash(block_chain.chain[-1])
    # nonce = block_chain.proof_of_work()
    # block_chain.create_block(nonce, previous_hash)

    utils.pprint(block_chain.chain)




