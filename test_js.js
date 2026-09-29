const { JSDOM } = require('jsdom');
const fs = require('fs');

const html = fs.readFileSync('subjects/java/question-bank.html', 'utf-8');
const dom = new JSDOM(html, {
    url: 'file:///C:/Users/nihal/OneDrive/Desktop/revision-hub/subjects/java/question-bank.html',
    runScripts: 'dangerously'
});

const window = dom.window;
const document = window.document;

// Mock requestIdleCallback
window.requestIdleCallback = function(fn) { setTimeout(fn, 1); };
window.requestAnimationFrame = function(fn) { setTimeout(fn, 1); };

// Mock IntersectionObserver
window.IntersectionObserver = class {
    constructor() {}
    observe() {}
    unobserve() {}
    disconnect() {}
};

try {
    const scriptContent = fs.readFileSync('shared/app-utils.js', 'utf-8');
    window.eval(scriptContent);
    
    setTimeout(() => {
        console.log('After timeout');
        console.log('Progress Text:', document.getElementById('progressText').textContent);
        console.log('Showing Text:', document.getElementById('showing-text').textContent);
    }, 1000);
} catch (e) {
    console.error('Error during execution:', e);
}
