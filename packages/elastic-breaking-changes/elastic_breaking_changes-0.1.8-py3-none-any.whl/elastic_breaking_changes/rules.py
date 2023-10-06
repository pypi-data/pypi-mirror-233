rules = {}
rules['.*"order":{"_term":".*'] = """
The terms aggregation no longer supports the _term order key.
Details
The terms aggregation no longer supports the _term key in order values. To sort buckets by their term, use _key instead.

Impact
Discontinue use of the _term order key. Requests that include a _term order key will return an error.

Compatibility
When rest-api-compatibility is requested, the _term order is ignored and key is used instead.
"""

rules['.*"order":{"_time":".*'] = """
The date_histogram aggregation no longer supports the _time order key.
Details
The date_histogram aggregation no longer supports the _time key in order values. To sort buckets by their key, use _key instead.

Impact
Discontinue use of the _time order key. Requests that include a _time order key will return an error.

Compatibility
When rest-api-compatibility is requested, the _time order is ignored and _key is used instead.
"""

rules['.*"aggs":.*{"moving_avg":{.*'] = """
The moving_avg aggregation has been removed.
Details
The moving_avg aggregation was deprecated in 6.4 and has been removed. To calculate moving averages, use the moving_fn aggregation instead.

Impact
Discontinue use of the moving_avg aggregation. Requests that include the moving_avg aggregation will return an error.
"""

rules['.*"aggs":.*{"date_histogram":{.*"interval".*'] = """
The date_histogram aggregation’s interval parameter is no longer valid.
Details
It is now an error to specify the interval parameter to the date_histogram aggregation or the https://www.elastic.co/guide/en/elasticsearch/reference/8.9/search-aggregations-bucket-composite-aggregation.html#_date_histogram[composite
date_histogram source. Instead, please use either calendar_interval or fixed_interval as appropriate.

Impact
Uses of the interval parameter in either the date_histogram aggregation or the date_histogram composite source will now generate an error. Instead please use the more specific fixed_interval or calendar_interval parameters.

Compatibility
When rest-api-compatibility is requested, the interval parameter is adapted to either a fixed or calendar interval.
"""

rules['.*(nGram|edgeNGram).*'] = """
The nGram and edgeNGram token filter names have been removed.
Details
The nGram and edgeNGram token filter names that have been deprecated since version 6.4 have been removed. Both token filters can only be used by their alternative names ngram and edge_ngram since version 7.0.

Impact
Use the equivalent ngram and edge_ngram token filters. Requests containing the nGram and edgeNGram token filter names will return an error.

OR:

The nGram and edgeNGram tokenizer names have been removed.
Details
The nGram and edgeNGram tokenizer names haven been deprecated with 7.6 and are no longer supported on new indices. Mappings for indices created after 7.6 will continue to work but emit a deprecation warning. The tokenizer name should be changed to the fully equivalent ngram or edge_ngram names for new indices and in index templates.

Impact
Use the ngram and edge_ngram tokenizers. Requests to create new indices using the nGram and edgeNGram tokenizer names will return an error.
"""

rules['.*{"wildcard":{.*'] = """
The EQL wildcard function has been removed.
Details
The wildcard function was deprecated in Elasticsearch 7.13.0 and has been removed.

Impact
Use the like or regex keywords instead.
"""

rules['.*POST.*_upgrade.*'] = """
The deprecated _upgrade API has been removed.
Details
Previously, the _upgrade API upgraded indices from the previous major version to the current version. The _reindex API should be used instead for that purpose.

Impact
Requests made to the old _upgrade API will return an error.
"""

rules['.*POST.*_freeze.*'] = """
The deprecated freeze index API has been removed.
Details
The freeze index API (POST /<index>/_freeze) has been removed. Improvements in heap memory usage have eliminated the reason to freeze indices. You can still unfreeze existing frozen indices using the unfreeze index API. For some use cases, the frozen tier may be a suitable replacement for frozen indices. See data tiers for more information.

Impact
Requests made to the old freeze index API will return an error.
"""

rules['.*PUT.*_template.*{"template.*'] = """
The create or update index template API’s template parameter has been removed.
Details
In 6.0, we deprecated the template parameter in create or update index template requests in favor of using index_patterns. Support for the template parameter is now removed in 8.0.

Impact
Use the create or update index template API's index_patterns parameter. Requests that include the template parameter will return an error.

Compatibility
When rest-api-compatibility is requested, the template parameter is mapped to index_patterns.
"""

rules['.*?wait_for_active_shards.*'] = """
The default for the ?wait_for_active_shards parameter on the close index API has changed.
Details
When closing an index in earlier versions, by default Elasticsearch would not wait for the shards of the closed index to be properly assigned before returning. From version 8.0 onwards the default behaviour is to wait for shards to be assigned according to the index.write.wait_for_active_shards index setting.

Impact
Accept the new behaviour, or specify ?wait_for_active_shards=0 to preserve the old behaviour if needed.
"""

rules['.*GET.*_stats/.*types=.*'] = """
The index stats API’s types query parameter has been removed.
Details
The index stats API’s types query parameter has been removed. Previously, you could combine types with the indexing query parameter to return indexing stats for specific mapping types. Mapping types have been removed in 8.0.

Impact
Discontinue use of the types query parameter. Requests that include the parameter will return an error.

Compatibility
When rest-api-compatibility is requested, the types query parameter is ignored and stats are returned for the entire index.
"""

rules['.*"user_agent":{.*"ecs".*'] = """
The user_agent ingest processor’s ecs parameter has no effect.
Details
In 7.2, we deprecated the ecs parameter for the user_agent ingest processor. In 8.x, the user_agent ingest processor will only return Elastic Common Schema (ECS) fields, regardless of the ecs value.

Impact
To avoid deprecation warnings, remove the parameter from your ingest pipelines. If a pipeline specifies an ecs value, the value is ignored.
"""

rules['.*include_type_name.*'] = """
The include_type_name query parameter has been removed.
Details
The include_type_name query parameter has been removed from the index creation, index template, and mapping APIs. Previously, you could set include_type_name to true to indicate that requests and responses should include a mapping type name. Mapping types have been removed in 8.x.

Impact
Discontinue use of the include_type_name query parameter. Requests that include the parameter will return an error.

Compatibility
When rest-api-compatibility is requested, the include_type_name query parameter is ignored and any custom mapping types in the request are removed.
"""

rules['.*POST.*_reindex{.*"size":.*'] = """
In the reindex, delete by query, and update by query APIs, the size parameter has been renamed.
Details
Previously, a _reindex request had two different size specifications in the body:

Outer level, determining the maximum number of documents to process
Inside the source element, determining the scroll/batch size.
The outer level size parameter has now been renamed to max_docs to avoid confusion and clarify its semantics.

Similarly, the size parameter has been renamed to max_docs for _delete_by_query and _update_by_query to keep the 3 interfaces consistent.

Impact
Use the replacement parameters. Requests containing the size parameter will return an error.

Compatibility
When rest-api-compatibility is requested, the size parameter is mapped to the max_docs parameter.
"""


rules['.*POST.*_update_by_query.*script_fields":{.*'] = """
The update by query API now rejects unsupported script fields.
Details
An update by query API request that includes an unsupported field in the script object now returns an error. Previously, the API would silently ignore these unsupported fields.

Impact
To avoid errors, remove unsupported fields from the script object.
"""


rules['.*PUT.*_scripts.*"code":.*'] = """
The create or update stored script API’s code parameter has been removed.
Details
The create or update stored script API's code parameter has been removed. Use the source parameter instead.

Impact
Discontinue use of the code parameter. Requests that include the parameter will return an error.
"""


rules['.*GET.*_search.*"_type":.*'] = """
Searches on the _type field are no longer supported.
Details
In 8.x, the _type metadata field has been removed. Elasticsearch now handles a search on the _type field as a search on a non-existent field. A search on a non-existent field matches no documents, regardless of the query string.


In 7.x, a search for _doc in the _type field would match the same documents as a match_all query.

Impact
Remove queries on the _type field from your search requests and search templates. Searches that include these queries may return no results.
"""


rules['.*_msearch.*'] = """
The multi search API now parses an empty first line as action metadata in text files.
Details
The multi search API now parses an empty first line as empty action metadata when you provide a text file as the request body, such as when using curl’s --data-binary flag.

The API no longer supports text files that contain:

An empty first line followed by a line containing only {}.
An empty first line followed by another empty line.
Impact
Don’t provide an unsupported text file to the multi search API. Requests that include an unsupported file will return an error.
"""


rules['.*"sort":{.*"string".*'] = """
The unmapped_type: string sort option has been removed.
Details
Search requests no longer support the unmapped_type: string sort option. Instead, use unmapped_type: keyword to handle an unmapped field as if it had the keyword field type but ignore its values for sorting.

Impact
Discontinue use of unmapped_type: string. Search requests that include the unmapped_type: string sort option will return shard failures.
"""


rules['.*"aggs":{.*"_id".*'] = """
Aggregating and sorting on _id is disallowed by default.
Details
Previously, it was possible to aggregate and sort on the built-in _id field by loading an expensive data structure called fielddata. This was deprecated in 7.6 and is now disallowed by default in 8.0.

Impact
Aggregating and sorting on _id should be avoided. As an alternative, the _id field’s contents can be duplicated into another field with docvalues enabled (note that this does not apply to auto-generated IDs).
"""


rules['.*_search.*"common":{.*'] = """
The common query has been removed.
Details
The common query, deprecated in 7.x, has been removed in 8.0. The same functionality can be achieved by the match query if the total number of hits is not tracked.

Impact
Discontinue use of the common query. Search requests containing a common query will return an error.
"""


rules['.*"cutoff_frequency".*'] = """
The cutoff_frequency parameter has been removed from the match and multi_match query.
Details
The cutoff_frequency parameter, deprecated in 7.x, has been removed in 8.0 from match and multi_match queries. The same functionality can be achieved without any configuration provided that the total number of hits is not tracked.

Impact
Discontinue use of the cutoff_frequency parameter. Search requests containing this parameter in a match or multi_match query will return an error.
"""


rules['.*(nested_filter|nested_path).*'] = """
The nested_filter and nested_path properties have been removed from the search API’s sort request body parameter.
Details
The nested_filter and nested_path options, deprecated in 6.x, have been removed in favor of the nested context.

Impact
Discontinue use of the sort request body parameter’s nested_filter and nested_path properties. Requests containing these properties will return an error.
"""


rules['.*"doc_field".*'] = """
Vector functions using (query, doc['field']) are no longer supported.
Details
The vector functions of the form function(query, doc['field']) were deprecated in 7.6, and are now removed in 8.x. The form function(query, 'field') should be used instead. For example, cosineSimilarity(query, doc['field']) is replaced by cosineSimilarity(query, 'field').

Impact
Use the function(query, 'field') form. Discontinue use of the function(query,
doc['field']) form. Requests containing the function(query,
doc['field']) form will return an error.
"""

rules['.*"indices_boost".*'] = """
The search API’s indices_boost request body parameter no longer accepts object values.
Details
The indices_boost option in the search request used to accept the boosts both as an object and as an array. The object format has been deprecated since 5.2 and is now removed in 8.0.

Impact
Use only array values in the indices_boost parameter. Requests containing an object value in the indices_boost parameter will return an error.
"""


rules['.*"use_field_mapping".*'] = """
The search API’s use_field_mapping request body parameter has been removed.
Details
In 7.0, we began formatting docvalue_fields by default using each field’s mapping definition. To ease the transition from 6.x, we added the format option use_field_mapping. This parameter was deprecated in 7.0, and is now removed in 8.0.

Impact
Discontinue use of the use_field_mapping request body parameter. Requests containing this parameter will return an error.

Compatibility
When rest-api-compatibility is requested, the use_field_mapping parameter is ignored.
"""

rules['.*"from":-.*'] = """
The search API’s from request body and url parameter cannot be negative.
Details
Search request used to accept -1 as a from in the search body and the url, treating it as the default value of 0. Other negative values got rejected with an error already. We now also reject -1 as an invalid value.

Impact
Change any use of -1 as from parameter in request body or url parameters by either setting it to 0 or omitting it entirely. Requests containing negative values will return an error.
"""

rules['.*"range".*'] = """
Range queries on date fields treat numeric values alwas as milliseconds-since-epoch.
Details
Range queries on date fields used to misinterpret small numbers (e.g. four digits like 1000) as a year when no additional format was set, but would interpret other numeric values as milliseconds since epoch. We now treat all numeric values in absence of a specific format parameter as milliseconds since epoch. If you want to query for years instead, with a missing format you now need to quote the input value (e.g. "1984").

Impact
If you query date fields without a specified format, check if the values in your queries are actually meant to be milliseconds-since-epoch and use a numeric value in this case. If not, use a string value which gets parsed by either the date format set on the field in the mappings or by strict_date_optional_time by default.
"""

rules['.*"geo_bounding_box".*'] = """
The geo_bounding_box query’s type parameter has been removed.
Details
The geo_bounding_box query’s type parameter was deprecated in 7.14.0 and has been removed in 8.0.0. This parameter is a no-op and has no effect on the query.

Impact
Discontinue use of the type parameter. geo_bounding_box queries that include this parameter will return an error.
"""

rules['.*"type".*'] = """
The type query has been removed.
Details
The type query has been removed. Mapping types have been removed in 8.0.

Impact
Discontinue use of the type query. Requests that include the type query will return an error.
"""



rules['.*action.destructive_requires_name.*'] = """
action.destructive_requires_name now defaults to true.
Details
The default for the action.destructive_requires_name setting changes from false to true in Elasticsearch 8.0.0.

Previously, defaulting to false allowed users to use wildcard patterns to delete, close, or change index blocks on indices. To prevent the accidental deletion of indices that happen to match a wildcard pattern, we now default to requiring that destructive operations explicitly name the indices to be modified.

Impact
To use wildcard patterns for destructive actions, set action.destructive_requires_name to false using the https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cluster-update-settings.html cluster settings API].
"""

rules['.*xpack.searchable.snapshot.shared_cache.size.*'] = """
You can no longer set xpack.searchable.snapshot.shared_cache.size on non-frozen nodes.
Details
You can no longer set xpack.searchable.snapshot.shared_cache.size on a node that doesn’t have the data_frozen node role. This setting reserves disk space for the shared cache of partially mounted indices. Elasticsearch only allocates partially mounted indices to nodes with the data_frozen role.

Impact
Remove xpack.searchable.snapshot.shared_cache.size from elasticsearch.yml for nodes that don’t have the data_frozen role. Specifying the setting on a non-frozen node will result in an error on startup.
"""

rules['.*indices.query.bool.max_clause_count.*'] = """
indices.query.bool.max_clause_count is deprecated and has no effect.
Details
Elasticsearch will now dynamically set the maximum number of allowed clauses in a query, using a heuristic based on the size of the search thread pool and the size of the heap allocated to the JVM. This limit has a minimum value of 1024 and will in most cases be larger (for example, a node with 30Gb RAM and 48 CPUs will have a maximum clause count of around 27,000). Larger heaps lead to higher values, and larger thread pools result in lower values.

Impact
Queries with many clauses should be avoided whenever possible. If you previously bumped this setting to accommodate heavy queries, you might need to increase the amount of memory available to Elasticsearch, or to reduce the size of your search thread pool so that more memory is available to each concurrent search.

In previous versions of Lucene you could get around this limit by nesting boolean queries within each other, but the limit is now based on the total number of leaf queries within the query as a whole and this workaround will no longer help.

Specifying indices.query.bool.max_clause_count will have no effect but will generate deprecation warnings. To avoid these warnings, remove the setting from elasticsearch.yml during an upgrade or node restart.
"""

rules['.*indices.lifecycle.poll_interval.*'] = """
indices.lifecycle.poll_interval must be greater than 1s.
Details
Setting indices.lifecycle.poll_interval too low can cause excessive load on a cluster. The poll interval must now be at least 1s (one second).

Impact
Set indices.lifecycle.poll_interval setting to 1s or greater in elasticsearch.yml or through the cluster update settings API.

Setting indices.lifecycle.poll_interval to less than 1s in elasticsearch.yml will result in an error on startup. Cluster update settings API requests that set indices.lifecycle.poll_interval to less than 1s will return an error.
"""

rules['.*xpack.security.authc.realms.*'] = """
The file and native realms are now enabled unless explicitly disabled.
Details
The file and native realms are now enabled unless explicitly disabled. If explicitly disabled, the file and native realms remain disabled at all times.

Previously, the file and native realms had the following implicit behaviors:

If the file and native realms were not configured, they were implicitly disabled if any other realm was configured.
If no other realm was available because realms were either not configured, not permitted by license, or explicitly disabled, the file and native realms were enabled, even if explicitly disabled.
Impact
To explicitly disable the file or native realm, set the respective file.<realm-name>.enabled or native.<realm-name>.enabled setting to false under the xpack.security.authc.realms namespace in elasticsearch.yml.

The following configuration example disables the native realm and the file realm.

xpack.security.authc.realms:

  native.realm1.enabled: false
  file.realm2.enabled: false

  ...
"""

rules['.*xpack.security.authc.realms.*'] = """
The realm order setting is now required.
Details
The xpack.security.authc.realms.{type}.{name}.order setting is now required and must be specified for each explicitly configured realm. Each value must be unique.

Impact
The cluster will fail to start if the requirements are not met.

For example, the following configuration is invalid:

xpack.security.authc.realms.kerberos.kerb1:
  keytab.path: es.keytab
  remove_realm_name: false
And must be configured as:

xpack.security.authc.realms.kerberos.kerb1:
  order: 0
  keytab.path: es.keytab
  remove_realm_name: false

"""

rules['.*cluster.routing.allocation.disk.include_relocations.*'] = """
cluster.routing.allocation.disk.include_relocations has been removed.
Details
Elasticsearch now always accounts for the sizes of relocating shards when making allocation decisions based on the disk usage of the nodes in the cluster. In earlier versions, you could disable this by setting cluster.routing.allocation.disk.include_relocations to false. That could result in poor allocation decisions that could overshoot watermarks and require significant extra work to correct. The cluster.routing.allocation.disk.include_relocations setting has been removed.

Impact
Remove the cluster.routing.allocation.disk.include_relocations setting. Specifying this setting in elasticsearch.yml will result in an error on startup.
"""

rules['.*cluster.join.timeout.*'] = """
cluster.join.timeout has been removed.
Details
The cluster.join.timeout setting has been removed. Join attempts no longer time out.

Impact
Remove cluster.join.timeout from elasticsearch.yml.
"""

rules['.*discovery.zen.*'] = """
discovery.zen settings have been removed.
Details
All settings under the discovery.zen namespace are no longer supported. They existed only only for BWC reasons in 7.x. This includes:

discovery.zen.minimum_master_nodes
discovery.zen.no_master_block
discovery.zen.hosts_provider
discovery.zen.publish_timeout
discovery.zen.commit_timeout
discovery.zen.publish_diff.enable
discovery.zen.ping.unicast.concurrent_connects
discovery.zen.ping.unicast.hosts.resolve_timeout
discovery.zen.ping.unicast.hosts
discovery.zen.ping_timeout
discovery.zen.unsafe_rolling_upgrades_enabled
discovery.zen.fd.connect_on_network_disconnect
discovery.zen.fd.ping_interval
discovery.zen.fd.ping_timeout
discovery.zen.fd.ping_retries
discovery.zen.fd.register_connection_listener
discovery.zen.join_retry_attempts
discovery.zen.join_retry_delay
discovery.zen.join_timeout
discovery.zen.max_pings_from_another_master
discovery.zen.send_leave_request
discovery.zen.master_election.wait_for_joins_timeout
discovery.zen.master_election.ignore_non_master_pings
discovery.zen.publish.max_pending_cluster_states
discovery.zen.bwc_ping_timeout
Impact
Remove the discovery.zen settings from elasticsearch.yml. Specifying these settings will result in an error on startup.
"""

rules['.*http.content_type.required.*'] = """
http.content_type.required has been removed.
Details
The http.content_type.required setting was deprecated in Elasticsearch 6.0 and has been removed in Elasticsearch 8.0. The setting was introduced in Elasticsearch 5.3 to prepare users for Elasticsearch 6.0, where content type auto detection was removed for HTTP requests.

Impact
Remove the http.content_type.required setting from elasticsearch.yml. Specifying this setting will result in an error on startup.
"""

rules['.*http.tcp_no_delay.*'] = """
http.tcp_no_delay has been removed.
Details
The http.tcp_no_delay setting was deprecated in 7.x and has been removed in 8.0. Use`http.tcp.no_delay` instead.

Impact
Replace the http.tcp_no_delay setting with http.tcp.no_delay. Specifying http.tcp_no_delay in elasticsearch.yml will result in an error on startup.
"""

rules['.*network.tcp.connect_timeout.*'] = """
network.tcp.connect_timeout has been removed.
Details
The network.tcp.connect_timeout setting was deprecated in 7.x and has been removed in 8.0. This setting was a fallback setting for transport.connect_timeout.

Impact
Remove the`network.tcp.connect_timeout` setting. Use the transport.connect_timeout setting to change the default connection timeout for client connections. Specifying network.tcp.connect_timeout in elasticsearch.yml will result in an error on startup.
"""

rules['.*node.max_local_storage_nodes.*'] = """
node.max_local_storage_nodes has been removed.
Details
The node.max_local_storage_nodes setting was deprecated in 7.x and has been removed in 8.0. Nodes should be run on separate data paths to ensure that each node is consistently assigned to the same data path.

Impact
Remove the node.max_local_storage_nodes setting. Specifying this setting in elasticsearch.yml will result in an error on startup.
"""

rules['.*accept_default_password.*'] = """
The accept_default_password setting has been removed.
Details
The xpack.security.authc.accept_default_password setting has not had any affect since the 6.0 release of Elasticsearch and is no longer allowed.

Impact
Remove the xpack.security.authc.accept_default_password setting from elasticsearch.yml. Specifying this setting will result in an error on startup.
"""

rules['.*roles.index.cache.*'] = """
The roles.index.cache.* settings have been removed.
Details
The xpack.security.authz.store.roles.index.cache.max_size and xpack.security.authz.store.roles.index.cache.ttl settings have been removed. These settings have been redundant and deprecated since the 5.2 release of Elasticsearch.

Impact
Remove the xpack.security.authz.store.roles.index.cache.max_size and xpack.security.authz.store.roles.index.cache.ttl settings from elasticsearch.yml . Specifying these settings will result in an error on startup.
"""

rules['.*transport.profiles.*.xpack.security.type.*'] = """
The transport.profiles.*.xpack.security.type setting has been removed.
Details
The transport.profiles.*.xpack.security.type setting is no longer supported. The Transport Client has been removed and all client traffic now uses the HTTP transport. Transport profiles using this setting should be removed.

Impact
Remove the transport.profiles.*.xpack.security.type setting from elasticsearch.yml. Specifying this setting in a transport profile will result in an error on startup.
"""

rules['.*nameid_format.*'] = """
The nameid_format SAML realm setting no longer has a default value.
Details
In SAML, Identity Providers (IdPs) can either be explicitly configured to release a NameID with a specific format, or configured to attempt to conform with the requirements of a Service Provider (SP). The SP declares its requirements in the NameIDPolicy element of a SAML Authentication Request. In Elasticsearch, the nameid_format SAML realm setting controls the NameIDPolicy value.

Previously, the default value for nameid_format was urn:oasis:names:tc:SAML:2.0:nameid-format:transient. This setting created authentication requests that required the IdP to release NameID with a transient format.

The default value has been removed, which means that Elasticsearch will create SAML Authentication Requests by default that don’t put this requirement on the IdP. If you want to retain the previous behavior, set nameid_format to urn:oasis:names:tc:SAML:2.0:nameid-format:transient.

Impact
If you currently don’t configure nameid_format explicitly, it’s possible that your IdP will reject authentication requests from Elasticsearch because the requests do not specify a NameID format (and your IdP is configured to expect one). This mismatch can result in a broken SAML configuration. If you’re unsure whether your IdP is explicitly configured to use a certain NameID format and you want to retain current behavior , try setting nameid_format to urn:oasis:names:tc:SAML:2.0:nameid-format:transient explicitly.
"""

rules['.*xpack.security.transport.ssl.enabled.*'] = """
The xpack.security.transport.ssl.enabled setting is now required to configure xpack.security.transport.ssl settings.
Details
It is now an error to configure any SSL settings for xpack.security.transport.ssl without also configuring xpack.security.transport.ssl.enabled.

Impact
If using other xpack.security.transport.ssl settings, you must explicitly specify the xpack.security.transport.ssl.enabled setting.

If you do not want to enable SSL and are currently using other xpack.security.transport.ssl settings, do one of the following:

Explicitly specify xpack.security.transport.ssl.enabled as false
Discontinue use of other xpack.security.transport.ssl settings
If you want to enable SSL, follow the instructions in Encrypting communications between nodes in a cluster. As part of this configuration, explicitly specify xpack.security.transport.ssl.enabled as true.

For example, the following configuration is invalid:

xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: elastic-certificates.p12
And must be configured as:

xpack.security.transport.ssl.enabled: true 
xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: elastic-certificates.p12

or false.
"""

rules['.*xpack.security.transport.ssl.enabled.*'] = """
A xpack.security.transport.ssl certificate and key are now required to enable SSL for the transport interface.
Details
It is now an error to enable SSL for the transport interface without also configuring a certificate and key through use of the xpack.security.transport.ssl.keystore.path setting or the xpack.security.transport.ssl.certificate and xpack.security.transport.ssl.key settings.

Impact
If xpack.security.transport.ssl.enabled is set to true, provide a certificate and key using the xpack.security.transport.ssl.keystore.path setting or the xpack.security.transport.ssl.certificate and xpack.security.transport.ssl.key settings. If a certificate and key is not provided, Elasticsearch will return in an error on startup.
"""

rules['.*elasticsearch.username:kibana.*'] = """
The kibana user has been replaced by kibana_system.
Details
The kibana user was historically used to authenticate Kibana to Elasticsearch. The name of this user was confusing, and was often mistakenly used to login to Kibana. This has been renamed to kibana_system in order to reduce confusion, and to better align with other built-in system accounts.

Impact
Replace any use of the kibana user with the kibana_system user. Specifying the kibana user in kibana.yml will result in an error on startup.

If your kibana.yml used to contain:

elasticsearch.username: kibana
then you should update to use the new kibana_system user instead:

elasticsearch.username: kibana_system
The new kibana_system user does not preserve the previous kibana user password. You must explicitly set a password for the kibana_system user.
"""


rules['.*search.remote.*'] = """
The search.remote.* settings have been removed.
Details
In 6.5 these settings were deprecated in favor of cluster.remote. In 7.x we provided automatic upgrading of these settings to their cluster.remote counterparts. In 8.0.0, these settings have been removed. Elasticsearch will refuse to start if you have these settings in your configuration or cluster state.

Impact
Use the replacement cluster.remote settings. Discontinue use of the search.remote.* settings. Specifying these settings in elasticsearch.yml will result in an error on startup.
"""

rules['.*pidfile.*'] = """
The pidfile setting has been replaced by node.pidfile.
Details
To ensure that all settings are in a proper namespace, the pidfile setting was previously deprecated in version 7.4.0 of Elasticsearch, and is removed in version 8.0.0. Instead, use node.pidfile.

Impact
Use the node.pidfile setting. Discontinue use of the pidfile setting. Specifying the pidfile setting in elasticsearch.yml will result in an error on startup.
"""

rules['.*processors.*'] = """
The processors setting has been replaced by node.processors.
Details
To ensure that all settings are in a proper namespace, the processors setting was previously deprecated in version 7.4.0 of Elasticsearch, and is removed in version 8.0.0. Instead, use node.processors.

Impact
Use the node.processors setting. Discontinue use of the processors setting. Specifying the processors setting in elasticsearch.yml will result in an error on startup.
"""

rules['.*node.processors.*'] = """
The node.processors setting can no longer exceed the available number of processors.
Details
Previously it was possible to set the number of processors used to set the default sizes for the thread pools to be more than the number of available processors. As this leads to more context switches and more threads but without an increase in the number of physical CPUs on which to schedule these additional threads, the node.processors setting is now bounded by the number of available processors.

Impact
If specified, ensure the value of node.processors setting does not exceed the number of available processors. Setting the node.processors value greater than the number of available processors in elasticsearch.yml will result in an error on startup.
"""

rules['.*cluster.remote.connect.*'] = """
The cluster.remote.connect setting has been removed.
Details
In Elasticsearch 7.7.0, the setting cluster.remote.connect was deprecated in favor of setting node.remote_cluster_client. In Elasticsearch 8.0.0, the setting cluster.remote.connect is removed.

Impact
Use the node.remote_cluster_client setting. Discontinue use of the cluster.remote.connect setting. Specifying the cluster.remote.connect setting in elasticsearch.yml will result in an error on startup.
"""

rules['.*node.local_storage.*'] = """
The node.local_storage setting has been removed.
Details
In Elasticsearch 7.8.0, the setting node.local_storage was deprecated and beginning in Elasticsearch 8.0.0 all nodes will require local storage. Therefore, the node.local_storage setting has been removed.

Impact
Discontinue use of the node.local_storage setting. Specifying this setting in elasticsearch.yml will result in an error on startup.
"""

rules['.*auth.password.*'] = """
The auth.password setting for HTTP monitoring has been removed.
Details
In Elasticsearch 7.7.0, the setting xpack.monitoring.exporters.<exporterName>.auth.password was deprecated in favor of setting xpack.monitoring.exporters.<exporterName>.auth.secure_password. In Elasticsearch 8.0.0, the setting xpack.monitoring.exporters.<exporterName>.auth.password is removed.

Impact
Use the xpack.monitoring.exporters.<exporterName>.auth.secure_password setting. Discontinue use of the xpack.monitoring.exporters.<exporterName>.auth.password setting. Specifying the xpack.monitoring.exporters.<exporterName>.auth.password setting in elasticsearch.yml will result in an error on startup.
"""

rules['.*(xpack.enrich.enabled|xpack.flattened.enabled|xpack.ilm.enabled|xpack.monitoring.enabled|xpack.rollup.enabled|xpack.slm.enabled|xpack.sql.enabled|xpack.transform.enabled|xpack.vectors.enabled).*'] = """
Settings used to disable basic license features have been removed.
Details
The following settings were deprecated in Elasticsearch 7.8.0 and have been removed in Elasticsearch 8.0.0:

xpack.enrich.enabled
xpack.flattened.enabled
xpack.ilm.enabled
xpack.monitoring.enabled
xpack.rollup.enabled
xpack.slm.enabled
xpack.sql.enabled
xpack.transform.enabled
xpack.vectors.enabled
These basic license features are now always enabled.

If you have disabled ILM so that you can use another tool to manage Watcher indices, the newly introduced xpack.watcher.use_ilm_index_management setting may be set to false.

Impact
Discontinue use of the removed settings. Specifying these settings in elasticsearch.yml will result in an error on startup.
"""

rules['.*(gateway.expected_nodes|gateway.expected_master_nodes|gateway.recover_after_nodes|gateway.recover_after_master_nodes).*'] ="""
Settings used to defer cluster recovery pending a certain number of master nodes have been removed.
Details
The following cluster settings have been removed:

gateway.expected_nodes
gateway.expected_master_nodes
gateway.recover_after_nodes
gateway.recover_after_master_nodes
It is safe to recover the cluster as soon as a majority of master-eligible nodes have joined so there is no benefit in waiting for any additional master-eligible nodes to start.

Impact
Discontinue use of the removed settings. If needed, use gateway.expected_data_nodes or gateway.recover_after_data_nodes to defer cluster recovery pending a certain number of data nodes.
"""

rules['.*(node.data|node.ingest|node.master|node.ml|node.remote_cluster_client|node.transform|node.voting_only).*'] = """
Legacy role settings have been removed.
Details
The legacy role settings:

node.data
node.ingest
node.master
node.ml
node.remote_cluster_client
node.transform
node.voting_only
have been removed. Instead, use the node.roles setting. If you were previously using the legacy role settings on a 7.13 or later cluster, you will have a deprecation log message on each of your nodes indicating the exact replacement value for node.roles.

Impact
Discontinue use of the removed settings. Specifying these settings in elasticsearch.yml will result in an error on startup.
"""

rules['.*bootstrap.system_call_filter.*'] = """
The system call filter setting has been removed.
Details
Elasticsearch uses system call filters to remove its ability to fork another process. This is useful to mitigate remote code exploits. These system call filters are enabled by default, and were previously controlled via the setting bootstrap.system_call_filter. Starting in Elasticsearch 8.0, system call filters will be required. As such, the setting bootstrap.system_call_filter was deprecated in Elasticsearch 7.13.0, and is removed as of Elasticsearch 8.0.0.

Impact
Discontinue use of the removed setting. Specifying this setting in Elasticsearch configuration will result in an error on startup.
"""

rules['.*._tier.*'] = """
Tier filtering settings have been removed.
Details
The cluster and index level settings ending in ._tier used for filtering the allocation of a shard to a particular set of nodes have been removed. Instead, the tier preference setting, index.routing.allocation.include._tier_preference should be used. The removed settings are:

Cluster level settings:

cluster.routing.allocation.include._tier
cluster.routing.allocation.exclude._tier
cluster.routing.allocation.require._tier
Index settings:

index.routing.allocation.include._tier
index.routing.allocation.exclude._tier
index.routing.allocation.require._tier
Impact
Discontinue use of the removed settings. Specifying any of these cluster settings in Elasticsearch configuration will result in an error on startup. Any indices using these settings will have the settings archived (and they will have no effect) when the index metadata is loaded.
"""

rules['.*path.data.*'] = """
Shared data path and per index data path settings are deprecated.
Details
Elasticsearch uses the shared data path as the base path of per index data paths. This feature was previously used with shared replicas. Starting in 7.13.0, these settings are deprecated. Starting in 8.0 only existing indices created in 7.x will be capable of using the shared data path and per index data path settings.

Impact
Discontinue use of the deprecated settings.
"""

rules['.*cluster.routing.allocation.disk.watermark.enable_for_single_data_node.*'] = """
The single data node watermark setting is deprecated and now only accepts true.
Details
In 7.14, setting cluster.routing.allocation.disk.watermark.enable_for_single_data_node to false was deprecated. Starting in 8.0, the only legal value will be true. In a future release, the setting will be removed completely, with same behavior as if the setting was true.

If the old behavior is desired for a single data node cluster, disk based allocation can be disabled by setting cluster.routing.allocation.disk.threshold_enabled: false

Impact
Discontinue use of the deprecated setting.
"""

rules['.*cluster.routing.allocation.disk.watermark.enable_for_single_data_node.*'] = """
The gateway.auto_import_dangling_indices setting has been removed.
Details
The gateway.auto_import_dangling_indices cluster setting has been removed. Previously, you could use this setting to automatically import dangling indices. However, automatically importing dangling indices is unsafe. Use the dangling indices APIs to manage and import dangling indices instead.

Impact
Discontinue use of the removed setting. Specifying the setting in elasticsearch.yml will result in an error on startup.
"""

rules['.*listener.*'] = """
The listener thread pool has been removed.
Details
Previously, the transport client used the thread pool to ensure listeners aren’t called back on network threads. The transport client has been removed in 8.0, and the thread pool is no longer needed.

Impact
Remove listener thread pool settings from elasticsearch.yml for any nodes. Specifying listener thread pool settings in elasticsearch.yml will result in an error on startup.
"""

rules['.*fixed_auto_queue_size.*'] = """
The fixed_auto_queue_size thread pool type has been removed.
Details
The fixed_auto_queue_size thread pool type, previously marked as an experimental feature, was deprecated in 7.x and has been removed in 8.0. The search and search_throttled thread pools have the fixed type now.

Impact
No action needed.
"""

rules['.*(transport.tcp.port|transport.tcp.compress|transport.tcp.connect_timeout|transport.tcp_no_delay|transport.profiles.profile_name.tcp_no_delay|transport.profiles.profile_name.tcp_keep_alive|transport.profiles.profile_name.reuse_address|transport.profiles.profile_name.send_buffer_size|transport.profiles.profile_name.receive_buffer_size).*'] = """
Several transport settings have been replaced.
Details
The following settings have been deprecated in 7.x and removed in 8.0. Each setting has a replacement setting that was introduced in 6.7.

transport.tcp.port replaced by transport.port
transport.tcp.compress replaced by transport.compress
transport.tcp.connect_timeout replaced by transport.connect_timeout
transport.tcp_no_delay replaced by transport.tcp.no_delay
transport.profiles.profile_name.tcp_no_delay replaced by transport.profiles.profile_name.tcp.no_delay
transport.profiles.profile_name.tcp_keep_alive replaced by transport.profiles.profile_name.tcp.keep_alive
transport.profiles.profile_name.reuse_address replaced by transport.profiles.profile_name.tcp.reuse_address
transport.profiles.profile_name.send_buffer_size replaced by transport.profiles.profile_name.tcp.send_buffer_size
transport.profiles.profile_name.receive_buffer_size replaced by transport.profiles.profile_name.tcp.receive_buffer_size
Impact
Use the replacement settings. Discontinue use of the removed settings. Specifying the removed settings in elasticsearch.yml will result in an error on startup.
"""

rules['.*transport.compress.*'] = """
Selective transport compression has been enabled by default.
Details
Prior to 8.0, transport compression was disabled by default. Starting in 8.0, transport.compress defaults to indexing_data. This configuration means that the propagation of raw indexing data will be compressed between nodes.

Impact
Inter-node transit will get reduced along the indexing path. In some scenarios, CPU usage could increase.
"""

rules['.*transport.compression_scheme.*'] = """
Transport compression defaults to lz4.
Details
Prior to 8.0, the transport.compression_scheme setting defaulted to deflate. Starting in 8.0, transport.compress_scheme defaults to lz4.

Prior to 8.0, the cluster.remote.<cluster_alias>.transport.compression_scheme setting defaulted to deflate when cluster.remote.<cluster_alias>.transport.compress was explicitly configured. Starting in 8.0, cluster.remote.<cluster_alias>.transport.compression_scheme will fallback to transport.compression_scheme by default.

Impact
This configuration means that transport compression will produce somewhat lower compression ratios in exchange for lower CPU load.
"""

rules['.*repositories.fs.compress.*'] = """
The repositories.fs.compress node-level setting has been removed.
Details
For shared file system repositories ("type": "fs"), the node level setting repositories.fs.compress could previously be used to enable compression for all shared file system repositories where compress was not specified. The repositories.fs.compress setting has been removed.

Impact
Discontinue use of the repositories.fs.compress node-level setting. Use the repository-specific compress setting to enable compression instead. Refer to Shared file system repository settings.
"""

rules['.*xpack.security.fips_mode.enabled.*'] = """
When FIPS mode is enabled the default password hash is now PBKDF2_STRETCH
Details
If xpack.security.fips_mode.enabled is true (see FIPS 140-2), the value of xpack.security.authc.password_hashing.algorithm now defaults to pbkdf2_stretch.

In earlier versions this setting would always default to bcrypt and a runtime check would prevent a node from starting unless the value was explicitly set to a "pbkdf2" variant.

There is no change for clusters that do not enable FIPS 140 mode.

Impact
This change should not have any impact on upgraded nodes. Any node with an explicitly configured value for the password hashing algorithm will continue to use that configured value. Any node that did not have an explicitly configured password hashing algorithm in Elasticsearch 6.x or Elasticsearch 7.x would have failed to start.
"""


rules['.*xpack.monitoring.history.duration.*'] = """
The xpack.monitoring.history.duration will not delete indices created by metricbeat or elastic agent
Details

Prior to 8.0, Elasticsearch would internally handle removal of all monitoring indices according to the xpack.monitoring.history.duration setting.

When using metricbeat or elastic agent >= 8.0 to collect monitoring data, indices are managed via an ILM policy. If the setting is present, the policy will be created using the xpack.monitoring.history.duration as an initial retention period.

If you need to customize retention settings for monitoring data collected with metricbeat, please update the .monitoring-8-ilm-policy ILM policy directly.

The xpack.monitoring.history.duration setting will only apply to monitoring indices written using (legacy) internal collection, not indices created by metricbeat or agent.

Impact
After upgrading, insure that the .monitoring-8-ilm-policy ILM policy aligns with your desired retention settings.

If you only use metricbeat or agent to collect monitoring data, you can also remove any custom xpack.monitoring.history.duration settings.
"""

#=============================================


rules['.*IndexLifecycle.*'] = """
The indexlifecycle package has been renamed ilm in the Java High Level REST Client.
Details
In the high level REST client, the indexlifecycle package has been renamed to ilm to match the package rename inside the Elasticsearch code.

Impact
Update your workflow and applications to use the ilm package in place of indexlifecycle.
"""


rules['.*fuzziness.*'] = """
Changes to Fuzziness.
Details
To create Fuzziness instances, use the fromString and fromEdits method instead of the build method that used to accept both Strings and numeric values. Several fuzziness setters on query builders (e.g. MatchQueryBuilder#fuzziness) now accept only a `Fuzziness`instance instead of an Object.

Fuzziness used to be lenient when it comes to parsing arbitrary numeric values while silently truncating them to one of the three allowed edit distances 0, 1 or 2. This leniency is now removed and the class will throw errors when trying to construct an instance with another value (e.g. floats like 1.3 used to get accepted but truncated to 1).

Impact
Use the available constants (e.g. Fuzziness.ONE, Fuzziness.AUTO) or build your own instance using the above mentioned factory methods. Use only allowed Fuzziness values.
"""


rules['.*es.disk.auto_release_flood_stage_block.*'] = """
es.disk.auto_release_flood_stage_block has been removed.
Details
If a node exceeds the flood-stage disk watermark then we add a block to all of its indices to prevent further writes as a last-ditch attempt to prevent the node completely exhausting its disk space. By default, from 7.4 onwards the block is automatically removed when a node drops below the high watermark again, but this behaviour could be disabled by setting the system property es.disk.auto_release_flood_stage_block to false. This behaviour is no longer optional, and this system property must now not be set.

Impact
Discontinue use of the es.disk.auto_release_flood_stage_block system property. Setting this system property will result in an error on startup.
"""



rules['.*JodaCompatibleZonedDateTime.*'] = """
The JodaCompatibleZonedDateTime class has been removed.
Details
As a transition from Joda datetime to Java datetime, scripting used an intermediate class called JodaCompatibleZonedDateTime. This class has been removed and is replaced by ZonedDateTime. Any use of casting to a JodaCompatibleZonedDateTime or use of method calls only available in JodaCompatibleZonedDateTime in a script will result in a compilation error, and may not allow the upgraded node to start.

Impact
Before upgrading, replace getDayOfWeek with getDayOfWeekEnum().value in any scripts. Any use of getDayOfWeek expecting a return value of int will result in a compilation error or runtime error and may not allow the upgraded node to start.

The following JodaCompatibleZonedDateTime methods must be replaced using ZonedDateTime methods prior to upgrade:

getMillis() → toInstant().toEpochMilli()
getCenturyOfEra() → get(ChronoField.YEAR_OF_ERA) / 100
getEra() → get(ChronoField.ERA)
getHourOfDay() → getHour()
getMillisOfDay() → get(ChronoField.MILLI_OF_DAY)
getMillisOfSecond() → get(ChronoField.MILLI_OF_SECOND)
getMinuteOfDay() → get(ChronoField.MINUTE_OF_DAY)
getMinuteOfHour() → getMinute()
getMonthOfYear() → getMonthValue()
getSecondOfDay() → get(ChronoField.SECOND_OF_DAY)
getSecondOfMinute() → getSecond()
getWeekOfWeekyear() → get(IsoFields.WEEK_OF_WEEK_BASED_YEAR)
getWeekyear() → get(IsoFields.WEEK_BASED_YEAR)
getYearOfCentury() → get(ChronoField.YEAR_OF_ERA) % 100
getYearOfEra() → get(ChronoField.YEAR_OF_ERA)
toString(String) → a DateTimeFormatter
toString(String, Locale) → a DateTimeFormatter
"""


rules['.*(scheme=|.*host=|port=).*'] = """
Previously the client would use scheme="http", host="localhost", and port=9200 defaults when specifying which node(s) to connect to. Starting in 8.0 these defaults have been removed and instead require explicit configuration of scheme, host, and port or to be configured using cloud_id to avoid confusion about which Elasticsearch instance is being connected to.

This choice was made because starting 8.0.0 Elasticsearch enables HTTPS is by default, so it’s no longer a good assumption that http://localhost:9200 is the locally running cluster.
https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/migration.html#migration-strict-client-config
"""

rules['.*\(.*=.*\).*'] = """
APIs used to support both positional and keyword arguments, however using keyword-only arguments was always recommended in the documentation. Starting in 7.14 using positional arguments would raise a DeprecationWarning but would still work.

Now starting in 8.0 keyword-only arguments are now required for APIs for better forwards-compatibility with new API options. When attempting to use positional arguments a TypeError will be raised.

# 8.0+ SUPPORTED USAGE:
client.indices.get(index="*")

# 7.x UNSUPPORTED USAGE (Don't do this!):
client.indices.get("*")
"""

rules['.*(scheme=|.*host=|port=).*'] = """
Previously the client would use scheme="http", host="localhost", and port=9200 defaults when specifying which node(s) to connect to. Starting in 8.0 these defaults have been removed and instead require explicit configuration of scheme, host, and port or to be configured using cloud_id to avoid confusion about which Elasticsearch instance is being connected to.

This choice was made because starting 8.0.0 Elasticsearch enables HTTPS is by default, so it’s no longer a good assumption that http://localhost:9200 is the locally running cluster.
https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/migration.html#migration-strict-client-config
"""


rules['.*headers.*api_key.*http_auth.*opaque_id.*request_timeout.*ignore.*'] = """
Previously some per-request options like api_key and ignore were allowed within client API methods. Starting in 8.0 this is deprecated for all APIs and for a small number of APIs may break in unexpected ways if not changed.

The parameters headers, api_key, http_auth, opaque_id, request_timeout, and ignore are effected:

from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200")

# 8.0+ SUPPORTED USAGE:
client.options(api_key=("id", "api_key")).search(index="blogs")

# 7.x DEPRECATED USAGE (Don't do this!):
client.search(index="blogs", api_key=("id", "api_key"))
"""

rules['.*(ignore_status|http_auth).*'] = """
Previously the client would use scheme="http", host="localhost", and port=9200 defaults when specifying which node(s) to connect to. Starting in 8.0 these defaults have been removed and instead require explicit configuration of scheme, host, and port or to be configured using cloud_id to avoid confusion about which Elasticsearch instance is being connected to.

This choice was made because starting 8.0.0 Elasticsearch enables HTTPS is by default, so it’s no longer a good assumption that http://localhost:9200 is the locally running cluster.
https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/migration.html#migration-strict-client-config
"""


rules['.*(sql.query.*request_timeout|security.grant_api_key.*api_key|render_search_template.*params|search_template.*params).*'] = """
APIs where this change is breaking and doesn’t have a deprecation period due to conflicts between the client API and Elasticsearch’s API:

sql.query using request_timeout
security.grant_api_key using api_key
render_search_template using params
search_template using params
You should immediately evaluate the usage of these parameters and start using .options(...) to avoid unexpected behavior. Below is an example of migrating away from using per-request api_key with the security.grant_api_key API:

# 8.0+ SUPPORTED USAGES:
resp = (
    client.options(
        # This is the API key being used for the request
        api_key=("request-id", "request-api-key")
    ).security.grant_api_key(
        # This is the API key being granted
        api_key={
            "name": "granted-api-key"
        },
        grant_type="password",
        username="elastic",
        password="changeme"
    )
)

# 7.x DEPRECATED USAGES (Don't do this!):
resp = (
    # This is the API key being used for the request
    client.security.grant_api_key(
        api_key=("request-id", "request-api-key"),
        # This is the API key being granted
        body={
            "api_key": {
                "name": "granted-api-key"
            },
            "grant_type": "password",
            "username": "elastic",
            "password": "changeme"
        }
    )
)
"""





