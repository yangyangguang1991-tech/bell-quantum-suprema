"""Check the scientific tables, bibliography and benchmark comparisons."""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
import collections,json,re,sys

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'third_party/vendor'),str(ROOT)]
sys.dont_write_bytecode=True
import sympy as S
from tools.build_manuscript_tables import render

def require(ok,message):
    if not ok:raise ArithmeticError(message)
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def comparison(interval,display,definition):
    if '/'in display or '*'in display or 'sqrt'in display or '.'not in display:
        require(definition['kind']=='radicals','An exact benchmark needs an exact expression')
        require(S.simplify(S.sympify(display)-S.sympify(definition['q']))==0,'Exact benchmark value differs')
        return 'exact'
    q=Q(display);unit=Q(1,10**len(display.split('.')[1]));lo,hi=map(Q,interval)
    if q-unit/2<=lo<=hi<=q+unit/2:return 'agrees_at_printed_precision'
    require(hi<q-unit/2 or lo>q+unit/2,'Ambiguous benchmark rounding comparison')
    return 'outside_rounding_cell'

def main():
    data=load(ROOT/'data/prior_work_and_contributions.json');records=data['records']
    require([r['id']for r in records]==list(range(1,47)),'Incomplete historical comparison')
    analytic=[];decimals=[];discrepancies=[];kinds=collections.Counter()
    for row in records:
        i=row['id'];entry=ROOT/'entries'/f'S{i:03d}'
        f=load(entry/'functional.json');spec=load(entry/'strategy_spec.json')
        exact=load(entry/'attainment/strategy_exact.json')
        require(row['local_bound']==f['local_bound'],'Local bound comparison mismatch')
        require(row['archive_value_kind']==spec['kind'],'Exact-value type mismatch')
        require(row['attaining_state_column']==exact['column_index_zero_based'],'State column mismatch')
        require(row['eigenvalue_multiplicity']==exact['binding']['multiplicity'],'Eigenvalue multiplicity mismatch')
        # Bind to the exact attainment file's supplied enclosure, not a decimal display.
        interval=exact['binding']['parameter_intervals']['q']
        require(row['certified_value_interval']==interval,'Historical comparison interval is unbound')
        kinds[spec['kind']]+=1
        old=row['lopez_rosa_2016']
        if old['report_type']=='analytic_expression':
            require(comparison(interval,old['value'],spec)=='exact','Reported analytic value differs')
            analytic.append(i)
        else:
            decimals.append(i)
            result=comparison(interval,old['value'],spec)
            require(old['comparison']==result,'2016 decimal classification differs')
            if result=='outside_rounding_cell':discrepancies.append(i)
        later=row['vallins_2017_corrected_2018']
        result=comparison(interval,later['value'],spec)
        require(result in ('exact','agrees_at_printed_precision')and result==later['comparison'],'Corrected later benchmark differs')
        expected=['IoannouRosset2021, Section IX']if i in(3,10,11,14)else[]
        require(row['explicit_class_sos_in_audited_literature']==expected,'Prior SOS attribution differs')
    require(len(analytic)==27 and len(decimals)==19,'Historical report counts differ')
    require(discrepancies==[16,21,22,24,25,27,31,32,33,34,35,36,39,40,41,42],'Decimal discrepancy list differs')
    require(kinds=={'radicals':28,'univariate':8,'system':10},'Exact representation counts differ')
    for name,text in render().items():
        require((ROOT/'manuscript'/name).read_text(encoding='utf-8')==text,'Generated manuscript file differs: '+name)
    bib=(ROOT/'references.bib').read_text(encoding='utf-8')
    require(bib==(ROOT/'manuscript/references.bib').read_text(encoding='utf-8'),'Bibliography copies differ')
    keys=re.findall(r'@\w+\s*\{\s*([^,]+),',bib)
    require(len(keys)==len(set(keys)),'Duplicate bibliography keys')
    cff=(ROOT/'CITATION.cff').read_text(encoding='utf-8')
    for value in('Yang','Guang','0000-0001-9236-7544','yangyangguang1991@gmail.com','1.0.0'):
        require(value in cff,'Incomplete citation identity: '+value)
    doi=re.search(r'^doi:\s*[\"\x27]?([^\s\"\x27]+)',cff,re.M)
    if doi:require(re.fullmatch(r'10\.\d{4,9}/\S+',doi[1])is not None,'Malformed DOI metadata')
    print(json.dumps({'status':'PASS_PUBLICATION_AND_BENCHMARK_CONSISTENCY','entries':46,
        'prior_analytic_expressions_symbolically_equal':len(analytic),'prior_decimal_rows':len(decimals),
        'corrected_later_quantum_column_agreements':46,'older_decimal_rounding_discrepancies':discrepancies,
        'exact_representation_counts':dict(kinds),'bibliography_entries':len(keys)},indent=2))

if __name__=='__main__':main()
