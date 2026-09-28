# Assistant Smart Mode Test Plan

> **Note to Developer:** My current headless environment does not support WebGPU, so I could not run this test plan natively. Please run these tests locally in Chrome/Brave with WebGPU enabled.

## Environment Setup
1. Use Chrome or Brave with WebGPU enabled.
2. Ensure you have the `revision-hub` running locally via a server (e.g. `python -m http.server 8000`).
3. Open the Assistant Modal from the Dashboard or any Subject page.
4. Click "Download & Load" for a recommended ~3B model tier (e.g. Llama-3-8B-Instruct-q4f16_1-MLC if using 7B tier or a 3B tier model). Wait for caching to complete.

## Test Cases (30 Prompts across 6 Subjects)

### DBMS
1. **Prompt**: "What is 2NF?"
   - **Criteria**: Returns 2-3 lines of definition + example, cites a question number if found.
2. **Prompt**: "give an example"
   - **Criteria**: Uses chat history to provide an example of 2NF.
3. **Prompt**: "Show me the top 3 most important questions for Unit 1."
   - **Criteria**: Returns 3 tool-generated links. One-line LLM intro. No hallucinatory text.
4. **Prompt**: "Difference between DBMS and RDBMS for 5 marks"
   - **Criteria**: Lengthy output: definition, explanation, ASCII/description diagram, example, exam tip.
5. **Prompt**: "What is my progress?"
   - **Criteria**: Tool-generated progress percentage. 1-line LLM intro.

### Java
6. **Prompt**: "what is overloading in Java"
   - **Criteria**: Returns correct concept with reference notes cited.
7. **Prompt**: "how is it different from overriding? (3 marks)"
   - **Criteria**: Definition + points + example format. Cites previous context.
8. **Prompt**: "Recommend what to revise next."
   - **Criteria**: Tool-based suggestion of unreviewed important questions.
9. **Prompt**: "Quiz me."
   - **Criteria**: Tool-based response redirecting to the interactive quiz page.
10. **Prompt**: "Write a Java program to reverse a string."
    - **Criteria**: General answer (not in bank) fallback triggered. Minimal runnable code.

### OS
11. **Prompt**: "What is a semaphore?"
    - **Criteria**: Standard 2-3 lines unless marks specified. Cited from bank.
12. **Prompt**: "Explain deadlock conditions for 5 marks."
    - **Criteria**: Detailed 5-mark structure: definition, explanation, ASCII diagram/list, example, exam tip.
13. **Prompt**: "Top 2 Unit II questions."
    - **Criteria**: Router extracts unit 'II', n '2', intent 'topQuestions'. Tool lists 2 links.
14. **Prompt**: "What happens during a context switch?"
    - **Criteria**: Extract from OS bank, accurate and cited.
15. **Prompt**: "Is Windows better than Linux?"
    - **Criteria**: Off-topic. General answer fallback, labeled "General answer (not from your question bank)".

### DAA
16. **Prompt**: "Explain the Master Theorem."
    - **Criteria**: Concept answer using question bank references.
17. **Prompt**: "Give a 3 mark answer for Dijkstra's algorithm."
    - **Criteria**: Definition + points + example.
18. **Prompt**: "Show me 5 unread questions."
    - **Criteria**: Tool-based list of 5 unreviewed questions.
19. **Prompt**: "What is the time complexity of QuickSort?"
    - **Criteria**: Short, concise answer.
20. **Prompt**: "What is a neural network?"
    - **Criteria**: Off-topic for DAA. General answer fallback.

### ML
21. **Prompt**: "Explain Backpropagation for 5 marks."
    - **Criteria**: 5-mark structure with ASCII diagram and exam tip.
22. **Prompt**: "Unit III ML question on SVM."
    - **Criteria**: JSON router extracts Unit III, search intent. Returns SVM questions from Unit 3.
23. **Prompt**: "What next?"
    - **Criteria**: Triggers 'nextToRevise' intent. Tool-based list with 1-line intro.
24. **Prompt**: "How much have I completed?"
    - **Criteria**: Triggers 'progress' intent.
25. **Prompt**: "What is overfitting?"
    - **Criteria**: Extract from ML bank, accurate and cited.

### Maths
26. **Prompt**: "What is a bipartite graph?"
    - **Criteria**: Accurate definition from Maths bank.
27. **Prompt**: "Give an example."
    - **Criteria**: Contextual memory test (should remember bipartite graph).
28. **Prompt**: "Prove Euler's formula for 5 marks."
    - **Criteria**: 5-mark structure, proof points, exam tip.
29. **Prompt**: "How to bake a cake?"
    - **Criteria**: Completely off-topic. General answer fallback, labeled properly.
30. **Prompt**: "Summarize Unit IV."
    - **Criteria**: General search/summary. May use JSON router to extract Unit IV.

## Functional Buttons
- **Stop**: Click while streaming; generation should halt immediately.
- **Regenerate**: Click after completion; should replace the previous response with a fresh one.
- **Delete Model Data**: Click in the Smart Mode UI header; clears Cache API storage.
