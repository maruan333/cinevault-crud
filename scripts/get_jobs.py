import urllib.request, json, pprint
url='https://api.github.com/repos/maruan333/cinevault-crud/actions/runs/26690805444/jobs'
with urllib.request.urlopen(url) as r:
    data=json.load(r)
out=[]
for j in data.get('jobs',[]):
    out.append({'id': j['id'], 'name': j['name'], 'conclusion': j['conclusion'], 'status': j['status'], 'steps': [(s.get('name'), s.get('conclusion')) for s in j.get('steps', [])]})
pp = pprint.PrettyPrinter()
pp.pprint(out)
