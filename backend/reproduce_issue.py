import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_fetch_institution_sports():
    print("Testing fetching institution sports...")
    
    # 1. Try to access organizer/sports without auth
    print("\n1. Testing /organizer/sports without auth (Expected 401/403)")
    try:
        response = requests.get(f"{BASE_URL}/organizer/sports")
        print(f"Status: {response.status_code}")
        if response.status_code in [401, 403]:
            print("SUCCESS: blocked as expected")
        else:
            print("FAILURE: expected block, got access")
    except Exception as e:
        print(f"Error: {e}")

    # 2. Try to access a hypothetical public endpoint
    print("\n2. Testing /institutions/1/sports (Expected 404 as it is likely missing)")
    try:
        response = requests.get(f"{BASE_URL}/institutions/1/sports")
        print(f"Status: {response.status_code}")
        if response.status_code == 404:
            print("SUCCESS: Endpoint missing as suspected")
        else:
            print("FAILURE: Endpoint exists?")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fetch_institution_sports()
