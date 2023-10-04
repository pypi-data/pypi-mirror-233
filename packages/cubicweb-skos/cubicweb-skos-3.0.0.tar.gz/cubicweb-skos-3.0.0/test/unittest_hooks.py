# copyright 2015-2023 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-skos unit tests for hooks"""

from yams import ValidationError
from cubicweb.devtools import testlib


class HooksTC(testlib.CubicWebTC):
    def test_externaluri_to_concept(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity("ConceptScheme", title="preexisting")
            concept = scheme.add_concept(
                "something", cwuri="http://data.bnf.fr/ark:/12148/cb11934798x"
            )
            exturi = cnx.create_entity(
                "ExternalUri",
                cwuri="http://someuri/someobject",
                uri="http://someuri/someobject",
                exact_match=concept,
            )
            cnx.commit()
            # now insert a concept with the external uri as cwuri
            scheme = cnx.create_entity("ConceptScheme")
            new_concept = scheme.add_concept(
                "some object", cwuri="http://someuri/someobject"
            )
            cnx.commit()
            # ensure the external uri has been replaced by the concept and deleted
            concept.cw_clear_all_caches()
            self.assertEqual(concept.exact_match[0].eid, new_concept.eid)
            self.assertFalse(cnx.execute("Any X WHERE X eid %(x)s", {"x": exturi.eid}))

    def test_skos_source(self):
        with self.admin_access.repo_cnx() as cnx:
            skos = cnx.create_entity(
                "SKOSSource", name="a source", url="http://skos.org\nhttp://skos.net"
            )
            cnx.commit()
            source = cnx.find("CWSource", name="a source").one()
            self.assertEqual(source.url, "http://skos.org\nhttp://skos.net")
            skos.cw_set(name="new name", url="http://skos.com")
            self.assertEqual(source.name, "new name")
            self.assertEqual(source.url, "http://skos.com")

    def check_duplicated_preferred_label(self, language_code, expected_errors):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity("ConceptScheme", title="scheme")
            concept = scheme.add_concept("un concept", language_code=language_code)
            cnx.create_entity(
                "Label",
                label="le concept",
                kind="preferred",
                label_of=concept,
                language_code=language_code,
            )
            with self.assertRaises(ValidationError) as cm:
                cnx.commit()
        self.assertEqual(cm.exception.errors, expected_errors)

    def test_concept_unique_pref_label_language(self):
        self.check_duplicated_preferred_label(
            "fr",
            {
                "": 'a preferred label in "%(lang)s" language already exists',
                "language_code": "please use another language code",
            },
        )

    def test_concept_unique_pref_label_no_language(self):
        self.check_duplicated_preferred_label(
            None,
            {
                "": "a preferred label without language already exists",
                "language_code": "please specify a language code",
            },
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
