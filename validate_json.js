const fs = require('fs');
const path = require('path');

const subjects = ['daa', 'dbms', 'java', 'maths', 'ml', 'os'];
let totalQuestions = 0;
let totalQuizzes = 0;
let totalGaps = 0;

console.log('Validating JSON files...');

subjects.forEach(sub => {
    try {
        const qPath = path.join(__dirname, 'data', sub, sub + '_questions.json');
        const questions = JSON.parse(fs.readFileSync(qPath, 'utf8'));
        totalQuestions += questions.length;
        console.log([] Validated  questions);

        const quizPath = path.join(__dirname, 'data', sub, sub + '_quiz.json');
        const quizzes = JSON.parse(fs.readFileSync(quizPath, 'utf8'));
        totalQuizzes += quizzes.length;
        console.log([] Validated  quiz questions);

        const gapsPath = path.join(__dirname, 'data', sub, 'coverage_gaps.json');
        const gaps = JSON.parse(fs.readFileSync(gapsPath, 'utf8'));
        totalGaps += gaps.length;
        console.log([] Validated  coverage gaps);
        
    } catch (e) {
        console.error(Error validating :, e.message);
    }
});
console.log(Total questions: , quizzes: , gaps: );
