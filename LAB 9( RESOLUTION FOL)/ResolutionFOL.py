

def is_variable(x):
    return x[0].islower() and len(x) == 1

def unify(x, y, subs=None):
    if subs is None:
        subs = {}
    if x == y:
        return subs
    if is_variable(x):
        return unify_var(x, y, subs)
    if is_variable(y):
        return unify_var(y, x, subs)
    if isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for a, b in zip(x, y):
            subs = unify(a, b, subs)
            if subs is None:
                return None
        return subs
    return None

def unify_var(var, x, subs):
    if var in subs:
        return unify(subs[var], x, subs)
    if x in subs:
        return unify(var, subs[x], subs)
    if occurs_check(var, x, subs):
        return None
    subs[var] = x
    return subs

def occurs_check(var, x, subs):
    if var == x:
        return True
    if isinstance(x, list):
        return any(occurs_check(var, xi, subs) for xi in x)
    if x in subs:
        return occurs_check(var, subs[x], subs)
    return False

def negate(literal):
    return literal[1:] if literal.startswith("¬") else "¬" + literal

def parse_predicate(pred):
    name, args = pred.split("(")
    args = args[:-1].split(",")
    args = [a.strip() for a in args]
    return name.strip(), args

def substitute(literal, subs):
    name, args = parse_predicate(literal.replace("¬", ""))
    new_args = [subs.get(a, a) for a in args]
    new_lit = name + "(" + ", ".join(new_args) + ")"
    return "¬" + new_lit if literal.startswith("¬") else new_lit

def unify_predicates(p1, p2):
    p1_clean = p1.replace("¬", "")
    p2_clean = p2.replace("¬", "")
    n1, a1 = parse_predicate(p1_clean)
    n2, a2 = parse_predicate(p2_clean)
    if n1 != n2 or len(a1) != len(a2):
        return None
    return unify(a1, a2)

def resolve(ci, cj):
    for li in ci:
        for lj in cj:
            if lj == negate(li):
                subs = unify_predicates(li, lj)
                if subs is not None:
                    new_clause = set()
                    for l in ci.union(cj):
                        if l != li and l != lj:
                            new_clause.add(substitute(l, subs))
                    return new_clause, (li, lj), subs
    return None, None, None


KB = [
    {"¬food(x)", "likes(John,x)"},        
    {"food(Apple)"},                      
    {"food(vegetables)"},                 
    {"¬eats(y,z)", "killed(y)", "food(z)"}, 
    {"eats(Anil,Peanuts)"},               
    {"alive(Anil)"},                      
    {"¬eats(Anil,w)", "eats(Harry,w)"},   
    {"killed(g)", "alive(g)"},            
    {"¬alive(k)", "¬killed(k)"},          
    {"likes(John,Peanuts)"}               
]

def resolution_tree(KB, query):

    print("         PROOF BY RESOLUTION (FOL)         ")

    print(f"Goal: Prove that {query}\n")
    print("Converting to CNF and negating the query...\n")

    clauses = [c.copy() for c in KB]
    negated_query = negate(query)
    clauses.append({negated_query})

    print(f"Negated query added to KB: {negated_query}\n")

    new = []
    step = 1
    proof_steps = []
    tree_nodes = []

    while True:
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses))
                 for j in range(i + 1, len(clauses))]

        for (ci, cj) in pairs:
            resolvent, used, subs = resolve(ci, cj)
            if resolvent is not None:
                proof_steps.append({
                    "step": step,
                    "parents": (ci, cj),
                    "used": used,
                    "subs": subs,
                    "resolvent": resolvent
                })

                print(f"Step {step}: Resolving {ci} and {cj}")
                print(f"       Used literals: {used}")
                if subs:
                    print(f"       Substitution: {subs}")
                print(f"       ⇒ New Clause: {resolvent}\n")

                tree_nodes.append((ci, cj, resolvent))

                if not resolvent:
                    print(" Empty clause derived — Query is PROVED!\n")
                    print("\n============ PROOF TREE ============\n")
                    print_tree(tree_nodes)
                    return True

                if resolvent not in clauses:
                    new.append(resolvent)
                step += 1

        if not new:
            print(" No new clauses can be derived — Query cannot be proven.\n")
            print("\n============ PROOF TREE (Partial) ============\n")
            print_tree(tree_nodes)

            return False

        clauses.extend(new)
        new = []

def print_tree(nodes):
    def print_branch(node, level=0):
        indent = "   " * level
        c1, c2, result = node
        print(f"{indent}├─ Derived {result} from:")
        print(f"{indent}│    {c1}")
        print(f"{indent}│    {c2}")

    for n in nodes:
        print_branch(n)
        print("")

if __name__ == "__main__":
    query = "likes(John,Peanuts)"
    result = resolution_tree(KB, query)
    print("Result:", " PROVED" if result else " NOT PROVED")