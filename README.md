## Expense sharing service
#### A service to manage expenses between multiple users
#### Provides following methods for splitting expense
* Equal : Divided equally among all the participants
* Exact : Divided based on the exact amount per split
* Percentages : Divided based on the percentage per participant

### Setup
#### 1] Make migrations
```
python manage.py makemigrations
python manage.py migrate
```
#### 2] Run server
```
python manage.py runserver
```

### Api endpoints
### GET
* _api_/_user-details_/user_id/ : returns a json with user's name, email and mobile number
  
* _api_/_user-expenses_/user_id/ : returns all the expenses of the given user
  sample output
  ```
  [
    {
        "id": 1,
        "amount": "3000.00",
        "date": "2024-10-08",
        "split": [
            {
                "user": 1,
                "amount": "1000.00"
            }
        ]
    }
  ]
  ```
* _api_/_overall-expenses_/ : returns expenses of all the users in the database.
  sample output
  ```
  {
    "total_expenses": [
        {
            "id": 1,
            "amount": "3000.00",
            "date": "2024-10-08",
            "split_method": "equal",
            "users": [
                1,
                2,
                3
            ],
            "splits": [
                {
                    "amount": "1000.00"
                },
                {
                    "amount": "1000.00"
                },
                {
                    "amount": "1000.00"
                }
            ]
        }
     ]
  }
* _api_/_download-balance-sheet_/ : returns a csv file with all  user's expenses
  sample output
  ```
  Date,User,Amount
  2024-10-08,Will Smith,1000.00
  2024-10-08,John batman,1000.00
  2024-10-08,Huge Jackman,1000.00
  2024-10-20,Will Smith,1500.00
  2024-10-20,John batman,1500.00
  2024-10-21,Will Smith,100.00
  2024-10-21,John batman,700.00
  2024-10-21,John batman,2500.00
  2024-10-21,Huge Jackman,2500.00
  ```
### POST
* _api_/_create-user_ : create user with name, email and mobile number
  
  ```
  {
    "name":"Huge Jackman",
    "email":"wolverine@xfactor",
    "mobile":"101010101010"
  }
  ```

* _api_/_add-expense_ : generates expense based on the request's details.

  ```
  {
    "amount": 5000,
    "split_method": "percentage",
    "users": [2, 3],
    "split_percentages":[50,50]
  }
  ```
