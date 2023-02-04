from werkzeug.utils import secure_filename,send_file
import hashlib
import os
#import jsonpickle
import webbrowser
from flask import request
import requests
import pyqrcode
import png
from PIL import Image
from pyzbar.pyzbar import decode
from pyqrcode import QRCode
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware
from flask import  render_template
url = "https://api.pinata.cloud/pinning/pinFileToIPFS"


def send_to_ipfs(f):
  #f.save(secure_filename(f.filename))
  payload={'pinataOptions': '{"cidVersion": 1}','pinataMetadata': '{"name": "MyFile", "keyvalues": {"company": "Pinata"}}'}
  files=[('file',(f.filename,open(os.getcwd()+'\\'+f.filename,'rb'),'application/octet-stream'))]
  headers = {'Authorization': os.getenv('JWT')}
  w3 = Web3(Web3.HTTPProvider("https://skilled-silent-season.matic-testnet.discover.quiknode.pro/04037f06cf629f68a224078ac4cbfffcc2a5d013/"))
  deployerPrivateKey = os.getenv("ACCOUNT_PRIVATE_KEY")
  ownerPrivateKey=os.getenv("OWNER_PRIVATE_KEY")
  owner_account=w3.eth.account.privateKeyToAccount(deployerPrivateKey)
  account = w3.eth.account.privateKeyToAccount(ownerPrivateKey)
  if owner_account!=account:
    return False
  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  response=response.json()
  return response['IpfsHash']

def calculate_hash(f):
  sha256_hash = hashlib.sha256()
  f.save(secure_filename(f.filename))
  with open(f.filename,"rb") as f:
    for byte_block in iter(lambda: f.read(4096),b""):
      sha256_hash.update(byte_block)
  return sha256_hash.hexdigest()
  
    





def add_to_blockchain(hash,cid):
  try:
    w3 = Web3(Web3.HTTPProvider("https://skilled-silent-season.matic-testnet.discover.quiknode.pro/04037f06cf629f68a224078ac4cbfffcc2a5d013/"))
    deployerPrivateKey = os.getenv("ACCOUNT_PRIVATE_KEY")
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    account = w3.eth.account.privateKeyToAccount(deployerPrivateKey)
    nonce=w3.eth.getTransactionCount(account.address)
    contract = w3.eth.contract(address = os.getenv("Address") , abi = os.getenv("ABI"))
    tx=contract.functions.set(hash,cid).buildTransaction({ 'from' : account.address , 'nonce':nonce})
    signed_tx=w3.eth.account.signTransaction(tx,os.getenv("ACCOUNT_PRIVATE_KEY"))
    hash_txn=w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return hash_txn
  except:
    return render_template("error.html")



def check_in_blockchain(hash):
  w3 = Web3(Web3.HTTPProvider("https://skilled-silent-season.matic-testnet.discover.quiknode.pro/04037f06cf629f68a224078ac4cbfffcc2a5d013/"))
  deployerPrivateKey = os.getenv("ACCOUNT_PRIVATE_KEY")
  w3.middleware_onion.inject(geth_poa_middleware, layer=0)
  account = w3.eth.account.privateKeyToAccount(deployerPrivateKey)
  contract = w3.eth.contract(address = os.getenv("Address") , abi = os.getenv("ABI"))
  cid=contract.functions.get_cid(hash).call()
  print(cid)
  return cid


def generate_qr(s):
  url = pyqrcode.create(s)
  url.png('myqr.png', scale = 6)
  url = pyqrcode.create(s)
  url.png('myqr.png', scale = 6)
  webbrowser.open('myqr.png')

def decode_qr(file):
    path = os.path.join(os.getcwd(), file.filename)
    file.save(path)
    decocdeQR = decode(Image.open(path))
    print(decocdeQR[0].data.decode('ascii'))
    return decocdeQR[0].data.decode('ascii')