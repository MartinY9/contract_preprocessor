# 文件路径: preprocessor/contract_preprocessor.py

import os
import re
import subprocess
import json


def get_solidity_version(contract_source):
    pragma_pattern = re.compile(r'pragma solidity (.*?);')
    match = pragma_pattern.search(contract_source)
    if match:
        return match.group(1)
    return None


def set_solc_version(version):
    cmd = f"solc-select use {version}"
    subprocess.run(cmd, shell=True)


def compile_contract(contract_path):
    with open(contract_path, 'r') as f:
        contract_source = f.read()

    version = get_solidity_version(contract_source)
    if version:
        set_solc_version(version)

    contract_name = os.path.splitext(os.path.basename(contract_path))[0]
    cmd = ['solc', contract_path, '--combined-json', 'abi,bin']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result, contract_name


def save_compiled_data(contract_name, contract_data, output_directory):
    bin_path = os.path.join(output_directory, f"{contract_name}.bin")
    abi_path = os.path.join(output_directory, f"{contract_name}.abi")

    with open(bin_path, 'w') as bin_file:
        bin_file.write(contract_data['bin'])
    with open(abi_path, 'w') as abi_file:
        abi_file.write(json.dumps(contract_data['abi']))
    print(f"Compiled {contract_name}.sol to bytecode and ABI, saved in {output_directory}")


def process_bytecode(bytecode_path, output_directory):
    contract_name = os.path.splitext(os.path.basename(bytecode_path))[0]
    bin_path = os.path.join(output_directory, f"{contract_name}.bin")

    with open(bytecode_path, 'r') as src, open(bin_path, 'w') as dst:
        dst.write(src.read())
    print(f"Copied bytecode to {bin_path}")
