// shared/assistant-core.js
// No dependencies, lazy-loaded.

export class AssistantCore {
  constructor(subjectId, aliases = {}, indexData = []) {
    this.subjectId = subjectId || 'default';
    this.aliases = Object.create(null);
    Object.assign(this.aliases, aliases);
    this.indexData = indexData;
    this.sessionState = {
      lastTopic: null,
      lastQuestionId: null
    };
    this.buildBM25();
  }

  // --- BM25 Search Engine ---
  buildBM25() {
    this.docFreq = {};
    this.docs = [];
    this.numDocs = this.indexData.length;
    
    // Config
    this.k1 = 1.2;
    this.b = 0.75;
    
    let totalLen = 0;
    
    for (let doc of this.indexData) {
      let docText = (doc.title + " " + doc.chunks.join(" ")).toLowerCase();
      let tokens = this.tokenize(docText);
      tokens = this.expandAliases(tokens);
      
      let tf = {};
      for (let t of tokens) {
        tf[t] = (tf[t] || 0) + 1;
      }
      
      this.docs.push({ id: doc.id, tf, len: tokens.length, doc });
      totalLen += tokens.length;
      
      // df
      let uniqueTokens = new Set(tokens);
      for (let t of uniqueTokens) {
        this.docFreq[t] = (this.docFreq[t] || 0) + 1;
      }
    }
    
    this.avgdl = this.numDocs > 0 ? totalLen / this.numDocs : 0;
  }
  
  tokenize(text) {
    return text.replace(/[^\w\s]/g, ' ').split(/\s+/).filter(t => t.length > 0);
  }
  
  expandAliases(tokens) {
    let expanded = [...tokens];
    for (let t of tokens) {
      if (Object.hasOwn(this.aliases, t) && Array.isArray(this.aliases[t])) {
        for (let syn of this.aliases[t]) {
          expanded.push(...this.tokenize(syn.toLowerCase()));
        }
      }
    }
    return expanded;
  }
  
  bm25Search(query) {
    let qTokens = this.tokenize(query.toLowerCase());
    qTokens = this.expandAliases(qTokens);
    
    let scores = [];
    for (let doc of this.docs) {
      let score = 0;
      for (let t of qTokens) {
        if (!doc.tf[t]) continue;
        let idf = Math.log(1 + (this.numDocs - this.docFreq[t] + 0.5) / (this.docFreq[t] + 0.5));
        let tf = doc.tf[t];
        // Title boost
        let titleTokens = this.tokenize((doc.doc.title || "").toLowerCase());
        let titleCount = titleTokens.filter(x => x === t).length;
        if (titleCount > 0) tf += titleCount * 5; // Title boost multiplier
        
        score += idf * (tf * (this.k1 + 1)) / (tf + this.k1 * (1 - this.b + this.b * (doc.len / this.avgdl)));
      }
      if (score > 0) {
        scores.push({ score, doc: doc.doc });
      }
    }
    return scores.sort((a, b) => b.score - a.score);
  }

  // --- Rule-based Router ---
  routeIntent(text) {
    let t = text.toLowerCase();
    
    // Follow-up rewrite before routing
    if (t.match(/^(give an example|explain simpler|make it|what about)/)) {
      if (this.sessionState.lastTopic) {
        t = t + " " + this.sessionState.lastTopic.toLowerCase();
      }
    }
    
    let intent = "search";
    let params = {
      subject: this.subjectId,
      unit: null,
      marks: null,
      n: null,
      unreviewedOnly: false,
      midterm: false
    };

    // Subject extraction
    let subjMatch = t.match(/\b(java|os|dbms|daa|ml|maths)\b/);
    if (subjMatch) {
      params.subject = subjMatch[1];
    }

    // Extract n
    let nMatch = t.match(/\b(?:top|first|give me|show(?: me)?|recommend)\s+(\d+)\b/);
    if (nMatch) {
      params.n = parseInt(nMatch[1]);
    } else {
      let nqMatch = t.match(/\b(\d+)\s+(?:most important |important |java |os |dbms |daa |ml |maths )*questions?\b/);
      if (nqMatch) params.n = parseInt(nqMatch[1]);
    }

    // Extract unit (strict)
    let unitMatch = t.match(/\bunit\s+([1-5]|i{1,3}|iv|v)\b/);
    if (unitMatch) {
      let u = unitMatch[1];
      const map = { '1':'I', '2':'II', '3':'III', '4':'IV', '5':'V', 'i':'I', 'ii':'II', 'iii':'III', 'iv':'IV', 'v':'V' };
      params.unit = map[u] || u.toUpperCase();
    }
    
    // Extract marks
    let marksMatch = t.match(/\b(\d+)\s*[-]*\s*marks?\b/);
    if (marksMatch) {
      params.marks = parseInt(marksMatch[1]);
    }

    // Extract unreviewed / unread
    if (t.match(/\b(unreviewed|unread|not done)\b/)) {
      params.unreviewedOnly = true;
    }
    
    // Extract midterm
    if (t.match(/\b(midterm|mid-term)\b/)) {
      params.midterm = true;
    }
    
    // Identify intent
    let hasRanking = t.match(/\b(top|best|most important|must-do|priority|recommend)\b/);
    let hasQuestionCue = t.match(/\b(question(s)?|revise|study|for the exam)\b/);
    let hasProgressCue = t.match(/\b(my progress|how many have i reviewed|how much is left|how much progress|how many marks left)\b/);
    let hasListCue = t.match(/\b(list|show|give me|all)\b/);
    
    if (t.match(/\b(revise next|next to revise|what next)\b/)) {
      intent = "nextToRevise";
    } else if (t.match(/\b(predict|likely|outside the bank|what else)\b/)) {
      intent = "predict";
    } else if (hasRanking && (hasQuestionCue || params.n !== null)) {
      intent = "topQuestions";
    } else if (hasProgressCue) {
      intent = "progress";
    } else if (t.match(/\b(quiz me|quiz|test me)\b/)) {
      intent = "quiz";
    } else if (t.match(/\b(q\d+)\b/)) {
      let qidMatch = t.match(/\b(q\d+)\b/);
      intent = "getQuestion";
      params.qId = qidMatch[1];
    } else if (t.match(/\b(compare|difference|vs)\b/)) {
      intent = "search";
    } else if (hasListCue && hasQuestionCue && (params.unit || params.marks || params.unreviewedOnly || params.midterm)) {
      intent = "filteredList";
    }

    return { intent, params, rewrittenQuery: t };
  }

  // --- Tools ---
  filteredList(params) {
    let qs = this.indexData.filter(d => d.type === 'question');
    if (params.unit) qs = qs.filter(q => q.unit === params.unit);
    if (params.marks) qs = qs.filter(q => q.marks === params.marks);
    if (params.midterm) qs = qs.filter(q => q.important && ['I', 'II', 'III'].includes(q.unit));
    if (params.unreviewedOnly) {
      const reviewedMap = JSON.parse(localStorage.getItem(`${this.subjectId}_reviewed`) || '{}');
      qs = qs.filter(q => !reviewedMap[q.id]);
    }
    return qs;
  }

  topQuestions(params) {
    let qs = this.indexData.filter(d => d.type === 'question');
    if (params.unit) qs = qs.filter(q => q.unit === params.unit);
    if (params.marks) qs = qs.filter(q => q.marks === params.marks);
    if (params.midterm) qs = qs.filter(q => q.important && ['I', 'II', 'III'].includes(q.unit));
    
    if (params.unreviewedOnly) {
      const reviewedMap = JSON.parse(localStorage.getItem(`${this.subjectId}_reviewed`) || '{}');
      qs = qs.filter(q => !reviewedMap[q.id]);
    }
    
    // Sort by score desc, then important, then marks, then bloom
    qs.sort((a, b) => {
      if ((b.score || 0) !== (a.score || 0)) return (b.score || 0) - (a.score || 0);
      if (b.important !== a.important) return b.important ? 1 : -1;
      if (b.marks !== a.marks) return (b.marks || 0) - (a.marks || 0);
      return 0;
    });
    
    let picked = [];
    let pickedTokens = [];
    let limit = params.n || 5;

    const getTokenOverlap = (t1, tokensList) => {
       let maxOverlap = 0;
       let s1 = new Set(this.tokenize(t1.toLowerCase()));
       for (let t2 of tokensList) {
          let s2 = new Set(t2);
          let intersection = new Set([...s1].filter(x => s2.has(x)));
          let union = new Set([...s1, ...s2]);
          let overlap = union.size === 0 ? 0 : intersection.size / union.size;
          if (overlap > maxOverlap) maxOverlap = overlap;
       }
       return maxOverlap;
    };

    let unitBuckets = {};
    for (let q of qs) {
       if (!unitBuckets[q.unit]) unitBuckets[q.unit] = [];
       unitBuckets[q.unit].push(q);
    }
    let units = Object.keys(unitBuckets);
    let bucketIdx = 0;
    
    while(picked.length < limit && units.length > 0) {
       let currentUnit = units[bucketIdx % units.length];
       let bucket = unitBuckets[currentUnit];
       if (bucket.length === 0) {
           units.splice(bucketIdx % units.length, 1);
           continue;
       }
       
       let cand = bucket.shift();
       
       if (pickedTokens.length > 0 && getTokenOverlap(cand.title || "", pickedTokens) > 0.6) {
           // Near-duplicate, skip to next unit bucket without picking
           bucketIdx++;
           continue;
       }
       
       picked.push(cand);
       pickedTokens.push(this.tokenize((cand.title || "").toLowerCase()));
       bucketIdx++;
    }

    return picked.map(q => {
      let parts = [];
      if (q.score !== undefined) parts.push(`Score ${q.score}`);
      else parts.push(`Unscored`);
      if (q.marks) parts.push(`${q.marks} marks`);
      if (q.unit) parts.push(`Unit ${q.unit}`);
      if (q.bloom) parts.push(`Bloom ${q.bloom}`);
      if (q.important) parts.push(`flagged important`);
      return {
        ...q,
        reason: parts.join(' · ')
      };
    });
  }
  
  getQuestion(qId) {
    let q = this.indexData.find(q => q.id === qId);
    if (q) this.sessionState.lastTopic = q.title;
    return q;
  }

  search(query) {
    let results = this.bm25Search(query);
    this.sessionState.lastTopic = query;
    return results.slice(0, 5); // top 5
  }

  progress() {
    const reviewedMap = JSON.parse(localStorage.getItem(`${this.subjectId}_reviewed`) || '{}');
    const qs = this.indexData.filter(d => d.type === 'question');
    const total = qs.length;
    let done = 0;
    qs.forEach(q => { if (reviewedMap[q.id]) done++; });
    return { done, total, percent: total ? Math.round((done/total)*100) : 0 };
  }

  nextToRevise() {
    const reviewedMap = JSON.parse(localStorage.getItem(`${this.subjectId}_reviewed`) || '{}');
    let unreviewed = this.indexData.filter(d => d.type === 'question' && !reviewedMap[d.id]);
    // sort by important
    unreviewed.sort((a, b) => {
       if (b.important !== a.important) return b.important ? 1 : -1;
       return (b.score || 0) - (a.score || 0);
    });
    return unreviewed.slice(0, 3);
  }

  execute(text) {
    let { intent, params, rewrittenQuery } = this.routeIntent(text);
    let result = null;
    if (intent === 'topQuestions') result = this.topQuestions(params);
    else if (intent === 'filteredList') result = this.filteredList(params);
    else if (intent === 'getQuestion') result = this.getQuestion(params.qId);
    else if (intent === 'progress') result = this.progress();
    else if (intent === 'nextToRevise') result = this.nextToRevise();
    else if (intent === 'quiz') result = "Ready for a quiz? Go to the interactive quiz page from the dashboard!";
    else {
      intent = 'search'; // fallback
      result = this.search(rewrittenQuery);
    }
    
    return { intent, params, result };
  }
}
