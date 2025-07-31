import re
import subprocess
import sys

def caesar_decrypt(text, shift):
    """Decrypt text using Caesar cipher with given shift."""
    result = ""
    
    for char in text:
        if char.isalpha():
            if char.isupper():
                char_pos = ord(char) - ord('A')
                new_pos = (char_pos - shift) % 26
                result += chr(new_pos + ord('A'))
            else:
                char_pos = ord(char) - ord('a')
                new_pos = (char_pos - shift) % 26
                result += chr(new_pos + ord('a'))
        else:
            result += char
    
    return result

def caesar_auto_solver(ciphertext, english_words):
    """
    Automatically solve Caesar cipher by testing shifts in priority order
    and validating against English dictionary.
    """
    # Input validation
    if not ciphertext or not isinstance(ciphertext, str):
        raise ValueError("Input must be a non-empty string")
    
    if not re.search(r'[a-zA-Z]', ciphertext):
        raise ValueError("Input must contain alphabetic characters")
    
    # Priority shift order
    shifts_to_try = [13, 3, 1, 25, 7, 12, 2, 4, 5, 6, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    
    best_result = ""
    best_score = 0
    
    for shift in shifts_to_try:
        # Decrypt with current shift
        decrypted = caesar_decrypt(ciphertext, shift)
        
        # Extract and validate words
        words = re.findall(r'[a-zA-Z]+', decrypted.lower())
        if not words:
            continue
            
        valid_count = sum(1 for word in words if word in english_words)
        score = valid_count / len(words)
        
        # Track best result
        if score > best_score:
            best_score = score
            best_result = decrypted
        
        # Return immediately if we find good English (75%+ valid words)
        if score >= 0.75:
            return decrypted
    
    # Handle cases where no shift meets threshold
    if best_score < 0.30:
        return f"Error: No valid decryption found. Best attempt had {best_score:.1%} valid words. This may not be a Caesar cipher."
    
    return f"{best_result} (Confidence: {best_score:.1%})"

if __name__ == "__main__":
    # Handle dependency
    we_installed_it = False
    try:
        from english_words import get_english_words_set
        english_words = get_english_words_set(['web2'], lower=True)
    except ImportError:
        response = input("english-words is not installed. Install it? caesar_cipher.py will uninstall all dependent subprocesses after running. (y/n): ")
        if response.lower() != 'y':
            sys.exit()
        
        subprocess.run([sys.executable, "-m", "pip", "install", "english-words"])
        from english_words import get_english_words_set
        english_words = get_english_words_set(['web2'], lower=True)
        we_installed_it = True
    
    try:
        cipher = "KHOOR, ZRUOG! KRZ DUH BRX WRGDB?"
        result = caesar_auto_solver(cipher, english_words)
        print(f"Result: {result}")
    finally:
        # Cleanup
        if we_installed_it:
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "english-words", "-y"])