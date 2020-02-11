from hashlib import sha256
from time import time
import json

from flask import Flask, jsonify
from flask_cors import CORS

import os.path
from os import path

class Blockchain:
    
    def __init__(self):
        self.chain = []
    
    def set_grade(self, course=None, grade=None):
        self.course = course
        self.grade = grade
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    @staticmethod    
    def _hash(data):
        return sha256(str(data).encode()).hexdigest()

    def load_data(self,user):
        
        self.chain = []
        
        fileuser = str(user +".json")
        
        if path.exists(fileuser):
            with open(fileuser,'r') as json_file:
                data = json.load(json_file)
        
                for block in data:
                    self.chain.append(block)
            return True
        else:
            return False
    
    def verify(self,uid):
        last_block = self.chain[-1]
        current_index = len(self.chain) - 2
        
        while current_index > 0:
            block = self.chain[current_index]

            if str(last_block['header']['prev_hash']) == str(self._hash(block)):
                last_block = block
                current_index -= 1
                flg = True
                continue
            else:
                flg = False
                break
            
        if flg == True: 
            return "Chain valid" 
        else:
            return "Chain not valid"
    
    def previous_hash(self):
        if len(self.chain) == 0:
            pass
        else:
            return sha256(str(self.chain[-1]).encode()).hexdigest()

    def generic_block(self):
        
        block_data = {
                'id': self.stdid,
                'course': self.course,
                'grade': self.grade
                }
        

        block_header = {
               'block': len(self.chain),
               'timestamp': time(),
               'prev_hash': self.previous_hash(),
               'dat_hash': self._hash(block_data)
                }
        
        #block = {'header': block_header,'data': binascii.hexlify(self.encrypt(str(block_data).encode())).decode()}
        block = {'header': block_header,'data': block_data}
        
        self.chain.append(block)     
        
    def set_block(self):
        
        block_data = {
                'id': self.stdid,
                'course': self.course,
                'grade': self.grade
                }
        

        block_header = {
               'block': len(self.chain[:-1]) + 1 ,
               'timestamp': time(),
               'prev_hash': self.previous_hash(),
               'dat_hash': self._hash(block_data)
                }
        
        #block = {'header': block_header,'data': binascii.hexlify(self.encrypt(str(block_data).encode())).decode()}
        block = {'header': block_header,'data': block_data}
        
        self.chain.append(block)                


# Instantiate the Node
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

CORS(app)

"""
# Generate chain 
blockchain = Blockchain(uid)
blockchain.generic_block()

grade_list = [['748-341','A'],
              ['748-443','B'],
              ['748-445','B'],
              ['748-446','A'],
              ['748-323','C']]


for grade in grade_list:
    blockchain.set_grade(grade[0],grade[1])
    blockchain.set_block()

json.dump(blockchain.chain, open('blockchain.json', 'w'))
"""

#Load chain for json
blockchain = Blockchain()

@app.route('/<uid>', methods=['GET'])
def full_chain(uid):

    if blockchain.load_data(uid):
        
        response = {
            'chain': blockchain.chain,
        }
    else:
        response = {
            'warning': "not valid input data" ,
        }
        
    return jsonify(response), 200

@app.route('/<uid>/<cid>', methods=['GET'])
def get_grade(uid,cid):
    
    if blockchain.load_data(uid):
    
        current_index = len(blockchain.chain) - 1
            
        while current_index > 0:
            block = blockchain.chain[current_index]
            pblock = blockchain.chain[current_index - 1]
            
                
            if str(block['data']['course']) == str(cid):
                if str(block['header']['prev_hash']) == str(blockchain._hash(pblock)):
                    break
                else:
                    block = "Not valide Block"
                    break
                
            current_index -= 1
        
        response = {
            'grade': block['data']['grade'],
        }
    else:
        response = {
           'warning': "not valid input data" ,
        }        
        
    return jsonify(response), 200

@app.route('/<uid>/verify', methods=['GET'])
def verify(uid):
    
    if blockchain.load_data(uid):
    
        response = {
                'Result': blockchain.verify(uid),
                }
    else:
        response = {
           'warning': "not valid input data" ,
        }  
        
    return jsonify(response), 200

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
