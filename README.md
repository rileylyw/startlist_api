# Search and Pagination
The `/api/v1/startlists` endpoint will return all the existing startlists.

To move to the next page, simply add `?page=10` to the GET startlist endpoint:

![img_4.png](img_4.png)


# How to add an entry
Send a JSON object with POST request to this endpoint: `/api/v1/startlists/add`.

![img.png](img.png)

The JSON object must follow the following structure, and all the fields are required
```
    {
        "id": "xx",
        "eventId": "xx",
        "raceId": "xx",
        "ticketId": "xx",
        "eventTitle": "xx race",
        "raceTitle": "xx",
        "ticketTitle": "xx Ticket",
        "createdAt": "2022-11-27T01:20:57.371Z",
        "updatedAt": "2023-01-21T11:15:51.236Z",
        "fields": [
            {
                "id": "xx",
                "name": "xx",
                "value": "xx"
            }
        ]
    }
```


# How to delete an entry
Send a DELETE request to this endpoint specifying the id: `/api/v1/startlists/delete/<id>`.

![img_2.png](img_2.png)


# How to search for specific entries
1. Send a GET request to this endpoint with query param: `/api/v1/startlists/search?query=Weekend`.
It will return any matching entries.

![img_1.png](img_1.png)

2. Send a GET request to this endpoint with `id`: `/api/v1/startlists/search/<id>`.

![img_3.png](img_3.png)


# What else could be done
- Unit testing e.g. using `unittest` from Python
- Integration testing e.g. write tests that make requests to the API and assert the results based on json file changes, response codes, and body
- More exceptions for edge cases e.g. when the `id` field is not `UUID`, cannot add entry if certain fields already exist


# Other issues encountered
- The unrealistic data set - it was confusing when I was trying to parse the data since the fields do not make sense, e.g. `id: "dateOfBirth"`
