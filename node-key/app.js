const keypress = require('keypress');
const fs = require('fs');
const path = require('path');
const { log } = require('console');

keypress(process.stdin);

let userInput = '';

process.stdin.on('keypress', function(ch, key) {
  if (key && key.name !== 'return') {
    userInput += ch;
  } else if (key && key.name === 'return') {
    displayInput();
  }
});

function displayInput() {
  console.log(`Input: ${userInput}`);
  userInput = '';
}

console.log('Program sedang berjalan. Tekan Ctrl+C untuk menutup program.');
process.stdin.setRawMode(true);
process.stdin.resume();
