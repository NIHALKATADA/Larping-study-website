import glob

OLD = ' onclick="document.getElementById(\'fabMenu\').classList.toggle(\'open\'); this.classList.toggle(\'active\');"'
for p in glob.glob('*/comprehensive-report.html'):
    s = open(p, encoding='utf-8').read()
    n = s.count(OLD)
    s = s.replace(OLD, '')
    open(p, 'w', encoding='utf-8').write(s)
    print(p, 'removed', n)
