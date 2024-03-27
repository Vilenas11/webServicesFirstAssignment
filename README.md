# webServicesFirstAssignment
## Steps to set it up:
1. git clone https://github.com/Vilenas11/webServicesFirstAssignment.git
2. docker build -t autoimage .
3. docker run -p 5000:5000 autoimage


## [CLICK HERE FOR POSTMAN LINK](https://documenter.getpostman.com/view/33877517/2sA35D74jP#326993ab-b765-4e53-852a-d900f976bb35)

## Current functionality: 

### CREATE
```
http://localhost:5000/create/store 
```

### READ:
```
http://localhost:5000/ 
```
#### pvz: http://localhost:5000/ -X GET
```
http://localhost:5000/all 
```
#### pvz: http://localhost:5000/all -X GET
```
http://localhost:5000/show/store/<<int:id>>
```
#### pvz: http://localhost:5000/show/store/2 -X GET

### UPDATE
```
http://localhost:5000/update/<<int:id>>
```
#### curl http://localhost:5000/update/<1> -d '"owner": "Updated Owner Name",
    "listOfShops": [
        {
            "partId": 2345,
            "name": "Updated Part Name",
            "manufacturer": "Updated Manufacturer",
            "carBrand": "Updated Car Brand",
            "category": "Updated Category"
        },
        {
            "partId": 4555,
            "name": "Updated Part Name 2",
            "manufacturer": "Updated Manufacturer 2",
            "carBrand": "Updated Car Brand 2",
            "category": "Updated Category 2"
        }
    ]' -H "Content-Type: application/json" -X PUT

### DELETE
```
http://localhost:5000/delete/store/<<int:id>>
```
#### curl http://localhost:5000/delete/store/3 -X DELETE
```
http://localhost:5000/deleteAll
```
#### curl http://localhost:5000/deleteAll -X DELETE
