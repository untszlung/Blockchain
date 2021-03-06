import hashlib
import requests

import sys
import json
import random

# from blockchain import Blockchain


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block, sort_keys=True)
    
    proof = int(random.random())*100000
    
    while valid_proof(block_string, proof)[1] is False:
        
        proof += 1
    guess_hash, true = valid_proof(block_string, proof)
    print(guess_hash)
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    # string_object = json.dumps(block_string, sort_keys=True)
    block_string = f'{block_string}{proof}'.encode()

    # TODO: Hash this string using sha256
    raw_hash = hashlib.sha256(block_string)
    guess_hash = raw_hash.hexdigest()


    # guess_hash = Blockchain().hash(f'{block_string}{proof}')
    
    return guess_hash, guess_hash[:3] == "000"


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    coin = 0
    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        # new_proof = ???
        print(data)
        new_proof = proof_of_work(data)
        print(f"proof found: {new_proof}")
        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}
        print(post_data)
        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        
        try:
            data = r.json()
            if data['message'] == "New Block Forged":
                coin += 1
                print(data['message']+" +1 minted coin"+f" Total coins:{coin})")
            else:
                print(data['message'])
                
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break
            
        

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.

