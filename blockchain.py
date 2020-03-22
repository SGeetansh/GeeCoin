import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, prev_hash = '0')

    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash}
        
        self.chain.append(block)
        
        return block

    def get_prev_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof == False:
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def check_validity(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                prev_block = block
                block_index += 1
        return True


app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(proof, prev_hash)
    response = {'message': 'Congratulations! You just mined a block',
                'index': block['index'],
                'proof': block['proof'],
                'timestamp': block['timestamp'],
                'previous_hash': block['prev_hash']}
    return jsonify(response), 200

@app.route('/check_validity', methods = ['GET'])
def validity():
    is_valid = blockchain.check_validity(blockchain.chain)  
    if is_valid:
        response = {'message': 'The chain is valid'}
    else:
        response = {'message': 'We have a problem. The blockchain is invalid'}
    return response

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)
