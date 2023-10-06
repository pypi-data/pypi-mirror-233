import argparse
import requests
from setup import VERSION

MPIP_URL = 'http://127.0.0.1:8000/api'


def download_package(package_name):
    url = f'{MPIP_URL}/packages/{package_name}/download/'  # Replace this with the actual URL
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'{package_name}.mojopkg', 'wb') as f:
            f.write(response.content)
        print(f'{package_name} downloaded successfully.')
    else:
        print(f'Failed to download {package_name}.')


def main():
    parser = argparse.ArgumentParser(description='mpip: A custom package manager.')
    parser.add_argument('command', choices=['get'], help='Command to execute.')
    parser.add_argument('package_name', nargs='?', help='Name of the package.')

    # Add version argument
    parser.add_argument('--version', action='version', version=f'mpip version {VERSION}')

    args = parser.parse_args()

    if args.command == 'get':
        if args.package_name:
            download_package(args.package_name)
        else:
            print('Error: Package name missing.')
    else:
        print('Invalid command. Use "mpip get/save/list package_name".')

if __name__ == '__main__':
    main()














