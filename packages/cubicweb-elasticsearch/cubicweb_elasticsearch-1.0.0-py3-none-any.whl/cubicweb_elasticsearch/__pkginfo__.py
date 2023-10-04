# pylint: disable=W0622
"""cubicweb-elasticsearch application packaging information"""

modname = "elasticsearch"
distname = "cubicweb-elasticsearch"

numversion = (1, 0, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Simple ElasticSearch indexing integration for CubicWeb"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

__depends__ = {
    "cubicweb": ">= 4.0.0, < 5.0.0",
    "cubicweb-web": ">= 1.0.0, < 2.0.0",
    "cwtags": None,
    "elasticsearch": ">=7.0.0,<8.0.0",
    "elasticsearch-dsl": ">=7.0.0,<8.0.0",
    "beautifulsoup4": None,
}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
