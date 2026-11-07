"""Verify exact Sliwa-46 certificates and export attaining strategies offline."""
from __future__ import annotations
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,time,venv
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'third_party/vendor'),str(ROOT)]
sys.dont_write_bytecode=True

def require(ok,message):
    if not ok:raise RuntimeError(message)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_manifest():
    p=ROOT/'MANIFEST.sha256';require(p.is_file(),'Missing MANIFEST.sha256')
    expected={line.split('  ',1)[1]:line.split('  ',1)[0]for line in p.read_text(encoding='utf-8').splitlines()if line}
    actual={}
    for f in ROOT.rglob('*'):
        rel=f.relative_to(ROOT)
        if not f.is_file()or any(a in{'.git','__pycache__','exports','verification_runs'}for a in rel.parts):continue
        if f==p or f.suffix in{'.pyc','.pyo','.log'}:continue
        actual[rel.as_posix()]=digest(f)
    require(actual==expected,'Manifest mismatch: a tracked input is changed, missing or unexpected.')

def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')

def replay_upper(i,sandbox,executable,env):
    from bellverify.proof_inputs import check as bind_inputs
    from bellverify.replay_contract import check_entry,command_result_paths,snapshot,require_unchanged,snapshot_digest
    source=ROOT/'entries'/f'S{i:03d}';target=sandbox/'entries'/f'S{i:03d}'
    initial_binding=bind_inputs(source,i);source_files=snapshot(source)
    shutil.copytree(source,target)
    require_unchanged(target,source_files,context='Copied entry')
    upper=target/'upper_bound';config=check_entry(target,i)
    require(bind_inputs(target,i)==initial_binding,'Source and executed copy have different proof targets')
    started=time.monotonic();commands=[];step_checks=[]
    env=dict(env);env.update(PYTHONOPTIMIZE='0',PYTHONDONTWRITEBYTECODE='1')
    for command in config['commands']:
        require_unchanged(source,source_files,context='Source entry')
        require(bind_inputs(source,i)==initial_binding and bind_inputs(target,i)==initial_binding,
                'Upper target differs from the bound attaining target before execution')
        result_paths=command_result_paths(i,command)
        # Remove only this command's old result files in the disposable copy.
        # Every declared result must be produced anew; a previous root replay
        # cannot silently satisfy a missing producer step.
        for relative in result_paths:
            result=target/relative
            if result.exists():
                require(result.is_file()and not result.is_symlink(),'Invalid upper result path')
                result.unlink()
        input_files=snapshot(target,result_paths)
        if command.startswith('@'):
            args=[str(ROOT/'prooflib'/(command[1:]+'.py')),str(upper)]
        else:
            require(Path(command).name==command and (upper/command).is_file(),'Invalid upper verifier path')
            args=[str(upper/command)]
        print(f'S{i:03d}: upper {command}',flush=True)
        program=Path(args[0]);program_hash=digest(program)
        try:
            subprocess.run([str(executable),'-S',*args],cwd=upper,env=env,check=True)
        finally:
            require_unchanged(target,input_files,result_paths,'Executed proof inputs')
            require_unchanged(source,source_files,context='Source entry')
            require(digest(program)==program_hash,'Upper verifier program changed during execution')
            require(bind_inputs(source,i)==initial_binding and bind_inputs(target,i)==initial_binding,
                    'Upper target differs from the bound attaining target after execution')
        require(all((target/p).is_file()and not(target/p).is_symlink()for p in result_paths),
                'Upper command did not produce its declared fresh results')
        commands.append(command)
        step_checks.append({'command':command,'proof_inputs_unchanged':True,
                            'input_snapshot_sha256':snapshot_digest(input_files),
                            'fresh_result_files':list(result_paths)})
    return {'id':i,'status':'PASS_EXACT_GLOBAL_UPPER','commands':commands,'seconds':round(time.monotonic()-started,3),
            'fixed_command_contract':True,'source_entry_unchanged':True,'executed_inputs_unchanged':True,
            'target_sha256':initial_binding['target_sha256'],'source_entry_sha256':snapshot_digest(source_files),
            'step_checks':step_checks}

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True)
    for action in('verify','upper','export'):
        a=sub.add_parser(action);a.add_argument('--id',type=int);a.add_argument('--all',action='store_true')
        a.add_argument('--digits',type=int,default=80)
        a.add_argument('--report',help='Write a machine-readable execution report')
    sub.add_parser('manifest');sub.add_parser('list')
    args=p.parse_args()
    verify_manifest()
    if args.action=='manifest':print('PASS_MANIFEST');return
    if args.action=='list':
        for row in json.loads((ROOT/'catalogue.json').read_text(encoding='utf-8')):print(f"S{row['id']:03d}: {row['q_display']}")
        return
    require(args.all or args.id is not None,'Select --id N or --all')
    ids=list(range(1,47))if args.all else[args.id]
    require(all(1<=i<=46 for i in ids),'Entry id must be between 1 and 46')
    if args.action in('verify','upper','export'):require(__debug__,'Exact proof and strategy verifiers require assertions: do not use -O or -OO')
    from bellverify.proof_inputs import check as bind_inputs
    from bellverify.replay_contract import snapshot,require_unchanged
    from bellverify.exact import verify_binding
    from bellverify.strategy import export
    from tools.check_strategy import check as score
    from tools.check_exact_dag import check as dag
    records=[];upper_records=[];started=time.monotonic()
    env=os.environ.copy();env.update(PYTHONPATH=str(ROOT/'third_party/vendor'),PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='sliwa46-verify-')as temporary:
        sandbox=Path(temporary)
        executable=None
        if args.action in('verify','upper'):
            runtime=sandbox/'python'
            venv.EnvBuilder(with_pip=False,system_site_packages=False,symlinks=False).create(runtime)
            executable=runtime/('Scripts/python.exe'if os.name=='nt'else'bin/python')
        for i in ids:
            entry=ROOT/'entries'/f'S{i:03d}';binding=bind_inputs(entry,i);entry_files=snapshot(entry)
            if args.action in('verify','export'):
                dest=ROOT/'exports'/f'S{i:03d}'
                result=export(entry,dest,args.digits)
                save(dest/'independent_score.json',score(dest/'strategy_numeric.json'))
                save(dest/'independent_dag_audit.json',dag(dest/'strategy_exact.json',dest/'strategy_numeric.json'))
                records.append(result);print(f'S{i:03d}: exact attaining strategy PASS',flush=True)
            else:verify_binding(entry)
            if args.action in('verify','upper'):
                upper_result=replay_upper(i,sandbox,executable,env)
                require(upper_result['target_sha256']==binding['target_sha256'],
                        'Global upper and attainment refer to different exact targets')
                upper_records.append(upper_result)
            require_unchanged(entry,entry_files,context='Source entry')
            require(bind_inputs(entry,i)==binding,'Entry target changed during verification')
    verify_manifest()
    result={'status':'PASS_EXACT_GLOBAL_UPPER_AND_CONSTRUCTIVE_ATTAINMENT'if args.action=='verify'else'PASS_REQUESTED_CHECKS',
            'action':args.action,'ids':ids,'strategy_exports':records,'upper_bounds':upper_records,
            'seconds':round(time.monotonic()-started,3),
            'scope':'Exact upper proofs and exact constructive attainment'if args.action=='verify'else args.action}
    if args.report:save(Path(args.report),result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
