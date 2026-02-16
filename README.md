# Full-Stack Short test

This test will evaluate your front-end and back-end skills.

It will take at least 4 hours but no more than 6 to complete the test.

## Requirements

* You need to install docker desktop and Sign Up [Download Docker](https://www.docker.com/products/docker-desktop)


## Structure of the repository

```
.
├── Readme.md                           # Readme
├── back-end                            # Contain the back-end stack in various languages to create the api
│    ├── golang                         # stack in golang (Framework Gin)
│    ├── php                            # stack in PHP 7 (Framework Slim)
│    ├── python                         # stack in Python (Framework Flask/SqlAlchemy)
│    └── Readme.md                      # Back-End Readme
│
├── data                                # The data
│    ├── postman                        # Postman file (collection)
│    │      └── collection.json         # The postman collection of the back-end api
│    ├── mockup.png                     # Mockup of the UI to create
│    └── mpd.png                        # Structure of the database
│
├── database                            # The database in MySQL
│    ├── Readme.md                      # The readme explain how to run/stop/update the database
│    └── sql                            # Script to created the database, add fixtures,...
└── front-end                           # Stack of the Front-End (React.js)
```


## Back-End (BE) Tasks

Develop the following tasks in the language you prefer (PHP, Goland or Python). A stack is available for each of these languages in the folder `back-end`.


* TASK 1: As a user, I want to list all the vehicle model by vehicle make (Ex. Acura) to be able to define the row header of the grid
  - Implement a new endpoint to do this action

* TASK 2: As a user, I want to list all the vehicle years available to be able to define the column header of the grid
  - Implement a new endpoint to do this action

* TASK 3: As a user, I want to get the list of vehicle to be able to fill up the grid with the proper colors.
  - Implement a new endpoint to do this action

Example of response: (List of the years available by model for the make "Acura")
```json 
 {
  "coverage": {
    "ILX": [2017, 2016, 2015, 2014],
    "MDX": [2017, 2016, 2015, 2014],
    "RDX": [2011, 2010],
    "RLX": [2012, 2011, 2010],
    "TL": [2014, 2013, 2012, 2011, 2010],
    "TLX": [2016, 2015, 2014, 2013],
    "TSX": [2017, 2015]
  }
}
```
Note: You are free to structure the response as needed. The 3 first tasks can become only one if it's easier for the display of the front-end part.

* TASK 4: As a user, I want to be able to remove a vehicle from the coverage (model/year)
  - Update the database migration script `database/sql/update_database.sql` add a column `state` in all the tables existing. This column can take 2 values 0/1. (0 means the entry has been turn off)
  - Update the database migration script `database/sql/update_database.sql` add a column `updated` in all the tables existing. (This column contain the date and the time when the data has been changed)
  - Implement a new endpoint to do this action

Extra tasks:

* TASK 5: Secure the calls with a JWT token
* TASK 6: Add some Unit Test

## Front-End (FE) Tasks

* A single page "app" that displays years (BE Task #2) and vehicle models (BE Task #1) for the vehicle make __"Acura"__ in a grid format. The data are coming from an API that you will develop (Back-End Tasks).
* A grid with the contents of `years` and `vehicle-models` (as in the mockup below).

![Database structure](./data/mockup.png "Page Mockup")

* Set the corresponding box to be blue if the entry for that vehicle model and year exists. And grey if it doesn't exist. (An api call will be necessary BE Task #3)
* When clicking on a vehicle-model/year box, it is toggled and the visual displays the new state. (An api call will be necessary to be able to update the state in the database, BE Task #4)

### Example

Once the list of vehicles are loaded into the grid (BE Task #3)

- The years for the RLX are `"coverage":{"RLX":[2012,2011,2010]}`
- After clicking on the 2013 column next to RLX: `"coverage":{"RLX":[2013,2012,2011,2010]}`
- The visual should now show a blue box for the year 2013 next to RLX.
- Clicking on the 2010 column next to RLX:
  `"coverage":{"RLX":[2013,2012,2011]}`
- The visual should now show a grey box for the year 2010 next to RLX.


## How to submit your work?

Submit your work preferably on a github account else zip the source and send it by email.

## Evaluation

This will be evaluated on the compliance to the supplied visual (mockup.png), and the code quality.

You will have the opportunity to justify your decisions during the interview.

## How to start your Dev environment?

You need to start:

* the database
* the back-end
* the front-end

### Start the database

Check the [Readme](./database/README.md)  in the database folder

### Start the back-end

The process will depend on the language you choose for developing the back-end:

* In PHP check the [Readme](./back-end/php/README.md) in the back-end/php folder
* In Python check the [Readme](./back-end/python/README.md) in the back-end/python folder
* In Golang check the [Readme](./back-end/golang/README.md) in the back-end/golang folder

### Start the front-end

Check the [Readme](./front-end/README.md)  in the front-end folder


# Vehicle Coverage API – Implementation Overview

## Architecture

The application is built using:

* **Python / Flask**
* **3-layer architecture pattern**:

  * **API Layer** → Handles HTTP requests and JWT protection
  * **Service Layer** → Contains business logic
  * **Repository Layer** → Handles database access via SQLAlchemy
* **SQLAlchemy ORM**

---

# Task 1 — List Vehicle Models by Make

### Endpoint

```
GET /vehicle-makes/<make_id>/models
```

### Description

Returns the list of vehicle models associated with a given vehicle make.

### Behavior

* Receives a `make_id` as a URL parameter (e.g., `1` for the make_name `Acura`  )
* Returns a list of models containing:

  * `id`
  * `name`
* Filters only:

  * Active vehicle makes (`state == 1`)
  * Active vehicle models (`state == 1`)

### Files Involved

* `vehicle.py`

  * API
  * Service
  * Repository
* `entities.py`

---

# Task 2 — List All Available Vehicle Years

### Endpoint

```
GET /vehicle-years
```

### Description

Returns the distinct list of all vehicle years available in the `vehicle` table.

### Behavior

* Returns only distinct years
* Sorted in **descending order**
* Filters only active vehicles (`state == 1`)

### Files Involved

* `vehicle.py`

  * API
  * Service
  * Repository

---

# Task 3 — Get Coverage Grid (Model/Year) by Make

### Endpoint

```
GET /vehicle-makes/<make_id>/coverage
```

### Description

Returns the coverage matrix (model/year grid) for a given vehicle make.

### Response Format

```json
{
  "ModelName1": [2020, 2021, 2022],
  "ModelName2": [2019, 2020]
}
```

### Purpose

Allows the frontend to render a coverage grid:

* 🟦 Blue cells → vehicle exists
* ⬜ Grey cells → vehicle does not exist

### Behavior

* Filters only active vehicles (`state == 1`)

### Files Involved

* `vehicle.py`

  * API
  * Service
  * Repository

---

# Task 4 — Toggle Vehicle Coverage (Activate / Deactivate)

### Endpoint

```
POST /vehicle-makes/<make_id>/coverage/toggle
```

### Request Body

```json
{
  "vehicle_model_id": <int>,
  "vehicle_year": <int>
}
```

### Behavior

* If the vehicle exists:

  * Toggle its `state` (0 → 1 or 1 → 0)
  * Update the `updated` timestamp
* If the vehicle does not exist:

  * Create it with:

    * `state = 1`
    * `updated = current datetime`

---

## Database Migration

File: `update_database.sql`

Adds the following columns to:

* `vehicle_make`
* `vehicle_model`
* `vehicle`

### New Columns

```sql
state TINYINT DEFAULT 1
updated DATETIME
```

---

## SQLAlchemy Models Update

The following fields were added to all three entities in `entities.py`:

* `state` → Integer (default = 1)
* `updated` → DateTime



