"""Build or check the manuscript tables directly from the certificate inputs."""
from __future__ import annotations
from pathlib import Path
from decimal import Decimal, localcontext
from fractions import Fraction
import argparse, collections, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'third_party/vendor'))
sys.dont_write_bytecode=True
import sympy as S

def load(path):return json.loads(path.read_text(encoding='utf-8'))
def exact_decimal(value,places):
    q=Fraction(value)
    with localcontext()as ctx:
        ctx.prec=max(100,places+30)
        out=f'{Decimal(q.numerator)/Decimal(q.denominator):.{places}f}'
    if Fraction(out)!=q:raise ArithmeticError('A selecting endpoint was rounded')
    return out

def bell_terms(expression):
    out=[]
    for term in re.findall(r'[+-]?[^+-]+',expression.replace(' ','')):
        match=re.fullmatch(r'([+-]?)(\d*)([AaBbCc]+)',term)
        if match is None:raise ValueError('Unexpected Bell monomial')
        sign,coefficient,word=match.groups()
        out.append(('-'if sign=='-'else '+')+(coefficient or '')+word)
    out[0]=out[0].lstrip('+')
    return out

def render():
    catalogue=load(ROOT/'catalogue.json')
    history={r['id']:r for r in load(ROOT/'data/prior_work_and_contributions.json')['records']}
    selectors={r['id']:r for r in load(ROOT/'data/compact_root_selectors.json')['records']}
    records=[]
    for row in catalogue:
        directory=ROOT/'entries'/f"S{row['id']:03d}"
        spec=load(directory/'strategy_spec.json')
        exact=load(directory/'attainment/strategy_exact.json')
        records.append(dict(row,functional=load(directory/'functional.json'),definition=spec,
            multiplicity=exact['binding']['multiplicity'],
            column=exact['column_index_zero_based'],
            historical_report=history[row['id']]['lopez_rosa_2016']['report_type']))
    output={}
    lines=[r'\begin{longtable}{rrrrrrr}',
       r'\caption{Complete catalogue in the literal normalization of Appendix~\ref{app:functionals}. Decimal displays are rounded; exact definitions appear in Appendices~\ref{app:radicals}--\ref{app:systems}. R, U and S mean rational/radical, univariate and system definitions. A/D records an analytic/decimal value in the 2016 benchmark. $m$ is the eigenvalue multiplicity and $j$ is the zero-based state column in Section~\ref{sec:attainment}.}\label{tab:catalogue}\\',
       r'\toprule $i$ & $L_i$ & $q_i$ (display) & Type & 2016 & $m$ & $j$\\\midrule\endfirsthead',
       r'\toprule $i$ & $L_i$ & $q_i$ (display) & Type & 2016 & $m$ & $j$\\\midrule\endhead',
       r'\bottomrule\endfoot']
    for r in records:
        q=f"{Decimal(r['q_display']):.10f}"
        typ={'radicals':'R','univariate':'U','system':'S'}[r['definition']['kind']]
        old='A'if r['historical_report']=='analytic_expression'else'D'
        lines.append(f"{r['id']} & {r['local_bound']} & {q} & {typ} & {old} & {r['multiplicity']} & {r['column']}"+r'\\')
    lines.append(r'\end{longtable}')
    output['catalogue_table.tex']='\n'.join(lines)
    groups=collections.OrderedDict()
    for r in records:
        if r['definition']['kind']=='radicals':
            expr=S.sympify(r['definition']['q'])
            key=next((a for a in groups if S.simplify(a-expr)==0),expr)
            groups.setdefault(key,[]).append(r['id'])
    lines=[r'\begin{longtable}{ll}',
           r'\caption{Rational and radical value definitions.}\label{tab:radicals}\\',
           r'\toprule Indices $i$ & Exact value $q_i$\\\midrule\endfirsthead',
           r'\caption[]{Rational and radical value definitions (continued).}\\',
           r'\toprule Indices $i$ & Exact value $q_i$\\\midrule\endhead']
    for value,ids in groups.items():lines.append(', '.join(map(str,ids))+' & $'+S.latex(value)+'$'+r'\\')
    lines.extend([r'\bottomrule\end{longtable}'])
    output['radical_values.tex']='\n'.join(lines)
    lines=[]
    q=S.Symbol('q')
    for r in records:
        if r['definition']['kind']!='univariate':continue
        p=S.Poly(S.sympify(r['definition']['polynomial']),q)
        terms=[S.latex(c*q**m[0])for m,c in p.terms()]
        chunks=[];chunk=[];length=0
        for term in terms:
            if chunk and (length+len(term)>52 or len(chunk)>=3):
                chunks.append(chunk);chunk=[];length=0
            chunk.append(term);length+=len(term)
        if chunk:chunks.append(chunk)
        lines.append(r'\paragraph{Index '+str(r['id'])+r'.}')
        lines.append(r'\begin{align*}')
        for j,chunk in enumerate(chunks):
            text=' + '.join(chunk).replace('+ -','- ')
            if j==0:line=f"p_{{{r['id']}}}(q)={{}}&{text}"
            else:line='&{}'+(text if text.startswith('-')else'+ '+text)
            if j!=len(chunks)-1:line+=r'\\'
            else:line+='.'
            lines.append(line)
        lo,hi=[exact_decimal(a,6)for a in selectors[r['id']]['interval']]
        lines.append(r'\end{align*}')
        lines.append(r'The selecting interval is $('+lo+','+hi+r')$.')
    output['univariate_values.tex']='\n'.join(lines)
    lines=[r'\begin{table}[htbp]\centering\small',
           r'\caption{Exact rational centres of the system selecting boxes; every coordinate radius is $10^{-11}$. In row 28, the independent coordinates are $q,x,y$ and the attaining $z$ equals $y$.}\label{tab:centres}',r'\begin{tabular}{rrrrr}',
           r'\toprule $i$ & $q$ centre & $x$ centre & $y$ centre & $z$ centre\\\midrule']
    for r in records:
        if r['definition']['kind']!='system':continue
        centers=[exact_decimal(a,12)for a in selectors[r['id']]['centers']]
        if r['id']==28:centers.append(r'$y$')
        lines.append(str(r['id'])+' & '+' & '.join(centers)+r'\\')
    lines.extend([r'\bottomrule\end{tabular}\end{table}'])
    output['system_centres.tex']='\n'.join(lines)
    lines=[]
    for r in records:
        lines.append(r'\paragraph{Index '+str(r['id'])+r' (local bound $'+str(r['local_bound'])+r'$).}')
        ts=bell_terms(r['functional']['expression']);chunks=[ts[j:j+7]for j in range(0,len(ts),7)]
        lines.append(r'\begin{align*}')
        for j,chunk in enumerate(chunks):
            line=(r'\B_{'+str(r['id'])+r'}={}&'if j==0 else '&{}')+' '.join(chunk)
            line+=r'\\'if j<len(chunks)-1 else'.'
            lines.append(line)
        lines.append(r'\end{align*}')
    output['bell_functionals.tex']='\n'.join(lines)
    output['catalogue_data.json']=json.dumps({'schema':'sliwa-manuscript-source-data-v1','records':records},ensure_ascii=False,indent=2)
    return {name:content.rstrip()+'\n'for name,content in output.items()}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args();directory=ROOT/'manuscript'
    for name,text in render().items():
        path=directory/name
        if args.check:
            if not path.is_file()or path.read_text(encoding='utf-8')!=text:
                raise ArithmeticError('Manuscript source mismatch: '+name)
        else:path.write_text(text,encoding='utf-8',newline='\n')
    print('PASS_MANUSCRIPT_TABLE_SOURCE_CONSISTENCY'if args.check else'BUILT_MANUSCRIPT_TABLES')

if __name__=='__main__':main()
