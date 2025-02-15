# Get paths of graphviz programs
import pygraphviz as pgv

A = pgv.AGraph()
progs_list = ['neato', 'dot', 'twopi', 'circo', 'fdp', 'nop', 'wc', 'acyclic', 'gvpr', 'gvcolor',
              'ccomps', 'sccmap', 'tred', 'sfdp', 'unflatten']
for prog in progs_list:
    try:
        runprog = A._get_prog(prog)
        print(f'{runprog}')
    except ValueError as e:
        print(f'{prog} gets this error: {str(e).strip()}')