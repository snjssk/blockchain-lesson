import base58
import codecs
import hashlib

from ecdsa import NIST256p
from ecdsa import SigningKey

class Wallet(object):

    def __init__(self):
        # 秘密鍵と公開鍵の生成
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_blockchain_address()

    @property
    def private_key(self):
        return self._private_key.to_string().hex()

    @property
    def public_key(self):
        return self._public_key.to_string().hex()

    @property
    def blockchain_address(self):
        return self._blockchain_address

    def generate_blockchain_address(self):
        # 2 sha256で作成
        public_key_bytes = self._private_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()

        # 3 sha256→ripemd ripemdはhashよりも短いハッシュを生成できる
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest= ripemd160_bpk.digest()
        ripemd160_bpk_hex= codecs.encode(ripemd160_bpk_digest, 'hex')

        # 4 ネットワークのバイトを足す、ビットコインネットワークの仕様っぽいもの
        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key, 'hex')

        # 5 Double SHA-256 で作る
        sha256_bpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_bpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')

        # 6 chacksum
        checksum = sha256_hex[:8]

        # 7
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')

        # 8
        blockchain_address = base58.b58encode(address_hex).decode('utf-8')
        return blockchain_address


if __name__ == '__main__':
    wallet = Wallet()
    print(wallet.private_key)
    print(wallet.public_key)
    print(wallet.blockchain_address)