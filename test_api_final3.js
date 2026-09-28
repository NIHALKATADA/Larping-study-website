const http = require('https');
const data = JSON.stringify({
  messages: [{ role: 'user', content: 'Say the word SUCCESS' }]
});

const req = http.request({
  hostname: 'larping-study.vercel.app',
  path: '/api/chat',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length,
    'Origin': 'https://larping-study.vercel.app'
  }
}, (res) => {
  console.log('STATUS:', res.statusCode);
  let body = '';
  res.on('data', d => body += d);
  res.on('end', () => console.log('BODY:', body));
});

req.on('error', (e) => console.error(e));
req.write(data);
req.end();
