#!/usr/bin/env python3
"""Independent literal/benchmark comparison; no author programs or third-party imports.

Reads the manuscript's claimed exact intervals but does not certify their validity;
that mathematical obligation belongs to the other independent upper/state audits.
Primary-source transcriptions are frozen next to this script.
"""
import argparse, ast, hashlib, itertools, json, re
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

def require(ok, msg):
    if not ok:
        raise ArithmeticError(msg)

def squarefree(n):
    require(isinstance(n, int) and n >= 0, 'noninteger or negative radicand')
    if n == 0:
        return 0, 1
    out, factor = 1, 2
    while factor * factor <= n:
        while n % (factor * factor) == 0:
            out *= factor
            n //= factor * factor
        factor += 1
    return out, n

def add(a,b):
    c=dict(a)
    for n,v in b.items(): c[n]=c.get(n,Q(0))+v
    return {n:v for n,v in c.items() if v}

def mul(a,b):
    c={}
    for n,v in a.items():
        for m,w in b.items():
            k,d=squarefree(n*m)
            c[d]=c.get(d,Q(0))+k*v*w
    return {n:v for n,v in c.items() if v}

def algebraic(s):
    def rec(n):
        if isinstance(n,ast.Constant) and type(n.value) is int:
            return {1:Q(n.value)} if n.value else {}
        if isinstance(n,ast.UnaryOp):
            a=rec(n.operand)
            if isinstance(n.op,ast.USub): return {k:-v for k,v in a.items()}
            if isinstance(n.op,ast.UAdd): return a
        if isinstance(n,ast.BinOp):
            a,b=rec(n.left),rec(n.right)
            if isinstance(n.op,ast.Add): return add(a,b)
            if isinstance(n.op,ast.Sub): return add(a,{k:-v for k,v in b.items()})
            if isinstance(n.op,ast.Mult): return mul(a,b)
            if isinstance(n.op,ast.Div):
                require(set(b)=={1} and b[1], 'nonrational or zero denominator')
                return {k:v/b[1] for k,v in a.items()}
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='sqrt' and len(n.args)==1 and not n.keywords:
            a=rec(n.args[0]);require(set(a)=={1} and a[1].denominator==1, 'unsupported nested radical')
            k,d=squarefree(a[1].numerator)
            return {d:Q(k)} if k else {}
        raise ValueError('Unsupported exact expression: '+s)
    return rec(ast.parse(s,mode='eval').body)

def latex_expression(s):
    s=s.replace('\\left','').replace('\\right','')
    s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',s)
    s=re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',s)
    s=re.sub(r'(?<=[0-9])(?=sqrt|\()', '*', s)
    s=re.sub(r'(?<=\))(?=[(0-9]|sqrt)', '*', s)
    return s

def literal(s):
    s=re.sub(r'\s+','',s)
    parts=re.findall(r'([+-]?)(\d*)([Aa]?[Bb]?[Cc]?)',s)
    c={};rebuilt=''
    for sign,digits,word in parts:
        if not (sign or digits or word): continue
        require(word and len({x.lower() for x in word})==len(word), 'bad word')
        rebuilt+=sign+digits+word
        require(word not in c,'duplicate term')
        c[word]=(-1 if sign=='-' else 1)*int(digits or '1')
    require(rebuilt==s, 'unsupported literal syntax')
    return c

def normal_repr(v): return {str(k):str(x) for k,x in sorted(v.items())}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('package',type=Path);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    root=args.package.resolve();out=args.output.resolve();require(not out.is_relative_to(root),'output must be outside original package')
    source_path=Path(__file__).with_name('primary_source_values.json')
    source=json.loads(source_path.read_text())
    hist_path=root/'data/prior_work_and_contributions.json'
    history=json.loads(hist_path.read_text());rows={r['id']:r for r in history['records']}
    require(set(rows)==set(range(1,47)),'history index coverage')
    for key in ['literals','lopez_values','vallins_values']:
        require(set(map(int,source[key]))==set(range(1,47)), 'primary-source index coverage')
    tracked=[hist_path,root/'manuscript/catalogue_table.tex',root/'manuscript/radical_values.tex']
    tracked += [root/'entries'/f'S{i:03d}'/name for i in range(1,47) for name in ['functional.json','strategy_spec.json']]
    before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
    results=[];literal_terms=0
    for i in range(1,47):
        r=rows[i];directory=root/'entries'/f'S{i:03d}'
        fun=json.loads((directory/'functional.json').read_text());spec=json.loads((directory/'strategy_spec.json').read_text())
        orig=literal(fun['expression']);web=source['literals'][str(i)]
        require(orig==literal(web['expression']),f'S{i} literal source mismatch')
        require(fun['local_bound']==web['local_bound']==r['local_bound'],f'S{i} local-bound source mismatch')
        assignments=[dict(zip('AaBbCc',v)) for v in itertools.product([-1,1],repeat=6)]
        scores=[sum(c*product(a[k] for k in word) for word,c in orig.items()) for a in assignments]
        require(max(scores)==fun['local_bound'],f'S{i} deterministic local bound')
        literal_terms+=len(orig)
        prev=source['lopez_values'][str(i)];row={'id':i,'literal_and_local_bound':'PASS','type':spec['kind']}
        interval=list(map(Q,r['certified_value_interval']));lo,hi=interval
        require(lo<=hi, 'reversed claimed exact interval')
        if re.fullmatch(r'\d+\.\d+',prev):
            require(r['lopez_rosa_2016']['report_type']=='decimal_display','history source kind mismatch')
            require(r['lopez_rosa_2016']['value']==prev,'history decimal transcription mismatch')
            v=Q(prev);delta=Q(1,2*10**len(prev.split('.')[1]))
            within=v-delta<lo<=hi<v+delta
            outside=hi<v-delta or lo>v+delta
            require(within or outside,'unresolved rounding-cell relation')
            row['lopez']='agrees_at_printed_precision' if within else 'outside_rounding_cell'
            row['lopez_printed']=prev
            require(row['lopez']==r['lopez_rosa_2016']['comparison'],'history rounding assertion mismatch')
        else:
            require(spec['kind']=='radicals','previous analytic expression no longer radial')
            require(algebraic(latex_expression(prev))==algebraic(spec['q']),f'S{i} 2016 symbolic value mismatch')
            require(algebraic(r['lopez_rosa_2016']['value'])==algebraic(spec['q']),'history analytic transcription mismatch')
            row['lopez']='exact_symbolic_equality'
        prev=source['vallins_values'][str(i)]
        if '.' in prev:
            v=Q(prev);delta=Q(1,2*10**len(prev.split('.')[1]))
            require(v-delta<lo<=hi<v+delta,f'S{i} Vallins rounding cell')
            require(prev==r['vallins_2017_corrected_2018']['value'],'Vallins source transcription mismatch')
            row['vallins']='agrees_at_printed_precision'
        else:
            require(spec['kind']=='radicals' and algebraic(prev)==algebraic(spec['q']),f'S{i} Vallins exact expression')
            row['vallins']='exact_symbolic_equality'
        results.append(row)
    tex=(root/'manuscript/radical_values.tex').read_text()
    radial_rows=re.findall(r'^([0-9, ]+) & (.+)\\\\$',tex,re.M)
    radical_ids=[int(x.strip()) for group,_ in radial_rows for x in group.split(',')]
    require(len(radical_ids)==28 and len(set(radical_ids))==28,'radical table membership')
    require(set(radical_ids)=={r['id']for r in results if r['type']=='radicals'},'radical table types')
    catalogue=(root/'manuscript/catalogue_table.tex').read_text()
    table=re.findall(r'^(\d+) & (\d+) & ([\d.]+) & ([RUS]) & ([AD]) & (\d+) & (\d+)\\\\$',catalogue,re.M)
    require(len(table)==46 and set(int(v[0])for v in table)==set(range(1,47)),'catalogue coverage')
    for sid,local,q,kind,old,m,j in table:
        i=int(sid);r=rows[i]
        require({'R':'radicals','U':'univariate','S':'system'}[kind]==r['archive_value_kind'],'catalogue representation type')
        require((old=='A')==(r['lopez_rosa_2016']['report_type']=='analytic_expression'),'catalogue A/D')
        v=Q(q);delta=Q(1,2*10**len(q.split('.')[1]));lo,hi=map(Q,r['certified_value_interval'])
        require(v-delta<lo<=hi<v+delta,'catalogue display rounding')
        require(int(local)==r['local_bound'],'catalogue local bound')
    # Exact normalization and output relabeling of Werner-Wolf Appendix (A2).
    ww={''.join(word):1 for word in itertools.product('Aa','Bb','Cc')};ww['ABC']-=4
    mapped={w:c*((-1)**sum(k.isupper()for k in w)) for w,c in ww.items()}
    require(mapped==literal(json.loads((root/'entries/S007/functional.json').read_text())['expression']),'WW-to-S7 mapping')
    after={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
    require(before==after,'input changed during audit')
    result={'status':'PASS_FRESH_PRIMARY_BENCHMARK_COMPARISON','scope':'literal coefficients, local integer maxima, source transcriptions, radical equalities, classifications, relative locations of author-claimed exact intervals; no independent proof of those interval enclosures or global upper bounds', 'standard_library_only':True,'author_code_imported':False,'original_inputs_unchanged':True,'source_transcription_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),'frozen_input_hashes':before,'entry_count':46,'literal_integer_terms':literal_terms,'local_assignments_per_entry':64,'representation_counts':dict(Counter(r['type']for r in results)),'lopez_counts':dict(Counter(r['lopez']for r in results)),'lopez_outside_ids':[r['id']for r in results if r['lopez']=='outside_rounding_cell'],'vallins_counts':dict(Counter(r['vallins']for r in results)),'radical_table_group_count':len(radial_rows),'ww_s7_mapping':{'status':'PASS_EXACT_INTEGER_COEFFICIENT_IDENTITY','substitution':{'a1':'-A','a2':'a','b1':'-B','b2':'b','c1':'-C','c2':'c'},'scale':4,'normalized_reported_value':'5/3','raw_value':'20/3'},'results':results}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['results','frozen_input_hashes']},indent=2))

def product(values):
    v=1
    for x in values: v*=x
    return v

if __name__=='__main__': main()
