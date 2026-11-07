"""Constructive real three-qubit strategies with exact scalar-arithmetic DAGs."""
from __future__ import annotations
import csv,json,re
from fractions import Fraction as F
from pathlib import Path
import sympy as S
import mpmath as mp
from .exact import characteristic_path,V,q,x,y,z,expression,load,verify_binding,require,interval,add,mul,sqrt_interval,power

u,v,w=S.symbols('u v w')
NAMES='AaBbCc'

def terms(literal):
    out=[]
    for term in re.findall(r'[+-]?[^+-]+',literal.replace(' ','')):
        m=re.fullmatch(r'([+-]?)(\d*)([AaBbCc]+)',term)
        require(m is not None,f'Invalid Bell monomial: {term}')
        sign,num,word=m.groups();coefficient=(-1 if sign=='-' else 1)*int(num or '1')
        require(len({a.upper()for a in word})==len(word),'Same-party product in correlator')
        out.append((coefficient,word))
    return out

def symbolic_observables():
    Z=S.diag(1,-1)
    return dict(zip(NAMES,[Z,S.Matrix([[x,u],[u,-x]]),Z,S.Matrix([[y,v],[v,-y]]),Z,S.Matrix([[z,w],[w,-z]])]))

def symbolic_bell(literal):
    obs=symbolic_observables();I=S.eye(2);M=S.zeros(8)
    for coefficient,word in terms(literal):
        local=[I,I,I]
        for name in word:local['ABC'.index(name.upper())]=obs[name]
        M+=coefficient*S.kronecker_product(*local)
    return M.applyfunc(S.expand)

def to_mp(a):
    a=S.sympify(a)
    if a.is_Rational:return mp.mpf(int(a.p))/int(a.q)
    return mp.mpf(str(S.N(a,mp.mp.dps+10)))

def numeric_parameters(spec):
    if spec['kind']=='radicals':
        return [to_mp(expression(spec['q'])),*[to_mp(expression(a))for a in spec['overlaps']]]
    if spec['kind']=='univariate':
        P=S.Poly(expression(spec['polynomial']),q)
        coefficients=[to_mp(a)for a in P.all_coeffs()]
        a,b=[to_mp(expression(t))for t in spec['interval']]
        def f(t):return mp.polyval(coefficients,t)
        qa=mp.findroot(f,(a,b),solver='secant',tol=mp.mpf(10)**(-mp.mp.dps+15),maxsteps=100)
        require(a<=qa<=b,'Numerical refinement escaped exact q selector')
        overlaps=[S.lambdify(q,expression(s),'mpmath')(qa)for s in spec['overlaps']]
        return [qa,*overlaps]
    variables=[S.Symbol(a)for a in spec['variables']]
    equations=list(map(expression,spec['equations']))
    centers=[(to_mp(expression(a))+to_mp(expression(b)))/2 for a,b in spec['box']]
    fun=S.lambdify(variables,equations,'mpmath')
    sol=list(mp.findroot(fun,centers,tol=mp.mpf(10)**(-mp.mp.dps+15),maxsteps=50))
    for a,(lo,hi)in zip(sol,spec['box']):require(to_mp(expression(lo))<=a<=to_mp(expression(hi)),'Root refinement escaped certified box')
    env=dict(zip(variables,sol))
    overlaps=[S.lambdify(variables,expression(s),'mpmath')(*sol)for s in spec['overlaps']]
    return [env[q],*overlaps]

def published_eigen_residual(numerical):
    """Evaluate the eigen-equation using the published rounded coordinates."""
    state=list(map(mp.mpf,numerical['state_vector_real']))
    observables={name:[[mp.mpf(a)for a in row]for row in matrix]
                 for name,matrix in numerical['observables_real'].items()}
    identity=[[mp.mpf(1),mp.mpf(0)],[mp.mpf(0),mp.mpf(1)]]
    matrix=mp.zeros(8)
    for coefficient,word in terms(numerical['literal_expression']):
        local=[identity,identity,identity]
        for name in word:local['ABC'.index(name.upper())]=observables[name]
        for i in range(8):
            for j in range(8):
                value=mp.mpf(coefficient)
                for axis in range(3):
                    value*=local[axis][(i>>(2-axis))&1][(j>>(2-axis))&1]
                matrix[i,j]+=value
    target=mp.mpf(numerical['q_display'])
    return max(abs(sum(matrix[i,j]*state[j]for j in range(8))-target*state[i])for i in range(8))

class Dag:
    def __init__(self):self.nodes=[];self.cache={}
    def node(self,op,*args):
        key=(op,*args)
        if key not in self.cache:
            self.cache[key]=len(self.nodes);self.nodes.append({'op':op,'args':list(args)})
        return self.cache[key]
    def const(self,a):return self.node('rational',str(a))
    def expr(self,e):
        if e.is_Rational:return self.const(e)
        if e.is_Symbol:return self.node('parameter',str(e))
        if e.is_Add:return self.node('add',*[self.expr(a)for a in e.args])
        if e.is_Mul:return self.node('multiply',*[self.expr(a)for a in e.args])
        if e.is_Pow:
            base,exponent=e.args
            require(exponent.is_Integer,'DAG polynomial exponent must be integer')
            return self.node('integer_power',self.expr(base),int(exponent))
        raise ValueError(str(e))
    def evaluate_interval(self,env):
        values=[]
        for node in self.nodes:
            op=node['op'];args=node['args']
            if op=='rational':a=F(args[0]);value=(a,a)
            elif op=='parameter':value=env[S.Symbol(args[0])]
            elif op=='integer_power':value=power(values[args[0]],args[1])
            elif op=='sqrt':value=sqrt_interval(values[args[0]])
            else:
                value=(F(0),F(0))if op=='add'else(F(1),F(1))
                for i in args:value=(add if op=='add'else mul)(value,values[i])
            values.append(value)
        return values

def construct(directory,digits=80):
    directory=Path(directory);mp.mp.dps=max(120,digits+45)
    functional=load(directory/'functional.json');spec=load(directory/'strategy_spec.json')
    binding=verify_binding(directory)
    parameters=numeric_parameters(spec)
    require(all(abs(a)<=1 for a in parameters[1:]),'Illegal numerical overlaps')
    values=[*parameters,*[mp.sqrt(max(mp.mpf(0),1-a*a))for a in parameters[1:]]]
    symbols=[*V,u,v,w];env=dict(zip(symbols,values))
    M=symbolic_bell(functional['expression'])
    MM=mp.matrix(S.lambdify(symbols,M,'mpmath')(*values))
    rcoeff=list(map(expression,binding['complementary_factor_coefficients_descending']))
    rc=[S.lambdify(V,a,'mpmath')(*parameters)for a in rcoeff]
    NN=rc[0]*mp.eye(8)
    for a in rc[1:]:NN=MM*NN+a*mp.eye(8)
    j=max(range(8),key=lambda k:sum(NN[i,k]**2 for i in range(8)))
    raw=NN[:,j];norm=mp.sqrt(sum(a*a for a in raw));psi=raw/norm
    # The exact DAG uses a deterministic positive scale without a phase choice;
    # changing the global sign of the numerical vector has no physical effect.
    dag=Dag();matrix_nodes=[[dag.expr(M[i,k])for k in range(8)]for i in range(8)]
    coefficients=[dag.expr(a)for a in rcoeff]
    zero=dag.const(0);vector=[coefficients[0]if i==j else zero for i in range(8)]
    for c in coefficients[1:]:
        nxt=[]
        for i in range(8):
            summands=[dag.node('multiply',matrix_nodes[i][k],vector[k])for k in range(8)]
            if i==j:summands.append(c)
            nxt.append(dag.node('add',*summands))
        vector=nxt
    norm_squared=dag.node('add',*[dag.node('integer_power',a,2)for a in vector])
    norm_node=dag.node('sqrt',norm_squared)
    normalized=[dag.node('multiply',a,dag.node('integer_power',norm_node,-1))for a in vector]
    intervals={S.Symbol(a):tuple(map(F,b))for a,b in binding['parameter_intervals'].items()}
    for a,b in zip((u,v,w),(x,y,z)):
        squared=power(intervals[b],2)
        intervals[a]=sqrt_interval(add((F(1),F(1)),(-squared[1],-squared[0])))
    ivs=dag.evaluate_interval(intervals)
    require(ivs[norm_squared][0]>0,'Exact state column is not certified nonzero')
    residual=max(abs(a)for a in MM*psi-parameters[0]*psi)
    require(residual<mp.mpf(10)**(-digits+15),f'Constructive eigenvector residual too large: {residual}')
    eig=mp.eigsy(MM,eigvals_only=True)
    require(abs(eig[7]-parameters[0])<mp.mpf(10)**(-digits+15),'Target is not the numerical top eigenvalue')
    obs=symbolic_observables()
    def fmt(a):return mp.nstr(a,digits,strip_zeros=False)
    numerical={
        'schema':'sliwa-real-strategy-v1','id':functional['id'],'basis_order':['000','001','010','011','100','101','110','111'],
        'precision_decimal_digits':digits,'literal_expression':functional['expression'],
        'q_display':fmt(parameters[0]),'local_dimensions':[2,2,2],
        'state_vector_real':[fmt(a)for a in psi],
        'observables_real':{name:[[fmt(S.lambdify(symbols,O[a,b],'mpmath')(*values))for b in range(2)]for a in range(2)]for name,O in obs.items()},
        'overlaps_display':[fmt(a)for a in parameters[1:]],
        'construction':'Normalized nonzero column of R(M), not a numerical optimizer output',
        'exact_certificate':'strategy_exact.json',
        'warning':'Finite decimal coordinates are approximations. Exact optimality is established by the algebraic recipe and upper-bound certificate, not by this decimal residual.'}
    numerical['floating_point_eigen_residual_display']=fmt(published_eigen_residual(numerical))
    numerical['residual_evaluation']={
        'quantity':'Infinity norm of M*psi-q*psi',
        'inputs':'Published finite-decimal state_vector_real, observables_real and q_display',
        'working_decimal_digits':mp.mp.dps}
    exact={
        'schema':'sliwa-exact-arithmetic-dag-v1','id':functional['id'],
        'parameters':spec,'additional_parameters':{'u':'nonnegative sqrt(1-x^2)','v':'nonnegative sqrt(1-y^2)','w':'nonnegative sqrt(1-z^2)'},
        'observables':{name:[[str(a)for a in O.row(k)]for k in range(2)]for name,O in obs.items()},
        'bell_matrix':[[str(M[i,k])for k in range(8)]for i in range(8)],
        'characteristic_polynomial':characteristic_path(directory).read_text().strip(),
        'binding':{k:v for k,v in binding.items() if k!='status'},'column_index_zero_based':j,'nodes':dag.nodes,
        'unnormalized_vector_nodes':vector,'normalization_squared_node':norm_squared,'state_vector_nodes':normalized,
        'normalization_squared_rational_interval':[str(a)for a in ivs[norm_squared]],
        'proof':'P(t)=(t-q)^m R(t); for a Hermitian M with characteristic polynomial P, (M-qI)R(M)=0 by the spectral theorem. The positive lower bound on the chosen column norm proves a nonzero state. Each listed node is a finite exact scalar arithmetic operation; the eight state_vector_nodes are explicit exact state coordinates.'}
    return numerical,exact

def export(directory,destination,digits=80):
    numerical,exact=construct(directory,digits)
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    for name,data in [('strategy_numeric.json',numerical),('strategy_exact.json',exact)]:
        (destination/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    with (destination/'state_vector.csv').open('w',encoding='utf-8',newline='')as handle:
        writer=csv.writer(handle,lineterminator='\n');writer.writerow(['basis','real_amplitude','imaginary_amplitude'])
        writer.writerows(zip(numerical['basis_order'],numerical['state_vector_real'],['0']*8))
    with (destination/'measurements.csv').open('w',encoding='utf-8',newline='')as handle:
        writer=csv.writer(handle,lineterminator='\n');writer.writerow(['observable','row_zero_based','column_zero_based','real_value','imaginary_value'])
        for name,O in numerical['observables_real'].items():
            for i in range(2):
                for j in range(2):writer.writerow([name,i,j,O[i][j],'0'])
    return {'id':numerical['id'],'status':'PASS_CONSTRUCTIVE_STRATEGY_EXPORT','digits':digits,
            'exact_dag_nodes':len(exact['nodes']),'normalization_positive':True}
