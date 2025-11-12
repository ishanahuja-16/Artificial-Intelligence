class Predicate:
    def __init__(self, name, args):
        self.name = name
        self.args = args  # list of constants or variables

    def __repr__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"

    def __eq__(self, other):
        return isinstance(other, Predicate) and self.name == other.name and self.args == other.args

    def __hash__(self):
        return hash((self.name, tuple(self.args)))

class Var:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Const:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Const) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

def is_variable(x):
    return isinstance(x, Var)

def unify(x, y, subst={}):
    if subst is None:
        return None
    elif x == y:
        return subst
    elif is_variable(x):
        return unify_var(x, y, subst)
    elif is_variable(y):
        return unify_var(y, x, subst)
    elif isinstance(x, Predicate) and isinstance(y, Predicate):
        if x.name != y.name or len(x.args) != len(y.args):
            return None
        for a, b in zip(x.args, y.args):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    else:
        return None

def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    elif is_variable(x) and x in subst:
        return unify(var, subst[x], subst)
    elif occurs_check(var, x, subst):
        return None
    else:
        subst_copy = subst.copy()
        subst_copy[var] = x
        return subst_copy

def occurs_check(var, x, subst):
    if var == x:
        return True
    elif is_variable(x) and x in subst:
        return occurs_check(var, subst[x], subst)
    elif isinstance(x, Predicate):
        return any(occurs_check(var, arg, subst) for arg in x.args)
    else:
        return False

def substitute(predicate, subst):
    new_args = []
    for arg in predicate.args:
        val = arg
        while is_variable(val) and val in subst:
            val = subst[val]
        new_args.append(val)
    return Predicate(predicate.name, new_args)

class Rule:
    def __init__(self, premises, conclusion):
        self.premises = premises  # list of Predicate
        self.conclusion = conclusion  # Predicate

    def __repr__(self):
        return f"{' ∧ '.join(map(str, self.premises))} => {self.conclusion}"

def forward_chain(kb_facts, kb_rules, query):
    inferred = set(kb_facts)
    print("Initial Facts:")
    for f in inferred:
        print(f"  {f}")
    print("\nStarting inference steps:\n")

    new_inferred = True

    while new_inferred:
        new_inferred = False
        for rule in kb_rules:
            possible_substs = [{}]  # substitutions for premises

            for premise in rule.premises:
                temp_substs = []
                for fact in inferred:
                    for subst in possible_substs:
                        subst_try = unify(premise, fact, subst)
                        if subst_try is not None:
                            temp_substs.append(subst_try)
                possible_substs = temp_substs

            for subst in possible_substs:
                concluded_fact = substitute(rule.conclusion, subst)
                if concluded_fact not in inferred:
                    print(f"Inferred: {concluded_fact} from rule {rule} using substitution {subst}")
                    inferred.add(concluded_fact)
                    new_inferred = True
                    if unify(concluded_fact, query) is not None:
                        print(f"\nQuery {query} proved!")
                        return True

    print(f"\nQuery {query} not proved.")
    return False

if __name__ == "__main__":
    a = Const('a')
    b = Const('b')
    c = Const('c')
    x = Var('x')
    y = Var('y')
    z = Var('z')

    kb_facts = {
        Predicate('Parent', [a, b]),
        Predicate('Parent', [b, c]),
    }

    kb_rules = [
        Rule([Predicate('Parent', [x, y])], Predicate('Ancestor', [x, y])),
        Rule([Predicate('Parent', [x, y]), Predicate('Ancestor', [y, z])], Predicate('Ancestor', [x, z])),
    ]

    query = Predicate('Ancestor', [a, c])

    print("Running forward chaining...\n")
    forward_chain(kb_facts, kb_rules, query)