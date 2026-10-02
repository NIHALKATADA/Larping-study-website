const fs = require('fs');
let code = fs.readFileSync('shared/app-utils.js', 'utf8');

code = code.replace(/document\.body\.style\.paddingRight = scrollbarWidth \+ 'px';/g, 
  "document.body.style.paddingRight = scrollbarWidth + 'px';\n            modal.style.paddingRight = scrollbarWidth + 'px';");

code = code.replace(/document\.body\.style\.paddingRight = '';/g, 
  "document.body.style.paddingRight = '';\n        modal.style.paddingRight = '';");

fs.writeFileSync('shared/app-utils.js', code);
