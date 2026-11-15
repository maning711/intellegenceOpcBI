const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
const elements=new Map(),context={console,Date,Set,RegExp,IntersectionObserver:class{observe(){}disconnect(){}},document:{getElementById(id){if(!elements.has(id))elements.set(id,{value:'7',textContent:'',innerHTML:''});return elements.get(id)},querySelectorAll(){return []}},fetch:()=>new Promise(()=>{}),setInterval(){}};
vm.createContext(context);vm.runInContext(fs.readFileSync('static/app.js','utf8'),context);
vm.runInContext(`
state={articles:[
 {category:'ai',title:'Agent workflow',summary:'automation',source:'A',url:'https://example.com/new',published:new Date(Date.now()-86400000).toISOString()},
 {category:'ai',title:'Old agent',summary:'',source:'A',url:'https://example.com/old',published:new Date(Date.now()-8*86400000).toISOString()},
 {category:'ai',title:'Future agent',summary:'',source:'A',url:'https://example.com/future',published:new Date(Date.now()+86400000).toISOString()},
 {category:'ai',title:'Unknown agent',summary:'',source:'A',url:'https://example.com/unknown',published:null},
 {category:'database',title:'Query benchmark',summary:'',source:'B',url:'https://example.com/db',published:new Date().toISOString()}
],sources:[]};tab='ai';
if(recentRows().length!==1)throw Error('Rolling window includes old, future, unknown or wrong category');
$('search').value='not matching';renderWeekly();if(!$('weekly').innerHTML.includes('1 篇'))throw Error('Weekly report depends on search');
if(!opcEligible(state.articles[0])||opcEligible(state.articles[4]))throw Error('OPC relevance filtering failed');
state.articles=[];renderWeekly();if(!$('weekly').innerHTML.includes('暂不生成'))throw Error('Empty report invents analysis');
`,context);console.log('Frontend: rolling 7-day window, category filtering, search independence, OPC relevance, empty state passed');
