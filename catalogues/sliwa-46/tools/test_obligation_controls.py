"""Black-box regression controls for complete upper-proof obligations.

Run with assertions enabled. All mutations and verifier output stay in isolated
temporary entry copies; the package and its mathematical inputs are read-only.
The negative controls call the actual entry verifier, not a duplicate schema
implementation. Positive controls replay the six affected original entries;
S40 includes both of its upper commands. This is not a full 46-entry replay.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]
BOOTSTRAP=("import runpy,sys;from pathlib import Path;"
           "root=Path(sys.argv[1]);script=sys.argv[2];"
           "sys.path[:0]=[str(root/'third_party'/'vendor'),str(root)];"
           "sys.argv=sys.argv[2:];runpy.run_path(script,run_name='__main__')")


def negative_cases():
    cases=[]
    common=[
        ('empty_cover_arrays','All six outer slabs are required'),
        ('missing_outer_slab','All six outer slabs are required'),
        ('duplicate_outer_slab','Slab cover'),
        ('empty_spectral_array','All seven spectral coefficients required'),
        ('repeated_spectral_index','Spectral coefficient indices must be 1 through 7 exactly once'),
        ('duplicate_outer_leaf','Duplicate leaf'),
        ('duplicate_spectral_leaf','Duplicate leaf'),
        ('empty_outer_leaves','Nonempty leaf cover required'),
        ('empty_spectral_leaves','Nonempty leaf cover required'),
    ]
    for entry in (19,22,39,40):
        for mutation,reason in common:
            cases.append({'name':f'S{entry:03d}_{mutation}','entry':entry,
                          'mutation':mutation,'expected_rejection':reason})
    for mutation,reason in common[-4:]:
        cases.append({'name':f'S024_{mutation}','entry':24,
                      'mutation':mutation,'expected_rejection':reason})
    cases.append({'name':'S023_four_copies_of_e1','entry':23,'mutation':'four_copies_of_e1',
                  'expected_rejection':'All four S23 obligations must occur exactly once'})
    selected=[
        ('q_interval_minus_1e20','Certificate q interval differs from selected root'),
        ('q_interval_plus_1e20','Certificate q interval differs from selected root'),
        ('unbound_q_box','Stored root box must equal centers plus/minus radius'),
        ('unbound_overlap_box','Stored root box must equal centers plus/minus radius'),
        ('unbound_center','Stored root box must equal centers plus/minus radius'),
        ('zero_radius','Selected-root radius must be positive'),
        ('negative_radius','Selected-root radius must be positive'),
        ('wrong_variable_order','Selected-root variable order must be q,x,y'),
        ('missing_equation','Selected-root system must have three equations'),
        ('extra_equation','Selected-root system must have three equations'),
        ('wrong_equation','Wrong selected-root equations'),
        ('wrong_center_dimension','Selected-root center dimension must be three'),
        ('wrong_box_dimension','Selected-root box must have three intervals'),
        ('wrong_preconditioner_dimension','Selected-root preconditioner must be 3 by 3'),
        ('reversed_q_interval','Positive q enclosure required'),
        ('nonphysical_overlap_box','Selected-root overlaps must lie inside the physical cube'),
    ]
    for mutation,reason in selected:
        cases.append({'name':'S040_'+mutation,'entry':40,'mutation':mutation,
                      'expected_rejection':reason})
    return cases


def mutate(upper,entry,kind):
    path=upper/f'S{entry}_full_certificate.json'
    certificate=json.loads(path.read_text())
    root_path=upper/'S40_selected_root.json'
    selected=json.loads(root_path.read_text()) if entry==40 else None
    delta=Fraction(1,10**20)
    if kind=='empty_cover_arrays':
        certificate['outer_boxes']=[];certificate['elementary_coefficients']=[]
    elif kind=='missing_outer_slab':certificate['outer_boxes'].pop()
    elif kind=='duplicate_outer_slab':certificate['outer_boxes'][-1]=copy.deepcopy(certificate['outer_boxes'][-2])
    elif kind=='empty_spectral_array':certificate['elementary_coefficients']=[]
    elif kind=='repeated_spectral_index':certificate['elementary_coefficients']=[copy.deepcopy(certificate['elementary_coefficients'][0]) for _ in range(7)]
    elif kind in ('duplicate_outer_leaf','duplicate_spectral_leaf','empty_outer_leaves','empty_spectral_leaves'):
        key='outer_boxes' if 'outer' in kind else 'elementary_coefficients'
        leaves=certificate[key][0]['leaves']
        if kind.startswith('duplicate'):leaves.append(copy.deepcopy(leaves[0]))
        else:certificate[key][0]['leaves']=[]
    elif kind=='four_copies_of_e1':
        e1=next(r for r in certificate['certificates'] if r['name']=='e1')
        certificate['certificates']=[copy.deepcopy(e1) for _ in range(4)]
    elif kind in ('q_interval_minus_1e20','q_interval_plus_1e20'):
        shift=-delta if 'minus' in kind else delta
        certificate['q_interval']=[str(Fraction(v)+shift) for v in certificate['q_interval']]
    elif kind=='unbound_q_box':
        selected['box'][0]=[str(Fraction(v)+delta) for v in selected['box'][0]]
        certificate['q_interval']=selected['box'][0][:]
    elif kind=='unbound_overlap_box':selected['box'][1]=[str(Fraction(v)+delta) for v in selected['box'][1]]
    elif kind=='unbound_center':selected['centers'][0]=str(Fraction(selected['centers'][0])+delta)
    elif kind=='zero_radius':selected['radius']='0'
    elif kind=='negative_radius':selected['radius']=str(-Fraction(selected['radius']))
    elif kind=='wrong_variable_order':selected['variables']=['q','y','x']
    elif kind=='missing_equation':selected['equations'].pop()
    elif kind=='extra_equation':selected['equations'].append('0')
    elif kind=='wrong_equation':selected['equations'][0]='1'
    elif kind=='wrong_center_dimension':selected['centers'].pop()
    elif kind=='wrong_box_dimension':selected['box'].pop()
    elif kind=='wrong_preconditioner_dimension':selected['preconditioner'][0].pop()
    elif kind=='reversed_q_interval':certificate['q_interval'].reverse()
    elif kind=='nonphysical_overlap_box':
        radius=Fraction(selected['radius']);selected['centers'][1]='2'
        selected['box'][1]=[str(2-radius),str(2+radius)]
    else:raise ValueError('Unknown mutation: '+kind)
    path.write_text(json.dumps(certificate,indent=2)+'\n')
    if selected is not None:root_path.write_text(json.dumps(selected,indent=2)+'\n')


def file_digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(package):
    paths=[package/'prooflib/radical.py']
    for entry in (19,22,23,24,39,40):
        directory=package/f'entries/S{entry:03d}'
        paths.append(directory/'functional.json')
        paths.extend(p for p in (directory/'upper_bound').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    return {str(p.relative_to(package)):file_digest(p) for p in paths}


def run_case(case,package,temporary,output,timeout):
    started=time.monotonic();entry=case['entry'];name=case['name']
    entry_dir=temporary/name/f'S{entry:03d}'
    source=package/f'entries/S{entry:03d}'
    upper=entry_dir/'upper_bound'
    shutil.copytree(source/'upper_bound',upper,ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy2(source/'functional.json',entry_dir/'functional.json')
    if case.get('mutation'):mutate(upper,entry,case['mutation'])
    if entry==23:
        commands=[(package/'prooflib/radical.py',[str(upper)])]
    else:
        commands=[(upper/f'verify_{entry}_independent.py',[])]
        if entry==40 and not case.get('mutation'):
            commands.append((upper/'verify_40_single_field.py',[]))
    results=[]
    for index,(script,arguments) in enumerate(commands,1):
        argv=[sys.executable,'-B','-S','-c',BOOTSTRAP,str(package),str(script),*arguments]
        t=time.monotonic()
        completed=subprocess.run(argv,cwd=upper,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
        log_name=f'{name}_{index}_{script.stem}.log'
        (output/log_name).write_text(completed.stdout)
        result={'command_name':script.name,'argv':argv,'returncode':completed.returncode,
                'seconds':time.monotonic()-t,'log':log_name}
        if case.get('mutation'):
            result['expected_rejection']=case['expected_rejection']
            result['reason_found']=case['expected_rejection'] in completed.stdout
        results.append(result)
        if completed.returncode:break
    if case.get('mutation'):
        passed=bool(results) and results[-1]['returncode']!=0 and results[-1]['reason_found']
        status='REJECTED_FOR_EXPECTED_REASON' if passed else 'FAILED_NEGATIVE_CONTROL'
    else:
        passed=len(results)==len(commands) and all(r['returncode']==0 for r in results)
        status='ACCEPTED_UNCHANGED_CERTIFICATE' if passed else 'FAILED_POSITIVE_CONTROL'
    if passed and not case.get('mutation'):
        initial_names={p.name for p in (source/'upper_bound').glob('*.json')}
        for p in upper.glob('*.json'):
            if p.name not in initial_names:shutil.copy2(p,output/f'{name}_{p.name}')
    return {**case,'status':status,'passed':passed,'commands':results,'seconds':time.monotonic()-started}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package',type=Path,default=ROOT)
    parser.add_argument('--output-dir',type=Path,required=True,help='New directory outside the package for all logs and the summary.')
    parser.add_argument('--jobs',type=int,default=2)
    parser.add_argument('--timeout',type=float,default=1800)
    args=parser.parse_args()
    if not __debug__:raise RuntimeError('Run obligation controls without -O or -OO')
    package=args.package.resolve();output=args.output_dir.resolve()
    if output.exists() or output.is_relative_to(package):raise ValueError('Use a new output directory outside the package')
    if args.jobs<1 or args.timeout<=0:raise ValueError('Positive jobs and timeout required')
    if not (package/'third_party/vendor/sympy').is_dir():raise ValueError('Expected the offline package with bundled SymPy')
    output.mkdir(parents=True)
    before=snapshot(package);started=time.monotonic();records=[]
    phases=[negative_cases(),[{'name':f'S{entry:03d}_unchanged_positive','entry':entry} for entry in (19,22,23,24,39,40)]]
    with tempfile.TemporaryDirectory(prefix='sliwa-obligation-controls-') as directory:
        temporary=Path(directory)
        for phase in phases:
            with ThreadPoolExecutor(max_workers=args.jobs) as pool:
                futures={pool.submit(run_case,c,package,temporary,output,args.timeout):c for c in phase}
                for future in as_completed(futures):
                    case=futures[future]
                    try:record=future.result()
                    except Exception as error:
                        record={**case,'status':'CONTROL_EXECUTION_ERROR','passed':False,'error':repr(error)}
                    records.append(record)
                    print(record['name'],record['status'],flush=True)
            if any(not r['passed'] for r in records):break
    after=snapshot(package);unchanged=before==after
    negatives=[r for r in records if r.get('mutation')]
    positives=[r for r in records if not r.get('mutation')]
    expected_negative_count=len(phases[0])
    success=unchanged and len(negatives)==expected_negative_count and len(positives)==6 and all(r['passed'] for r in records)
    report={
        'status':'PASS_OBLIGATION_AND_S40_BINDING_CONTROLS' if success else 'FAIL_OBLIGATION_CONTROLS',
        'scope':'Actual entry verifier subprocesses on isolated copies: obligation completeness, duplicate/nonempty leaves, S23 exact name set, and S40 root/interval binding. Six unchanged upper positive controls; no full 46 replay.',
        'negative_control_count':len(negatives),'expected_negative_control_count':expected_negative_count,
        'negative_rejected_for_expected_reason':sum(r['passed'] for r in negatives),
        'positive_control_count':len(positives),'positive_accepted':sum(r['passed'] for r in positives),
        'positive_upper_command_count':sum(len(r.get('commands',[])) for r in positives),
        'note':'S40 shifted-interval negatives must fail in verify_40_independent.py. The separate single-field identifier is not claimed to read the global coefficient interval.',
        'valid_root_leaf_path':'The empty string is a legal root leaf; nonempty checks apply to the leaf list.',
        'package_inputs_unchanged':unchanged,'input_sha256':before,
        'jobs':args.jobs,'seconds':time.monotonic()-started,'records':sorted(records,key=lambda r:r['name']),
    }
    (output/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','negative_control_count','negative_rejected_for_expected_reason','positive_control_count','positive_accepted','positive_upper_command_count','package_inputs_unchanged','seconds']},indent=2),flush=True)
    if not success:raise SystemExit(1)


if __name__=='__main__':main()
