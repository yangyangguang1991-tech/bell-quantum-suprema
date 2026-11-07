"""Independent standard-library evaluation of exported exact coordinate DAGs.

The algebraic root proof is separate. This checker audits that the finite
arithmetic graph actually reproduces the supplied coordinate approximation.
"""
from __future__ import annotations
import argparse,json
from decimal import Decimal as D,localcontext
from pathlib import Path

def require(ok,message):
    if not ok:raise ArithmeticError(message)

def rational(text):
    parts=str(text).split('/')
    require(len(parts)in(1,2),'Bad rational literal')
    return D(parts[0])if len(parts)==1 else D(parts[0])/D(parts[1])

def check(exact_path,numeric_path):
    exact=json.loads(Path(exact_path).read_text(encoding='utf-8'))
    numerical=json.loads(Path(numeric_path).read_text(encoding='utf-8'))
    require(exact['id']==numerical['id'],'Exact/numeric identifiers disagree')
    digits=numerical['precision_decimal_digits']
    with localcontext()as context:
        context.prec=digits+50
        parameters={'q':D(numerical['q_display'])}
        parameters.update(zip('xyz',map(D,numerical['overlaps_display'])))
        parameters.update({name:(1-parameters[angle]**2).sqrt()for name,angle in zip('uvw','xyz')})
        values=[]
        for j,node in enumerate(exact['nodes']):
            op=node['op'];args=node['args']
            if op=='rational':value=rational(args[0])
            elif op=='parameter':require(args[0]in parameters,'Unknown parameter');value=parameters[args[0]]
            else:
                references=args[:1]if op in('integer_power','sqrt')else args
                require(all(isinstance(a,int)and 0<=a<j for a in references),'DAG is not strictly forward evaluated')
                if op=='integer_power':require(isinstance(args[1],int),'Noninteger exponent');value=values[args[0]]**args[1]
                elif op=='sqrt':require(values[args[0]]>=0,'Negative square root');value=values[args[0]].sqrt()
                elif op=='add':value=sum((values[a]for a in args),D(0))
                elif op=='multiply':
                    value=D(1)
                    for a in args:value*=values[a]
                else:raise ArithmeticError(f'Unknown DAG operation {op}')
            values.append(value)
        roots=exact['state_vector_nodes'];require(len(roots)==8,'Expected eight state coordinates')
        vector=[values[j]for j in roots]
        target=list(map(D,numerical['state_vector_real']))
        err=max(abs(a-b)for a,b in zip(vector,target))
        require(err<D(10)**(-digits+22),f'Exact DAG and numeric state disagree: {err}')
        norm2=values[exact['normalization_squared_node']]
        lo,hi=map(rational,exact['normalization_squared_rational_interval'])
        slack=D(10)**(-digits+22)*max(D(1),abs(norm2))
        require(0<lo<=hi and lo-slack<=norm2<=hi+slack,'Constructed norm disagrees with the positive rational certificate')
        return {'status':'PASS_INDEPENDENT_EXACT_DAG_COORDINATE_AUDIT','id':exact['id'],
                'nodes':len(values),'maximum_coordinate_error':str(err),
                'positive_normalization_interval':True,
                'scope':'Checks graph structure and coordinate evaluation; exact algebraic binding and global upper certificate are replayed separately.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('exact');p.add_argument('numeric');p.add_argument('--output')
    args=p.parse_args();result=check(args.exact,args.numeric);text=json.dumps(result,indent=2)
    if args.output:Path(args.output).write_text(text+'\n',encoding='utf-8',newline='\n')
    print(text)

if __name__=='__main__':main()
