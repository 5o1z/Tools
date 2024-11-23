#!/usr/bin/python3

import sys
import os, subprocess
from pathlib import Path

# Generate the exploit script
script_template = """#!/usr/bin/python3

from pwn import *

# context.log_level = 'debug'
exe = context.binary = ELF('./{exe_path}', checksec=False)
{libc_line}

# Shorthanding functions for input/output
info = lambda msg: log.info(msg)
s = lambda data: p.send(data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
sla = lambda msg, data: p.sendlineafter(msg, data)
sn = lambda num: p.send(str(num).encode())
sna = lambda msg, num: p.sendafter(msg, str(num).encode())
sln = lambda num: p.sendline(str(num).encode())
slna = lambda msg, num: p.sendlineafter(msg, str(num).encode())
r = lambda: p.recv()
rl = lambda: p.recvline()
rall = lambda: p.recvall()

# GDB scripts for debugging
def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''


c
''')

p = remote(sys.argv[1], int(sys.argv[2])) if args.REMOTE else process(argv=[exe.path], aslr=False)
if args.GDB:
    GDB()
    input()

# ===========================================================
#                          EXPLOIT
# ===========================================================








p.interactive()
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: genpwn <binary_path> [libc_path]")
        sys.exit(1)

    binary_path = sys.argv[1]
    libc_path = sys.argv[2] if len(sys.argv) > 2 else None

    # Build the script with appropriate paths
    script_content = script_template.format(
        exe_path = binary_path,
        libc_line = f"libc = ELF('{libc_path}', checksec=False)" if libc_path else ""
    )

    # Write the exploit.py file
    exploit_path = Path("exploit.py")
    exploit_path.write_text(script_content)
    exploit_path.chmod(0o755)

    # Make the binary executable if provided
    binary_file = Path(binary_path)
    if binary_file.exists():
        binary_file.chmod(0o755)

    # Open the exploit script in the default editor
    os.system(f"subl {exploit_path}")

if __name__ == "__main__":
    main()
