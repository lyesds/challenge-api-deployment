## API to get the estimated price of a property in Belgium

Welcome to my first API that will return the predicted price of a property!

Please visit https://lyesapp1.herokuapp.com/ to send your *own* data describing a real estate property (location, number of rooms, area, ...) and receive back an
estimate of its price in euros.

The data sent is processed with a machine learning model (https://github.com/Misterkadrix/challenge-regression) that is trained on real world data coming from Immoweb.com.

Please see below for the input data to submit.

#### Available routes

Two routes are available:
- A route at `/` that accept a GET request and returns "alive" if the server is alive.
- A route at `/predict` that accept:
  - POST request that receives the data of a property in JSON format.
  - GET request returning a short description of the goal and the format.


### Accepted format for the POST resquest

```
{
  "0": {
    "location": int,
    "type": str "APARTMENT" | "HOUSE",
    "area": int,
    "room_number": int,
    "kitchen_equipped": bool 0 | 1,
    "furnished": bool 0 | 1,
    "garden": bool 0 | 1,
    "garden_area": int,
    "terrace": bool 0 | 1,
    "terrace_area": int,
    "facade_count": int 1 | 2 | 3 | 4,
    "swimming_pool": bool 0 | 1,
    "fireplace": bool 0 | 1,
    "land_surface": int,
    "building_condition": "AS_NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO_BE_DONE_UP" | "TO_RESTORE"
  }
}
```
