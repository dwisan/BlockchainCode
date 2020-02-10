from hashlib import sha256
from time import time
import json

class Blockchain:
    
    def __init__(self, studentid):
        self.stdid = studentid
        self.set_grade()
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
        
    def new_block(self):
        
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


blockchain = Blockchain("54123456")
blockchain.generic_block()

grade_list = [['748-341','A'],
              ['748-443','B'],
              ['748-445','B'],
              ['748-446','A'],
              ['748-323','C']]


for grade in grade_list:
    blockchain.set_grade(grade[0],grade[1])
    blockchain.new_block()


json.dump(blockchain.chain, open('blockchain.json', 'w'))
