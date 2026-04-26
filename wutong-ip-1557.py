import argparse
import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        return response.json()['ip']
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

def get_geolocation(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching geolocation data: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="IP工具 - Public IP checker with geolocation")
    parser.add_argument('--help', action='help', help='Show this help message and exit')
    parser.add_argument('--json', action='store_true', help='Output results in JSON format')
    parser.add_argument('--output', type=str, help='File to save the output to')
    
    args = parser.parse_args()
    
    public_ip = get_public_ip()
    if not public_ip:
        return
    
    geolocation = get_geolocation(public_ip)
    if not geolocation:
        return
    
    if args.json:
        result = {
            'public_ip': public_ip,
            **geolocation
        }
        print(result)
    else:
        print(f"Public IP: {public_ip}")
        for key, value in geolocation.items():
            print(f"{key.capitalize()}: {value}")
    
    if args.output:
        with open(args.output, 'w') as f:
            if args.json:
                import json
                json.dump(result, f, indent=4)
            else:
                for line in result.split('\n'):
                    f.write(line + '\n')

if __name__ == "__main__":
    main()