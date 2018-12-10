from anytree import Node
from nltk.corpus import wordnet as wn


def wordnet_branch(node):
    """Generates branches in the ontology tree with wordnet"""

    synsets = wn.synsets(node.name)

    if synsets:
        synset = synsets[0]

        hyp = lambda s: s.hypernyms()
        tree = synset.tree(rel=hyp, depth=5)
        hyponyms = synset.hyponyms()

        generate_branches(hyponyms, parent=node)

    return node


def generate_branches(hyponyms, parent):
    current_node = parent

    if not isinstance(hyponyms, list):
        name = hyponyms.name().split(".")[0]
        current_node = Node(name, parent=parent)
        return

    for item in hyponyms:
        generate_branches(item, parent=current_node)


subjects = Node("subject")

science = Node("science", parent=subjects)

computing = Node("computing", parent=science)
robotics = wordnet_branch(Node("robotics", parent=computing))
artificial_intelligence = wordnet_branch(
    Node("artificial_intelligence", parent=computing)
)
graphics = wordnet_branch(Node("graphics", parent=computing))
hci = wordnet_branch(Node("hci", parent=computing))

physics = wordnet_branch(Node("physics", parent=science))
chemistry = wordnet_branch(Node("chemistry", parent=science))

art = wordnet_branch(Node("art", parent=subjects))

health_and_safety = wordnet_branch(Node("health_and_safety", parent=science))

# Subject
# |-- Science
# |   |-- Computing
# |   |   |-- Robotics
# |   |   |   |-- (WordNet)
# |   |   |-- Artificial Intelligence
# |   |   |   |-- (WordNet)
# |   |   |-- Graphics
# |   |   |   |-- (WordNet)
# |   |   |-- HCL
# |   |   |   |-- (WordNet)
# |   |-- Physics
# |   |   |-- (WordNet)
# |   |-- Chemistry
# |   |   |-- (WordNet)
# |   +-- Health and Safety
# |   |   |-- (WordNet)
# +-- Art
# |  |-- (WordNet)
