"""
MiCADO Submission Engine CSAR Utilities
---------------------------------------
Handles various aspects of CSARchives

Eg. Validate raw CSAR files (zip) by passing individual templates
to the YAML validator
"""

import os
import shutil
import tempfile
import zipfile

from micadoparser import parser
from micadoparser.utils.yaml import handle_yaml
from micadoparser.exceptions import MultiError, ValidationError


def handle_csar(path, parsed_params):
    """Handles CSAR (multi-file) ADTs and returns any errors caught
    :params: path, parsed_params
    :type: string, dictionary
    :return: template

    | parsed_params: dictionary containing the input to change
    | path: local or remote path to the file to parse
    """
    errors = csar_validation(path, parsed_params)
    if errors:
        raise MultiError(errors, "Cannot parse CSAR, issues in templates...")
        
    template = parser.get_template(path, parsed_params)

    template.nodetemplates = get_concrete_nodes(template)

    return template


def csar_validation(file, parsed_params):
    """Validates individual YAML files inside a CSAR"""
    temp_dir = None
    errors = set()
    try:
        temp_dir = tempfile.NamedTemporaryFile().name
        with zipfile.ZipFile(file, "r") as zf:
            zf.extractall(temp_dir)
    except Exception as e:
        raise ValidationError("[CSAR] Could not extract CSARchive")

    for file in os.listdir(temp_dir):

        path = os.path.join(temp_dir, file)
        try:
            if not os.path.isfile(path):
                continue

            # There is an opportunity here to create a new
            # CSAR from "fixed" single YAML files (eg. TOSCA v1.3)
            handle_yaml(path, parsed_params)
        except Exception as e:
            errors.add(f"[{file}] {e}")

    if temp_dir:
        shutil.rmtree(temp_dir)

    return errors


def get_concrete_nodes(tpl):
    """Pulls CSAR sub nodes up to top level"""
    concrete_nodes = []
    abstract_nodes = []
    for node in tpl.nodetemplates:
        if not hasattr(node.sub_mapping_tosca_template, "nodetemplates"):
            concrete_nodes.append(node)
            continue

        abstract_nodes.append(node)
        for subnode in node.sub_mapping_tosca_template.nodetemplates:
            concrete_nodes.append(subnode)

    for node in abstract_nodes:
        if not node.related:
            continue

        concrete_related = {}

        # iterate over other abstract nodes under requirements
        for abst_node, conc_rel in node.related.items():

            # iterate over concrete nodes of the abstract node
            for conc_node in abst_node.sub_mapping_tosca_template.nodetemplates:

                # build the related map using concrete nodes and relationships
                concrete_related.update({conc_node: conc_rel})

        for subnode in node.sub_mapping_tosca_template.nodetemplates:

            subnode.related.update(concrete_related)
            # TODO: can we implement something like this?
            # subnode._requirements += node.requirements

    return concrete_nodes
