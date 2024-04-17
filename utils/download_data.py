import os
import requests as rq

import utils


def download_data(url: str, target: str) -> bool:
    """
    Download the given URL and save it to a target directory
    :param url: URL to get the data from
    :param target: Target directory where to save the data
    :return: True if the file was successfully downloaded, False otherwise
    """
    try:
        response = rq.get(url, headers={'User-Agent': 'Mozilla/5.0', "Referer": utils.REFERER})
        file_name = url.split('/')[-1].split('?')[0]
        if response.ok:
            file_path = os.path.join(target, file_name)
            print(f"Downloading {file_name}.....")
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"File {file_name} saved to {file_path}")
            return True
        print(f"Failed to download {file_name} from {url}: {response.status_code}")
    except Exception as e:
        print(f"An error occurred downloading {url}: {e}")
    return False
