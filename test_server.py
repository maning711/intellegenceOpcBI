import json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import server
class FeedTests(unittest.TestCase):
 def test_atom_feed_and_unsafe_link(self):
  raw=b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Agent deployment</title><link href="https://example.com/news"/><updated>2026-11-15T10:00:00Z</updated><summary>Production &amp; evaluation</summary></entry><entry><title>bad</title><link href="javascript:alert(1)"/></entry></feed>'''
  class Response:
   def __enter__(self): return self
   def __exit__(self,*args): pass
   def read(self,*args): return raw
  with patch.object(server.urllib.request,'urlopen',return_value=Response()):
   rows,status=server.fetch(('Example','fde','https://example.com/rss'))
  self.assertTrue(status['ok']);self.assertEqual(len(rows),1);self.assertEqual(rows[0]['summary'],'Production & evaluation');self.assertIsNotNone(rows[0]['published'])
 def test_failed_source_preserves_cached_articles(self):
  with tempfile.TemporaryDirectory() as directory:
   cache=Path(directory)/'news.json';cache.write_text(json.dumps({'articles':[dict(source='Example',url='https://example.com/old',published=None,category='ai',title='Old',summary='')],'sources':[],'updated':None}))
   with patch.object(server,'CACHE',cache),patch.object(server,'SOURCES',[('Example','ai','https://example.com/rss')]),patch.object(server,'fetch',return_value=([],dict(name='Example',category='ai',ok=False,error='timeout'))):
    result=server.refresh()
   self.assertTrue(result['articles'][0]['stale']);self.assertFalse(result['sources'][0]['ok']);self.assertEqual(json.loads(cache.read_text()),result)
if __name__=='__main__':unittest.main()
