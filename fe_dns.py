import requests
import json
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class Flexible_Engine_DNS_APIs:
    
    def __init__(self):
        # For endpoints list -> https://docs.prod-cloud-ocb.orange-business.com/en-us/endpoint/index.html
        self.iam_endpoint = 'https://iam.eu-west-0.prod-cloud-ocb.orange-business.com'
        self.dns_endpoint = 'https://dns.prod-cloud-ocb.orange-business.com'
        self.verify_ssl = True
        self.username = '*********'
        self.password = '*********'
        self.domain_name = '*********'
        self.project_name = 'eu-west-0'
        self.token = None
        self.session = requests.Session()


    def authenticate(self):
        """
        Authenticate & get a token that'll be used in furthur requests
        """
        self.session.verify = self.verify_ssl

        data = {
            "auth": {
                "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": self.username,
                        "password": self.password,
                        "domain": {
                            "name": self.domain_name
                        }
                    }
                }
                },
                "scope": {
                    "project": {
                        "name": self.project_name
                    }
                }
            }
        }

        headers = {"Content-Type": "application/json"}
        url = self.iam_endpoint + "/v3/auth/tokens"
        req = self.session.post(url, headers=headers ,json=data)
        if req.status_code == int(201):
            #  response_data = json.loads(req.text)
             self.token = req.headers['X-Subject-Token']
        else:
            print(req.text)
            raise SystemExit(f"ERROR -- Failed Request to {self.iam_endpoint} , {req.status_code} , {req.reason})")


    def list_zones(self, type='public', limit=20, offset=0, tags='', name=None):
        """
        Return a list of zones
        - Can search for a specific zone using tags & name
        https://docs.prod-cloud-ocb.orange-business.com/api/dns/dns_api_62003.html
        """
        # GET /v2/zones?type={type}&limit={limit}&marker={marker}&offset={offset}&tags={tags}&name={name}&status={status}&enterprise_project_id={id}
        if self.token is None:
            self.authenticate()
        url = self.dns_endpoint + f"/v2/zones?type={type}&limit={limit}&offset={offset}"
        if tags:
            url = url + "&tags={tags}"
        if name is not None:
            url = url + f"&name={name}"
            
        headers = {"X-Auth-Token": self.token}
        try:
            req = self.session.get(url, headers=headers)
            if req.status_code == int(200):
                response_data = json.loads(req.text)
                return {'success': True, 'output': response_data, 'fail_reason': ''}
            else:
                return {'success': False, 'output': {}, 'fail_reason': f'Failed Request to {self.iam_endpoint} , {req.status_code} , {req.reason} >> {req.text}'}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'output': {}, 'fail_reason': e}

    def create_record(self, zone_id, name, records, description=None, ttl=3600, record_type="A", tags=None):
        """
        https://docs.prod-cloud-ocb.orange-business.com/api/dns/dns_api_64001.html
        """
        if self.token is None:
            self.authenticate()

        url = self.dns_endpoint + f"/v2/zones/{zone_id}/recordsets"
        headers = {"X-Auth-Token": self.token}

        if description is None:
            description = f"{record_type} record for {name}"

        if tags is None:
            tags = [
                {
                "key": "name",
                "value": name
                }
            ]

        data = {
            "name": name,
            "description": description,
            "type": record_type,
            "ttl": ttl,
            "records": records,
            "tags": tags
        }

        try:
            req = self.session.post(url, headers=headers, json=data)
            if (req.status_code == int(200) or req.status_code == int(202) or req.status_code == int(204)):
                response_data = json.loads(req.text)
                return {'success': True, 'output': response_data, 'fail_reason': ''}
            else:
                return {'success': False, 'output': {}, 'fail_reason': f'Failed Request to {self.iam_endpoint} , {req.status_code} , {req.reason} >> {req.text}'}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'output': {}, 'fail_reason': e}


    def delete_record(self, zone_id, recordset_id):
        """
        https://docs.prod-cloud-ocb.orange-business.com/api/dns/dns_api_64005.html
        """
        if self.token is None:
            self.authenticate()

        url = self.dns_endpoint + f"/v2/zones/{zone_id}/recordsets/{recordset_id}"
        headers = {"X-Auth-Token": self.token}

        try:
            req = self.session.delete(url, headers=headers)
            if (req.status_code == int(200) or req.status_code == int(202) or req.status_code == int(204)):
                response_data = json.loads(req.text)
                return {'success': True, 'output': response_data, 'fail_reason': ''}
            else:
                return {'success': False, 'output': {}, 'fail_reason': f'Failed Request to {self.iam_endpoint} , {req.status_code} , {req.reason} >> {req.text}'}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'output': {}, 'fail_reason': e}


    def list_records_in_zone(self, zone_id, limit=10, offset=0, tags=None, status=None, type=None, name=None, id=None):
        """
        https://docs.prod-cloud-ocb.orange-business.com/api/dns/dns_api_64004.html
        """
        if self.token is None:
            self.authenticate()

        url = self.dns_endpoint + f"/v2/zones/{zone_id}/recordsets?limit={limit}&offset={offset}"
        if tags is not None:
            url = url + f"&tags={tags}"
        if status is not None:
            url = url + f"&status={status}"
        if type is not None:
            url = url + f"&type={type}"
        if name is not None:
            url = url + f"&name={name}"
        if id is not None:
            url = url + f"&id={id}"

        headers = {"X-Auth-Token": self.token}

        try:
            req = self.session.get(url, headers=headers)
            if (req.status_code == int(200) or req.status_code == int(202) or req.status_code == int(204)):
                response_data = json.loads(req.text)
                return {'success': True, 'output': response_data, 'fail_reason': ''}
            else:
                return {'success': False, 'output': {}, 'fail_reason': f'Failed Request to {self.iam_endpoint} , {req.status_code} , {req.reason} >> {req.text}'}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'output': {}, 'fail_reason': e}




        


dns = Flexible_Engine_DNS_APIs()

# List zones
# print(dns.list_zones())


# Search for a zone by name
# print(dns.list_zones(name='your-domain.com.').get('output').get('zones')[0])


# Get zone's ID
zone_id = dns.list_zones(name='your-domain.com.').get('output').get('zones')[0]['id']

# Create A record
print(dns.create_record(zone_id=zone_id, name="love1.your-domain.com.", records=['192.168.1.50']))

# List records in a specific Zone
# print(dns.list_records_in_zone(your-domain_zone_id).get('output').get('recordsets'))

# Get the id of specific Record
record_id = dns.list_records_in_zone(zone_id, name='love1.your-domain.com.').get('output').get('recordsets')[0].get('id')

# print(record_id)

# Delete a record
print(dns.delete_record(zone_id, record_id))


