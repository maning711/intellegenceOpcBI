const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
const store=new Map(),context={console,Date,URL,structuredClone,localStorage:{getItem:k=>store.get(k)||null,setItem:(k,v)=>store.set(k,v)},alert:()=>{throw Error('Storage failed')}};vm.createContext(context);vm.runInContext(fs.readFileSync('static/career.js','utf8'),context);
vm.runInContext(`
const news=[{title:'PostgreSQL query performance',summary:'database benchmark',url:'https://example.com/sql',published:new Date().toISOString()},{title:'Agent tool integration',summary:'mcp workflow',url:'https://example.com/agent',published:new Date().toISOString()},{title:'Old agent',summary:'mcp',url:'https://example.com/old',published:new Date(Date.now()-8*86400000).toISOString()},{title:'Future agent',summary:'mcp',url:'https://example.com/future',published:new Date(Date.now()+86400000).toISOString()}];
careerData.profile.role='database';let recs=careerRecommendations(news);if(recs.length!==2||recs[0].key!=='database')throw Error('Career ranking/window');
careerData.profile.hours=2;if(careerBudget()!=='short')throw Error('Budget');if(!createCareerTask(recs[0])||createCareerTask(recs[0]))throw Error('Duplicate task');
if(careerSafeUrl('javascript:alert(1)')||!careerSafeUrl('https://github.com/test'))throw Error('Unsafe evidence URL');
careerData.tasks[0].notes='Persisted reflection';careerSave();if(!JSON.parse(localStorage.getItem(careerKey)).tasks[0].notes)throw Error('Persistence');
`,context);console.log('Career: relevance, recent window, time budget, deduplication, safe evidence links, persistence passed');
