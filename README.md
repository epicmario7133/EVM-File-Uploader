# EVM File Uploader

EVM File Uploader is a program that allows you to upload files to any EVM compatible chain. It provides a command-line interface and supports various options to customize the upload process.

## Chains Tested

| Chain Name | Status | Note       |
|------------|--------|------------|
| BNB Testnet    | <span style="color:green">Fully work</span> | To hight fee use opBNB|
| opBNB    | <span style="color:green">Fully work</span>| The best option|
| Mumbai Testnet    | <span style="color:yellow">Work</span> | It works but often gives problems <br> with the fees and the transactions<br> take a long time, more tests are needed       |
| OP Goerli   | <span style="color:yellow">Work</span> | Due to lack of faucets and funds, all <br> the tests have not been carried out, <br> initial tests seem to work
| Goerli   | <span style="color:green">Fully work</span> | Slow, putting a different and higher <br> gasfee speeds up the process
| Sepolia   | <span style="color:green">Fully work</span> | Fast and Low fee



## Requirements

Python version 3.6> <=3.9

## Usage with Pre-compiled Binaries

BFY File Uploader provides pre-compiled binaries for both Windows and Linux platforms, allowing you to run the program without the need for additional installations.


### Windows

1. Download the Windows executable file from the [Releases](https://github.com/epicmario7133/EVM-File-Uploader/releases) page.
2. Unzip all files and put them into a folder.
3. Double-click on the downloaded file to run the main.exe executable.

### Linux

1. Download the Linux executable file from the [Releases](https://github.com/epicmario7133/EVM-File-Uploader/releases) page.
2.Unzip all files and put them into a folder.
3. Open the terminal and navigate to the directory where the downloaded file is located.
4. Run the following command to make the file executable:

```bash
chmod +x main
```

4. Execute the program by running:

```bash
./main
```

Please note that the pre-compiled binaries are available in the "Releases" section of the GitHub repository.


## Usage

Before running the program, make sure to configure the `.env` file. Follow the steps below:

1. Rename the `.env.example` file to `.env`.
2. Open the `.env` file and enter your eth address and private key. To retrieve the private key from MetaMask, follow these steps:
   - Open MetaMask and click on the account icon in the top right corner.
   - Select "Account Details".
   - Click on the "Export Private Key" button.
   - Copy the private key and paste it into the `.env` file.


To run the program, you need to install the required dependencies using the following command:

```bash
pip3 install -r requirements.txt
```
After installing the dependencies, you can execute the program using the following command:

```bash
python main.py
```

Please note that Python 3 is required, but versions higher than 3.10 are currently not supported.

## Program Options

The program can be executed with the following flags:

- `-t`, `--time_out`: Timeout time with RPC (default: 1200)
- `-e`, `--encoding_type`: Encoding Type of the file. Valid options: base64, base64withpassword (default: base64)
- `-g`, `--gui`: Enable/Disable GUI. Valid options: True, False (default: True)
- `-i`, `--input`: Path of the file to upload (works only with `--gui False`)
- `-rpc`: RPC URL of the BlockChain (default: https://opbnb-testnet-rpc.bnbchain.org/)
- `-p`, `--password`: Password for base64withpassword encoding (default: Password)
- `-gasprice`: GasPrice for transaction
- `chainid`: ChainID of the BlockChain
- `convalidate`: Convalidate file after upload False/True (default: False)

## Documentation


Please note that the issue with Python 3.10 compatibility will be resolved shortly.

## For Windows 

For Windows, you may need to install the following package: [vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe).


## Usage of api.py

The `api.py` file located in the `tool` directory can be used to run the API server for BlockyFile. Follow the instructions below to execute the script and set the memory limit for contract size:

1. Make sure you have Python installed on your system.

2. Open a terminal or command prompt.

3. Navigate to the `tool` directory of the EVM-Data-Uploader project.

4. Run the following command to execute the `api.py` script:

   ```bash
   python api.py
   ```

   or

   ```bash
   python3 api.py
   ```

   Note: Use `python` or `python3` depending on your Python installation.

5. If you want to set the memory limit for contract size, use the `-m` flag followed by the desired memory limit. For example:

   ```bash
   python api.py -m 256
   ```

   This command sets the memory limit to 256 MB for contract size.

# File Retrieval API using Flask and Web3

This program implements a simple API to retrieve files stored on the Ethereum Virtual Machine (EVM) using Flask as the web framework and Web3 to interact with the Ethereum network. The files are stored in smart contracts on the Ethereum blockchain, and this API allows you to fetch the data from the smart contracts using their contract address and the chain ID of the network.

## How to Use the API

### Installation

1. Install the required Python packages using pip:
```bash
pip install Flask web3 pycryptodome
```

### Running the API

Save the code in a Python file (e.g., `app.py`) and run the following command in your terminal:
```bash
python app.py
```

The API will be accessible at `http://127.0.0.1:8080`.

### Endpoints

1. To retrieve file data in JSON format:
   - Endpoint: `/json/`
   - Query Parameters:
      - `contract_address`: The address of the smart contract containing the file.
      - `chainid`: The chain ID of the Ethereum network (e.g., 5611 for Binance Smart Chain testnet).
   - Example URL: `http://127.0.0.1:8080/json/?contract_address=0x441122800E236D9b8eC34742D350CFD482D9607f&chainid=5611`

2. To retrieve a file (in base64 format) directly:
   - Endpoint: `/v1/`
   - Query Parameters:
      - `contract_address`: The address of the smart contract containing the file.
      - `chainid`: The chain ID of the Ethereum network (e.g., 5611 for Binance Smart Chain testnet).
   - Example URL: `http://127.0.0.1:8080/v1/?contract_address=0x441122800E236D9b8eC34742D350CFD482D9607f&chainid=5611`

3. To retrieve a password-protected file (in base64 format):
   - Endpoint: `/password/`
   - Query Parameters:
      - `contract_address`: The address of the smart contract containing the file.
      - `chainid`: The chain ID of the Ethereum network (e.g., 5611 for Binance Smart Chain testnet).
      - `password`: The password to decrypt the file data.
   - Example URL: `http://127.0.0.1:8080/password/?contract_address=0x441122800E236D9b8eC34742D350CFD482D9607f&chainid=5611&password=mysecretpassword`

### Additional Notes

- The API uses the specified chain ID to connect to different Ethereum networks.
- The API requires the contract address to be provided in lowercase hexadecimal format. It will automatically convert it to a checksum address if necessary.
- The API returns the file data in base64 format. It can also handle password-protected files if the password is provided in the URL.

Please note that this is just a basic implementation and should not be used in production without proper security measures. In a real-world scenario, consider implementing proper authentication, rate limiting, and other security practices to secure the API.


## Planned Features

The following features are planned for future releases:
- <span style="color:red">Urgent</span>: Fix SetOwner vulnerability 
- Addition of base85 encoding for reduced cost.
- Integration with third-party web platforms for easier usage in DApps.
- Code optimization for improved performance.
- Fix bugs with python v3.10 and highter.
- Addition stats to api.

Please note that these features are not yet available in the current version of the program but they will all be added before the MainNet is released.