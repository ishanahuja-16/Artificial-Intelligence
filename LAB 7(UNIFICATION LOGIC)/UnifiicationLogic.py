class Term:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Term) and self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return str(self.value)

class Constant(Term):
    pass

class Variable(Term):
    pass

class Function(Term):
    def __init__(self, predicate_symbol, arguments):
        self.value = predicate_symbol
        self.arguments = list(arguments)

    def __eq__(self, other):
        return (isinstance(other, Function) and
                self.value == other.value and
                self.arguments == other.arguments)

    def __hash__(self):
        return hash((self.value, tuple(self.arguments)))

    def __repr__(self):
        return f"{self.value}({', '.join(map(str, self.arguments))})"

FAILURE = 'FAILURE'

def occurs_in(var, term):
    if var == term:
        return True
    if isinstance(term, Function):
        return any(occurs_in(var, arg) for arg in term.arguments)
    return False

def apply_substitution(substitution, term):
    if substitution is None or not substitution:
        return term

    if isinstance(term, Variable):
        return substitution.get(term, term)

    if isinstance(term, Function):
        new_arguments = [apply_substitution(substitution, arg) for arg in term.arguments]
        return Function(term.value, new_arguments)

    return term

def compose_substitutions(subst_new, subst_current):
    if subst_new is None or not subst_new:
        return subst_current
    if subst_current is None or not subst_current:
        return subst_new

    new_subst = {var: apply_substitution(subst_new, term) for var, term in subst_current.items()}

    for var, term in subst_new.items():
        if var not in subst_current:
            new_subst[var] = term

    return new_subst

def unify(psi1, psi2):
    if isinstance(psi1, (Variable, Constant)) or isinstance(psi2, (Variable, Constant)):

        if psi1 == psi2:
            return None

        if isinstance(psi1, Variable):
            if occurs_in(psi1, psi2):
                return FAILURE
            return {psi1: psi2}

        if isinstance(psi2, Variable):
            if occurs_in(psi2, psi1):
                return FAILURE
            return {psi2: psi1}

        return FAILURE

    if not isinstance(psi1, Function) or not isinstance(psi2, Function):
        return FAILURE

    if psi1.value != psi2.value:
        return FAILURE

    if len(psi1.arguments) != len(psi2.arguments):
        return FAILURE

    subst = {}

    for i in range(len(psi1.arguments)):
        arg1 = psi1.arguments[i]
        arg2 = psi2.arguments[i]

        l1 = apply_substitution(subst, arg1)
        l2 = apply_substitution(subst, arg2)

        S = unify(l1, l2)

        if S == FAILURE:
            return FAILURE

        if S is not None and S:
            subst = compose_substitutions(S, subst)

    return subst

X = Variable('X')
Y = Variable('Y')
Z = Variable('Z')
A = Constant('a')
B = Constant('b')

term_a = Function('P', [X, A])
term_b = Function('P', [B, Y])
term_c = Function('Q', [X, A])
term_d = Function('R', [X, Function('f', [X])])
term_e = Function('R', [Y, Z])

print("Unify Examples:")
print(f"1. Unify({term_a}, {term_b}): {unify(term_a, term_b)}")
print(f"2. Unify({term_a}, {term_c}): {unify(term_a, term_c)}")
print(f"3. Unify({X}, {Function('f', [X])}): {unify(X, Function('f', [X]))}")
print(f"4. Unify({term_d}, {term_e}): {unify(term_d, term_e)}")