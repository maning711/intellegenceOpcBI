"""Cached public-news translation using MyMemory; errors never replace source text."""
import hashlib, json, threading, urllib.parse, urllib.request
from pathlib import Path
CACHE=Path(__file__).resolve().parent/'data/translations.json'
LOCK=threading.Lock()
def translate(text):
 if not text:return ''
 key=hashlib.sha256(text.encode()).hexdigest()
 with LOCK:
  try:cache=json.loads(CACHE.read_text())
  except (OSError,ValueError):cache={}
  if key in cache:return cache[key]
  chunks=[];chunk=''
  for word in text.split():
   if len((chunk+' '+word).encode())>450 and chunk:chunks.append(chunk);chunk=''
   chunk=(chunk+' '+word).strip()
  if chunk:chunks.append(chunk)
  translated=[]
  for part in chunks:
   query=urllib.parse.urlencode({'q':part,'langpair':'en|zh-CN'})
   request=urllib.request.Request('https://api.mymemory.translated.net/get?'+query,headers={'User-Agent':'WorldPulse/1.0'})
   with urllib.request.urlopen(request,timeout=12) as r:data=json.load(r)
   if str(data.get('responseStatus'))!='200' or data.get('quotaFinished'):raise ValueError(data.get('responseDetails') or '翻译免费额度已用完，请稍后重试')
   value=data.get('responseData',{}).get('translatedText','')
   if not value or 'MYMEMORY WARNING' in value.upper():raise ValueError('翻译服务暂不可用')
   translated.append(value)
  result=' '.join(translated);cache[key]=result;CACHE.parent.mkdir(exist_ok=True);temporary=CACHE.with_suffix('.tmp');temporary.write_text(json.dumps(cache,ensure_ascii=False));temporary.replace(CACHE);return result
