import logging
import sys
import time

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class BlockChain(object):

    def __init__(self):
        self.transcction_pool = []
        self.chain = []
        #初期を作成
        self.create_block(0, 'init hash')

    # blockの作成
    def create_block(self, nonce, previous_hash):
        block = {
            'timestamp': time.time(),
            'transactions': self.transcction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        self.transcction_pool = []
        return block


def pprint(chains):
    for i, chain in enumerate(chains):
        print(f'{"="*25} Chain {i} {"="*25}')
        for k, v in chain.items():
            print(f'{k:15}{v}')


if __name__ == '__main__':
    block_chain = BlockChain()
    pprint(block_chain.chain)
    block_chain.create_block(1, 'hash 1')
    block_chain.create_block(2, 'hash 2')
    pprint(block_chain.chain)




