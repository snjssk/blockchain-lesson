import hashlib
import json
import logging
import sys
import time

# 3rd party
from ecdsa import NIST256p
from ecdsa import VerifyingKey

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
                        recipient_blockchain_address, value,
                        sender_public_key=None, signature=None):
        # valueは小数点がくるためfloat
        transaction = utils.sorted_dict_by_key({
            'sender_blockchain_address': sender_blockchain_address,
            'recipient_blockchain_address': recipient_blockchain_address,
            'value': float(value)
        })

        # マイニング処理の場合
        if sender_blockchain_address == MINING_SENDER:
            self.transaction_pool.append(transaction)
            return True

        # signatureをチェック
        if self.verify_transaction_signature(
                sender_public_key, signature, transaction):
            self.transaction_pool.append(transaction)
            return True
        return False

    # 受け取るトランザクションの証明
    def verify_transaction_signature(
            self, sender_public_key, signature, transaction):
        sha256 = hashlib.sha256()
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        signature_bytes = bytes().fromhex(signature)
        verifying_key = VerifyingKey.from_string(
            bytes().fromhex(sender_public_key), curve=NIST256p)
        verified_key = verifying_key.verify(signature_bytes, message)
        return  verified_key

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
        # ブロックチェーンNode側で処理するブロック
        nonce = self.proof_of_work()
        self.add_transaction(
            sender_blockchain_address=MINING_SENDER,
            recipient_blockchain_address=self.blockchain_address,
            value=MINING_REWARD)
        previous_hash = self.hash(self.chain[-1])
        self.create_block(nonce, previous_hash)
        logging.info({'action': 'minig', 'status': 'success'})
        return True

    def calculate_total_amount(self, blockchain_address):
        total_amount = 0.0
        for block in self.chain:
            for transaction in block['transactions']:
                value = float(transaction['value'])
                # 受け取るためプラス
                if blockchain_address == transaction['recipient_blockchain_address']:
                    total_amount += value
                if blockchain_address == transaction['sender_blockchain_address']:
                    total_amount -= value
        return total_amount

'''
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

    print('my', block_chain.calculate_total_amount(my_blockchain_address))
    print('C', block_chain.calculate_total_amount('C'))
    print('D', block_chain.calculate_total_amount('D'))
'''



