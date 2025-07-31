// Minimal word set for testing
const englishWords = new Set([
  "hello", "world", "how", "are", "you", "today", "the", "quick", "brown", "fox",
  "jumps", "over", "lazy", "dog", "and", "cat", "sat", "on", "mat", "in",
  "house", "with", "mouse", "red", "blue", "green", "yellow", "black", "white", "purple",
  "venture", "bench", "doctor", "address", "big", "small", "tall", "short", "fast", "slow"
]);

function caesarDecrypt(text, shift) {
  let result = "";
  
  for (let char of text) {
    if (char.match(/[a-zA-Z]/)) {
      if (char.match(/[A-Z]/)) {
        let charPos = char.charCodeAt(0) - 65;
        let newPos = ((charPos - shift) % 26 + 26) % 26;
        result += String.fromCharCode(newPos + 65);
      } else {
        let charPos = char.charCodeAt(0) - 97;
        let newPos = ((charPos - shift) % 26 + 26) % 26;
        result += String.fromCharCode(newPos + 97);
      }
    } else {
      result += char;
    }
  }
  
  return result;
}

function caesarAutoSolver(ciphertext, englishWords) {
  if (!ciphertext || typeof ciphertext !== 'string') {
    throw new Error("Input must be a non-empty string");
  }
  
  if (!ciphertext.match(/[a-zA-Z]/)) {
    throw new Error("Input must contain alphabetic characters");
  }
  
  const shiftsToTry = [13, 3, 1, 25, 7, 12, 2, 4, 5, 6, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24];
  
  let bestResult = "";
  let bestScore = 0;
  
  for (let shift of shiftsToTry) {
    const decrypted = caesarDecrypt(ciphertext, shift);
    const words = decrypted.toLowerCase().match(/[a-zA-Z]+/g) || [];
    
    if (words.length === 0) continue;
    
    const validCount = words.filter(word => englishWords.has(word)).length;
    const score = validCount / words.length;
    
    if (score > bestScore) {
      bestScore = score;
      bestResult = decrypted;
    }
    
    if (score >= 0.75) {
      return decrypted;
    }
  }
  
  if (bestScore < 0.30) {
    return `Error: No valid decryption found. Best attempt had ${(bestScore * 100).toFixed(1)}% valid words. This may not be a Caesar cipher.`;
  }
  
  return `${bestResult} (Confidence: ${(bestScore * 100).toFixed(1)}%)`;
}

// Main execution
const cipher = "KHOOR, ZRUOG! KRZ DUH BRX WRGDB?";
const result = caesarAutoSolver(cipher, englishWords);
console.log(`Result: ${result}`);