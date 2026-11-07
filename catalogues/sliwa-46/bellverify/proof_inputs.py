"""Bind exported selectors to the actual embedded upper-proof input files."""
from __future__ import annotations
import hashlib,json
from fractions import Fraction
from pathlib import Path
from .replay_contract import check_entry

def load(path):return json.loads(path.read_text(encoding='utf-8'))

def canonical(value):
    if isinstance(value,str):return value.replace(' ','').replace('^','**')
    if isinstance(value,list):return [canonical(v)for v in value]
    if isinstance(value,dict):return {k:canonical(v)for k,v in value.items()}
    return value

def check(directory,expected_id=None):
    directory=Path(directory);config=check_entry(directory,expected_id)
    i=config['id'];group=config['engine']
    p=directory/'upper_bound'
    if group=='analytic':
        row=next(r for r in load(p/'certificate.json')['rows']if r['id']==i)
        expected=dict(kind='radicals',q=row['quantum_value'],overlaps=row['overlaps'])
    elif group=='radical':
        c=load(p/f'S{i}_full_certificate.json')
        expected=dict(kind='radicals',q=c['q_exact'],overlaps=c['cosines'])
    elif i==16:
        # verify_16_algebra.py independently proves the square-root formula;
        # certificate_16_field_bernstein.json binds its square to the same r.
        expected=dict(kind='radicals',q='4*sqrt(1149+156*sqrt(13))/27',
                      overlaps=['(1-sqrt(13))/6','(5-2*sqrt(13))/9','(5-2*sqrt(13))/9'])
        if load(p/'certificate_16_field_bernstein.json')['r']!='(6128+832sqrt(13))/243':
            raise RuntimeError('S16 upper-field definition changed')
    elif i in(19,22,39):
        c=load(p/f'S{i}_full_certificate.json')
        expected=dict(kind='univariate',polynomial=c['q_polynomial'],interval=c['q_interval'],
                      overlaps=c['critical_point']if i==19 else[c['overlap']]*3)
    elif i==21:
        c=load(p/'S21_global_certificate.json')
        local=c['local_convexity_box']
        if len(local)!=3 or tuple(map(Fraction,local[0]))!=tuple(map(Fraction,local[1])):
            raise RuntimeError('S21 symmetric slab construction requires equal first two contact intervals')
        expected=dict(kind='univariate',polynomial=c['root_polynomial'],interval=['5','6'],overlaps=c['critical_point'])
        # This broad interval isolates exactly one polynomial root in the
        # symbolic binding. The upper proof's own interval is strictly inside.
        if not(5<Fraction(c['q_interval'][0])<Fraction(c['q_interval'][1])<6):
            raise RuntimeError('S21 upper selector is outside the exported selector')
    elif i in(27,33):
        c=load(p/f'S{i}_exact_algebraic_point.json')
        if not(0<Fraction(c['q_root_isolating_interval'][0])<Fraction(c['q_root_isolating_interval'][1])):
            raise RuntimeError('Signed q-power bounds require a positive ordered root interval')
        overlaps=([c['x_coordinate_rational_polynomial'],c['y_coordinate_rational_polynomial'],c['y_coordinate_rational_polynomial']]
                  if i==27 else[c['common_measurement_cosine_rational_polynomial']]*3)
        expected=dict(kind='univariate',polynomial=c['q_minimal_polynomial'],interval=c['q_root_isolating_interval'],overlaps=overlaps)
    elif i==40:
        c=load(p/'S40_single_field_definition.json')
        if c['root_selector']!='unique real root in (8,9)':raise RuntimeError('S40 upper selector changed')
        root=load(p/'S40_selected_root.json');full=load(p/'S40_full_certificate.json')
        if root['variables']!=['q','x','y'] or len(root['centers'])!=3 or len(root['box'])!=3:
            raise RuntimeError('S40 selected root must have exactly q,x,y coordinates')
        centers=list(map(Fraction,root['centers']));radius=Fraction(root['radius'])
        box=[tuple(map(Fraction,b))for b in root['box']]
        if radius<=0 or any(b!=(a-radius,a+radius)for a,b in zip(centers,box)):
            raise RuntimeError('S40 stored root box differs from its center and radius')
        if tuple(map(Fraction,full['q_interval']))!=box[0]:
            raise RuntimeError('S40 global q interval differs from selected-root q box')
        if not(8<box[0][0]<box[0][1]<9)or Fraction(c['z'])!=0:
            raise RuntimeError('S40 root box or z coordinate differs from the single-field selector')
        # verify_40_single_field.py proves that this same univariate root and
        # x(q),y(q),z=0 lie inside the now-bound original contact-root box.
        expected=dict(kind='univariate',polynomial=c['q_polynomial'],interval=['8','9'],overlaps=[c[k]for k in['x','y','z']])
    elif i==46:
        c=load(p/'certificate_46_reduced.json')
        full=load(p/'certificate_46_full_bernstein.json')
        if tuple(map(Fraction,c['isolating_interval']))!=tuple(map(Fraction,full['q_interval'])):
            raise RuntimeError('S46 reduced and full upper targets have different q intervals')
        expected=dict(kind='univariate',polynomial=c['polynomial'],interval=c['isolating_interval'],overlaps=[c['attaining_t'],c['attaining_t'],'1'])
    elif i==28:
        c=load(p/'S28_selected_root_certificate.json')
        expected=dict(kind='system',variables=c['variables'],equations=c['equations'],box=c['root_box'],overlaps=['x','y','y'])
    else:
        c=load(p/f'S{i}_selected_root.json')
        expected=dict(kind='system',variables=c['variables'],equations=c['equations'],box=c['box'],overlaps=['x','y','z'])
    spec=load(directory/'strategy_spec.json')
    if canonical(spec)!=canonical(expected):
        raise RuntimeError(f'S{i}: exported exact-value/measurement definitions differ from the embedded upper-proof inputs')
    target={'id':i,'literal':load(directory/'functional.json')['expression'],
            'parameters':canonical(spec),
            'characteristic_sha256':hashlib.sha256((p/config['characteristic_file']).read_bytes()).hexdigest()}
    target_hash=hashlib.sha256(json.dumps(target,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
    return {'id':i,'group':group,'status':'PASS_UPPER_ATTAINMENT_INPUT_BINDING',
            'target_sha256':target_hash}
