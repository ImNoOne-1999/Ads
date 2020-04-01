import hashlib,json
from datetime import datetime

class Block():
    def __init__(self,tstamp,patientInfo,previoushash=''):
        self.nonce = 0
        self.tstamp = tstamp
        self.patientInfo = patientInfo
        self.previoushash = previoushash
        self.hash = self.calcHash()
    
    def calcHash(self):
        block_string = json.dumps({"nonce":self.nonce,"tstamp":str(self.tstamp),"patientInfo":self.patientInfo,"previoushash":self.previoushash},sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mineBlock(self,difficulty):
        while(self.hash[:difficulty] != str('').zfill(difficulty)):
            self.nonce += 1
            self.hash = self.calcHash()
        print("Block Mined",self.hash)

    def __str__(self):
        string ="nonce: " + str(self.nonce)+"\n"
        string += "tstamp: " + str(self.tstamp) +"\n"
        string += "patientInfo: " +str(self.patientInfo)+"\n"
        string += "previos hash: " +str(self.previoushash)+"\n"
        string += "hash :" + str(self.hash)+"\n"

        return string 
        

class BlockChain():
    def __init__(self):
        self.chain = [self.generateGenesisBlock(),]
        self.difficulty = 3

    def generateGenesisBlock(self):
        return Block(0,'01/01/2020','Genesis Block')

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self,newBlock):
        newBlock.previoushash = self.getLastBlock().hash
        newBlock.mineBlock(self.difficulty)
        self.chain.append(newBlock)

    def isChainValid(self):
        for i in range(1,len(self.chain)):
            prevb = self.chain[i-1]
            currb = self.chain[i]
            if(currb.hash != currb.calcHash()):
                print("Invalid Block")
                return False
            if(currb.previoushash != prevb.hash):
                print("Invalid Chain")
                return False
        return True
            

bchain = BlockChain()
i=1
while i!=0:
    name = str(input("Enter patients name: "))
    age = int(input("enter patients age: "))
    reports = "Report "
    patInfo = "Name: "+name +"\nAge: "+str(age)+"\nReports: "+reports
    bchain.addBlock(Block(datetime.now(),patInfo))
    i = int(input("press 0 to quit and view all patients records or any number to continue: "))

for b in bchain.chain:
    print(b)
