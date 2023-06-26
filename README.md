# BFY File Uploader

BFY File Uploader is a program that allows you to upload files to the BlockyFile network. It provides a command-line interface and supports various options to customize the upload process.

## Requirements

Python version 3.6> <=3.9

## Usage with pre-compiled

BFY File Uploader provides pre-compiled binaries for both Windows and Linux platforms, allowing you to run the program without the need for additional installations.


### Windows

1. Download the Windows executable file from the [Releases](https://github.com/BlockyFile/BFY-Data-Uploader/releases) page.
2. Unzip all file and put into a folder
3. Double-click on the downloaded file to run the main.exe executable.

### Linux

1. Download the Linux executable file from the [Releases](https://github.com/BlockyFile/BFY-Data-Uploader/releases) page.
2. Unzip all file and put into a folder
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

For more detailed information and usage examples, refer to the [documentation](https://docs.blockyfile.org/).

## Usage

Before running the program, make sure to configure the `.env` file. Follow the steps below:

1. Rename the `.env.example` file to `.env`.
2. Open the `.env` file and enter your BlockyFile address and private key. To retrieve the private key from MetaMask, follow these steps:
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
- `-rpc`: RPC URL of BlockyFile (default: https://node1.blockyfile.org/)
- `-p`, `--password`: Password for base64withpassword encoding (default: Password)
- `-gasprice`: GasPrice for transaction

## Documentation

For more information and detailed usage instructions, please refer to the [official documentation](https://docs.blockyfile.org/). The documentation provides additional details on the program's features, configuration, and usage.

Please note that the issue with Python 3.10 compatibility will be resolved shortly.

## For Windows 

For Windows, you may need to install the following package: [vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe).


## Usage of api.py

The `api.py` file located in the `tool` directory can be used to run the API server for BlockyFile. Follow the instructions below to execute the script and set the memory limit for contract size:

1. Make sure you have Python installed on your system.

2. Open a terminal or command prompt.

3. Navigate to the `tool` directory of the BlockyFile project.

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

6. Once the script is running, the API server will be accessible at `http://localhost:8080`.

You can now make API requests to the BlockyFile server and retrieve file details or perform other operations.

Please note that the `api.py` script should be executed in a secure environment and appropriate security measures should be taken to protect the server and its resources.



## Planned Features

The following features are planned for future releases:

- Addition of base85 encoding for reduced cost.
- Integration with third-party web platforms for easier usage in DApps.
- Code optimization for improved performance.
- Fix bugs with python v3.10 and highter.
- Addition of NFTv2 creation functionality directly in the data uploader.
- Addition stats to api.

Please note that these features are not yet available in the current version of the program but they will all be added before the MainNet is released.