# TFL Data API
JSON API for querying the TFL station dataset

`GET /stations`
```
{
  "stations": [
    {
      "id": "1",
      "name": "River Street , Clerkenwell",
      "terminalName": "001023",
      "lat": 51.52916347,
      "lng": -0.109970527,
      "bikes": 16,
      "empty_docks": 3,
      "total_docks": 19
    }
  ]
}
```

`GET /stations/:id/history`
```
{
  "station": {
    "id": "1",
    "history": [
      {
        "timestamp": "1413493261464",
        "bikes": 16,
        "empty_docks": 3
      },
      {
        "timestamp": "1413493209753",
        "bikes": 10,
        "empty_docks": 9
      }
    ]
  }
}
```
