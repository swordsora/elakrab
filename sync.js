const SYNC_QUEUE_KEY='tawoos:pwa:sync-queue';
export function syncConfig(baseUrl){return {baseUrl:String(baseUrl||'').replace(/\/$/,'')}}
export function queueInvoice(invoice){const q=JSON.parse(localStorage.getItem(SYNC_QUEUE_KEY)||'[]');q.push(invoice);localStorage.setItem(SYNC_QUEUE_KEY,JSON.stringify(q));return q.length}
export async function pushQueuedInvoices(config,token){if(!config?.baseUrl||!token)return 0;const q=JSON.parse(localStorage.getItem(SYNC_QUEUE_KEY)||'[]');let sent=0;for(const invoice of q){const r=await fetch(`${config.baseUrl}/api/invoices`,{method:'POST',headers:{'content-type':'application/json',authorization:`Bearer ${token}`},body:JSON.stringify(invoice)});if(!r.ok)break;sent++}if(sent){q.splice(0,sent);localStorage.setItem(SYNC_QUEUE_KEY,JSON.stringify(q))}return sent}
export function queuedCount(){return JSON.parse(localStorage.getItem(SYNC_QUEUE_KEY)||'[]').length}
