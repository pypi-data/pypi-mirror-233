import httpx

class users:

    @staticmethod
    def name_by_id(
        id: int
    ):

        url = f"https://users.roblox.com/v1/users/{id}"

        with httpx.Client() as client:
            response = client.get(url)

            if response.status_code == 200:

                user_data = response.json()
                return user_data

            else:

                print(f"Status code: {response.status_code}")
                return


    @staticmethod
    def id_by_name(
        username: str
    ):

        url = "https://users.roblox.com/v1/usernames/users"

        requestPayload = {
        "usernames": [
                username
            ],

            "excludeBannedUsers": True # Whether to include banned users within the request, change this as you wish
        }
        with httpx.Client() as client:
            response = client.post(url, json=requestPayload)

            if response.status_code == 200:

                user_data = response.json()

                return user_data['data'][0]
            else:
                print(f"Status code: {response.status_code}")
                return
