Summary
-------
Simple ElasticSearch indexing integration for CubicWeb


Parameters
~~~~~~~~~~

* elasticsearch-locations (CW_ELASTICSEARCH_LOCATIONS)
* index-name (CW_INDEX_NAME)
* elasticsearch-verify-certs (CW_ELASTICSEARCH_VERIFY_CERTS)
* elasticsearch-ssl-show-warn (CW_ELASTICSEARCH_SSL_SHOW_WARN)

Pyramid debug panel
~~~~~~~~~~~~~~~~~~~

To activate the debug panel, you'll need to install ``pyramid_debugtoolbar``,
typically with::

  pip install pyramid_debugtoolbar

Then, you'll have activate the debug toolbar and include the ElasticSearch
panel in your ``pyramid.ini``:

  pyramid.includes =
      pyramid_debugtoolbar
  debugtoolbar.includes =
      cubicweb_elasticsearch.pviews.espanel


**Alltext** field
~~~~~~~~~~~~~~~~~~

The `cubicweb_elasticsearch.search_helpers.compose_search` referencies
a custom `alltext` field which contains all indexed text. This field  must be
defined in the custom Indexer mapping.

HTTPS and SSL certificates in communication with server
-------------------------------------------------------

In some cases (ElasticSearch Kubernetes deployment for example), self signed
certificates are used and can be ignored using elasticsearc-verify-certs, in
this case, the python binding will issue warnings for each request, which is
cumbersome when running requests in a `ccplugin` command. You can use
`elasticsearch-ssl-show-warn (CW_ELASTICSEARCH_SSL_SHOW_WARN)` to remove
those warnings (default is to show them). Most of the time, a better solution
is to have proper certificates to authenticate the servers you are talking to.
