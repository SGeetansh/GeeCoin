import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1, prevHash = '0')

    def createBLock(self, proof, prevHash):
        block = {'index': len(self.chain)+1
                 'timestamp': str(datetime.datetime.now())
                 'proof': proof,
                 'prevHash': prevHash}
        
        self.chain.append(block)
        
        return block

    def getPrevBlock(self):
        return self.chain[-1]

    def proofOfWork(self, prevProof):
        newProof = 1
        checkProof = False
        while checkProof = False:
            hashOperation = hashlib.sha256(str(newProof^2 - prevProof^2)).encode().hexdigest()
            if hashOperation[:4] == '0000':
                checkProof = True
            else:
                newProof += 1
        return newProof

    def hash(self, block):
        encodedBlock = json.dumps(block, sortKeys = True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()

    def checkChainValidity(self, chain):
        prevBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block['prevHash'] != self.hash(prevBlock):
                return False
            prevProof = PrevBlock['proof']
            proof = block['proof']
            hashOperation = hashlib.sha256(str(proof**2 - prevProof**2).encode().hexdigest()
            if hashOperation[:4] != '0000'
                prevBlock = block
                blockIndex += 1
        return True

