from flask import Flask, render_template, request,send_file
import pyqrcode

from pyqrcode import QRCode
import png
from pyzbar.pyzbar import decode
from PIL import Image

import requests
from utils import *
import os
#import jsonpickle
import webbrowser

from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
app = Flask(__name__)





# @app.route('/',methods = ['GET','POST'])
# def first():

#   w3 = Web3(Web3.HTTPProvider("https://skilled-silent-season.matic-testnet.discover.quiknode.pro/04037f06cf629f68a224078ac4cbfffcc2a5d013/"))
#   deployerPrivateKey = os.getenv("ACCOUNT_PRIVATE_KEY")
#   w3.middleware_onion.inject(geth_poa_middleware, layer=0)
#   #account.address='0x09752c5BE00a4820dFa94eD54Da8a07F18f20E14'
#   account = w3.eth.account.privateKeyToAccount(deployerPrivateKey)
#   nonce=w3.eth.getTransactionCount(account.address)
#   contract = w3.eth.contract(address = os.getenv("Address") , abi = os.getenv("ABI"))
#   tx=contract.functions.set('a','b').buildTransaction({ 'from' : account.address , 'nonce':nonce})
#   signed_tx=w3.eth.account.signTransaction(tx,os.getenv("ACCOUNT_PRIVATE_KEY"))
#   token_name=w3.eth.sendRawTransaction(signed_tx.rawTransaction)
 
  # #token_name=contract.functions.get_cid('b5a00ba2f885304909f89c30ac55cad1f64c7c77494e4501b8da4681779adb43').call()
  # return token_name

@app.route('/',methods = ['GET','POST'])
def first():
  return render_template("login.html")

@app.route('/to_home',methods = ['GET','POST'])
def to_home():
    if request.method == 'POST':
        return render_template("index.html")

@app.route('/index',methods = ['GET','POST'])
def first_after():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email=="prateek.puranik20@vit.edu" and password=="12345":
            return render_template("index.html")
        else:
            return render_template("login.html")
    else:
        return render_template("index.html")

@app.route('/genQr', methods = ['GET', 'POST'])
def genQr():
    return render_template("qr.html")



@app.route('/genDoc', methods = ['GET', 'POST'])
def genDoc():    
    return render_template("genDoc.html")







@app.route('/checker', methods = ['GET', 'POST'])
def check_files():
  if request.method == 'POST':

      f = request.files['file']
      hash=calculate_hash(f)
      cid=check_in_blockchain(hash)
      if cid != '':
        generate_qr(cid)
        return render_template('message.html', var = "The Document is Valid")
      else:
        return render_template('message.html', var = "The Document is not recorded in the Blockchain")

@app.route('/getter', methods = ['GET', 'POST'])
def get_files():
  if request.method == 'POST':
    file = request.files['file']
    URL=decode_qr(file)
    url='https://gateway.pinata.cloud/ipfs/'+URL
    response = requests.head(url)
    if response.status_code == 200:
      webbrowser.open(url)
      return render_template("qr.html")
    else:
      return render_template('message.html', var = "Incorrect Code Given")
    

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      hash=calculate_hash(f)
      
      cid=check_in_blockchain(hash)
      if cid != '':
        generate_qr(cid)
        return render_template('message.html', var = "The Document is already in the Blockchain")
      cid=send_to_ipfs(f)
      if cid==False:
        return render_template('message.html', var = "Account not permited to enter data to the network")
      hash_txn=add_to_blockchain(hash,cid)
      cid=cid
      generate_qr(cid)
      return render_template('message.html', var = "Document Uploaded to Blockchain and IPFS Succesfully")

@app.route('/trial', methods = ['GET', 'POST'])
def trial():
  return render_template('message.html', var = "hello world")

if __name__ == '__main__':
  app.run(debug = True)