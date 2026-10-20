from daily20 import RUN,write,fetch
urls={
'calviri':'https://www.calviri.com/_files/ugd/0c6e92_4c2de71dc15947a68ef654f53efdbd80.pdf',
'cancv4':'https://cve.edu.au/Common/Uploaded%20files/CT/Canine%20Cancer%20Vaccine%20CnT%206027%20June%202024.pdf',
'brain-carmustine':'https://readyfor.jp/projects/k9braintumor',
'histotripsy-publication':'https://www.nature.com/articles/s41598-026-42319-z'}
p=[dict(source_id='discovery:'+k,url=v,route='clinical_signal_primary') for k,v in urls.items()]
write(RUN/'last-leads-plan.json',p)
fetch(p)
