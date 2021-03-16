import requests

def getGeolocation(address,city):
    address = address.replace(" ","+")
    address = address.replace("#","")
    token_ = "AIzaSyCqCpsFt8HkJrbVrOWcSm0nvHg8bWJ3EEE"
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+","+city+"&key="+token_
    response = requests.get(url)
    result_address = response.json()
    array_address = {}
    array_address["address_show"] = result_address["results"][0]["formatted_address"]
    array_address["latitude"] = result_address["results"][0]["geometry"]["location"]["lat"]
    array_address["lenght"] = result_address["results"][0]["geometry"]["location"]["lng"]
    return array_address
