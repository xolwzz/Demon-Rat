#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import shutil
import random
import string
import tempfile
import base64
import re
import platform

def generate_random_name(length=8):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def create_decoy_imports():
    """Create a list of harmless decoy imports to confuse static analysis."""
    decoys = [
        "import datetime", 
        "import json",
        "import csv",
        "import xml.etree.ElementTree as ET",
        "import logging",
        "import math",
        "import statistics",
        "import urllib.request",
        "import zipfile",
        "import hashlib",
        "import uuid",
        "import socket",
        "import platform"
    ]
    return "\n".join(random.sample(decoys, k=random.randint(3, 7)))

def get_pyinstaller_version():
    """Get the installed PyInstaller version."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "pyinstaller"],
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Extract version from output
        match = re.search(r'Version: (\d+\.\d+(?:\.\d+)?)', result.stdout)
        if match:
            version_str = match.group(1)
            # Convert to tuple of integers for easy comparison
            return tuple(map(int, version_str.split('.')))
        return None
    except:
        return None

def compile_python_stealth(file_path, one_file=True, console=False, icon=None, name=None, 
                          add_decoys=True, encrypt_strings=True, use_upx=True):
    """
    Compiles a Python file into an executable with stealth features.
    
    Args:
        file_path (str): Path to the Python file
        one_file (bool): Whether to create a single executable file
        console (bool): Whether to show console window when running
        icon (str): Path to icon file (.ico)
        name (str): Custom name for the output executable
        add_decoys (bool): Add decoy imports and functions
        encrypt_strings (bool): Basic string obfuscation
        use_upx (bool): Use UPX packer for smaller size
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False
    
    if not file_path.endswith('.py'):
        print(f"Error: File '{file_path}' is not a Python file.")
        return False
    
    # Check if PyInstaller is installed
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", "pyinstaller"], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("PyInstaller not found. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("PyInstaller installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing PyInstaller: {e}")
            return False
    
    # Get PyInstaller version
    pyinstaller_version = get_pyinstaller_version()
    
    # Create a temporary directory for our modified source
    temp_dir = tempfile.mkdtemp()
    try:
        # Read the original Python file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
        
        modified_code = original_code
        
        # Apply obfuscation techniques if requested
        if add_decoys or encrypt_strings:
            print("Applying code obfuscation techniques...")
            
            if add_decoys:
                # Add decoy imports at the top
                decoy_imports = create_decoy_imports()
                
                # Create some decoy functions that never get called
                decoy_functions = []
                for _ in range(3):
                    func_name = generate_random_name()
                    decoy_functions.append(f"""
def {func_name}():
    \"\"\"This function does nothing but confuse static analysis.\"\"\"
    {generate_random_name()} = {random.randint(1, 1000)}
    return {generate_random_name()} if {random.choice([True, False])} else {random.randint(1, 1000)}
""")
                
                # Insert decoys at the beginning of the file
                modified_code = decoy_imports + "\n\n" + "\n".join(decoy_functions) + "\n\n" + modified_code
            
            if encrypt_strings:
                # Very basic string obfuscation - in a real scenario you'd want something more sophisticated
                # This just demonstrates the concept
                def encode_string(match):
                    s = match.group(1)
                    encoded = base64.b64encode(s.encode()).decode()
                    return f"base64.b64decode('{encoded}').decode()"
                
                # Add base64 import if not already there
                if "import base64" not in modified_code:
                    modified_code = "import base64\n" + modified_code
        
        # Create a random name for the temporary file
        temp_file_name = generate_random_name() + ".py"
        temp_file_path = os.path.join(temp_dir, temp_file_name)
        
        # Write the modified code to the temporary file
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            f.write(modified_code)
        
        # Build the PyInstaller command
        cmd = [sys.executable, "-m", "PyInstaller"]
        
        if one_file:
            cmd.append("--onefile")
        
        # Always add --noconsole by default for stealth
        cmd.append("--noconsole")
        
        if icon and os.path.exists(icon):
            cmd.extend(["--icon", icon])
        
        # Use a random name if none provided
        output_name = name if name else generate_random_name()
        cmd.extend(["--name", output_name])
        
        # Add advanced options for stealth
        cmd.append("--clean")  # Clean PyInstaller cache
        
        # Only use --strip on non-Windows platforms
        if platform.system() != "Windows":
            cmd.append("--strip")  # Strip symbols from executable
        
        # Only add --key for PyInstaller versions before 6.0
        if pyinstaller_version and pyinstaller_version < (6, 0):
            cmd.append("--key=" + generate_random_name(16))  # Encryption key for pyz archive
        
        # Add runtime hooks to modify behavior
        cmd.append("--runtime-hook=" + create_runtime_hook(temp_dir))
        
        # Use UPX if requested (makes exe smaller and changes signature)
        if use_upx:
            try:
                # Check if UPX is installed
                subprocess.run(["upx", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                cmd.append("--upx-dir=.")
            except (subprocess.SubprocessError, FileNotFoundError):
                print("UPX not found. Continuing without UPX compression.")
        
        # Add the Python file to compile
        cmd.append(temp_file_path)
        
        print(f"Compiling with stealth options...")
        try:
            subprocess.run(cmd, check=True)
            
            # Get the executable path
            dist_dir = os.path.join(os.getcwd(), "dist")
            
            if os.name == 'nt':  # Windows
                exe_path = os.path.join(dist_dir, f"{output_name}.exe")
            else:  # Linux/Mac
                exe_path = os.path.join(dist_dir, output_name)
            
            if os.path.exists(exe_path):
                # Copy the executable to the current directory
                final_path = os.path.join(os.getcwd(), os.path.basename(exe_path))
                shutil.copy2(exe_path, final_path)
                
                print(f"Compilation successful! Executable created at: {final_path}")
                
                # Clean up build files
                build_dir = os.path.join(os.getcwd(), "build")
                spec_file = os.path.join(os.getcwd(), f"{output_name}.spec")
                
                if os.path.exists(build_dir):
                    shutil.rmtree(build_dir)
                if os.path.exists(spec_file):
                    os.remove(spec_file)
                if os.path.exists(dist_dir):
                    shutil.rmtree(dist_dir)
                    
                return True
            else:
                print(f"Error: Executable not found at expected path: {exe_path}")
                return False
        
        except subprocess.CalledProcessError as e:
            print(f"Error during compilation: {e}")
            return False
    
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

def create_runtime_hook(temp_dir):
    """Create a PyInstaller runtime hook to modify behavior at runtime."""
    hook_content = """
import os
import sys
import random
import time

# Add random sleep to avoid sandbox detection
time.sleep(random.uniform(0.1, 0.5))

# Modify some environment variables to look more legitimate
os.environ['PYTHONHOME'] = ''
os.environ['PYTHONPATH'] = ''

# Change process name if possible
try:
    import ctypes
    if hasattr(ctypes.cdll.kernel32, 'SetConsoleTitleW'):
        ctypes.cdll.kernel32.SetConsoleTitleW(f"Python {sys.version_info[0]}.{sys.version_info[1]}")
except:
    pass
"""
    hook_path = os.path.join(temp_dir, "runtime_hook.py")
    with open(hook_path, 'w') as f:
        f.write(hook_content)
    return hook_path

def main():
    parser = argparse.ArgumentParser(description="Compile Python files to stealthy executables")
    parser.add_argument("file", help="Python file to compile")
    parser.add_argument("--no-onefile", action="store_true", help="Create a directory of files instead of a single executable")
    parser.add_argument("--console", action="store_true", help="Show console window when running the executable (default: hidden)")
    parser.add_argument("--icon", help="Path to icon file (.ico)")
    parser.add_argument("--name", help="Custom name for the output executable")
    parser.add_argument("--no-decoys", action="store_true", help="Don't add decoy code")
    parser.add_argument("--no-encrypt", action="store_true", help="Don't encrypt strings")
    parser.add_argument("--no-upx", action="store_true", help="Don't use UPX compression")
    
    args = parser.parse_args()
    
    compile_python_stealth(
        args.file,
        one_file=not args.no_onefile,
        console=args.console,  # Default is False (no console)
        icon=args.icon,
        name=args.name,
        add_decoys=not args.no_decoys,
        encrypt_strings=not args.no_encrypt,
        use_upx=not args.no_upx
    )

if __name__ == "__main__":
    main()
