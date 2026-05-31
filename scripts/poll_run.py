import time, urllib.request, json, sys
url = 'https://api.github.com/repos/maruan333/cinevault-crud/actions/runs/26690805444'
for i in range(40):
    try:
        with urllib.request.urlopen(url) as resp:
            r = json.load(resp)
    except Exception as e:
        print(time.strftime('%Y-%m-%dT%H:%M:%S'), 'error', e)
        time.sleep(5)
        continue
    print(time.strftime('%Y-%m-%dT%H:%M:%S'), r.get('status'), r.get('conclusion'))
    if r.get('status') == 'completed':
        sys.exit(0)
    time.sleep(5)
sys.exit(1)
