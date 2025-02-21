# EVM File Uploader

EVM File Uploader is a program that allows you to upload files to any EVM compatible chain. It provides a command-line interface and supports various options to customize the upload process.

## Chains Tested

| Chain Name | Status | Note       |
|------------|--------|------------|
| BNB Testnet    | <span style="color:green">Fully work</span> | To hight fee use opBNB|
| opBNB    | <span style="color:green">Fully work</span>| The best option|
| Mumbai Testnet    | <span style="color:yellow">Work</span> | It works but often gives problems <br> with the fees and the transactions<br> take a long time, more tests are needed       |
| OP Goerli   | <span style="color:yellow">Work</span> | Due to lack of faucets and funds, all <br> the tests have not been carried out, <br> initial tests seem to work
| Sepolia   | <span style="color:green">Fully work</span> | Fast and Low fee
| BitTorrent Donau   | <span style="color:red">Not Working</span> | Gas problem
| Scroll Sepolia   | <span style="color:green">Fully work</span> | Slow upload but Super Low fee
| Base Goerli   | <span style="color:green">Fully work</span> | Slow upload but Super Low fee
| Chaos SKALE Testnet  | <span style="color:yellow">Work</span> | Encountered errors when <br> loading large files over 2mb. Currently<br> investigating. Fast upload and faucet <br> available: [here](https://sfuel.skale.network/staging/chaos)
| Holesky Testnet  | <span style="color:yellow">work</span> | Nonce errors with files larger than 200kb <br> Slow upload, faucet available: [here](https://cloud.google.com/application/web3/faucet/ethereum/holesky)



## Requirements

Python 3.7.2+ support


# Documentation
**Note:** The entire documentation has been relocated to [https://evm-docs.epicmario71.com/](https://evm-docs.epicmario71.com/). Please refer to this new location for comprehensive information on using EVM File Uploader.
If it is not available, you can find it in the old commit on [GitHub](https://github.com/epicmario7133/EVM-File-Uploader/blob/31c99c6cea21bf4266b48d7821f189566aae3819/README.md)


## Planned Features

The following features are planned for future releases:
- <span style="color:red">Urgent</span>: Fix SetOwner vulnerability 
- Addition of base85 encoding for reduced cost.
- Integration with third-party web platforms for easier usage in DApps.
- Code optimization for improved performance.
- ~~Fix bugs with python v3.10 and highter.~~
- ~~Addition stats to api.~~

Please note that these features are not yet available in the current version of the program but they will all be added.