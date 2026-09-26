import http from 'node:http';
import {readFile,stat,realpath} from 'node:fs/promises';
import {resolve,extname,sep,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const args=process.argv.slice(2),arg=(key,fallback)=>{const i=args.indexOf(key);return i<0?fallback:args[i+1];};
const root=await realpath(resolve(dirname(fileURLToPath(import.meta.url)),'..',arg('--dir','.')));
const host=arg('--host','127.0.0.1'),port=Number(arg('--port',process.env.PORT||'8787'));
if(!Number.isInteger(port)||port<1||port>65535)throw Error('Invalid port');
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.webmanifest':'application/manifest+json','.json':'application/json','.png':'image/png','.md':'text/markdown; charset=utf-8'};
const server=http.createServer(async(req,res)=>{
 const headers={'X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Cache-Control':'no-store','Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'; worker-src 'self'"};
 try{
  if(!['GET','HEAD'].includes(req.method)){res.writeHead(405,headers).end();return;}
  let pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  if(pathname.split('/').some(p=>p.startsWith('.')&&p!=='.nojekyll')){res.writeHead(404,headers).end('Not found');return;}
  let file=resolve(root,'.'+pathname);if(file!==root&&!file.startsWith(root+sep)){res.writeHead(403,headers).end('Forbidden');return;}
  const info=await stat(file);if(info.isDirectory()){if(!pathname.endsWith('/')){res.writeHead(301,{...headers,Location:pathname+'/'}).end();return;}file=resolve(file,'index.html');}
  const actual=await realpath(file);if(actual!==root&&!actual.startsWith(root+sep)){res.writeHead(403,headers).end('Forbidden');return;}
  const data=await readFile(actual);res.writeHead(200,{...headers,'Content-Type':types[extname(actual)]||'application/octet-stream','Content-Length':data.length});res.end(req.method==='HEAD'?undefined:data);
 }catch(error){res.writeHead(error.code==='ENOENT'?404:400,headers).end('Not found or invalid request');}
});
server.listen(port,host,()=>console.log(`RL Mission Control: http://${host}:${port}\nRoot: ${root}\nPress Ctrl+C to stop.`));
process.on('SIGINT',()=>server.close(()=>process.exit(0)));
