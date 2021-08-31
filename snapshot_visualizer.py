import json
import graphviz


def main():
    with open('snapshot.json') as snapshot_file:
        snapshot = snapshot_file.read()
        snapshot = json.loads(snapshot)
    nodes = snapshot['values']
    heads = snapshot['heads']
    graph = dict()

    for node in nodes:
        graph.update({
            node['hash']: node
        })

    dot = graphviz.Digraph(comment='Messages')
    for head in heads:
        parse_graph(graph=graph, node=head, dot=dot, color='red')

    print(dot.source)
    dot.render('snapshot_graph_colors.gv', view=True)


def parse_graph(graph, node, dot, **node_kwargs):
    refs = node['refs']  # ignore refs for now. Maybe draw them with different color?
    current_node_name = node['hash']
    dot.node(name=current_node_name, label=node['payload']['value'], **node_kwargs)
    nexts = node['next']
    if not nexts:
        return

    for ref_hash in refs:
        try:
            graph[ref_hash]
        except KeyError:
            print('REF FAILED! No node with hash {} in graph'.format(ref_hash))
        else:
            dot.edge(tail_name=current_node_name, head_name=ref_hash)

    for next_hash in nexts:
        try:
            next_node = graph[next_hash]
        except KeyError:
            print('No node with hash: {} in graph!'.format(next_hash))
            return
        dot.edge(tail_name=current_node_name, head_name=next_hash, color='red')
        parse_graph(graph=graph, node=next_node, dot=dot)


if __name__ == "__main__":
    main()
