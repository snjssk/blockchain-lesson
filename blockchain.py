import hashlib
import json
import logging
import sys
import time

import utils

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

    def hash(self, block):
        # sortの二重チェック
        # 文字列にするときにjson.dumps(xx, sort_keys=True)とするとソートしてくれる
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()

def pprint(chains):
    for i, chain in enumerate(chains):
        print(f'{"="*25} Chain {i} {"="*25}')
        for k, v in chain.items():
            print(f'{k:15}{v}')


if __name__ == '__main__':
    block_chain = BlockChain()
    pprint(block_chain.chain)

    previous_hash = block_chain.hash(block_chain.chain[-1])
    block_chain.create_block(1, previous_hash)

    previous_hash = block_chain.hash(block_chain.chain[-1])
    block_chain.create_block(2, previous_hash)

    pprint(block_chain.chain)




