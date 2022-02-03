import os

import requests
import json
from dotenv import load_dotenv
from pyutttils import utt_auth
import getopt
import sys

from alive_progress import alive_bar

import urllib3


def main(argv):
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    try:
        requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass

    if not os.getenv("APP_ENV") or os.getenv("APP_ENV") != "prod":
        load_dotenv()

    utt_user = os.getenv("UTT_USER") if os.getenv("UTT_USER") else ""
    utt_password = os.getenv("UTT_PASSWORD") if os.getenv("UTT_PASSWORD") else ""

    if not os.path.exists(os.getenv("IMAGES_FOLDER")):
        os.mkdir(os.getenv("IMAGES_FOLDER"))

    data = {
        "grant_type": "client_credentials",
        "scopes": "public",
        "client_id": os.environ.get("ETUUTT_CLIENT_ID"),
        "client_secret": os.environ.get("ETUUTT_CLIENT_SECRET")
    }
    base_url = "https://etu.utt.fr/api"

    utt_session = utt_auth.cas("https://etu.utt.fr/user/cas", utt_user, utt_password)
    web_access_token = requests.post(base_url + "/oauth/token", data=data)

    if web_access_token.status_code == 200:
        access_token = json.loads(web_access_token.content)["access_token"]
        data = {
            "access_token": access_token,
            "page": 1,
        }
        page = json.loads(requests.get(base_url + "/public/users", params=data).content)
        total_pages = page["pagination"]["totalPages"]
        total_items = page["pagination"]["totalItems"]
        with alive_bar(total_items, title='Importing profile pictures') as bar:
            for j in range(1, total_pages + 1):
                data["page"] = j
                for user in json.loads(requests.get(base_url + "/public/users", params=data).content)["data"]:
                    if user.get("studentId") and user.get("studentId", -1) > 0:
                        bar.text = user.get("fullName")+" - "+str(user["studentId"])
                        photo = utt_session.get(
                            "https://local-sig.utt.fr/Pub/trombi/individu/" + str(user["studentId"]) + ".jpg",
                            verify=False)
                        open(os.getenv("IMAGES_FOLDER") + "/" + str(user["studentId"]) + ".jpg", "wb").write(photo.content)
                    bar()


if __name__ == "__main__":
    main(sys.argv[1:])
