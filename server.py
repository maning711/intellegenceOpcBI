import concurrent.futures as cf, datetime as dt, email.utils, html, json, re, threading, time, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
ROOT=Path(__file__).resolve().parent
CACHE=ROOT/'data/news.json'
LOCK=threading.Lock()
SOURCES=[('PostgreSQL','database','https://www.postgresql.org/news.rss'),('MongoDB','database','https://www.mongodb.com/blog/rss'),('AWS Database','database','https://aws.amazon.com/blogs/database/feed/'),('Azure SQL','database','https://devblogs.microsoft.com/azure-sql/feed/'),('TechCrunch AI','ai','https://techcrunch.com/category/artificial-intelligence/feed/'),('Google Research','ai','https://research.google/blog/rss/'),('Hugging Face','ai','https://huggingface.co/blog/feed.xml'),('Simon Willison','fde','https://simonwillison.net/atom/everything/'),('The New Stack','fde','https://thenewstack.io/feed/')]
def clean(s):return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>',' ',s or ''))).strip()
def fetch(s):
 name,category,url=s
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'WorldPulse/1.0 RSS'})
  with urllib.request.urlopen(req,timeout=20) as r:raw=r.read(4000001)
  if len(raw)>4000000:raise ValueError('Feed too large')
  root=ET.fromstring(raw); rows=[]
  for e in (root.findall('.//item') or root.findall('{http://www.w3.org/2005/Atom}entry'))[:35]:
   def val(*keys):
    for k in keys:
     child=e.find(k)
     if child is not None:return ''.join(child.itertext())
    return ''
   title=clean(val('title','{http://www.w3.org/2005/Atom}title'));summary=clean(val('description','{http://www.w3.org/2005/Atom}summary','{http://www.w3.org/2005/Atom}content'))[:650]
   link=val('link') or next((l.get('href','') for l in e.findall('{http://www.w3.org/2005/Atom}link') if l.get('rel','alternate')=='alternate'),'')
   if not title or not link.startswith(('https://','http://')):continue
   if category=='fde' and not any(w in (title+' '+summary).lower() for w in ['agent','deploy','production','enterprise','workflow','evaluation','observability','integration','customer','engineering']):continue
   stamp=val('pubDate','{http://www.w3.org/2005/Atom}published','{http://www.w3.org/2005/Atom}updated')
   try:
    try:date=email.utils.parsedate_to_datetime(stamp)
    except Exception:date=dt.datetime.fromisoformat(stamp.replace('Z','+00:00'))
    if date.tzinfo is None:date=date.replace(tzinfo=dt.timezone.utc)
    published=date.isoformat()
   except Exception:published=None
   rows.append(dict(title=title,summary=summary,url=link,published=published,source=name,category=category))
  if not rows:raise ValueError('No matching feed entries')
  return rows,dict(name=name,category=category,url=url,ok=True,count=len(rows))
 except Exception as ex:return [],dict(name=name,category=category,url=url,ok=False,error=str(ex)[:160])
def read():
 try:return json.loads(CACHE.read_text())
 except (OSError,ValueError):return dict(articles=[],sources=[],updated=None)
def refresh():
 if not LOCK.acquire(False):return read()
 try:
  old=read(); articles=[];sources=[]
  with cf.ThreadPoolExecutor(max_workers=9) as pool:
   for rows,status in pool.map(fetch,SOURCES):
    if not status['ok']:rows=[dict(a,stale=True) for a in old['articles'] if a['source']==status['name']]
    articles.extend(rows);sources.append(status)
  payload=dict(articles=sorted({a['url']:a for a in articles}.values(),key=lambda a:a['published'] or '',reverse=True),sources=sources,updated=dt.datetime.now(dt.timezone.utc).isoformat())
  CACHE.parent.mkdir(exist_ok=True);temp=CACHE.with_suffix('.tmp');temp.write_text(json.dumps(payload,ensure_ascii=False));temp.replace(CACHE);return payload
 finally:LOCK.release()
def daily():
 while True:
  try:age=time.time()-dt.datetime.fromisoformat(read()['updated']).timestamp()
  except Exception:age=86401
  if age>=86400:refresh()
  time.sleep(60)
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kw):super().__init__(*args,directory=str(ROOT/'static'),**kw)
 def respond(self,data):
  body=json.dumps(data,ensure_ascii=False).encode();self.send_response(200);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
 def do_GET(self):
  if self.path=='/api/news':self.respond(read())
  else:super().do_GET()
 def do_POST(self):
  if self.path=='/api/refresh':self.respond(refresh())
  else:self.send_error(404)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--refresh',action='store_true');p.add_argument('--port',type=int,default=8765);a=p.parse_args()
 if a.refresh:
  result=refresh();print(json.dumps(dict(count=len(result['articles']),sources=result['sources']),ensure_ascii=False,indent=2))
 else:
  threading.Thread(target=daily,daemon=True).start();print(f'http://127.0.0.1:{a.port}',flush=True);ThreadingHTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
