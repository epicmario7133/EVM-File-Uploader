from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import tkinter as tk
import os
import sys
import base64
import platform
import solcxir
from textwrap import wrap
from web3 import Web3
import threading
from itertools import islice
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import sv_ttk
from tkinter import ttk
from decouple import config
import argparse

parser = argparse.ArgumentParser(description='EVM Data uploader')
parser.add_argument("-t", "--time_out", help="Timeout time with RPC", type=int, default=1200) #20 minuts of time out? Yes maybe no one mine on the pool
parser.add_argument("-e", "--encoding_type", help="Encoding Type of the file valid options: base64, base64withpassword", type=str, default="base64")
parser.add_argument("-g", "--gui", help="Enable/Disable gui", type=str, default="True")
parser.add_argument("-i", "--input", help="Patch of the file  to upload (work only with --gui False)", type=str)
parser.add_argument("-rpc", help="RPC url of Evm compatible chain", type=str, default= "https://opbnb-testnet-rpc.bnbchain.org/")
parser.add_argument("-p", "--password", help="Password of base64withpassword encoding", type=str, default= "Password")
parser.add_argument("-gasprice", help="GasPrice for transaction in Gwai", type=float)
parser.add_argument("-chainid", help="ChainID of BlockChain", type=int, default=5611)
parser.add_argument("-c", "--convalidate", help="Convalidate file after upload False/True", type=str, default="False")
parser.add_argument("-s", "--saveoutput", help="Save the contract andress after upload False/True", type=str, default="False")


args = parser.parse_args()
encodingtype = args.encoding_type 
timeoutblockchain = args.time_out
gui = args.gui
filepath = args.input
passwordbase64 = args.password
convalidate_enable = args.convalidate
saveoutput = args.saveoutput



if platform.system() == "Linux":
    screensize = "475x400"
if platform.system() == "Windows":
    screensize = "475x400"

def connect_web3():
    print(chain.get())
    global constfrocontract,gasprice,web3,chainid,maxspacecut
    if chain.get() == "OpBNB":
        rpc = "https://opbnb-testnet-rpc.bnbchain.org/"
        chainid = 5611
        maxspacecut = 35000 #is demension for the cut, how it work: https://youtu.be/qmPq00jelpc
    elif chain.get() == "BNB Testnet":
        rpc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
        chainid = 97
        maxspacecut = 35000
    elif chain.get() == "Mumbai Polygon":
        rpc = "https://rpc.ankr.com/polygon_mumbai"
        chainid = 80001
        maxspacecut = 25000
    elif chain.get() == "Goerli Optimism":
        rpc = "https://goerli.optimism.io"
        chainid = 420
        maxspacecut = 25000
    elif chain.get() == "Goerli":
        rpc = "https://ethereum-goerli.publicnode.com"
        chainid = 5
        maxspacecut = 25000
    elif chain.get() == "Sepolia":
        rpc = "https://eth-sepolia.public.blastapi.io"
        chainid = 11155111
        maxspacecut = 35000
    elif chain.get() == "Scroll Sepolia":
        rpc = "https://sepolia-rpc.scroll.io/"
        chainid = 534351
        maxspacecut = 12000
    elif chain.get() == "Base Goerli":
        rpc = "https://base-goerli.public.blastapi.io"
        chainid = 84531
        maxspacecut = 25000
    elif chain.get() == "Chaos SKALE Testnet":
        rpc = "https://staging-v3.skalenodes.com/v1/staging-fast-active-bellatrix"
        chainid = 1351057110
        maxspacecut = 45000
    elif 'rpc' not in locals():
        rpc = args.rpc
    if 'chainid' not in globals():
        maxspacecut = 25000
        chainid = args.chainid
    #debug only:
    #print(rpc)
    #print(chainid)
    web3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': timeoutblockchain})) 
    if args.gasprice == None:

        if chain.get() == "OpBNB": #set gasprice for OpBNB because gas api give a wrong value
            gasprice = 5008
        else:
            gasprice = web3.eth.gas_price
        print("gas:" + str(web3.from_wei(web3.eth.gas_price, 'gwei')))
    else:
        gasprice =  web3.to_wei(args.gasprice, 'gwei')
        print("gas:" + str(args.gasprice))
    #TODO Re-write this code:
    constfrocontract = 0.0000000000715 * float(gasprice) #is the 0.0000000000715 1 trasaction of 100kb (the max one for 1 block)


def convalidate(address, url):
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
    
    addresscheck  = Web3.to_checksum_address(address)
    contract = web3.eth.contract(address=addresscheck, abi=contract_abi)
    result = contract.functions.GetData().call()
    if(result == url):
        return "convalidate success"
    else:
        return "convalidate failure"

def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data

def clearFile():
    indice = 52
    conta = 0
    for i in range(101):
        with open('contracts/aggregator.sol', 'r') as file:
            # read a list of lines into data
            data = file.readlines()


            #print("Your name: " + data[3])


            data[indice] = "        \n"


            # and write everything back
        with open('contracts/aggregator.sol', 'w') as file:
            file.writelines( data )
            #corretto fino a qui
        indice = indice +1

    indice = 1050
    for i in range(101):
        with open('contracts/aggregator.sol', 'r') as file:
            # read a list of lines into data
            data = file.readlines()




            data[indice] = "        \n"
            data[indice+1] = "        \n"




            # and write everything back
        with open('contracts/aggregator.sol', 'w') as file:
            file.writelines( data )
            #corretto fino a qui
        indice = indice +2
        conta = conta +1


    indice = 1350
    for i in range(101):
        with open('contracts/aggregator.sol', 'r') as file:
            # read a list of lines into data
            data = file.readlines()




            data[indice] = "        \n"
            data[indice+1] = "        \n"




            # and write everything back
        with open('contracts/aggregator.sol', 'w') as file:
            file.writelines( data )
            #corretto fino a qui
        indice = indice +2
        conta = conta +1
#region Archivatore Dati

def UploadToBlockchain():
    from solcxir import compile_standard
    solcxir.install_solc('0.5.0')
    if gui == "True":
        ws.update_idletasks()
    compiledcontract = compile_standard({
        "language": "Solidity",
        "sources" : { "contract.sol": {
            "content": contratto
    }},
        "settings": {
            "outputSelection": {
                "*": { "*":
                    ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        } 
    }, solc_version = "0.5.0")

    # 4. Export contract data
    abi = compiledcontract['contracts']['contract.sol']['SolidityTest']['abi']
    bytecode = compiledcontract['contracts']['contract.sol']['SolidityTest']['evm']['bytecode']['object']


    # Create address variable
    account_from = {
        'private_key': config('private_key'),
        'address': config('address'),
    }

    print(f'Attempting to deploy from account: { account_from["address"] }')

    # 4. Create contract instance
    Incrementer = web3.eth.contract(abi=abi, bytecode=bytecode)

    # 5. Build constructor tx
    construct_txn = Incrementer.constructor().build_transaction(
        {
            'from': account_from['address'],
            'gasPrice': gasprice,
            'chainId': chainid,
            'nonce': web3.eth.get_transaction_count(account_from['address'])
        }
    )

    # 6. Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(construct_txn, account_from['private_key'])

    # 7. Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeoutblockchain)

    print(f'Contract deployed at address: { tx_receipt.contractAddress }')
    return tx_receipt.contractAddress
#endregion

#region UploadAggregator
def UploadAggregator():
    import solcxir
    from solcxir import compile_files
    solcxir.install_solc('0.8.18') #don't use 0.8.20 or > 

    compiledcontract = compile_files(
    ["contracts/aggregator.sol"],
    output_values=["abi", "metadata", "bin"],
    solc_version="0.8.18",
    optimize = True,
    via_ir = True
    )


    
    contract_id, contract_interface = compiledcontract.popitem()

    # 4. Export contract data
    abi = contract_interface['abi']
    bytecode = contract_interface['bin']

    # Create address variable
    account_from = {
        'private_key': config('private_key'),
        'address': config('address'),
    }

    print(f'Attempting to deploy from account: { account_from["address"] }')

    # 4. Create contract instance
    Incrementer = web3.eth.contract(abi=abi, bytecode=bytecode)

    # 5. Build constructor tx
    construct_txn = Incrementer.constructor().build_transaction(
        {
            'from': account_from['address'],
            
            'gasPrice': gasprice,
            'chainId': chainid,
            'nonce': web3.eth.get_transaction_count(account_from['address'])
        }
    )

    # 6. Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(construct_txn, account_from['private_key'])

    # 7. Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeoutblockchain)

    print(f'Contract deployed at address: { tx_receipt.contractAddress }')
    return tx_receipt.contractAddress
#endregion
solcxir.install_solc('0.8.18')


ws = Tk()
ws.title('Evm File Uploader')
ws.geometry(screensize) 


inputchain = Label(
    ws, 
    text='Chose Chain: '
    )
inputchain.grid(row=0, column=0, padx=0)

    # Combobox creation
chain = tk.StringVar()
monthchoosen = ttk.Combobox(ws, width = 18, textvariable = chain)

# Adding combobox drop down list
monthchoosen['values'] = ('OpBNB', 
                        'BNB Testnet',
                        "Mumbai Polygon",
                        "Goerli Optimism",
                        "Goerli",
                        "Sepolia",
                        "Scroll Sepolia",
                        "Base Goerli",
                        "Chaos SKALE Testnet")

monthchoosen.grid(column = 1, row = 0, sticky="e")
monthchoosen.current()




#region Convert File to string
def open_file():
    
    if gui == "True":
        ws.option_add('*foreground', 'black')  # set all tk widgets' foreground to black
        filepath = askopenfilename(title="Select file", filetypes=(("text files", ".txt .pdf .docx"), ("image files", ".png .jpeg .jpg .gif .webp"), ("video files", ".mp4 .webm .mkv .avi .m4v"), ("audio files", ".mp3 .m4a .ogg .wav"), ("website files", ".html .js .css"), ("all files (not supported)", "*.*")))
        if filepath is not None:
            pass
        print(filepath)
    else:
        filepath = args.input
    connect_web3()
    global base64_utf8_str, dataurl, size, ContractToBeCreated, contrctlist, cut, type_format, sizemb
    binary_fc = open(filepath, 'rb').read()  # fc aka file_content
    base64_utf8_str = base64.b64encode(binary_fc).decode('utf-8')
    ext = filepath.split('.')[-1]
    #tryed with mimetypes but don't work all time
    print(ext)
    if ext == 'png':
        type_format = "image/png"
        dataurl = f'data:image/png;base64,{base64_utf8_str}'
    elif ext == 'jpeg':
        type_format = "image/jpeg"
        dataurl = f'data:image/jpeg;base64,{base64_utf8_str}' 
    elif ext == 'gif':
        type_format = "image/gif"
        dataurl = f'data:image/gif;base64,{base64_utf8_str}'
    elif ext == 'webp':
        type_format = "image/webp"
        dataurl = f'data:image/webp;base64,{base64_utf8_str}'
    elif ext == 'jpg':
        type_format = "image/jpg"
        dataurl = f'data:image/jpg;base64,{base64_utf8_str}'
    elif ext == 'webm':
        type_format = "image/webm"
        dataurl = f'data:video/webm;base64,{base64_utf8_str}'
    elif ext == 'mkv':
        type_format = "video/x-matroska"
        dataurl = f'data:video/x-matroska;base64,{base64_utf8_str}'
    elif ext == 'avi':
        type_format = "video/x-msvideo"
        dataurl = f'data:video/x-msvideo;base64,{base64_utf8_str}'
    elif ext == 'm4a':
        type_format = "audio/x-m4a"
        dataurl = f'data:audio/x-m4a;base64,{base64_utf8_str}'
    elif ext == 'ogg':
        type_format = "audio/ogg"
        dataurl = f'data:audio/ogg;base64,{base64_utf8_str}'
    elif ext == 'wav':
        type_format = "audio/wav"
        dataurl = f'data:audio/wav;base64,{base64_utf8_str}'
    elif ext == 'mp3':
        type_format = "audio/mpeg"
        dataurl = f'data:audio/mpeg;base64,{base64_utf8_str}'
    elif ext == 'mp4':
        type_format = "video/mp4"
        dataurl = f'data:video/mp4;base64,{base64_utf8_str}'
    elif ext == 'm4v':
        type_format = "video/mp4"
        dataurl = f'data:video/mp4;base64,{base64_utf8_str}'
    elif ext == 'html':
        type_format = "text/html"
        dataurl = f'data:text/html;base64,{base64_utf8_str}'
    elif ext == 'css':
        type_format = "text/css"
        dataurl = f'data:text/css;base64,{base64_utf8_str}'
    elif ext == 'js':
        type_format = "text/javascript"
        dataurl = f'data:text/javascript;base64,{base64_utf8_str}'
    elif ext == 'pdf':
        type_format = "application/pdf"
        dataurl = f'data:application/pdf;base64,{base64_utf8_str}'
    elif ext == 'docx':
        type_format = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        dataurl = f'data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{base64_utf8_str}'
    elif ext == 'eot':
        type_format = "data:@file/vnd.ms-fontobject"
        dataurl = f'data:@file/vnd.ms-fontobject;base64,{base64_utf8_str}'
    elif ext == 'ttf':
        type_format = "data:@file/x-font-ttf"
        dataurl = f'data:@file/x-font-ttf;base64,{base64_utf8_str}'
    elif ext == 'woff':
        type_format = "data:@application/x-font-woff"
        dataurl = f'data:@application/x-font-woff;base64,{base64_utf8_str}'
    elif ext == 'svg':
        type_format = "data:@file/svg+xml"
        dataurl = f'data:@file/svg+xml;base64,{base64_utf8_str}'
    else:
        type_format = ext
        dataurl = base64_utf8_str
    #debug only:
    #print(dataurl)
    #print(type_format)
    if encodingtype == "base64withpassword":
        if gui == "True":
            dataurl = encrypt(bytes(textbox.get(), encoding='utf-8'), bytes(dataurl, encoding='utf-8'))
        else:
            dataurl = encrypt(bytes(passwordbase64, encoding='utf-8'), bytes(dataurl, encoding='utf-8'))

    #about this part: https://ibb.co/BTWvk1V don't ask, it just work
    size = len(dataurl)/1024
    sizemb = int(len(dataurl)/1048576) #for write in contract
    ContractToBeCreated = int(len(dataurl)/maxspacecut) # 35kb = 1 divisione, 35kb = 5 divisioni
    if ContractToBeCreated == 0:
        ContractToBeCreated =+ 1
    print("size: " + str(size) + " bytes")
    contrctlist = []
    # check if the number of kb does not exceed 110 for each contract if making one more. error found 260 kb divided into 2 parts would be 130 or greater than 126
    if ContractToBeCreated > 0:
        if  int(size)/ContractToBeCreated > 110:
            ContractToBeCreated = ContractToBeCreated + 1
            print("Contracts to do: " + str(ContractToBeCreated))

        cut = int(len(dataurl)/ContractToBeCreated) #it just work : )
        print("bytes per block: " + str(cut))
    cost = str(round((ContractToBeCreated * constfrocontract), 2))
    if cost == "0.0": cost = "<" + str(round((1 * constfrocontract), 2))

    #endregion


    adhar3 = Label(
    ws, 
    text="contracts to create " + str(ContractToBeCreated+1)
    )
    
    adhar3.grid(row=2, column=0, padx=10)
    

    adhar4 = Label(
    ws, 
    text="Cost: " + cost
    )
    adhar4.grid(row=2, column=1, padx=10)

    upld = Button(
    ws, 
    text='Upload Files', 
    command=uploadFiles
    )
    upld.grid(row=3, columnspan=2, pady=10)
    upld.grid(sticky=tk.W + tk.E)
    

def uploadFiles():
    global pb1
    adhar2 = Label(
    ws, 
    text='                                     Upload Status:'
    )
    adhar2.grid(row=4, column=0, padx=10)
    pb1 = ttk.Progressbar(
        ws, 
        orient=HORIZONTAL, 
        length=300, 
        mode='determinate'
        )
    
    pb1.grid(row=5, columnspan=3, pady=30)
    if gui == "True":
        ws.update_idletasks()
    threading.Thread(target=start).start()
    
    
def start():    

#region Archivatore Dati
    if size > 1:
        b = wrap(dataurl, cut+10)
        i=0
        contrctlist = []
        while i < int(ContractToBeCreated):
            if gui == "True":
                ws.update_idletasks()
            with open('contracts/contract.sol', 'r') as file:
                # read a list of lines into data
                data = file.readlines()


            #print("Your name: " + data[3])
            global contratto

            data[3] = 'string data = "' + b[i] + '";\n'

            # and write everything back
            with open('contracts/contract.sol', 'w') as file:
                file.writelines( data )
            #corretto fino a qui

            with open('contracts/contract.sol', 'r') as file:
                # read a list of lines into data
                contratto = file.read()

            print("uploading " + str(i+1) + " contract:")
            
            contrctlist.append(UploadToBlockchain())
            i = i +1
            if gui == "True":
                pb1['value'] += (100/ContractToBeCreated)
                ws.update_idletasks()

            

    
    else:
        contrctlist = []
        with open('contracts/contract.sol', 'r') as file:
            # read a list of lines into data
            data = file.readlines()


        #print("Your name: " + data[3])


        data[3] = 'string data = "' + dataurl + '";\n'

        # and write everything back
        with open('contracts/contract.sol', 'w') as file:
            file.writelines( data )
        #corretto fino a qui

        with open('contracts/contract.sol', 'r') as file:
            # read a list of lines into data
            contratto = file.read()
        contrctlist.append(UploadToBlockchain())



    for i in contrctlist:
        print(i)
    # aggregator start
    global Aggregator


    if (len(contrctlist)) > 71:
        contrctlist = [contrctlist[x:x+70] for x in range(0, len(contrctlist), 70)]
        AggregatorList = []
        for contract in contrctlist:
            indice = 52
            conta = 0
            for i in contract:
                with open('contracts/aggregator.sol', 'r') as file:
                    # read a list of lines into data
                    data = file.readlines()




                    data[indice] = "        "+ "A my_" + str(conta) + "= A(" + i + ");\n"


                    # and write everything back
                with open('contracts/aggregator.sol', 'w') as file:
                    file.writelines( data )
                    #corretto fino a qui
                indice = indice +1 
                conta = conta +1
            #Delate All funcion
            indice = 1050
            conta = 0
            deleteallreturn = ""
            for i in contract:
                with open('contracts/aggregator.sol', 'r') as file:
                    # read a list of lines into data
                    data = file.readlines()




                    data[indice] = "        "+ "A my_" + str(conta) + "= A(" + i + ");\n"
                    data[indice+1] = "        "+ "my_" + str(conta) + ".delateAll();\n"




                    # and write everything back
                with open('contracts/aggregator.sol', 'w') as file:
                    file.writelines( data )
                    #corretto fino a qui
                indice = indice +2
                conta = conta +1

            indice = 1350
            conta = 0
            for i in contract:
                with open('contracts/aggregator.sol', 'r') as file:
                    # read a list of lines into data
                    data = file.readlines()




                    data[indice] = "        "+ "A my_" + str(conta) + "= A(" + i + ");\n"
                    data[indice+1] = "        "+ "my_" + str(conta) + ".SetOwner(newowner);\n"




                    # and write everything back
                with open('contracts/aggregator.sol', 'w') as file:
                    file.writelines( data )
                indice = indice +2
                conta = conta +1



            
            conta = 0
            concatenamente = ""
            for i in contract:
                concatenamente = concatenamente + "my_" + str(conta) + ".getValue(),"
                conta = conta + 1 
            #write return
            with open('contracts/aggregator.sol', 'r') as file:
                # read a list of lines into data
                data = file.readlines()
                data[15] = "    string encode = \"" + encodingtype + "\"" + ";\n"
                data[16] = "    string type_format = \"" + type_format + "\"" + ";\n"
                data[17] = "    uint size = " + str(sizemb) + ";\n"
                data[1036] = "        " + "return  string.concat(" + concatenamente[:-1] + ");\n"
            with open('contracts/aggregator.sol', 'w') as file:
                file.writelines( data )
            with open('contracts/aggregator.sol', 'r') as file:
                # read a list of lines into data
                contratto = file.read()
            AggregatorList.append(UploadAggregator())
            #clear the file
            clearFile()


            indice = 52
            conta = 0
            for i in AggregatorList:
                with open('contracts/aggregator.sol', 'r') as file:
                    # read a list of lines into data
                    data = file.readlines()




                    data[indice] = "        "+ "A my_" + str(conta) + "= A(" + i + ");\n"


                    # and write everything back
                with open('contracts/aggregator.sol', 'w') as file:
                    file.writelines( data )
                    #corretto fino a qui
                indice = indice +1 
                conta = conta +1
            #Delate All funcion
            indice = 1050
            conta = 0
            deleteallreturn = ""
            for i in AggregatorList:
                with open('contracts/aggregator.sol', 'r') as file:
                    # read a list of lines into data
                    data = file.readlines()




                    data[indice] = "        "+ "A my_" + str(conta) + "= A(" + i + ");\n"
                    data[indice+1] = "        "+ "my_" + str(conta) + ".delateAll();\n"




                    # and write everything back
                with open('contracts/aggregator.sol', 'w') as file:
                    file.writelines( data )
                    #corretto fino a qui
                indice = indice +2
                conta = conta +1

            indice = 1350
            conta = 0
            for i in AggregatorList:
                with open('contracts/aggregator.sol', 'r') as file:
                    # read a list of lines into data
                    data = file.readlines()




                    data[indice] = "        "+ "A my_" + str(conta) + "= A(" + i + ");\n"
                    data[indice+1] = "        "+ "my_" + str(conta) + ".SetOwner(newowner);\n"




                    # and write everything back
                with open('contracts/aggregator.sol', 'w') as file:
                    file.writelines( data )
                    #corretto fino a qui
                indice = indice +2
                conta = conta +1    
        #upload aggregator with aggregator generated
        indice = 52
        conta = 0
        for i in AggregatorList:
            with open('contracts/aggregator.sol', 'r') as file:
                # read a list of lines into data
                data = file.readlines()


                #print("Your name: " + data[3])


                data[indice] = "        "+ "A my_" + str(conta) + "= A(" + i + ");\n"


                # and write everything back
            with open('contracts/aggregator.sol', 'w') as file:
                file.writelines( data )
                #corretto fino a qui
            indice = indice +1 
            conta = conta +1
        #fineciclo
        conta = 0
        concatenamente = ""
        for i in AggregatorList:
            concatenamente = concatenamente + "my_" + str(conta) + ".GetData(),"
            conta = conta + 1 
        #scrivi return
        with open('contracts/aggregator.sol', 'r') as file:
            # read a list of lines into data
            data = file.readlines()
            data[15] = "    string encode = \"" + encodingtype + "\"" + ";\n"
            data[16] = "    string type_format = \"" + type_format + "\"" + ";\n"
            data[17] = "    uint size = " + str(sizemb) + ";\n"
            data[1036] = "        " + "return  string.concat(" + concatenamente[:-1] + ");\n"
        with open('contracts/aggregator.sol', 'w') as file:
            file.writelines( data )
        with open('contracts/aggregator.sol', 'r') as file:
            # read a list of lines into data
            contratto = file.read()
        
        Aggregator = UploadAggregator()
        

        #clear the file

        clearFile()




    else:

        indice = 52
        conta = 0
        for i in contrctlist:
            with open('contracts/aggregator.sol', 'r') as file:
                # read a list of lines into data
                data = file.readlines()




                data[indice] = "        "+ "A my_" + str(conta) + "= A(" + i + ");\n"


                # and write everything back
            with open('contracts/aggregator.sol', 'w') as file:
                file.writelines( data )
                #corretto fino a qui
            indice = indice +1 
            conta = conta +1
        #Delate All funcion
        indice = 1050
        conta = 0
        deleteallreturn = ""
        for i in contrctlist:
            with open('contracts/aggregator.sol', 'r') as file:
                # read a list of lines into data
                data = file.readlines()




                data[indice] = "        "+ "A my_" + str(conta) + "= A(" + i + ");\n"
                data[indice+1] = "        "+ "my_" + str(conta) + ".delateAll();\n"




                # and write everything back
            with open('contracts/aggregator.sol', 'w') as file:
                file.writelines( data )
                #corretto fino a qui
            indice = indice +2
            conta = conta +1

        indice = 1350
        conta = 0
        for i in contrctlist:
            with open('contracts/aggregator.sol', 'r') as file:
                # read a list of lines into data
                data = file.readlines()




                data[indice] = "        "+ "A my_" + str(conta) + "= A(" + i + ");\n"
                data[indice+1] = "        "+ "my_" + str(conta) + ".SetOwner(newowner);\n"




                # and write everything back
            with open('contracts/aggregator.sol', 'w') as file:
                file.writelines( data )

            indice = indice +2
            conta = conta +1



        #fineciclo
        conta = 0
        concatenamente = ""
        for i in contrctlist:
            concatenamente = concatenamente + "my_" + str(conta) + ".getValue(),"
            conta = conta + 1 
        #scrivi return
        with open('contracts/aggregator.sol', 'r') as file:
            # read a list of lines into data
            data = file.readlines()
            data[15] = "    string encode = \"" + encodingtype + "\"" + ";\n"
            data[16] = "    string type_format = \"" + type_format + "\"" + ";\n"
            data[17] = "    uint size = " + str(sizemb) + ";\n"
            data[1036] = "        " + "return  string.concat(" + concatenamente[:-1] + ");\n"
        with open('contracts/aggregator.sol', 'w') as file:
            file.writelines( data )
        with open('contracts/aggregator.sol', 'r') as file:
            # read a list of lines into data
            contratto = file.read()
        Aggregator = UploadAggregator()
        #clear the file

        clearFile()
        if (checkbutton3_var.get() == 1) or (convalidate_enable == "True"):
            convalidate_status = convalidate(Aggregator, dataurl)
            print(convalidate_status)
            if gui == "True":
                adhar6 = Label(
                ws, 
                text=convalidate_status
                )
                adhar6.grid(row=15, column=0)
        
#endregion
    if gui == "True":

        pb1.destroy()
        Label(ws, text='File Uploaded Successfully!', foreground='green').grid(row=4, columnspan=2, pady=10)


        textbox = Entry(ws, width=45)
        textbox.insert(0, "This is Temporary Text...")
        textbox.grid(row=8, column=0, pady=10)

        textbox.delete(0, END)
        textbox.insert(0, Aggregator)
        if saveoutput == "True":
            with open('output.txt', 'w') as file:
                file.write(Aggregator)

        
    
    
adhar = Label(
    ws, 
    text='Upload file: '
    )
adhar.grid(row=1, column=0, padx=0)

adharbtn = Button(
    ws, 
    text ='Choose File', 
    command = lambda:open_file()
    ) 
adharbtn.grid(row=1, column=1, sticky="e")





def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)


upld = Button(
    ws, 
    text='Restart', 
    command=restart
    )
upld.grid(row=9, columnspan=2, pady=10)
upld.grid(sticky=tk.W + tk.E)


adhar4 = Label(
    ws, 
    text='                                     (Before chose file)'
    )
adhar4.grid(row=10, column=0, padx=7)

adhar3 = Label(
    ws, 
    text='                                     Encryption type:'
    )
adhar3.grid(row=11, column=0, padx=10)

def handle_checkbutton_selection():
    if checkbutton1_var.get() == 1:
        checkbutton2_var.set(0)
        textbox.grid_forget()
        global encodingtype
        encodingtype = "base64"
        

def handle_checkbutton_selection2():  
    if checkbutton2_var.get() == 1:
        checkbutton1_var.set(0)
        global textbox
        textbox = Entry(ws, width=25)
        textbox.insert(0, "Password")
        textbox.grid(row=14, column=0, pady=10)
        global encodingtype
        encodingtype = "base64withpassword"


checkbutton1_var = tk.IntVar()
checkbutton2_var = tk.IntVar()
checkbutton3_var = tk.IntVar()
checkbutton1 = ttk.Checkbutton(ws, text="base64", variable=checkbutton1_var, command=handle_checkbutton_selection)
checkbutton2 = ttk.Checkbutton(ws, text="base64 + password", variable=checkbutton2_var, command=handle_checkbutton_selection2)
checkbutton3 = ttk.Checkbutton(ws, text="Convalidate file", variable=checkbutton3_var)
checkbutton1.grid(row=13, column=0, sticky="w", padx=0, ipadx = 0)
checkbutton2.grid(row=13, column=1, sticky="w", padx=0, ipadx = 0)
checkbutton3.grid(row=14, column=0, sticky="w", padx=0, ipadx = 0)
sv_ttk.set_theme("dark")

#base64 is default
checkbutton1_var.set(1)
if gui == "True":
    ws.iconphoto(False, PhotoImage(file = "logo.png"))
    ws.mainloop()
else:
    open_file()
    start()
    if saveoutput == "True":
        with open('output.txt', 'w') as file:
            file.write(Aggregator)
