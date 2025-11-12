import itertools
import re

def evaluate(expr, model):


    # Replace biconditional and implication first
    expr = expr.replace("<->", " == ")
    expr = expr.replace("->", " <= ")

    # Replace negation ~ with explicit parentheses (not X)
    expr = re.sub(r'~(\w+)', r'(not \1)', expr)
    expr = re.sub(r'~\(([^)]+)\)', r'(not (\1))', expr)

    # Replace AND and OR
    expr = expr.replace("^", " and ")
    expr = expr.replace("v", " or ")

    # Replace symbols with their boolean values in the model
    for sym, val in model.items():
        expr = re.sub(r'\b' + re.escape(sym) + r'\b', str(val), expr)

    # Evaluate the final Python boolean expression
    return eval(expr)


def tt_entails(kb, query, symbols):
   

    entails = True
    models = list(itertools.product([True, False], repeat=len(symbols)))

    print("Truth Table Evaluation:\n")
    header = " | ".join(symbols) + " | KB | Query | KB ⇒ Query"
    print(header)
    print("-" * len(header) * 2)

    for values in models:
        model = dict(zip(symbols, values))
        kb_val = evaluate(kb, model)
        query_val = evaluate(query, model)
        implication = (not kb_val) or query_val

        if kb_val and not query_val:
            entails = False

        row = " | ".join(['T' if v else 'F' for v in values])
        row += f" | {'T' if kb_val else 'F'}  | {'T' if query_val else 'F'}   | {'T' if implication else 'F'}"
        print(row)

    print("\nResult:")
    if entails:
        print("The Knowledge Base entails the Query (KB ⊨ Query)")
    else:
        print("The Knowledge Base does NOT entail the Query (KB ⊭ Query)")


# Example usage:

kb = "(Q -> P) ^ (P -> ~Q) ^ (Q v R)"
symbols = ["P", "Q", "R"]

queries = ["R", "R -> P", "Q -> R"]

for query in queries:
    print(f"\nEvaluating Query: {query}\n")
    tt_entails(kb, query, symbols)
    print("\n" + "="*50 + "\n")