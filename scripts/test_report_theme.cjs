const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const projectRoot = path.join(__dirname, '..');
const report = fs.readFileSync(path.join(projectRoot, 'subjects', 'dbms', 'comprehensive-report.html'), 'utf8');
const dom = new JSDOM(report, {
  url: 'http://localhost:8000/subjects/dbms/comprehensive-report.html',
  runScripts: 'outside-only'
});
const { window } = dom;

window.scrollTo = () => {};
window.requestAnimationFrame = callback => setTimeout(callback, 0);
window.requestIdleCallback = callback => setTimeout(callback, 0);
window.IntersectionObserver = class {
  observe() {}
  unobserve() {}
  disconnect() {}
};

window.eval(fs.readFileSync(path.join(projectRoot, 'shared', 'app-utils.js'), 'utf8'));

setTimeout(() => {
  const buttons = window.document.querySelectorAll('#themeToggleBtn');
  assert.strictEqual(buttons.length, 1, 'the DBMS report must expose one theme control');

  const before = window.document.documentElement.getAttribute('data-theme');
  buttons[0].click();
  const after = window.document.documentElement.getAttribute('data-theme');
  assert.notStrictEqual(after, before, 'clicking the theme control must change the theme');
  assert.strictEqual(window.localStorage.getItem('global_theme'), after, 'the selected theme must persist');
  console.log('✅ Report theme toggle works');
}, 350);
