"""Rebuild the supplied NumPy variant; development tools are explicit inputs."""
from pathlib import Path
import argparse,hashlib,os,re,subprocess,sys,tarfile

def apply_unified(root,patch):
    lines=patch.splitlines(keepends=True);i=0
    while i<len(lines):
        if not lines[i].startswith('--- a/'):raise ValueError('Unexpected patch header')
        name=lines[i][6:].strip();i+=1
        if lines[i].strip()!='+++ b/'+name:raise ValueError('Patch target mismatch')
        i+=1;old=(root/name).read_text().splitlines(keepends=True);new=[];pos=0
        while i<len(lines) and not lines[i].startswith('--- a/'):
            m=re.match(r'@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@',lines[i])
            if not m:raise ValueError('Unexpected patch hunk')
            start=int(m.group(1))-1;new.extend(old[pos:start]);pos=start;i+=1
            while i<len(lines) and not lines[i].startswith(('@@','--- a/')):
                line=lines[i];i+=1
                if line.startswith((' ','-')):
                    if old[pos]!=line[1:]:raise ValueError('Source does not match patch')
                    pos+=1
                if line.startswith((' ','+')):new.append(line[1:])
        new.extend(old[pos:]);(root/name).write_text(''.join(new),newline='\n')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--toolchain',required=True,type=Path,help='LLVM-MinGW 20261104 extraction directory')
    p.add_argument('--build-deps',required=True,type=Path,help='Directory containing Cython 3.3.1 and Ninja 1.13.2')
    p.add_argument('--work',required=True,type=Path,help='New writable build directory')
    args=p.parse_args();root=Path(__file__).resolve().parents[2]
    arc=root/'sources/numpy-2.3.5.tar.gz'
    if hashlib.sha256(arc.read_bytes()).hexdigest()!='784db1dcdab56bf0517743e746dfb0f885fc68d948aba86eeec2cba234bdf1c0':raise ValueError('NumPy source hash mismatch')
    args.work.mkdir(parents=True,exist_ok=False)
    src=args.work.resolve()/'source';build=args.work.resolve()/'build';install=args.work.resolve()/'install'
    with tarfile.open(arc) as t:
        for m in t.getmembers():
            rel=Path(*Path(m.name).parts[1:])
            if '..' in rel.parts or rel.is_absolute():raise ValueError('Unsafe source member')
            dst=src/rel
            if m.isdir():dst.mkdir(parents=True,exist_ok=True)
            elif m.isfile():dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(t.extractfile(m).read())
    apply_unified(src,(Path(__file__).with_name('binary64-mingw.patch')).read_text())
    env=dict(os.environ);tools=args.toolchain.resolve()/'bin';deps=args.build_deps.resolve()
    env['PATH']=str(tools)+';'+str(deps/'bin')+';'+str(Path(sys.executable).parent)+';'+os.environ['SystemRoot']+'\\System32'
    env['PYTHONPATH']=str(deps);env['PYTHONDONTWRITEBYTECODE']='1'
    env['CC']=str(tools/'x86_64-w64-mingw32-clang.exe');env['CXX']=str(tools/'x86_64-w64-mingw32-clang++.exe')
    env['CYTHON']=str(deps/'bin/cython.exe')
    flags='-mlong-double-64 -ffile-prefix-map=../source=numpy-source'
    env['CFLAGS']=env['CXXFLAGS']=flags
    meson=[sys.executable,str(src/'vendored-meson/meson/meson.py')]
    subprocess.run(meson+['setup',str(build),str(src),'--prefix='+str(install),'-Dblas=none','-Dlapack=none','-Dcpu-dispatch=none','-Dcpu-baseline=min','-Dbuildtype=release'],env=env,check=True)
    subprocess.run(meson+['compile','-C',str(build),'-j','4'],env=env,check=True)
    subprocess.run(meson+['install','-C',str(build)],env=env,check=True)
    cfg=install/'Lib/site-packages/numpy/__config__.py';s=cfg.read_text()
    s=re.sub(r'(\"commands\": r\")[^\"]+[/\\]([^/\\\"]+)(\")',r'\1\2\3',s)
    s=re.sub(r'(\"path\": r\")[^\"]+[/\\](python.exe)(\")',r'\1\2\3',s)
    cfg.write_text(s,newline='\n')
    print(install/'Lib/site-packages')

if __name__=='__main__':main()
