import io,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import translation
class TranslationTests(unittest.TestCase):
 def test_success_is_cached(self):
  with tempfile.TemporaryDirectory() as d,patch.object(translation,'CACHE',Path(d)/'translations.json'):
   response=io.BytesIO(json.dumps({'responseStatus':200,'responseData':{'translatedText':'数据库性能'}}).encode())
   with patch.object(translation.urllib.request,'urlopen',return_value=response) as request:
    self.assertEqual(translation.translate('Database performance'),'数据库性能')
    self.assertEqual(translation.translate('Database performance'),'数据库性能')
    self.assertEqual(request.call_count,1)
 def test_quota_failure_is_not_cached(self):
  with tempfile.TemporaryDirectory() as d,patch.object(translation,'CACHE',Path(d)/'translations.json'):
   response=io.BytesIO(json.dumps({'responseStatus':200,'quotaFinished':True,'responseDetails':'quota exceeded'}).encode())
   with patch.object(translation.urllib.request,'urlopen',return_value=response):
    with self.assertRaisesRegex(ValueError,'quota exceeded'):translation.translate('Agent deployment')
   self.assertFalse(translation.CACHE.exists())
if __name__=='__main__':unittest.main()
