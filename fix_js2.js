const fs = require('fs');
let code = fs.readFileSync('shared/app-utils.js', 'utf8');
code = code.replace(/calc\(2rem \+ 48px \+ 1rem \+ \$\{scrollbarWidth\}px\)/g, 'calc(2rem + ${scrollbarWidth}px)');
fs.writeFileSync('shared/app-utils.js', code);
