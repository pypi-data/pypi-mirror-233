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
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""elasticsearch search views"""
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet
from bs4 import BeautifulSoup

from logilab.mtconverter import xml_escape

import cwtags.tag as t
from cubicweb import _
from cubicweb_web.view import StartupView

from cubicweb_elasticsearch.es import get_connection
from cubicweb_elasticsearch.search_helpers import compose_search


def normalize_value(value):
    # FIXME TODO have better typing mechanisme (inspect facets?)
    if not isinstance(value, str):
        return value
    try:
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        else:
            return int(value)
    except ValueError:
        pass
    return value


class CWFacetedSearch(FacetedSearch):
    # fields that should be searched
    fields = ["title^3", "description^2", "alltext"]

    facets = {
        # use bucket aggregations to define facets
        "cw_etype": TermsFacet(field="cw_etype"),
        "creation_date": DateHistogramFacet(field="creation_date", interval="month"),
    }

    def __init__(
        self,
        query=None,
        filters={},
        sort=(),
        doc_types=None,
        index=None,
        form=None,
        track_total_hits=True,
        **kwargs,
    ):
        if index:
            self.index = index
        if doc_types:
            self.doc_types = doc_types
        if form:
            self.form = form
        else:
            self.form = {}

        if type(sort) not in [list, tuple]:
            sort = (sort,)

        # Count all the hits by default
        self.track_total_hits = track_total_hits
        self.extra_kwargs = kwargs
        super().__init__(query, filters, sort=sort)

    def search(self):
        # override methods to add custom pieces
        s = super().search()
        return s.extra(track_total_hits=self.track_total_hits)

    def query(self, search, query):
        if query:
            common = "debug-es-disable-common" not in self.form  # default True
            phrase = "debug-es-disable-phrase" not in self.form  # default True
            fuzzy = "fuzzy" in self.form  # default False
            return compose_search(
                search,
                query=query,
                fields=self.fields,
                fuzzy=fuzzy,
                common=common,
                phrase=phrase,
            )
        return search

    def highlight(self, search):
        """
        Add custom highlighting
        """
        search = search.highlight(
            *(f if "^" not in f else f.split("^", 1)[0] for f in self.fields)
        )
        return search.highlight_options(fragment_size=150, encoder="html")


class ElasticSearchView(StartupView):
    __regid__ = "esearch"
    previous_link = " &lt; "
    next_link = " &gt; "
    middle_link = " &middot; " * 3
    title = _("Search")
    default_items_per_page = 10

    def render_search_comp(self):
        search_comp = self._cw.vreg["components"].select_or_none(
            "search-comp", self._cw
        )
        if search_comp:
            search_comp.render(w=self.w)

    def do_search(self, query_string):
        get_connection(self._cw.vreg.config)
        facet_selections = {}
        items_per_page = int(
            self._cw.form.get("items_per_page", self.default_items_per_page)
        )
        start, stop = 0, items_per_page
        for key, value in self._cw.form.items():
            if key.startswith("es_"):
                if isinstance(value, list):
                    for index in range(len(value)):
                        value[index] = normalize_value(value[index])
                else:
                    value = normalize_value(value)

                facet_selections[key.replace("es_", "")] = value
            if key == "page":
                try:
                    start = (max(int(value) - 1, 0)) * items_per_page
                    stop = start + items_per_page
                except ValueError:
                    pass
        search = self.customize_search(query_string, facet_selections, start, stop)
        if "debug-es" in self._cw.form:
            import json

            self.w("<pre>")
            self.w(json.dumps(search._s.to_dict(), indent=2))
            self.w("</pre>")
            self.w("<br/>")
        try:
            response = search.execute()
            if "debug-es" in self._cw.form:
                import json

                self.w("<pre>")
                self.w(json.dumps(response.to_dict(), indent=2))
                self.w("</pre>")
                self.w("<br/>")
            return response
        except NotFoundError:
            self.w("index not found in elasticsearch")
            return

    def call(self, **kwargs):
        # TODO if no ES configuration, redirect or display warning
        self.render_search_comp()
        query_string = self._cw.form.get("q", self._cw.form.get("search", ""))
        self.w(f"<h1>{self._cw._(self.title)}</h1>")
        response = self.do_search(query_string)
        if response.hits.total.value:
            self.w(f"<h2>Resultats pour : <em>{xml_escape(query_string)}</em></h2>")
            self.w(f"Resultats: {response.hits.total.value}")
            if hasattr(response, "facets"):
                self.display_facets(response)
        self.display_results(response)

    def customize_search(
        self, query_string, facet_selections, start=0, stop=10, **kwargs
    ):
        """
        This is where one can customize the search by modifying the
        query string and facet selection in an inherited class.

        For example :
        * add specific keywords sur as id:text and
          add them the facet_selection
        * use your own CWFacetedSearch class to modify fields
          and facets
        """
        return CWFacetedSearch(
            query_string,
            facet_selections,
            index=self._cw.vreg.config.get("index-name"),
            doc_types=["_doc"],
            form=self._cw.form,
            **kwargs,
        )[start:stop]

    def display_results(self, response):
        """
        Display results obtained from elasticsearch
        """
        self.w('<div id="main-center" class="col-xs-10" role="main">')
        self.pagination(response)
        self.w("<ul>")
        for result in response:
            self.w("<li>")
            infos = result.to_dict()
            infos["_score"] = result.meta.score
            infos["keys"] = result.to_dict().keys()
            infos["url"] = (
                infos["cwuri"].startswith("_auto_generated")
                and infos["eid"]
                or infos["cwuri"]
            )
            self.customize_infos(infos)
            try:
                self.w(
                    f"<a href=\"{infos['url']}\">{infos['title']}</a> ({infos['_score']:.2f})<br/>"
                )
                if self._cw.form.get("debug-es"):
                    self.w(f" [{infos['keys']}] <br/>")
            except KeyError:
                self.w(f"Missing key in : {infos.keys()}")
            try:
                for fragment in result.meta.highlight.content:
                    self.w(f"... {BeautifulSoup(fragment, 'lxml').get_text()}")
                    self.w(" ... <br/>")
            except AttributeError:
                pass
            self.w("</li>")
        self.w("</ul>")
        self.pagination(response)
        self.w("</div>")

    def customize_infos(self, infos):
        """
        This is where one can customize the infos being displayed

        For example : set the title according to your rules and data set
        """
        pass

    def pagination(self, response):
        """
        Pagination HTML generation
        """
        if response.hits.total.value <= 10:
            return
        url_params = self._cw.form.copy()
        with t.ul(self.w, klass="pagination") as ul:
            current_page = int(url_params.get("page", 1))
            url_params["page"] = current_page - 1
            if current_page - 1 >= 1:
                ul(
                    t.li(
                        t.a(
                            self.previous_link,
                            href=xml_escape(self._cw.build_url(**url_params)),
                        )
                    )
                )
            else:
                ul(t.li(t.a(self.previous_link)))
            total_pages = min(
                (response.hits.total.value // self.default_items_per_page) + 2, 1000
            )
            page_padding = 3

            if current_page > page_padding:
                for page in range(
                    1, min(page_padding + 1, current_page - page_padding)
                ):
                    self.page_number(url_params, page, current_page, ul)
                if current_page > (page_padding * 2) + 1:
                    ul(t.li(t.a(self.middle_link)))
            for page in range(
                max(1, current_page - page_padding),
                min(current_page + page_padding, total_pages),
            ):
                self.page_number(url_params, page, current_page, ul)
            if current_page < total_pages - page_padding:
                if current_page < total_pages - page_padding * 2:
                    ul(t.li(t.a(self.middle_link)))
                for page in range(
                    max(current_page + page_padding, total_pages - page_padding),
                    total_pages,
                ):
                    self.page_number(url_params, page, current_page, ul)

            url_params["page"] = current_page + 1
            if current_page + 1 >= (total_pages):
                ul(t.li(t.a(self.next_link)))
            else:
                ul(
                    t.li(
                        t.a(
                            self.next_link,
                            href=xml_escape(self._cw.build_url(**url_params)),
                        )
                    )
                )

    def page_number(self, url_params, page, current_page, ul):
        """
        Generate HTML for page number (bold if page is current_page)
        """
        url_params["page"] = page
        url = self._cw.build_url(**url_params)
        if page == current_page:
            ul(
                t.li(
                    t.a(t.b(page), href=xml_escape(url)),
                    Class="active",
                )
            )
        else:
            ul(t.li(t.a(page, href=xml_escape(url))))
        return url

    @property
    def facets_to_display(self):
        """
        Method to list facets to display (can be customized)
        """
        return ("cw_etype",)

    def display_facets(self, response):
        """
        Generate HTML for facets
        """
        self.w(
            """<aside id="aside-main-left" class="col-xs-2 cwjs-aside">
                   <div class="panel panel-default contextFreeBox facet_filterbox">
                      <div class="panel-heading">
                         <div class="panel-title">Facettes</div>
                      </div>
        """
        )
        for attribute in self.facets_to_display:
            url_params = self._cw.form.copy()
            if "page" in url_params:
                del url_params["page"]
            self.w('<div class="facetBody vocabularyFacet">')
            self.w(f'<div class="facetTitle">{attribute}</div>')
            for tag, count, selected in response.facets[attribute]:
                # facetValueSelected / facetValueDisabled in class
                facet_item = (
                    '<div class="facetValue facetCheckBox">'
                    "    <span>"
                    '      <a href="{}">{} {}</a>'
                    "    </span>"
                    "</div>"
                )
                if url_params.get(f"es_{attribute}") != tag:
                    url_params[f"es_{attribute}"] = str(tag)
                else:
                    del url_params[f"es_{attribute}"]
                url = self._cw.build_url(**url_params)
                content = selected and f'<div class="facet-active">{tag}</div>' or tag
                self.w(facet_item.format(url, content, count))
            self.w("</div>")
        self.w("</div></aside>")
