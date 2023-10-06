# copyright 2016-2023 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""Tests for AuthorityRecord entities"""


from lxml import etree

from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_eac import testutils


class EACExportTC(CubicWebTC):
    """Unit tests for EAC-CPF exports."""

    def test_richstring_plain(self):
        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, "T-01", "Alice")
            desc = "ding\nlikes rabbits"
            mandate = cnx.create_entity(
                "Mandate",
                term="ding-girl",
                description=desc,
                description_format="text/plain",
                mandate_agent=alice,
            )
            cnx.commit()
            serializer = alice.cw_adapt_to("EAC-CPF")
            line1, line2 = serializer._eac_richstring_paragraph_elements(
                mandate, "description"
            )
        assert line1.tag == "p"
        assert line1.text == "ding"
        assert line2.tag == "p"
        assert line2.text == "likes rabbits"

    def test_richstring_html_simple(self):
        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, "T-01", "Alice")
            desc = "<span>ding</span>"
            mandate = cnx.create_entity(
                "Mandate",
                term="ding-girl",
                description=desc,
                description_format="text/html",
                mandate_agent=alice,
            )
            cnx.commit()
            serializer = alice.cw_adapt_to("EAC-CPF")
            (tag,) = serializer._eac_richstring_paragraph_elements(
                mandate, "description"
            )
        assert tag.tag == "span"
        self.assertIn(desc, etree.tostring(tag, encoding="unicode"))

    def test_richstring_html_multiple_elements(self):
        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, "T-01", "Alice")
            desc = ["<h1>she <i>rules!</i></h1>", '<a href="1">pif</a>']
            mandate = cnx.create_entity(
                "Mandate",
                term="chairgirl",
                description="".join(desc),
                description_format="text/html",
                mandate_agent=alice,
            )
            cnx.commit()
            serializer = alice.cw_adapt_to("EAC-CPF")
            h1, a = serializer._eac_richstring_paragraph_elements(
                mandate, "description"
            )
        assert h1.tag == "h1"
        assert a.tag == "a"
        self.assertIn(etree.tostring(h1, encoding="unicode"), desc[0])
        self.assertIn(etree.tostring(a, encoding="unicode"), desc[1])

    def test_richstring_markdown(self):
        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, "T-01", "Alice")
            desc = "[pif](http://gadget.com) is *red*"
            desc_html = '<a href="http://gadget.com">pif</a> ' "is <em>red</em>"
            mandate = cnx.create_entity(
                "Mandate",
                term="w",
                description=desc,
                description_format="text/markdown",
                mandate_agent=alice,
            )
            cnx.commit()
            serializer = alice.cw_adapt_to("EAC-CPF")
            (tag,) = serializer._eac_richstring_paragraph_elements(
                mandate, "description"
            )
        assert tag.tag == "p"
        self.assertIn(desc_html, etree.tostring(tag, encoding="unicode"))

    def test_richstring_rest(self):
        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, "T-01", "Alice")
            desc = "`pif <http://gadget.com>`_ is *red*"
            desc_html = (
                '<a class="reference" href="http://gadget.com">pif</a> '
                "is <em>red</em>"
            )
            mandate = cnx.create_entity(
                "Mandate",
                term="w",
                description=desc,
                description_format="text/rest",
                mandate_agent=alice,
            )
            cnx.commit()
            serializer = alice.cw_adapt_to("EAC-CPF")
            (ptag,) = serializer._eac_richstring_paragraph_elements(
                mandate, "description"
            )
        assert ptag.tag == "p"
        self.assertIn(desc_html, etree.tostring(ptag, encoding="unicode"))

    def test_richstring_empty(self):
        def check(authority_record):
            serializer = authority_record.cw_adapt_to("EAC-CPF")
            res = serializer._eac_richstring_paragraph_elements(mandate, "description")
            assert res == []

        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, "T-01", "Alice")
            mandate = cnx.create_entity(
                "Mandate", term="w", description=None, mandate_agent=alice
            )
            cnx.commit()
            check(alice)
        with self.admin_access.cnx() as cnx:
            cnx.execute('SET X description_format "text/rest" WHERE X is Mandate')
            cnx.commit()
            authority_record = cnx.execute(
                'Any X WHERE N name_entry_for X, N parts "Alice"'
            ).one()
            check(authority_record)

    def test_richstring_non_none_non_html(self):
        with self.admin_access.cnx() as cnx:
            arecord = testutils.authority_record(cnx, "R-01", "R")
            mandate = cnx.create_entity(
                "Mandate",
                term="w",
                description=" ",
                description_format="text/markdown",
                mandate_agent=arecord,
            )
            cnx.commit()
            serializer = arecord.cw_adapt_to("EAC-CPF")
            element = serializer.mandate_element(mandate)
            assert ["term"] == [child.tag for child in element]


if __name__ == "__main__":
    import unittest

    unittest.main()
