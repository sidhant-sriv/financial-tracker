# FJ-BE-R2-sidhant-srivastava-VIT

### Apps and Endpoints

1. User Authentication - user
    /api/user/register (POST)
    /api/user/profile (GET, PUT)
    /api/token (POST)
    /api/users/<int> (Admin only) (GET, PUT, DELETE)

2. Income 
    /api/income/ (GET, POST)    
    /api/income/<int> (GET, PUT, DELETE)

3. Expense
    /api/expense/ (GET, POST)    
    /api/expense/<int> (GET, PUT, DELETE)
    /api/expense/export-csv (GET)

4. Category
    /api/category/ (GET, POST)    
    /api/category/<int> (GET, PUT, DELETE)

5. Investment

6. Report

TODO:
- [x] Change depth of nested serializers 