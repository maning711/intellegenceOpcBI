const vm=require('node:vm'),fs=require('node:fs');
const ctx={console};vm.createContext(ctx);vm.runInContext(fs.readFileSync('static/timeseries.js','utf8'),ctx);
vm.runInContext(`
const greptime={category:'timeseries',source:'GreptimeDB Releases',title:'GreptimeDB · v1.0',summary:'SQL query and high cardinality',url:'https://github.com/GreptimeTeam/greptimedb/releases/tag/v1.0'};
const influx={category:'timeseries',source:'InfluxDB Releases',title:'InfluxDB · v3',summary:'storage and query'};
if(!tsIsArticle(greptime)||tsIsArticle({category:'database',title:'SQL Server pricing',summary:''}))throw Error('Topic relevance');
if(tsArticleProduct(greptime).id!=='greptime')throw Error('Product mapping');
tsMarket='cn';if(!tsFilter(greptime)||tsFilter(influx))throw Error('Market filtering');
tsMarket='all';tsGroup='cardinality';if(!tsFilter(greptime)||tsFilter(influx))throw Error('Technical filtering');
tsGroup='all';tsProduct='influx';if(tsFilter(greptime)||!tsFilter(influx))throw Error('Product filtering');
if(new Set(tsProducts.map(p=>p.id)).size!==tsProducts.length||tsGroups.length!==6)throw Error('Catalog integrity');
`,ctx);console.log('Timeseries: relevance, product identity, domestic/global, technical groups, product filters passed');
