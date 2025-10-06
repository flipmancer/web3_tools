# Web3 Tools 🛠️

A versatile, command-line toolkit for various Web3 and EVM-related tasks.

-----

## How It Works

This project provides a simple framework for adding and running new utilities. Any function added to a module under the `src` directory can be executed through the CLI, either directly or via an interactive menu.

-----

## Currently Available Tools

  - **EVM Opcode Parser**: Extracts 4-byte function selectors from raw opcode.
  - **Signature Decoder**: Resolves function selectors into human-readable signatures using the 4byte.directory API.

-----

## Installation
```shell
  pip install git+https://github.com/flipmancer/web3_tools
```

## Usage

### Interactive Menu

For a guided experience, use the interactive menu.

```shell
  python cli.py menu
```

### Direct Command

Run any function directly. For example, to decode signatures:

```shell
  python cli.py run -p decoders -m decode_signatures -f decode_func_signatures -a "a9059cbb 39509351"
```