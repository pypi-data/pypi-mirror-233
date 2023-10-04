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

import os
from io import BytesIO
from tempfile import NamedTemporaryFile

from cubicweb_web import Redirect
from cubicweb_web.devtools.testlib import WebCWTC

from cubicweb_skos.rdfio import default_graph


class ViewsTC(WebCWTC):
    def setup_database(self):
        with self.admin_access.client_cnx() as cnx:
            cnx.create_entity("ConceptScheme", title="musique")
            cnx.commit()

    def test_flat_scheme_concepts_import(self):
        with self.admin_access.web_request() as req:
            scheme = req.find("ConceptScheme", title="musique").one()
            # simply test the form properly render and is well formed
            self.view(
                "skos.scheme.import", rset=scheme.as_rset(), req=req, template=None
            )
            content = "\n\nélectro\nhip-hop\nrap\njazz\nclassique\n"
            req.form = self.fake_form(
                "skos.scheme.import",
                {
                    "stream": ("filename.txt", BytesIO(content.encode("utf-8"))),
                    "encoding": "utf-8",
                    "language_code": "fr",
                    "format": "simple",
                    "delimiter": "tab",
                },
                [(scheme, {})],
            )
            # now actually tests the import, using scheme.view and not self.view which doesn't like
            # exception, even Redirect
            self.assertRaises(Redirect, scheme.view, "skos.scheme.import")
            self.assertEqual(
                {c.dc_title() for c in scheme.top_concepts},
                set("électro hip-hop rap jazz classique".split()),
            )
            self.assertEqual(
                {
                    label.language_code
                    for concept in scheme.top_concepts
                    for label in concept.preferred_label
                },
                {"fr"},
            )

    def test_lcsv_scheme_concepts_import(self):
        with self.admin_access.web_request() as req:
            scheme = req.find("ConceptScheme", title="musique").one()
            # simply test the form properly render and is well formed
            self.view(
                "skos.scheme.import", rset=scheme.as_rset(), req=req, template=None
            )
            fname = "lcsv_example_shortened.csv"
            posted = {
                "stream": (fname, open(self.datapath(fname), "rb")),
                "encoding": "utf-8",
                "language_code": "fr",
                "delimiter": "tab",
                "format": "lcsv",
            }
            req.form = self.fake_form("skos.scheme.import", posted, [(scheme, {})])
            # now actually tests the import, using scheme.view and not self.view which doesn't like
            # exception, even Redirect
            self.assertRaises(Redirect, scheme.view, "skos.scheme.import")
        # check that the concept were added
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.find("ConceptScheme", title="musique").one()
            self.assertEqual(len(scheme.top_concepts), 2)
            concepts = cnx.find("Concept")
            self.assertEqual(len(concepts), 5)
            concept1 = cnx.find(
                "Concept",
                definition="Définition de l'organisation politique de l'organisme,",
            ).one()
            label = concept1.preferred_label[0]
            self.assertEqual(len(concept1.preferred_label), 1)
            self.assertEqual(
                (label.label, label.language_code), ("Vie politique", "fr")
            )
            self.assertEqual(len(concept1.narrower_concept), 2)
            concept2 = cnx.find(
                "Concept", definition="Création volontaire ou en application de la loi"
            ).one()
            self.assertEqual(concept2.broader_concept[0], concept1)

    def _test_skos_view(self, vid, nb_expected_triples):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.find("ConceptScheme", title="musique").one()
            scheme.add_concept("pop")
            with NamedTemporaryFile(delete=False) as fobj:
                try:
                    fobj.write(scheme.view(vid))
                    fobj.close()
                    graph = default_graph()
                    graph.load("file://" + fobj.name, rdf_format="xml")
                finally:
                    os.unlink(fobj.name)
            triples = set(graph.triples())
            self.assertEqual(len(triples), nb_expected_triples, triples)

    def test_skos_primary_view(self):
        self._test_skos_view("primary.rdf", 5)

    def test_skos_list_view(self):
        self._test_skos_view("list.rdf", 2)


class RelationWidgetTC(WebCWTC):
    """Functional test case about the relation widget."""

    def test_linkable_rset(self):
        with self.admin_access.repo_cnx() as cnx:
            lang = cnx.create_entity("Language")
            cnx.commit()
        with self.admin_access.web_request() as req:
            lang = req.entity_from_eid(lang.eid)
            req.form = {"relation": "language_to:Concept:subject"}
            view = self.vreg["views"].select(
                "search_related_entities", req, rset=lang.as_rset()
            )
            self.assertFalse(view.linkable_rset())
        with self.admin_access.repo_cnx() as cnx:
            lang_to_rtype = cnx.find("CWRType", name="language_to").one()
            scheme = cnx.create_entity(
                "ConceptScheme", title="languages", scheme_relation_type=lang_to_rtype
            )
            scheme.add_concept(label="fr")
            cnx.commit()
        with self.admin_access.web_request() as req:
            req.form = {"relation": "language_to:Concept:subject"}
            view = self.vreg["views"].select(
                "search_related_entities", req, rset=lang.as_rset()
            )
            self.assertEqual(len(view.linkable_rset()), 1)


if __name__ == "__main__":
    from unittest import main

    main()
