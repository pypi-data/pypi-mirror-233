from elastic_breaking_changes.elastic_breaking_changes import detect_breaking_changes

query = """
GET kibana_sample_data_flights/_search
{
  "aggs": {
    "_term": {
      "terms": {
        "field": "OriginWeather",
        "size": 10,
        "order": {
          "_term": "desc"
        }
      }
    },
    "test":{
      "date_histogram": {
        "field": "timestamp",
        "interval": "month",
        "order": {
          "_time": "asc"
        }
      }
    }
}

"""


detect_breaking_changes(query)