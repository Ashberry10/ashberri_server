Response = []

item = 23,25,6,32,2,23

for x in item:
    result = {

    }
    result.update({"id":x})
    result.update({"name":"Aman"})
    Response.append(result)
    
print("Respose from the server ")
print(Response)