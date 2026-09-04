let products=[];
const normalize=s=>String(s||'').trim().toLocaleLowerCase('ar-EG');
self.onmessage=e=>{const {type,payload}=e.data||{};if(type==='init'){products=(payload||[]).map(p=>({...p,code:String(p.code),searchText:p.searchText||`${normalize(p.name)} ${p.code}`}));return}if(type==='search'){const q=normalize(payload?.query);const found=[];if(q){for(const p of products){if(p.searchText.includes(q)){found.push(p);if(found.length>=40)break}}}self.postMessage({type:'results',query:payload?.query||'',results:found})}};
