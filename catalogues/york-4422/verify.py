"""Replay a single mathematical certificate locally without altering the distributed inputs."""
import argparse,hashlib,json,os,sys,subprocess,tempfile,zipfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def extract(z,target):
    target=target.resolve()
    for name in z.namelist():
        if not (target/name).resolve().is_relative_to(target.resolve()):raise ValueError(name)
    # Use Windows' extended path syntax when certificate subdirectories are long.
    # This changes neither archive member names nor their byte-level hashes.
    if os.name=='nt' and not str(target).startswith('\\\\?\\'):
        path=str(target)
        target=Path('\\\\?\\UNC\\'+path[2:] if path.startswith('\\\\') else '\\\\?\\'+path)
    z.extractall(target)
def unpack(E,target):
    config=json.loads((E/'proof.json').read_text(encoding='utf-8'))
    with tempfile.TemporaryFile() as file:
        h=hashlib.sha256()
        for name in config['parts']:
            x=(E/name).read_bytes();h.update(x);file.write(x)
        if h.hexdigest()!=config['sha256']:raise ValueError('Certificate digest mismatch.')
        with zipfile.ZipFile(file) as z:extract(z,target)
    return config
def runtime(tmp,n):
    import struct
    native=os.name=='nt' and sys.version_info[:2]==(3,12) and struct.calcsize('P')==8
    tags=['symbolic']
    if native and n in (9,13,41,59,124,128,139,165,168,169,172):tags+=['flint','scientific']
    out=tmp/'libraries';out.mkdir()
    for tag in tags:
        info=json.loads((ROOT/'runtime'/(tag+'.json')).read_text())
        with tempfile.TemporaryFile() as stream:
            h=hashlib.sha256()
            for part in info['parts']:
                x=(ROOT/'runtime'/part['file']).read_bytes()
                assert hashlib.sha256(x).hexdigest()==part['sha256']
                h.update(x);stream.write(x)
            assert h.hexdigest()==info['sha256']
            with zipfile.ZipFile(stream) as z:extract(z,out)
    return str(out)
def run(n):
    if not __debug__:raise RuntimeError('Verification requires assertions.')
    E=ROOT/'entries'/f'Y{n:03}'
    config=json.loads((E/'proof.json').read_text(encoding='utf-8'))
    env=dict(os.environ);env.update(PYTHONOPTIMIZE='',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',OMP_NUM_THREADS='1')
    with tempfile.TemporaryDirectory(prefix=f'y{n:03}_') as tmp:
        tmp=Path(tmp);core=tmp/'entry';core.mkdir();unpack(E,core)
        check_table(E,core,config)
        env['PYTHONPATH']=runtime(tmp,n)
        for exe in config['commands']:
            print('Running',n,exe,flush=True)
            args=exe if isinstance(exe,list) else [exe]
            subprocess.run([sys.executable,'-B',*args],env=env,cwd=core,check=True)
    print('PASS',f'Y{n:03}',flush=True)
def check_table(entry,tmp,config):
    public=json.loads((entry/'definition.json').read_text(encoding='utf8'))
    raw=[x for row in public['probability_table'] for x in row]
    binding=config['table_binding'];value=json.loads((tmp/binding['file']).read_bytes())
    for key in binding['path']:
        if key=='@R,C':value=value['R']+[x for row in value['C'] for x in row]
        else:value=value[key]
    if value!=raw or value!=public['coefficient_crosswalk']['CH25']:raise ValueError('Original Bell table mismatch.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('number',type=int);p.add_argument('--extract',type=Path);a=p.parse_args()
    if not 1<=a.number<=175:p.error('Choose a number from 1 to 175.')
    if a.number in (83,92,125,128):
        print('Exact unrestricted quantum supremum: unknown.')
    elif a.extract is not None:
        a.extract.mkdir(parents=True,exist_ok=False)
        entry=ROOT/'entries'/f'Y{a.number:03}'
        config=unpack(entry,a.extract)
        table_target=a.extract.resolve()
        if os.name=='nt' and not str(table_target).startswith('\\\\?\\'):
            path=str(table_target)
            table_target=Path('\\\\?\\UNC\\'+path[2:] if path.startswith('\\\\') else '\\\\?\\'+path)
        check_table(entry,table_target,config)
    else:run(a.number)

