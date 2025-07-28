import requests
def calc(x, y):
    return x + y

request = requests.get("https://www.google.com")


async def main(request):
    response = await request
    return response
    
    




def calc(x,y,**kwargs):
    operator = kwargs.get("operator")
    if  operator == "+":
        a = x + y
    elif operator == "-":
        a = x - y 
    return a
print(calc(1,2,operator="+")) 
