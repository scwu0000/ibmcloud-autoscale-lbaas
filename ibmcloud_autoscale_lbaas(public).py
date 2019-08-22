#!/usr/bin/env python
# coding: utf-8

# In[1]:


import SoftLayer


# In[2]:


USERNAME = 'XXX'
API_KEY = 'XXXXX'


# In[3]:


###API Test, please ignore
# Declare the API client
client = SoftLayer.Client(username=USERNAME, api_key=API_KEY)
accountService = client['Account']

# Declaring the object mask to get information about the billing item.
objectMask1 = "mask[id, hostname, domain, datacenter[longName], billingItem[recurringFee]]"

try:
    # Retrieve the bare metal servers for the account.
    result1 = accountService.getHardware(mask=objectMask1)
    print(result1)
except SoftLayer.SoftLayerAPIError as e:
    print("Unable to retrieve the servers. " % (e.faultCode, e.faultString))
    exit(1)


# In[5]:


###retrieve Data Center name
client = SoftLayer.Client(username=USERNAME, api_key=API_KEY)
accountService = client['SoftLayer_Network_LBaaS_LoadBalancer']
# objectMask1 = "mask[address, name, operatingStatus, provisioningStatus, uuid, datacenter[longName]]"
objectMask2 = "mask[address, name, operatingStatus, provisioningStatus, uuid, datacenter[name]]"
try:
    # Retrieve the bare metal servers for the account.
    result2 = accountService.getAllObjects(mask=objectMask2)
    print(result2)
    for a in result2:
        dc = a['datacenter']['name']
        print(dc)
except SoftLayer.SoftLayerAPIError as e:
    print("Unable to retrieve the servers. " % (e.faultCode, e.faultString))
    exit(1)


# In[6]:


###retrieve uuid of LBaaS
client = SoftLayer.Client(username=USERNAME, api_key=API_KEY)
accountService = client['SoftLayer_Network_LBaaS_LoadBalancer']
objectMask3 = "mask[uuid]"
#objectMask1 = "mask[address, name, operatingStatus, provisioningStatus, datacenter[longName]]"
try:
    # Retrieve the bare metal servers for the account.
    # result = accountService.getLoadBalancer('d6ea0f93-4c57-48c5-9569-f8be37597f75')
    result3 = accountService.getAllObjects(mask=objectMask3)
    print(result3)
    for i in result3:
        uuid = i['uuid']
    print(uuid)
except SoftLayer.SoftLayerAPIError as e:
    print("Unable to retrieve the servers. " % (e.faultCode, e.faultString))
    exit(1)


# In[7]:


###retrieve uuid of LBaaS's members
client = SoftLayer.Client(username=USERNAME, api_key=API_KEY)
accountService = client['SoftLayer_Network_LBaaS_LoadBalancer']
#objectMask1 = "mask[address, name, operatingStatus, provisioningStatus, datacenter[longName]]"
try:
    # Retrieve the bare metal servers for the account.
    # result = accountService.getLoadBalancerMemberHealth('d6ea0f93-4c57-48c5-9569-f8be37597f75')
    result4 = accountService.getLoadBalancerMemberHealth(uuid)
    print(result4)
    for a in result4:
        members1 = a['membersHealth']
        print(members1)
        count1=0
        for b in members1:
            indi = b['uuid']
            print(indi)
            count1 = count1 + 1
        print(count1)
except SoftLayer.SoftLayerAPIError as e:
    print("Unable to retrieve the servers. " % (e.faultCode, e.faultString))
    exit(1)


# In[19]:


from prettytable import PrettyTable

def convertToMB(value):    
    """quick math"""
    return "{0:.2f}".format(float(value)/(10**6))

# Retrieve the listeners in LBaaS using masks
mask = "mask[members,listeners[defaultPool]]"
lbaas = client['Network_LBaaS_LoadBalancer'].getLoadBalancer(uuid, mask=mask)
listeners = lbaas['listeners']
statusTable = PrettyTable(['Instances Up','Instances Down'])
metricsTable = PrettyTable(['Throughput (bps)','Data Processed (MB)', 'Conection Rate (cps)', 'Active Connections'])
healthTable = PrettyTable(['Front-End Protocol','Front-End Port', 'Back-End Protocol', 'Back-End Port', 'Is Healthy'])

members = client['Network_LBaaS_LoadBalancer'].getLoadBalancerMemberHealth('d6ea0f93-4c57-48c5-9569-f8be37597f75')
statics = client['Network_LBaaS_LoadBalancer'].getLoadBalancerStatistics('d6ea0f93-4c57-48c5-9569-f8be37597f75')
statusTable.add_row([statics['numberOfMembersUp'], statics['numberOfMembersDown']])
metricsTable.add_row([statics['throughput'], convertToMB(statics['dataProcessedByMonth']), statics['connectionRate'], statics['totalConnections']])
print(statics)


if members:
    for listener in listeners:
        for member in members:
            if listener['defaultPool']['uuid'] == member['poolUuid']:
                healthy = all(m['status'] == "UP" for m in member['membersHealth'])
    

healthTable.add_row([listener['protocol'], listener['protocolPort'], listener['defaultPool']['protocol'], listener['defaultPool']['protocolPort'], healthy])

print (statusTable)
print (metricsTable)
print (healthTable)


# In[29]:


guestFilter = {"virtualGuests":{"datacenter":{"name":{"operation": dc}}}}
# hardwareFilter = {"hardware":{"datacenter":{"name":{"operation": dc}}}}
mask = "mask[id,fullyQualifiedDomainName,primaryBackendIpAddress]"
try:
    guests1 = client['Account'].getVirtualGuests(filter=guestFilter, mask=mask)
    # servers = client['Account'].getHardware(filter=hardwareFilter, mask=mask)
    print(guests1)
    count2=0
    for d in guests1:
        guests2 = d['primaryBackendIpAddress']
        print(guests2)
        count2 = count2 + 1
    print(count2)
except SoftLayer.SoftLayerAPIError as e:
    print("Unable to retrieve the servers. " % (e.faultCode, e.faultString))
    exit(1)


# In[31]:


instancesTable = PrettyTable(['Id','Name','Type','Private Ip'])
for g in guests1:
    instancesTable.add_row([g['id'], g['fullyQualifiedDomainName'], "Virtual Server", g['primaryBackendIpAddress']])
    
print(instancesTable)


# In[32]:


mask = "mask[members]"
try:
    result4 = client['Network_LBaaS_LoadBalancer'].getLoadBalancer(uuid, mask=mask)
    print(result4)
    result5 = result4['members']
    print(result5)
    lbcount2=0
    for a in result5:
        result6 = a['address']
        result7 = a['uuid']
        print(result6)
        print(result7)
        lbcount2 = lbcount2 + 1
    print(lbcount2)
except SoftLayer.SoftLayerAPIError as e:
    print("Unable to retrieve the servers. " % (e.faultCode, e.faultString))
    exit(1)


# In[33]:


import json
client = SoftLayer.Client(username=USERNAME, api_key=API_KEY)
#scaleGroupService = client['SoftLayer_Scale_Group']
accountService = client['SoftLayer_Account']
objectMask = "mask[id, name, status[name, keyName], regionalGroup[id, name, description]]"
#result = scaleGroupService.getObject()
try:
    scaleGroups = []
    result = accountService.getScaleGroups(mask=objectMask)
    for item in result:
        scaleGroup = {}
        scaleGroup['id'] = item['id']
        scaleGroup['name'] = item['name']
        scaleGroup['status'] = item['status']['name']
        scaleGroup['region'] = item['regionalGroup']['name']
        scaleGroups.append(scaleGroup)
    print(json.dumps(scaleGroups, sort_keys=True, indent=2, separators=(',', ': ')))
except SoftLayer.SoftLayerAPIError as e:
    print("Unable to get the scale groups. faultCode=%s, faultString=%s" % (e.faultCode, e.faultString))
autoscale_id = item['id']
print(autoscale_id)


# In[34]:


import SoftLayer
import json



scaleGroupId = autoscale_id

objectMaskMember = "mask[datacenter,scaleMember]"
objectFilterMember = {"virtualGuests": {"scaleMember": {"scaleGroupId": {"operation": scaleGroupId}}}}

#objectFilterAssets = {"virtualGuests": {"scaleAssets": {"scaleGroupId": {"operation": scaleGroupId}}}}
#objectMaskAssets = "mask[datacenter,scaleAssets]"

try:
    items = accountService.getVirtualGuests(mask=objectMaskMember, filter=objectFilterMember)
    #print(items)
    members = []
    for item in items:
        member = {}
        member['deviceName'] = item['fullyQualifiedDomainName']
        member['location'] = item['datacenter']['longName']
        member['publicIp'] = item['primaryIpAddress']
        member['privateIp'] = item['primaryBackendIpAddress']
        member['startDate'] = item['createDate']
        members.append(member)
    #items = accountService.getVirtualGuests(mask=objectMaskAssets, filter=objectFilterAssets)
    #assets = []
    #for item in items:
    #    asset = {}
    #    asset['deviceName'] = item['fullyQualifiedDomainName']
    #    asset['location'] = item['datacenter']['longName']
    #    asset['publicIp'] = item['primaryIpAddress']
    #    asset['privateIp'] = item['primaryBackendIpAddress']
    #    asset['startDate'] = item['createDate']
    #    assets.append(asset)
    config = {}
    config['members'] = members
    # config['assets'] = assets
    result = config['members']
    print(result)
    ascount3=0
    for e in result:
        result1 = e['privateIp']
        print(result1)
        ascount3 = ascount3 + 1
    print(ascount3)
    # print(json.dumps(config, sort_keys=True, indent=2, separators=(',', ': ')))
except SoftLayer.SoftLayerAPIError as e:
    print("Unable to get the scale group details. faultCode=%s, faultString=%s" % (e.faultCode, e.faultString))


# In[35]:


client = SoftLayer.Client(username=USERNAME, api_key=API_KEY)
mask = "mask[members]"

scaleGroupId = autoscale_id

objectMaskMember = "mask[datacenter,scaleMember]"
objectFilterMember = {"virtualGuests": {"scaleMember": {"scaleGroupId": {"operation": scaleGroupId}}}}

if ascount3 < lbcount2:
# add ip to LB
    print('lbcount2:'+str(lbcount2))
    try:
        lbresult10 = client['Network_LBaaS_LoadBalancer'].getLoadBalancer(uuid, mask=mask)
        #print(lbresult10)
        lbresult11 = lbresult10['members']
        #print(lbresult11)
        asitems = accountService.getVirtualGuests(mask=objectMaskMember, filter=objectFilterMember)
        #print(asitems)
        for a in lbresult11: 
            for b in asitems:
                asresult14 = b['primaryBackendIpAddress']
                #print('asresult14'+ str(asresult14))
                lbresult13 = a['address']
                #print('lbresult13'+ str(lbresult13))
                if a['address'] != b['primaryBackendIpAddress']:
                    lbresult12 = [a['uuid']]
                    lbresult13 = a['address']
                    #print(lbresult12)
                    #print(lbresult13)            
                    lbaasMemberService = client['Network_LBaaS_Member']
                    response = lbaasMemberService.deleteLoadBalancerMembers(uuid, lbresult12)
                    print(response)
    except SoftLayer.SoftLayerAPIError as e:
        print("Unable to retrieve the servers. " % (e.faultCode, e.faultString))
        exit(1)


# In[36]:


if ascount3 > lbcount2:
#remove ip from LB
    print('ascount3:'+str(ascount3))
    try:
        lbresult10 = client['Network_LBaaS_LoadBalancer'].getLoadBalancer(uuid, mask=mask)
        #print(lbresult10)
        lbresult11 = lbresult10['members']
        #print(lbresult11)
        asitems = accountService.getVirtualGuests(mask=objectMaskMember, filter=objectFilterMember)
        #print(asitems)
        for b in asitems:
            asresult14 = b['primaryBackendIpAddress']
            #print(asresult14)
            for a in lbresult11:
                if b['primaryBackendIpAddress'] != a['address']:
                    lbresult12 = a['uuid']
                    lbresult13 = a['address']
                    #print(lbresult12)
                    #print(lbresult13)            
                    serverInstances = [{ "privateIpAddress": b['primaryBackendIpAddress'], "weight": 50 }]
                    #print(serverInstances)
                    lbaasMemberService = client['Network_LBaaS_Member']
                    response = lbaasMemberService.addLoadBalancerMembers(uuid, serverInstances)
                    #print(response)
    except SoftLayer.SoftLayerAPIError as e:
        print("Unable to retrieve the servers. " % (e.faultCode, e.faultString))
        exit(1)


# In[37]:


if ascount3 == lbcount2:
#nothing to do
    print('ascount3:'+str(ascount3))
    print('lbcount2:'+str(lbcount2))


# In[ ]:




