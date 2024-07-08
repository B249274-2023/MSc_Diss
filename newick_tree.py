from Bio import Phylo
from cStringIO import StringIO

# Corrected Newick tree string
newick_tree = "((((((((((SPRET_EiJ:0.002,(PWK_PhJ:0.001,(CAST_EiJ:0.001,(WSB_EiJ:1e-05,(((NZO_HlLtJ:1e-06,(C57BL_6NJ:1e-06,C57B6J:1e-06)Anc23:1e-06)Anc21:1e-06,((NOD_ShiLtJ:1e-06,FVB_NJ:1e-06)Anc24:1e-06,(((DBA_2J:1e-06,(CBA_J:1e-06,C3H_HeJ:1e-06)Anc29:1e-06)Anc28:1e-06,AKR_J:1e-06)Anc26:1e-06,(BALB_cJ:1e-06,A_J:1e-06)Anc27:1e-06)Anc25:1e-06)Anc22:1e-06)Anc19:1e-06,(LP_J:1e-06,129S1_SvImJ:1e-06)Anc20:1e-06)Anc18:1e-06)Anc17:0.0001)Anc16:1e-06)splitPoint:1e-06)Anc14:0.015,CAROLI_EiJ:0.02)Anc13:0.01,Pahari_EiJ:0.03)Anc12:0.02,Rattus:0.013)msca_root:0.065,micOch1:0.15)stitch1:0.117,jacJac1:0.1859)stitch2:0.07,oryCun2:0.21)stitch3:0.01,((((hg19:0.00642915,panTro4:0.00638042)Anc11:0.00217637,gorGor3:0.00882142)Anc10:0.00935116,ponAbe2:0.0185056)Anc08:0.00440069,rheMac3:0.007)primates:0.1)stitch4:0.02,((oviAri3:0.019,bosTau8:0.0506)oviBos:0.17,(canFam3:0.11,felCat8:0.08)stitch5:0.06)stitch6:0.02)stitch7:0.02,loxAfr3:0.15)stitch8;"

# List of species to keep
species_to_keep = ['hg19', 'C57B6J', 'bosTau8', 'panTro4', 'gorGor3', 'ponAbe2', 'rheMac3', 'Rattus', 'micOch1', 'jacJac1', 'oryCun2', 'oviBos', 'oviAri3', 'canFam3', 'felCat8', 'loxAfr3']

# Mapping of scientific names to non-scientific names
species_mapping = {
    'hg19': 'Human (hg19)',
    'C57B6J': 'Mouse (C57B6J)',
    'bosTau8': 'Cow (bosTau8)',
    'panTro4': 'Chimpanzee (panTro4)',
    'gorGor3': 'Gorilla (gorGor3)',
    'ponAbe2': 'Orangutan (ponAbe2)',
    'rheMac3': 'Macaque (rheMac3)',
    'Rattus': 'Rat (Rattus)',
    'micOch1': 'Prairie Vole (micOch1)',
    'jacJac1': 'Egyptian Jerboa (jacJac1)',
    'oryCun2': 'Rabbit (oryCun2)',
    'oviBos': 'Musk Ox (oviBos)',
    'oviAri3': 'Sheep (oviAri3)',
    'canFam3': 'Dog (canFam3)',
    'felCat8': 'Cat (felCat8)',
    'loxAfr3': 'Elephant (loxAfr3)'
}


# Load the tree
tree = Phylo.read(StringIO(newick_tree), "newick")

# Prune the tree
print("Terminal nodes in the tree:")
for terminal in tree.get_terminals():
    print(terminal.name)

# Prune the tree manually
to_prune = [terminal for terminal in tree.get_terminals() if terminal.name not in species_to_keep]
for terminal in to_prune:
    tree.prune(terminal)

for terminal in tree.get_terminals():
    if terminal.name in species_mapping:
        terminal.name = species_mapping[terminal.name]


# Write the pruned tree
new_pruned_tree = StringIO()
Phylo.write(tree, new_pruned_tree, "newick")

# Output the pruned tree
print new_pruned_tree.getvalue()
