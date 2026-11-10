"""Known-data exclusion check; not a comprehensive secrets scanner."""
import argparse
from pathlib import Path
import tarfile
import zipfile

SKIP={'build','dist','.git','.venv','venv','__pycache__'}
BAD_SUFFIX={'.pdf','.docx','.xlsx','.png','.jpg','.jpeg','.zip','.pem','.key','.pyc'}
# Construct patterns so this checker does not match its own source literals.
BAD_TEXT=[('/'+'Users/').encode(),('C:'+'\\Users\\').encode(),
          ('IT_PEP'+'-Regulations').encode(),('CD-'+'00302').encode(),
          ('kommunikation-in-'+'veraenderungsvorhaben').encode(),
          ('bo'+'sch').encode()]

def inspect(name,data):
    path=Path(name)
    if any(p in {'runs','inputs','outputs','work'} for p in path.parts):raise ValueError('Private/local directory in bundle: '+name)
    if path.suffix.lower() in BAD_SUFFIX or path.name=='.env':raise ValueError('Excluded artifact in bundle: '+name)
    lowered=data.lower()
    for pattern in BAD_TEXT:
        if pattern.lower() in lowered:raise ValueError('Private source/host pattern in '+name)

def main():
    p=argparse.ArgumentParser(description=__doc__);group=p.add_mutually_exclusive_group(required=True);group.add_argument('--source',type=Path);group.add_argument('--archive',type=Path);a=p.parse_args();count=0
    if a.source:
        for f in a.source.rglob('*'):
            rel=f.relative_to(a.source)
            if any(part in SKIP or part.endswith('.egg-info') for part in rel.parts):continue
            if f.is_symlink():raise ValueError('Review symlink before release: '+str(rel))
            if f.is_file():inspect(str(rel),f.read_bytes());count+=1
    else:
        archives=sorted(a.archive.iterdir()) if a.archive.is_dir() else [a.archive]
        for archive in archives:
            if archive.suffix=='.whl' or archive.suffix=='.zip':
                with zipfile.ZipFile(archive) as z:
                    for n in z.namelist():
                        if not n.endswith('/'):inspect(n,z.read(n));count+=1
            elif archive.name.endswith('.tar.gz'):
                with tarfile.open(archive) as t:
                    for member in t.getmembers():
                        if member.issym() or member.islnk():raise ValueError('Symlink in source archive')
                        if member.isfile():inspect(member.name,t.extractfile(member).read());count+=1
            else:raise ValueError('Unsupported archive: '+archive.name)
    if not count:raise ValueError('No files inspected.')
    print(f'PASS: {count} files checked for known excluded artifacts, host paths and trial-source identifiers. Not a general secrets guarantee.')

if __name__=='__main__':main()
