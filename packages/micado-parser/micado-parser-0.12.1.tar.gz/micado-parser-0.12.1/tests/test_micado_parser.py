import unittest


from micadoparser.parser import set_template


class TestMicadoParser(unittest.TestCase):
    """UnitTests for micado_parser"""

    def test_parse_csar(self):
        set_template("tests/templates/thing-ce.csar")

    def test_parse_adt_from_url(self):
        tpl = set_template(
            "https://raw.githubusercontent.com/micado-scale/ansible-micado/main/demos/wordpress/wordpress_ec2.yaml"
        )
        self.assertIn("wordpress", [x.name for x in tpl.nodetemplates])

    def test_parse_adt_from_file(self):
        tpl = set_template("tests/templates/good_tosca.yaml")
        self.assertIn("stressynet", [x.name for x in tpl.nodetemplates])

    def test_tosca_occurences_indexed_properties(self):
        tpl = set_template("tests/templates/adt_fd.yaml")
        self.assertIn("fd-receiver-6", [x.name for x in tpl.nodetemplates])
        self.assertNotIn("fd-receiver", [x.name for x in tpl.nodetemplates])

    def test_tosca_occurences_no_indexed_properties(self):
        tpl = set_template("tests/templates/tosca.yaml")
        self.assertEqual(
            tpl.nodetemplates[3].entity_tpl["metadata"]["occurrences"], [1, 5]
        )

    def test_parent_interfaces_unmodified(self):
        tpl = set_template("tests/templates/tosca.yaml")
        self.assertIn(
            "get_property",
            tpl.nodetemplates[6].type_definition.interfaces["Kubernetes"]["create"][
                "inputs"
            ]["spec"]["hostPath"]["path"],
        )

    def test_get_input_string(self):
        string_match = "ECHOTEST123"
        tpl = set_template(
            "tests/templates/inputs_test.yaml", 
            parsed_params={"echo_msg": string_match}
        )
        env_vars = tpl.nodetemplates[0].get_property_value("env")
        self.assertEqual(
            string_match, env_vars[0]["value"]
        )

    def test_get_input_custom(self):
        tpl = set_template("tests/templates/inputs_test.yaml")
        input_type = tpl.inputs[0].type
        self.assertEqual(
            input_type, "string"
        )

if __name__ == "__main__":
    unittest.main()
