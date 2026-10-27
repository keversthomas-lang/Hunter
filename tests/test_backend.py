import base64, hashlib, importlib.util, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('hunter',Path(__file__).parents[1]/'backend/server.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)

class HunterTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.old_private=h.PRIVATE;self.old_files=h.FILES
        h.PRIVATE=Path(self.tmp.name);h.FILES=h.PRIVATE/'files';h.FILES.mkdir()
    def tearDown(self):h.PRIVATE=self.old_private;h.FILES=self.old_files;self.tmp.cleanup()
    def row(self,**kw):return h.normalize({'company':'Test Co','role':'COO','url':'https://example.com/jobs/coo','text':'Lead operations','date':str(h.today()),'match':85,'score':90,'compatible':True,'verified':True,'openConfirmed':True,**kw},True)
    def test_persistence(self):h.put('a',{'b':'é'});self.assertEqual(h.get('a'),{'b':'é'})
    def test_unverified_rejected(self):
        r=h.eligible(self.row(verified=False),{'match':70,'period':5});self.assertEqual(r['status'],'rejected');self.assertIn('Date non vérifiée',r['reason'])
    def test_closed_rejected(self):self.assertEqual(h.eligible(self.row(openConfirmed=False),{'match':70,'period':5})['status'],'rejected')
    def test_period_boundary(self):
        from datetime import timedelta
        r=self.row(date=str(h.today()-timedelta(days=5)));self.assertEqual(h.eligible(r,{'match':70,'period':5})['status'],'rejected')
    def test_reject_invalid_link(self):
        with self.assertRaises(ValueError):self.row(url='javascript:alert(1)')
    def test_future_date_not_fresh(self):self.assertFalse(self.row(date='2099-01-01')['verified'])
    def test_master_upload(self):
        text='Reference verified experience. '*10
        result=h.master_upload({'name':'master.txt','data':base64.b64encode(text.encode()).decode()})
        self.assertEqual(result['characters'],len(text));self.assertEqual(h.cv()['text'],text)
    def test_generation_waits_for_answers(self):
        h.put('master',{'text':'Verified source','hash':'abc'})
        r=self.row();h.put('opportunities',[r]);h.put('analysis:'+r['id'],{'masterHash':'abc','jobHash':h.job_hash(r),'questions':[{'id':'q0'}]})
        with self.assertRaisesRegex(ValueError,'Répondez'):h.generate({'id':r['id']})
    def test_stale_analysis_blocks_generation(self):
        h.put('master',{'text':'Verified source','hash':'new'});r=self.row();h.put('opportunities',[r]);h.put('analysis:'+r['id'],{'masterHash':'old','jobHash':h.job_hash(r)})
        with self.assertRaisesRegex(ValueError,'Refaites'):h.generate({'id':r['id']})
    def test_unopened_page_not_selected(self):
        h.put('master',{'text':'verified master','hash':'a'})
        row=self.row();row.update(dateEvidence='date',locationEvidence='remote',openEvidence='Apply')
        with patch.object(h,'ai',return_value=({'opportunities':[row]},set())):h.run_search({'match':70,'period':5})
        self.assertEqual(h.get('opportunities')[0]['status'],'rejected')
    def test_repeat_search_deduplicates(self):
        h.put('master',{'text':'verified master','hash':'a'});row=self.row();row.update(dateEvidence='date',locationEvidence='remote',openEvidence='Apply')
        with patch.object(h,'ai',return_value=({'opportunities':[row]},{row['url']})):
            h.run_search({'match':70,'period':5});h.run_search({'match':70,'period':5})
        self.assertEqual(len(h.get('opportunities')),1)
    def test_stale_generated_cv(self):
        r=self.row();h.put('opportunities',[r]);h.put('master',{'hash':'x'});h.put('generated:'+r['id'],{'masterHash':'old','jobHash':h.job_hash(r),'answersHash':'x'})
        self.assertIsNone(h.valid_generated(r['id']))
    def test_analysis_downgrades_false_evidence(self):
        r=self.row();h.put('opportunities',[r]);h.put('master',{'text':'Built a team','hash':'a'})
        response={'match':80,'keywords':[{'coverage':'covered','evidence':'SOC2 certification'}],'questions':[]}
        with patch.object(h,'ai',return_value=(response,set())):result=h.analyze({'id':r['id']})
        self.assertEqual(result['keywords'][0]['coverage'],'uncertain');self.assertEqual(h.get('opportunities')[0]['match'],80)
    def test_guard_missing_key(self):
        with patch.object(h,'env',return_value={}):
            with self.assertRaisesRegex(ValueError,'OPENAI_API_KEY'):h.ai('instructions',{})

    def test_cv_request_without_api_key(self):
        h.put('master',{'text':'Verified source','hash':'abc'});r=self.row();h.put('opportunities',[r])
        with patch.object(h,'env',return_value={}):result=h.request_cv({'id':r['id']})
        self.assertEqual(result['status'],'awaiting_chat');self.assertIn(r['id'],result['prompt']);self.assertNotIn('Verified source',result['prompt'])
        self.assertEqual(h.request_cv({'id':r['id']})['id'],result['id'])
    def test_cv_request_blocks_pending_answers(self):
        h.put('master',{'text':'Verified source','hash':'abc'});r=self.row();h.put('opportunities',[r]);h.put('analysis:'+r['id'],{'masterHash':'abc','jobHash':h.job_hash(r),'questions':[{'id':'q0'}]})
        with self.assertRaisesRegex(ValueError,'Répondez'):h.request_cv({'id':r['id'],'stage':'generate'})
    def test_cv_request_accepts_confirmed_answers(self):
        h.put('master',{'text':'Verified source','hash':'abc'});r=self.row();h.put('opportunities',[r]);h.put('analysis:'+r['id'],{'masterHash':'abc','jobHash':h.job_hash(r),'questions':[{'id':'q0'}]});h.put('answers:'+r['id'],{'q0':{'state':'confirmed','text':'Confirmed answer'}})
        result=h.request_cv({'id':r['id'],'stage':'generate'});self.assertEqual(result['stage'],'generate')

if __name__=='__main__':unittest.main()
