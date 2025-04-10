from pynxtools.dataconverter.helpers import generate_template_from_nxdl
from pynxtools.dataconverter.nexus_tree import *
from pynxtools.dataconverter.template import Template

spm_appdef = "NXspm"
spmT = generate_tree_from(spm_appdef)


def add_template_key_from(nx_node,
                       parent_path = ""):
    key = None
    unit = None
    if nx_node.type == "attribute":
        leaf_part = (f"{nx_node.name}[{nx_node.name}]"
                     if nx_node.variadic else nx_node.name)
        key = f"{parent_path}/@{leaf_part}"
    elif nx_node.type == "field":
        leaf_part = (f"{nx_node.name}[{nx_node.name}]"
                     if nx_node.variadic else nx_node.name)
        key = f"{parent_path}/{leaf_part}"
        if hasattr(nx_node, "unit") and nx_node.unit:
            unit = f"{key}/@units"
    elif nx_node.type == "group":
        leaf_part = f"{nx_node.name}[{nx_node.name}]"
        key = f"{parent_path}/{leaf_part}"
    if key:
        template[nx_node.optionality][key] = None
    if unit:
        template[nx_node.optionality][unit] = None
    return key
def build_template_from_nexus_tree(appdef_root, template, parent_path = ""):
    """
    Build a template from the nexus tree.
    """
    for child in appdef_root.children:
        key = add_template_key_from(child, parent_path)
        if not key:
            continue
        build_template_from_nexus_tree(child, template, key)
template = Template()
build_template_from_nexus_tree(spmT, template)
template_old = Template()

root, _ = get_nxdl_root_and_path(spm_appdef)
generate_template_from_nxdl(
    root=root,
    template=template_old,
)
print(' #### check optional missing keys')
template_ = template
template_old_ = template_old
def check_missing():
    for key, _ in template_['optional'].items():
        if key not in template_old_['optional']:
            print(f"OPTIONAL Missing key in template_old: {key}")
    print(' #### check required missing keys')
    for key, _ in template_['required'].items():
        if key not in template_old_['required']:
            print(f"REQUIRED: Missing key in template_old: {key}")
