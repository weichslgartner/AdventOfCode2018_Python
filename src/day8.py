class Node():
    def __init__(self, name, n_children, n_metadata):
        self.name = name
        self.n_children = n_children
        self.n_metadata = n_metadata
        self.metadata = []
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def add_medata(self, met):
        self.metadata.extend(met)

    def __repr__(self):
        return str(self.name) + '[' + str(self.children) + ']' + str(self.metadata)

# globals
m_sum = 0
pos = 0
nodes = {}
part2_sum = 0


def create_node(input, node_name):
    global m_sum, pos, nodes
    n_children = input[pos]
    n_metadata = input[pos + 1]
    cur_node = Node(node_name, n_children, n_metadata)
    pos += 2
    for j in range(0, n_children):
        cur_node.add_child(node_name + str(j + 1))
        create_node(input, node_name + str(j + 1))
    m_sum += sum(input_int[pos:pos + n_metadata])
    cur_node.add_medata(input_int[pos:pos + n_metadata])
    pos += n_metadata
    nodes[node_name] = cur_node


def calc_part2(nodes, cur_node_name):
    global part2_sum
    cur_node = nodes[cur_node_name]
    if cur_node.n_children == 0:
        part2_sum += sum(cur_node.metadata)
    else:
        for i in cur_node.metadata:
            if (i - 1) < cur_node.n_children and i > 0:
                next_node = cur_node.children[i - 1]
                calc_part2(nodes, next_node)


def calc_sum_metadata(nodes):
    n_sum = 0
    for node in nodes.values():
        n_sum += sum(node.metadata)
    print(n_sum)


input_raw = open('../input/input_8.txt').read().rstrip().split(' ')
input_int = [int(pos) for pos in input_raw]

create_node(input_int, 'A')
calc_sum_metadata(nodes)
calc_part2(nodes, 'A')
print(part2_sum)
