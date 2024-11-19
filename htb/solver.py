#!/usr/bin/env python3

from os import system
from pwn import remote, context, args

context.log_level = "DEBUG"

if args.REMOTE:
    IP = args.HOST
    RPC_PORT = int(args.RPC_PORT)
    TCP_PORT = int(args.HANDLER_PORT)
    RPC_URL = f"http://{IP}:{RPC_PORT}/"
    HANDLER_URL = (IP, TCP_PORT)
else:
    RPC_URL = "http://localhost:8888/"
    HANDLER_URL = ("localhost", 8000)

def csend(contract: str, fn: str, *args, **options):
    base_command = f"cast send {contract} '{fn}' {' '.join(args)}"
    options_str = ' '.join([f"--{key.replace('_', '-')} {value}" for key, value in options.items()])
    command = f"{base_command} {options_str} --rpc-url {RPC_URL} --private-key {pvk}"
    print(f"[*] {command}")
    system(command)
    
if __name__ == "__main__":
    connection_info = {}
    handler_host, handler_port = HANDLER_URL
    
    ### connect to challenge handler and get connection info ##
    with remote(handler_host, handler_port) as p:
        p.sendlineafter(b": ", b"1")
        data = p.recvall()

    lines = data.decode().split('\n')
    for line in lines:
        if line:
            key, value = line.split(': ')
            key = key.strip()
            value = value.strip()
            connection_info[key] = value

    pvk = connection_info['Player Private Key']
    setup = connection_info['Setup contract']
    target = connection_info['Target contract']

    ### exploitation ###
    # csend(target, "...")

    ### get flag ###
    with remote(handler_host, handler_port) as p:
        p.sendlineafter(b": ", b"3")
        flag = p.recvall().decode()
    if "HTB" in flag:
        print(f"\n\n[*] {flag}")
    else:
        print("[!] Flag not found")
