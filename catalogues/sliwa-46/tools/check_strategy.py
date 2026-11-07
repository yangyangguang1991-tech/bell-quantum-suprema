"""Independent Decimal-only score audit.  Does not import the exporter or SymPy."""
from __future__ import annotations
import argparse,json,re
from decimal import Decimal as D,localcontext
from pathlib import Path

def require(ok,message):
    if not ok:raise ArithmeticError(message)

def multiply(A,B):
    return [[sum((a*b for a,b in zip(row,col)),D(0))for col in zip(*B)]for row in A]

def tensor(A,B):
    return [[a*b for a in row for b in brow]for row in A for brow in B]

def check(path):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    digits=data['precision_decimal_digits']
    require(digits>=40,'Strategy export needs at least 40 decimal digits')
    with localcontext()as context:
        context.prec=digits+20
        tolerance=D(10)**(-digits+12)
        psi=list(map(D,data['state_vector_real']))
        require(len(psi)==8,'State must have eight amplitudes')
        observables={name:[[D(a)for a in row]for row in O]for name,O in data['observables_real'].items()}
        require(set(observables)==set('AaBbCc'),'Six observables required')
        I=[[D(1),D(0)],[D(0),D(1)]]
        largest_reflection_error=D(0)
        for name,O in observables.items():
            require(len(O)==2 and all(len(row)==2 for row in O),'Each observable must be 2x2')
            require(abs(O[0][1]-O[1][0])<tolerance,f'{name} is not Hermitian')
            square=multiply(O,O)
            largest_reflection_error=max(largest_reflection_error,*[abs(square[i][j]-I[i][j])for i in range(2)for j in range(2)])
        require(largest_reflection_error<tolerance,'Observable is not a reflection')
        norm=sum((a*a for a in psi),D(0));require(abs(norm-1)<tolerance,'State normalization failed')
        score=D(0);M=[[D(0)for _ in range(8)]for _ in range(8)];correlators=[]
        for token in re.findall(r'[+-]?[^+-]+',data['literal_expression'].replace(' ','')):
            match=re.fullmatch(r'([+-]?)(\d*)([AaBbCc]+)',token)
            require(match is not None,'Invalid correlator token')
            sign,integer,word=match.groups();coefficient=D((-1 if sign=='-'else 1)*int(integer or '1'))
            require(len({a.upper()for a in word})==len(word),'Duplicate party in monomial')
            local=[I,I,I]
            for name in word:local['ABC'.index(name.upper())]=observables[name]
            op=tensor(tensor(local[0],local[1]),local[2])
            expectation=sum((psi[i]*op[i][j]*psi[j]for i in range(8)for j in range(8)),D(0))
            score+=coefficient*expectation
            correlators.append({'word':word,'coefficient':str(coefficient),'expectation':str(expectation)})
            for i in range(8):
                for j in range(8):M[i][j]+=coefficient*op[i][j]
        assembled=sum((psi[i]*M[i][j]*psi[j]for i in range(8)for j in range(8)),D(0))
        target=D(data['q_display']);gap=score-target
        residual=max(abs(sum((M[i][j]*psi[j]for j in range(8)),D(0))-target*psi[i])for i in range(8))
        require(abs(score-assembled)<tolerance,'Termwise and assembled scores differ')
        require(abs(gap)<tolerance,'Score differs from target display')
        require(residual<tolerance,'Eigenvector residual is too large')
        return {'status':'PASS_INDEPENDENT_DECIMAL_STRATEGY','id':data['id'],
                'score':str(score),'q_display':str(target),'score_minus_target':str(gap),
                'normalization_error':str(abs(norm-1)),'reflection_error':str(largest_reflection_error),
                'eigen_residual':str(residual),'tolerance':str(tolerance),'correlators':correlators,
                'scope':'Independent finite-decimal cross-check; not a substitute for the exact upper and attainment certificates.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('strategy');parser.add_argument('--output')
    args=parser.parse_args();result=check(args.strategy)
    text=json.dumps(result,indent=2)
    if args.output:Path(args.output).write_text(text+'\n',encoding='utf-8',newline='\n')
    print(text)

if __name__=='__main__':main()
