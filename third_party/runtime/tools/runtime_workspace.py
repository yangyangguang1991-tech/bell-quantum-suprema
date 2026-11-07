"""Create a writable runtime workspace and test user-replaced shared libraries.

Standard library only. No downloads, installation, or edits to release inputs.
This utility is not a mathematical proof verifier.
"""
from pathlib import Path, PurePosixPath
import argparse, bisect, hashlib, io, json, os, struct, subprocess, sys, zipfile

ROOT = Path(__file__).resolve().parents[3]
SUPPLY = Path(__file__).resolve().parents[1]

class Parts(io.RawIOBase):
    def __init__(self, paths):
        self.paths=paths;self.sizes=[p.stat().st_size for p in paths]
        self.offsets=[0];self.pos=0;self.streams={}
        for n in self.sizes:self.offsets.append(self.offsets[-1]+n)
    def seekable(self):return True
    def readable(self):return True
    def tell(self):return self.pos
    def seek(self, n, whence=0):
        p=n if whence==0 else self.pos+n if whence==1 else self.offsets[-1]+n
        if p<0:raise ValueError('Negative seek.')
        self.pos=p;return p
    def read(self,n=-1):
        if n<0:n=self.offsets[-1]-self.pos
        out=[]
        while n>0 and self.pos<self.offsets[-1]:
            i=bisect.bisect_right(self.offsets,self.pos)-1
            if i not in self.streams:self.streams[i]=self.paths[i].open('rb')
            f=self.streams[i];f.seek(self.pos-self.offsets[i])
            b=f.read(min(n,self.offsets[i+1]-self.pos))
            if not b:raise OSError('Unexpected end of archive part.')
            out.append(b);self.pos+=len(b);n-=len(b)
        return b''.join(out)
    def close(self):
        for f in self.streams.values():f.close()
        super().close()

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while b:=f.read(4<<20):h.update(b)
    return h.hexdigest()

def safe(root,name):
    part=PurePosixPath(name)
    if not name or part.is_absolute() or '..' in part.parts or '\\' in name:
        raise ValueError('Unsafe archive name: '+name)
    p=(root/name).resolve()
    if not p.is_relative_to(root.resolve()):raise ValueError('Escaping archive name.')
    return p

def workspace(p):
    p=p.resolve()
    if p.is_relative_to(ROOT):raise ValueError('Use a workspace outside the release directory.')
    return p

def verify_sources():
    count=0
    for line in (SUPPLY/'sources.sha256').read_text().splitlines():
        expected,name=line.split('  ',1);p=safe(SUPPLY,name)
        if digest(p)!=expected:raise ValueError('Source hash mismatch: '+name)
        count+=1
    print(json.dumps({'source_archives_checked':count}))

def extract(dest,all_components):
    dest=workspace(dest);dest.mkdir(parents=True,exist_ok=False)
    if (ROOT/'catalogues/york-4422').exists():
        base=ROOT/'catalogues/york-4422/runtime'
        cfgs=[base/(n+'.json') for n in (('symbolic','scientific','flint') if all_components else ('flint',))]
    else:
        base=ROOT/'runtime';cfgs=[base/'manifest.json']
    receipt=[]
    for config in cfgs:
        info=json.loads(config.read_text());parts=[base/(x['file'] if isinstance(x,dict) else x) for x in info['parts']]
        h=hashlib.sha256()
        for p in parts:
            with p.open('rb') as f:
                while b:=f.read(4<<20):h.update(b)
        if h.hexdigest()!=info['sha256']:raise ValueError('Runtime archive hash mismatch.')
        count=0
        with Parts(parts) as stream,zipfile.ZipFile(stream) as z:
            for m in z.infolist():
                if m.is_dir():continue
                n=m.filename
                if not all_components and not n.startswith(('flint/','python_flint.libs/','python_flint-0.9.0.dist-info/')):continue
                if ((m.external_attr>>16)&0o170000)==0o120000:raise ValueError('Symlink not supported.')
                p=safe(dest,n);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(m));count+=1
        receipt.append({'archive_manifest':config.relative_to(ROOT).as_posix(),'archive_sha256':h.hexdigest(),'extracted_files':count})
    (dest/'runtime-extraction.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'workspace':str(dest),'bundles':receipt}))

PROBE = r'''
import sys,ctypes,pathlib,json
root=pathlib.Path(sys.argv[1]).resolve();sys.path.insert(0,str(root));import flint
assert pathlib.Path(flint.__file__).resolve().is_relative_to(root)
dll=next(root.glob('python_flint.libs/libflint*.dll'))
lib=ctypes.CDLL(str(dll));version=bytes((ctypes.c_char*6).in_dll(lib,'flint_version')).rstrip(b'\0').decode()
if sys.argv[2]:assert version==sys.argv[2],(version,sys.argv[2])
a=flint.fmpq_mat([[1,2],[3,4]])
assert str(a.det())=='-2'
assert a*a.inv()==flint.fmpq_mat([[1,0],[0,1]])
assert flint.fmpz(2)**100==1267650600228229401496703205376
assert flint.arb(2).sqrt().contains(1.4142135623730951)
print(json.dumps({'python_flint':flint.__version__,'loaded_flint_version':version,'integer_rational_matrix_and_ball_checks':True}))
'''

def probe(dest,version=''):
    if os.name!='nt' or struct.calcsize('P')!=8:raise ValueError('The supplied binary probe requires Windows x64.')
    env=dict(os.environ);env.update(PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1')
    subprocess.run([sys.executable,'-B','-c',PROBE,str(workspace(dest)),version],env=env,check=True,timeout=120)

def demonstrate(dest):
    dest=workspace(dest)
    p=next(dest.glob('python_flint.libs/libflint*.dll'));b=p.read_bytes();before=hashlib.sha256(b).hexdigest()
    if before!='aac725ed1c5dbb74c57230dda97634a87d6475e46acd54b3849d16c134a23e57':
        raise ValueError('Demonstration requires the original bundled FLINT DLL in a fresh workspace.')
    if b.count(b'3.6.0\0')!=1:raise ValueError('Unexpected version string layout.')
    b=b.replace(b'3.6.0\0',b'3.6.R\0');p.write_bytes(b)
    receipt={'changed_library':p.name,'before_sha256':before,'after_sha256':hashlib.sha256(b).hexdigest(),
             'change':'Exported version text only; no arithmetic code changed. This tests replacement, not source-build reproducibility or arbitrary ABI compatibility.'}
    probe(dest,'3.6.R')
    (dest/'replacement-demonstration.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('verify-sources')
    e=sub.add_parser('extract');e.add_argument('directory',type=Path);e.add_argument('--all-components',action='store_true')
    q=sub.add_parser('probe');q.add_argument('directory',type=Path);q.add_argument('--expected-flint-version',default='')
    d=sub.add_parser('demonstrate-replacement');d.add_argument('directory',type=Path)
    a=p.parse_args()
    if a.command=='verify-sources':verify_sources()
    elif a.command=='extract':extract(a.directory,a.all_components)
    elif a.command=='probe':probe(a.directory,a.expected_flint_version)
    else:demonstrate(a.directory)

if __name__=='__main__':main()
