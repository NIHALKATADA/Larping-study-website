import { AssistantCore } from '../shared/assistant-core.js';

global.localStorage = {
  getItem: () => null,
  setItem: () => {}
};

const mockData = [
  { id: "q1", type: "question", unit: "I", marks: 5, important: true, score: 10, title: "What is DBMS?", chunks: ["DBMS is a system..."] },
  { id: "q2", type: "question", unit: "III", marks: 10, important: false, score: 5, title: "SQL Queries", chunks: ["SQL stands for..."] }
];

const mockAliases = {
  "overloading": ["method overloading", "polymorphism"],
  "dbms": ["database"]
};

const assistant = new AssistantCore("dbms", mockAliases, mockData);

const tests = [
  { query: "give me 10 most important questions", expected: { intent: "topQuestions", n: 10 } },
  { query: "top 5 unreviewed unit 3 DBMS questions", expected: { intent: "topQuestions", n: 5, unit: "III", unreviewedOnly: true } },
  { query: "what is overloading in Java", expected: { intent: "search" } },
  { query: "quiz me", expected: { intent: "quiz" } },
  { query: "what should I revise next", expected: { intent: "nextToRevise" } },
  { query: "compare X vs Y", expected: { intent: "search" } },
  { query: "explain Q12", expected: { intent: "getQuestion", qId: "q12" } },
  { query: "show 5-mark questions unit 2", expected: { intent: "filteredList", marks: 5, unit: "II" } },
  { query: "top 20 questions for midterm", expected: { intent: "topQuestions", n: 20, midterm: true } },
  { query: "how much progress have I made?", expected: { intent: "progress" } },
  // Adding more to reach >= 30 cases
  { query: "give me top 3 unread 5 mark questions", expected: { intent: "topQuestions", n: 3, marks: 5, unreviewedOnly: true } },
  { query: "recommend 10 unit 1 questions", expected: { intent: "topQuestions", n: 10, unit: "I" } },
  { query: "what is polymorphism?", expected: { intent: "search" } },
  { query: "explain ACID properties", expected: { intent: "search" } },
  { query: "difference between 1NF and 2NF", expected: { intent: "search" } },
  { query: "what are the most important questions?", expected: { intent: "topQuestions" } },
  { query: "show top 15 questions", expected: { intent: "topQuestions", n: 15 } },
  { query: "show 10 marks questions", expected: { intent: "filteredList", marks: 10 } },
  { query: "midterm questions", expected: { intent: "search", midterm: true } },
  { query: "top 5 midterm questions", expected: { intent: "topQuestions", n: 5, midterm: true } },
  { query: "show top 5 unreviewed", expected: { intent: "topQuestions", n: 5, unreviewedOnly: true } },
  { query: "give me 5 marks questions unit 4", expected: { intent: "filteredList", marks: 5, unit: "IV" } },
  { query: "recommend next to revise", expected: { intent: "nextToRevise" } },
  { query: "what to revise next?", expected: { intent: "nextToRevise" } },
  { query: "how many marks left to revise?", expected: { intent: "progress" } },
  { query: "explain q1", expected: { intent: "getQuestion", qId: "q1" } },
  { query: "compare SJF and RR", expected: { intent: "search" } },
  { query: "what is BCNF?", expected: { intent: "search" } },
  { query: "top 10 important unit 5 questions", expected: { intent: "topQuestions", n: 10, unit: "V" } },
  { query: "give me unit 2 questions", expected: { intent: "filteredList", unit: "II" } },
  { query: "what is a left join", expected: { intent: "search" } },
  { query: "explain best fit vs worst fit allocation", expected: { intent: "search" } },
  { query: "what is the most important goal of an operating system", expected: { intent: "search" } },
  { query: "what is an important property of a transaction", expected: { intent: "search" } },
  { query: "what is a unit vector", expected: { intent: "search", unit: null } },
  { query: "what are the done transactions in a log", expected: { intent: "search" } },
  { query: "give me unit 2 5-mark questions", expected: { intent: "filteredList", unit: "II", marks: 5 } },
  { query: "top 10 java questions", expected: { intent: "topQuestions", n: 10, subject: "java" } },
  { query: "give me 10 most important questions", expected: { intent: "topQuestions", n: 10 } }
];

let passed = 0;
for (let t of tests) {
  let res = assistant.routeIntent(t.query);
  let ok = true;
  if (res.intent !== t.expected.intent) ok = false;
  for (let k in t.expected) {
    if (k !== 'intent' && res.params[k] !== t.expected[k]) ok = false;
  }
  
  if (ok) passed++;
  else {
    console.log(`Query: "${t.query}"`);
    console.log(`  Expected Intent: ${t.expected.intent}`);
    console.log(`  Got Intent:      ${res.intent}`);
    console.log(`  Expected Params: ${JSON.stringify(t.expected)}`);
    console.log(`  Got Params:      ${JSON.stringify(res.params)}`);
    console.log(`  Match:           ${ok ? '✅' : '❌'}`);
    console.log('---');
  }
}
console.log(`Passed ${passed} / ${tests.length} cases.`);

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.join(__dirname, '..');

console.log("\nTesting AssistantCore on all real subject data...");
const subjects = ['daa', 'dbms', 'java', 'maths', 'ml', 'os'];
const aliasesPath = path.join(projectRoot, 'shared', 'assistant-aliases.json');
let realAliases = {};
try {
  realAliases = JSON.parse(fs.readFileSync(aliasesPath, 'utf8'));
} catch (e) {
  console.warn("Could not load real aliases, using empty object");
}

for (const sub of subjects) {
  const indexPath = path.join(projectRoot, 'subjects', sub, 'assistant-index.json');
  try {
    const indexData = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
    const core = new AssistantCore(sub, realAliases, indexData);
    console.log(`✅ ${sub} loaded successfully (${indexData.length} docs)`);
  } catch (e) {
    console.error(`❌ ${sub} failed to load:`, e);
    process.exit(1);
  }
}
