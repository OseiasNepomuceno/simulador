const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

const input = path.resolve(__dirname, '..', 'post_ia_editais_coregov.svg');
const output = path.resolve(__dirname, '..', 'post_ia_editais_coregov.png');

// Sharp doesn't support SVG directly on Windows reliably
// Instead, we'll use a pure JS approach
const svgContent = fs.readFileSync(input, 'utf8');

sharp(Buffer.from(svgContent))
  .resize(1080, 1080)
  .png()
  .toFile(output)
  .then(() => console.log('Convertido: ' + output))
  .catch(err => console.error('Erro:', err.message));
