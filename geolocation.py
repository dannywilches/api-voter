import requests

def getGeolocation(address,city):
    address = address.replace(" ","+")
    address = address.replace("#","")
    token_ = "AIzaSyCqCpsFt8HkJrbVrOWcSm0nvHg8bWJ3EEE"
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+","+city+"&key="+token_
    response = requests.get(url)
    print(url)
    # print(response.status_code)
    # print(response.json())
    result_address = response.json()
    array_address = {}
    # print(result_address["results"][0]["geometry"]["location"])
    array_address["address_show"] = result_address["results"][0]["formatted_address"]
    array_address["latitude"] = result_address["results"][0]["geometry"]["location"]["lat"]
    array_address["lenght"] = result_address["results"][0]["geometry"]["location"]["lng"]
    # print(array_address)
    return array_address
