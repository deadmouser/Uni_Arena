import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_public_access():
    print("Testing public access to institutions...")
    
    # 1. Get Institution Detail
    print("\n1. GET /institutions/1")
    try:
        resp = requests.get(f"{BASE_URL}/institutions/1")
        if resp.status_code == 200:
            print("SUCCESS: Fetched institution")
            print(resp.json())
        else:
            print(f"FAILURE: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

    # 2. Get Institution Sports
    print("\n2. GET /institutions/1/sports")
    try:
        resp = requests.get(f"{BASE_URL}/institutions/1/sports")
        if resp.status_code == 200:
            data = resp.json()
            print(f"SUCCESS: Fetched {len(data)} sports")
            if len(data) > 0:
                print(f"Sample Sport: {data[0]['name']}")
        else:
            print(f"FAILURE: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_public_access()
