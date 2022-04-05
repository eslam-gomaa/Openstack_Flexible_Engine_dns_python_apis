
This is a Python class for the DNS Service of the **Flexible Engine** _Openstack based cloud platform_

<br>

The class contains the common methods that I've personally used, however more methods can be added easily.

---

## Usage

<br>

> Make sure you provide the correct endpoint

1. make an instance of the class
2. start using the methods !


```python
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
```

