"""Targeted regression controls for the fixed upper/attainment replay chain.

No original entry is written. Copies exercise the actual S46 reduced verifier,
complete positive S2/S28/S46 upper chains, and the common replay guards. This
does not stand in for the separate complete 46-entry verification run.
"""
from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'third_party/vendor'),str(ROOT)]
sys.dont_write_bytecode=True
import run as runner
from bellverify.proof_inputs import check as bind_inputs
from bellverify.replay_contract import (command_result_paths,expected_config,
                                      require_unchanged,snapshot)


def require(ok,message):
    if not ok:raise ArithmeticError(message)


def load(path):return json.loads(path.read_text(encoding='utf-8'))
def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,help='New directory for the report and command logs')
    args=parser.parse_args()
    out=args.output.resolve()if args.output else ROOT/'verification_runs/target_binding_controls'
    require(not out.exists(),'Use a new output directory')
    if ROOT in out.parents:
        require((ROOT/'verification_runs')in out.parents,'Inside the package, use verification_runs for test output')
    out.mkdir(parents=True)
    env=os.environ.copy();env.update(PYTHONPATH=str(ROOT/'third_party/vendor'),
                                     PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
    real_run=subprocess.run
    negatives=[];positives=[];started=time.monotonic()

    def rejects(name,action,expected_message):
        try:action()
        except RuntimeError as error:
            require(expected_message in str(error),f'{name}: rejected for an unrelated reason: {error}')
            negatives.append({'case':name,'status':'PASS_REJECTED','reason':str(error)})
        else:raise ArithmeticError('Regression input was accepted: '+name)

    total=0
    for i in range(1,47):
        result=bind_inputs(ROOT/'entries'/f'S{i:03d}',i)
        require(result['id']==i and result['status']=='PASS_UPPER_ATTAINMENT_INPUT_BINDING','Original binding failed')
        total+=len(expected_config(i)['commands'])
    require(total==52,'The fixed contract must preserve the original 52 commands')
    positives.append({'case':'all_46_original_input_bindings','entries':46,'ordered_upper_commands':total})

    with tempfile.TemporaryDirectory(prefix='sliwa-target-controls-')as temporary:
        temp=Path(temporary)
        def copy_entry(name,i):
            destination=temp/name
            shutil.copytree(ROOT/'entries'/f'S{i:03d}',destination)
            return destination

        changes=[
            ('empty_command_list',2,lambda c:c.update(commands=[])),
            ('missing_required_command',46,lambda c:c.update(commands=c['commands'][:-1])),
            ('duplicate_command',46,lambda c:c.update(commands=[c['commands'][0]]*4)),
            ('reordered_commands',46,lambda c:c.update(commands=list(reversed(c['commands'])))),
            ('wrong_engine',2,lambda c:c.update(engine='individual')),
            ('result_cannot_replace_characteristic_input',2,lambda c:c.update(characteristic_file='result.json')),
            ('wrong_config_identifier',2,lambda c:c.update(id=3)),
            ('certificate_cannot_declare_writable_inputs',2,lambda c:c.update(writable_outputs=['certificate.json'])),
        ]
        for name,i,change in changes:
            entry=copy_entry(name,i);path=entry/'upper_bound/inputs.json';config=load(path)
            change(config);save(path,config)
            rejects(name,lambda e=entry,j=i:bind_inputs(e,j),'fixed replay contract')

        for label,delta in [('above',Fraction(1,10**20)),('below',-Fraction(1,10**20))]:
            entry=copy_entry('s40_interval_'+label,40);path=entry/'upper_bound/S40_full_certificate.json'
            certificate=load(path);certificate['q_interval']=[str(Fraction(v)+delta)for v in certificate['q_interval']]
            save(path,certificate)
            rejects('s40_interval_'+label,lambda e=entry:bind_inputs(e,40),'global q interval differs')
        entry=copy_entry('s40_box_center_mismatch',40);path=entry/'upper_bound/S40_selected_root.json'
        root=load(path);root['centers'][0]=str(Fraction(root['centers'][0])+Fraction(1,10**20));save(path,root)
        rejects('s40_box_center_mismatch',lambda:bind_inputs(entry,40),'stored root box differs')

        entry=copy_entry('s46_false_ten_binding',46)
        spec=load(entry/'strategy_spec.json')
        spec.update(polynomial='q-10',interval=['9','11'],overlaps=['1','1','1']);save(entry/'strategy_spec.json',spec)
        path=entry/'upper_bound/certificate_46_reduced.json';certificate=load(path)
        certificate.update(polynomial='q-10',isolating_interval=['9','11'],attaining_t='1');save(path,certificate)
        rejects('s46_false_ten_binding',lambda:bind_inputs(entry,46),'different q intervals')

        reduced_cases=[('s46_wrong_polynomial','polynomial','q-10','input polynomial'),
                       ('s46_wrong_interval','isolating_interval',['12','13'],'input interval'),
                       ('s46_wrong_attaining_overlap','attaining_t','1','input attaining overlap')]
        for name,key,value,message in reduced_cases:
            entry=copy_entry(name,46);upper=entry/'upper_bound';path=upper/'certificate_46_reduced.json'
            certificate=load(path);certificate[key]=value;save(path,certificate)
            before=hashlib.sha256(path.read_bytes()).hexdigest();log=out/(name+'.log')
            with log.open('w',encoding='utf-8')as handle:
                result=real_run([sys.executable,'-S',str(upper/'verify_46_reduced.py')],cwd=upper,env=env,
                                stdout=handle,stderr=subprocess.STDOUT)
            require(result.returncode!=0 and message in log.read_text(),name+': verifier did not reject the intended defect')
            require(hashlib.sha256(path.read_bytes()).hexdigest()==before,'S46 verifier overwrote its input')
            negatives.append({'case':name,'status':'PASS_REJECTED','returncode':result.returncode,
                              'certificate_unchanged':True,'log':log.name})

        positive_targets={}
        def replay(i,sandbox,log,after_command=None):
            def logged_run(*a,**kw):
                kw.update(stdout=handle,stderr=subprocess.STDOUT)
                result=real_run(*a,**kw)
                if after_command is not None:after_command(a,kw)
                return result
            with log.open('w',encoding='utf-8')as handle,redirect_stdout(handle),patch.object(runner.subprocess,'run',logged_run):
                return runner.replay_upper(i,sandbox,sys.executable,env)

        for i in (2,28,46):
            sandbox=temp/f'positive_s{i}';sandbox.mkdir()
            log=out/f'positive_s{i:03d}.log';record=replay(i,sandbox,log)
            require(record['commands']==expected_config(i)['commands'],'A required positive command was skipped')
            require(record['executed_inputs_unchanged']and record['source_entry_unchanged'],'Missing immutability check')
            positives.append({'case':f'original_s{i:03d}_complete_upper_chain','log':log.name,**record})
            positive_targets[i]=sandbox/'entries'/f'S{i:03d}'
        positives.append({'case':'per_step_fresh_results_allowed','scope':'All expected result JSON files were produced by the three positive chains without being mistaken for original proof inputs.'})

        # The S28 root result is writable only for its producer. The global
        # consumer must see it as an ordinary frozen input.
        target=positive_targets[28];outputs=command_result_paths(28,'verify_s28_global_independent.py')
        before=snapshot(target,outputs);relative='upper_bound/S28_root_independent_replay.json'
        require(relative in before,'S28 intermediate proof was globally exempted as output')
        path=target/relative;path.write_bytes(path.read_bytes()+b'\n')
        rejects('s28_intermediate_result_is_frozen_for_consumer',
                lambda:require_unchanged(target,before,outputs),'S28_root_independent_replay.json')

        # Actually execute the small S2 upper proof, then simulate the former
        # post-execution input write. A mathematical no-op byte edit must also
        # fail, since the bound proof input is immutable during execution.
        sandbox=temp/'mutate_executed';sandbox.mkdir()
        def alter_executed(a,kw):
            path=Path(kw['cwd'])/'S02_charpoly.txt';path.write_bytes(path.read_bytes()+b'\n')
        rejects('executed_input_write_after_successful_command',
                lambda:replay(2,sandbox,out/'mutate_executed.log',alter_executed),'Executed proof inputs changed')

        fake=temp/'source_guard_package';(fake/'entries').mkdir(parents=True)
        shutil.copytree(ROOT/'entries/S002',fake/'entries/S002')
        shutil.copytree(ROOT/'prooflib',fake/'prooflib')
        sandbox=temp/'mutate_source';sandbox.mkdir()
        def alter_source(a,kw):
            path=fake/'entries/S002/strategy_spec.json';path.write_bytes(path.read_bytes()+b'\n')
        with patch.object(runner,'ROOT',fake):
            rejects('source_input_write_after_successful_command',
                    lambda:replay(2,sandbox,out/'mutate_source.log',alter_source),'Source entry changed')

    report={'status':'PASS_TARGET_BINDING_REGRESSION_CONTROLS','negative_controls':len(negatives),
            'positive_controls':positives,'rejected':negatives,'original_entries_written':False,
            'fixed_catalogue_entries':46,'fixed_upper_command_count':52,
            'scope':'Specific command omission/order, S46 input overwrite/target, S40 interval binding, per-step input immutability and S28 intermediate-result controls. Includes complete positive S2/S28/S46 upper replays; does not replace the full 46-entry verification.',
            'seconds':round(time.monotonic()-started,6)}
    save(out/'target_binding_controls.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
