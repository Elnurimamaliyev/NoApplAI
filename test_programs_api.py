#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

# Login
login_data = urllib.parse.urlencode({
    'username': 'demo@noapplai.com',
    'password': 'Demo123!@#'
}).encode('utf-8')

login_request = urllib.request.Request(
    'http://localhost:8000/api/v1/auth/login',
    data=login_data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)

try:
    with urllib.request.urlopen(login_request) as response:
        login_response = json.loads(response.read().decode('utf-8'))
        token = login_response['access_token']
        print(f"✓ Login successful")
        
        # Get programs
        programs_request = urllib.request.Request(
            'http://localhost:8000/api/v1/programs/',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        with urllib.request.urlopen(programs_request) as programs_response:
            programs = json.loads(programs_response.read().decode('utf-8'))
            print(f"\n✓ Programs API working!")
            print(f"✓ Total programs: {len(programs)}")
            print(f"\nFirst 3 programs:")
            for p in programs[:3]:
                print(f"  - {p['university_name']}: {p['program_name']} ({p['country']})")
            
            # Show sample program structure
            if programs:
                print(f"\nSample program fields:")
                print(json.dumps(programs[0], indent=2, default=str))
                
except urllib.error.HTTPError as e:
    print(f"✗ HTTP Error: {e.code}")
    print(f"Response: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"✗ Error: {e}")
