import datetime
import json
import os
import logging
import requests

try:
    os.mkdir('videos')
    os.mkdir(os.path.join('videos', 'copies'))
    os.mkdir('gifs')
    os.mkdir(os.path.join('gifs', 'copies'))
    # with open(f'logs_{datetime.datetime.now().strftime('%Y%m%d%H%M')}', 'w') as f:
    #     pass
except FileExistsError:
    pass

logging.basicConfig(
    level=logging.INFO,
    filename=f'{datetime.datetime.now().strftime('%Y%m%d%H%M')}.log',
    format='%(levelname)s: %(message)s\n'
)
logger = logging.getLogger(__name__)

with open('discord-favorite-gifs.json', 'r') as file:
    data = json.load(file)

i = 0
fails = 0
for y, x in data.items():
    i += 1
    print(i, '/', len(data), sep='')
    try:
        response = requests.get(x['src'])
        if response.status_code == 404:
            fails += 1
            logger.error(f'404 or different error\n{y}')
            continue
        filename = os.path.join(('videos' if x['format'] == 2 else 'gifs'), y.split('/')[-1])
        if os.path.exists(filename):
            num = 1
            filename = os.path.join(('videos' if x['format'] == 2 else 'gifs'), 'copies',
                                    str.join('', (y.split('/')[-1]).split('.')[0:-1]))
            extension = y.split('.')[-1]
            while os.path.exists(filename+str(num)+extension):
                num += 1

            filename = filename + str(num) + extension

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP Error {e}\n{y}')
        fails += 1

    except requests.exceptions.ConnectionError as e:
        logger.error(f'Connection Error {e}\n{y}')
        fails += 1

    except requests.exceptions.Timeout as e:
        logger.error(f'Timeout Error {e}\n{y}')
        fails += 1

    except requests.exceptions.RequestException as e:
        logger.error(f'Request Error {e}\n{y}')
        fails += 1

    except Exception as e:
        logger.error(f'Unknown Error {e}\n{y}')
        fails += 1


print('Done(?)\n'
      'Fails:', fails)
print('\nCheck the links in the logs by sending them in discord. Sometimes the gif may not have been extracted.')