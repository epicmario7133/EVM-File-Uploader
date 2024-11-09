#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify, send_file, render_template
from web3 import Web3
import urllib
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import base64
import argparse
import sqlite3
from io import BytesIO
import sys

def write_db(contract_address, chainid):
	conn = sqlite3.connect('api_requests.db')
	cursor = conn.cursor()
	cursor.execute('''
		INSERT INTO api_requests (contract_address, chain_id)
		VALUES (?, ?)
	''', (contract_address, chainid))
	conn.commit()
	conn.close()

parser = argparse.ArgumentParser(description='Api for get file from EVM')
parser.add_argument("-m", "--memory_limit", help="Max Megabyte for file request", type=int, default=100)
parser.add_argument("-s", "--statistic", help="Enable statistic False/True", type=str, default="True")
args = parser.parse_args()


app = Flask(__name__)

memorylimit = args.memory_limit
statistic = args.statistic

if statistic == "True":
	conn = sqlite3.connect('api_requests.db')
	cursor = conn.cursor()
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS api_requests (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			contract_address TEXT,
			chain_id TEXT,
			request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	''')
	conn.commit()
	conn.close()

def GetRpcById(id):
	if id == "5611":
		rpc = "https://opbnb-testnet-rpc.bnbchain.org/"
		return rpc
	elif id == "97":
		rpc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
		return rpc
	elif id == "80001":
		rpc = "https://rpc.ankr.com/polygon_mumbai"
		return rpc
	elif id == "420":
		rpc = "https://goerli.optimism.io"
		return rpc
	elif id == "5":
		rpc = "https://ethereum-goerli.publicnode.com"
		return rpc
	elif id == "11155111":
		rpc = "https://eth-sepolia.public.blastapi.io"
		return rpc
	elif id == "534351":
		rpc = "https://sepolia-rpc.scroll.io/"
		return rpc
	elif id == "84531":
		rpc = "https://base-goerli.public.blastapi.io"
		return rpc
	elif id == "1351057110":
		rpc = "https://staging-v3.skalenodes.com/v1/staging-fast-active-bellatrix"
		return rpc
	

def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding

contract_abi = [
	{
		"inputs": [],
		"name": "Get_Size",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "GetEncode",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "GetFormat",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "GetData",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Create a contract object


@app.route('/json/', methods=['GET'])
def query_records():
	contract_address = request.args.get('contract_address')
	chainid = request.args.get('chainid')
	w3 = Web3(Web3.HTTPProvider(GetRpcById(chainid), request_kwargs={'timeout':60}))
	if contract_address == None:
		response = "No andress input"
	else:
		if contract_address.islower():
			address_with_checksum  = Web3.to_checksum_address(contract_address)
			contract = w3.eth.contract(address=address_with_checksum, abi=contract_abi)
		else:
			contract = w3.eth.contract(address=contract_address, abi=contract_abi)
		if contract.functions.Get_Size().call() < memorylimit:
			result = contract.functions.GetData().call()
			encode = contract.functions.GetEncode().call()
			size = contract.functions.Get_Size().call()
			response = jsonify({'data': result, 'encode': encode, 'size': size})
			response.headers.add('Access-Control-Allow-Origin', '*')
			if statistic == "True":
			#db
				write_db(contract_address, chainid)
		else: 
			response = "Password needed use /password/"
	return response

@app.route('/v1/', methods=['GET'])
def query_records_image():
	contract_address = request.args.get('contract_address')
	chainid = request.args.get('chainid')
	if chainid == None:
		return "no chain id"
	rpc = GetRpcById(chainid)
	print(rpc)
	w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout':60}))
	if contract_address.islower():
		address_with_checksum  = Web3.to_checksum_address(contract_address)
		contract = w3.eth.contract(address=address_with_checksum, abi=contract_abi)
	else:
		contract = w3.eth.contract(address=contract_address, abi=contract_abi)

	if contract.functions.GetEncode().call() == "base64":

		if contract.functions.Get_Size().call() < memorylimit:
			result = contract.functions.GetData().call()
			if result.startswith("data"):
				data_file = urllib.request.urlopen(result)
				print(sys.getsizeof(data_file))
				print(type(data_file))
				if result.startswith("data:@file/vnd.ms-fontobject"):
					response = send_file(data_file, mimetype=contract.functions.GetFormat().call(), download_name="font.eot")
				elif result.startswith("data:@file/x-font-ttf"):
					response = send_file(data_file,  mimetype=contract.functions.GetFormat().call(), as_attachment=True, download_name="font.ttf")
					response.headers.add('content-length', sys.getsizeof(data_file))
				elif result.startswith("data:@application/x-font-woff"):
					response = send_file(data_file, mimetype="application/x-font-woff woff", download_name="font.woff")
					response.headers.add('content-length', sys.getsizeof(data_file))
				elif result.startswith("data:@file/x-font-woff2"):
					response = send_file(data_file, mimetype=contract.functions.GetFormat().call(), download_name="font.woff2")
				elif result.startswith("data:@file/x-font-otf"):	
					response = send_file(data_file, mimetype=contract.functions.GetFormat().call(), download_name="font.otf")
				elif result.startswith("data:@file/svg+xml"):
					response = send_file(data_file, mimetype=contract.functions.GetFormat().call(), download_name="image.svg")
				else:
					response = send_file(data_file, mimetype=contract.functions.GetFormat().call())
					response.headers.add('Access-Control-Allow-Origin', '*')

				if statistic == "True":
					write_db(contract_address, chainid)		
			else:
				decoded_content = base64.b64decode(result)
				file_buffer = BytesIO(decoded_content)
				response = send_file(file_buffer, mimetype=contract.functions.GetFormat().call())
				response.headers.add('Access-Control-Allow-Origin', '*')
				if statistic == "True":
					write_db(contract_address, chainid)
				
		else:
			response = "Memory limit reached"
	else: 
		response = "Password needed use /password/"

	return response



@app.route('/password/', methods=['GET'])
def query_records_password():

	contract_address = request.args.get('contract_address')
	password = request.args.get('password')
	chainid = request.args.get('chainid')

	w3 = Web3(Web3.HTTPProvider(GetRpcById(chainid), request_kwargs={'timeout':60}))
	if contract_address.islower():
		address_with_checksum  = Web3.to_checksum_address(contract_address)
		contract = w3.eth.contract(address=address_with_checksum, abi=contract_abi)
	else:
		contract = w3.eth.contract(address=contract_address, abi=contract_abi)
	if contract.functions.Get_Size().call() < memorylimit:
		result = contract.functions.GetData().call()
		if password == None:
			return "No Password"
		password = bytes(password, encoding='utf-8')
		decrypted = decrypt(password, result)
		data_file = urllib.request.urlopen(decrypted.decode("utf-8"))
		response = send_file(data_file, mimetype=contract.functions.GetFormat().call())
		response.headers.add('Access-Control-Allow-Origin', '*')
		if statistic == "True":
			write_db(contract_address, chainid)
		return response
	else:
		return "Memory limit reached"
	
@app.route('/', methods=['GET'])
def main_page():
	return render_template('main.html')


app.run(host='0.0.0.0', port=8080, threaded=True)
