import requests

if __name__ == '__main__':
    url = f"http://localhost:8080/SmartCityReceiver1/getWorkload"
    print(f"Sending Get Request to {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Response received successfully from server:")
            print("Response ", float(response.text))

        else:
          print(f"Failed to retrieve data from. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data from: {e}")