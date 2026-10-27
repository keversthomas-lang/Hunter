"""Synthetic export smoke test. Does not use the candidate's CV or claim a tailored CV."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'backend'))
import server
from pypdf import PdfReader
folder=Path('/private/tmp/hunter-export-check');folder.mkdir(exist_ok=True)
server.FILES=folder
result={'id':'f'*32,'name':'Test Candidate','headline':'Operations Leader','contact':'Synthetic layout test','sections':[{'title':'Profile','paragraphs':['Synthetic text for checking the document layout only.']},{'title':'Experience','paragraphs':['Example role | 2020 - 2025','Built an example team and operating model.']}]}
server.export_documents(result,{'role':'Test Role','company':'Test Company'})
assert len(PdfReader(folder/(result['id']+'.pdf')).pages)<=2
print(folder/(result['id']+'.docx'))
print(folder/(result['id']+'.pdf'))
