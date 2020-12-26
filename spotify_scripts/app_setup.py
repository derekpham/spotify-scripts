"""
Setting up client id and client secret for properties.sqlite
"""

from sqlitedict import SqliteDict
from spotify_scripts import property_constants


def __main__():
    print('Setting up properties.sqlite ...')
    properties = SqliteDict(property_constants.PROPERTY_FILE, autocommit=True)

    properties[property_constants.CLIENT_ID] = input('Enter client ID: ')
    properties[property_constants.CLIENT_SECRET] = input('Enter client secret: ')

    print('Finished setting up properties.sqlite')


if __name__ == '__main__':
    __main__()
