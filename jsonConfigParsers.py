import json,re,argparse

def convert(input):
    """
    To convert unicode to normal string
    """
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def findAllAAEPwithDomsAssoc(inputJson):
    """
    To find all AAEP and the associated domains, including l3extDomP, physDomP, l2extDomP, vmmDomP

    :param inputJson: parsed json config file
    :return: { aaep: [dom1, dom2 ....]}
    """

    aaepDomDict = {}
    infraInfra = {}
    infraAttEntityPList = []
    for child in inputJson["polUni"]["children"]:
        if u'infraInfra' in child:
            infraInfra = child
    for child in infraInfra[u'infraInfra'][u'children']:
        if u'infraAttEntityP' in child:
            infraAttEntityPList.append(child)
    for infraAttEntityP in infraAttEntityPList:
        aaepName = infraAttEntityP[u'infraAttEntityP'][u'attributes'][u'name'].encode("ascii")
        aaepDomDict[aaepName] = []
        for child in infraAttEntityP[u'infraAttEntityP'][u'children']:
            if u'infraRsDomP' in child:
                try:
                    aaepDomDict[aaepName].append(child[u'infraRsDomP'][u'attributes'][u'tDn']).encode("ascii")
                except AttributeError:
                    pass

    return aaepDomDict

def findAllinfraAccPortGrpwithinfraRsAttEntP(inputJson):
    """
    To find all interface port group and the associated AAEP

    :param inputJson: parsed json config file
    :return: { infraAccPort: infraRsAttEntP}
    """

    infraAccPortGrp_infraRsAttEntP_Dict = {}
    infraInfra = {}
    infraFuncP = {}
    infraAccPortGrpList = []
    for child in inputJson["polUni"]["children"]:
        if u'infraInfra' in child:
            infraInfra = child
    for child in infraInfra[u'infraInfra'][u'children']:
        if u'infraFuncP' in child:
            infraFuncP = child
    for child in infraFuncP[u'infraFuncP'][u'children']:
        if u'infraAccPortGrp' in child:
            infraAccPortGrpList.append(child)
    for infraAccPortGrp in infraAccPortGrpList:
        infraAccPortGrpName = infraAccPortGrp[u'infraAccPortGrp'][u'attributes'][u'name']
        for child in infraAccPortGrp[u'infraAccPortGrp'][u'children']:
            if u'infraRsAttEntP' in child:
                try:
                    infraAccPortGrp_infraRsAttEntP_Dict[infraAccPortGrpName] = child[u'infraRsAttEntP'][u'attributes'][u'tDn']
                except AttributeError:
                    pass

    return infraAccPortGrp_infraRsAttEntP_Dict



def findAllinfraAccPortGrpwithinfraRsL2IfPol(inputJson):
    """
    To find all interface port group and the associated l2 interface policy(port local/ global)

    :param inputJson: parsed json config file
    :return: { infraAccPort: infraRsL2IfPol}
    """

    infraAccPortGrp_infraRsL2IfPol_Dict = {}
    infraInfra = {}
    infraFuncP = {}
    infraAccPortGrpList = []
    for child in inputJson["polUni"]["children"]:
        if u'infraInfra' in child:
            infraInfra = child
    for child in infraInfra[u'infraInfra'][u'children']:
        if u'infraFuncP' in child:
            infraFuncP = child
    for child in infraFuncP[u'infraFuncP'][u'children']:
        if u'infraAccPortGrp' in child:
            infraAccPortGrpList.append(child)
    for infraAccPortGrp in infraAccPortGrpList:
        infraAccPortGrpName = infraAccPortGrp[u'infraAccPortGrp'][u'attributes'][u'name']
        for child in infraAccPortGrp[u'infraAccPortGrp'][u'children']:
            if u'infraRsL2IfPol' in child:
                try:
                    infraAccPortGrp_infraRsL2IfPol_Dict[infraAccPortGrpName] = child[u'infraRsL2IfPol'][u'attributes'][u'tnL2IfPolName']
                except AttributeError:
                    pass

    return infraAccPortGrp_infraRsL2IfPol_Dict



def findAllDomPwithVlanNs(inputJson):
    DomPVlanNsDict = {}
    infraInfra = {}
    DomList = []
    for child in inputJson["polUni"]["children"]:
        domPattern = [u'physDomP',u'l3extDomP',u'vmmDomP',u'l2extDomP']
        if any(pattern in child for pattern in domPattern):#u'physDomP' in child or u'l3extDomP' in child:
            DomList.append(child)
    for Dom in DomList:
        if u'physDomP' in Dom:
            DomName = Dom[u'physDomP'][u'attributes'][u'name']
            DomKey = u'physDomP'
        elif u'l3extDomP' in Dom:
            DomName = Dom[u'l3extDomP'][u'attributes'][u'name']
            DomKey = u'l3extDomP'
        elif u'vmmDomP' in Dom:
            DomName = Dom[u'vmmDomP'][u'attributes'][u'name']
            DomKey = u'vmmDomP'
        elif u'l2extDomP' in Dom:
            DomName = Dom[u'l2extDomP'][u'attributes'][u'name']
            DomKey = u'l2extDomP'


        if u'children' in Dom[DomKey]:
            for child in Dom[DomKey][u'children']:
                if u'infraRsVlanNs' in child:
                    DomPVlanNsDict[DomName] = child[u'infraRsVlanNs'][u'attributes'][u'tDn']

    return DomPVlanNsDict


def findAllfvAEPgwithDomain(inputJson):
    fvTenantList = []
    fvAEPgDomainDict = {}
    for child in inputJson["polUni"]["children"]:
        if u'fvTenant' in child:
            fvTenantList.append(child[u'fvTenant'])
    fvApList=[]
    for tenant in fvTenantList:
        for child in tenant[u'children']:
            if u'fvAp' in child:
                fvApList.append(child)
    fvAEPgList=[]
    for ap in fvApList:
        try:
            for child in ap[u'fvAp'][u'children']:
                if u'fvAEPg' in child:
                    fvAEPgList.append(child)
        except KeyError:
            pass
    epgName = ""

    for fvAEPg in fvAEPgList:
        epgName = fvAEPg[u'fvAEPg'][u'attributes'][u'name']
        fvAEPgDomainDict[epgName] = []
        try:
            for child in fvAEPg[u'fvAEPg'][u'children']:
                if u'fvRsDomAtt' in child:
                    fvAEPgDomainDict[epgName].append(child[u'fvRsDomAtt'][u'attributes'][u'tDn'])

        except KeyError:
            pass
    return fvAEPgDomainDict

parser=argparse.ArgumentParser(description='Generate')
parser.add_argument('--file',dest='file',nargs='+',action='store',default=None,help='inputfile')
args=parser.parse_args()

fvAEPgDomDict = {}
for file in args.file:
    f=open(file,'r')
    rawJson = ""
    for line in f:
        rawJson += line

    parsedJson = json.loads(rawJson)
    parsedJson = convert(parsedJson)
    #aaepDomDict = findAllAAEPwithDomsAssoc(parsedJson)
    #domVlanNsDict = findAllDomPwithVlanNs(parsedJson)
    fvAEPgDomDict.update(findAllfvAEPgwithDomain(parsedJson))
    #aaepDomVlanNs = {}

"""
for aaep,domList in aaepDomDict.iteritems():
    aaepDomVlanNs[aaep] = {}
    for domDn in domList:
        domName = re.search('uni\/(l3dom|l2dom|vmmp-VMware\/dom|phys)-(.*)',domDn).group(2)
        vlanNs = domVlanNsDict[domName]
        aaepDomVlanNs[aaep][domName] = vlanNs


"""
#print(aaepDomVlanNs)
"""
infraAccPortGrp_infraRsAttEntP_dict = findAllinfraAccPortGrpwithinfraRsAttEntP(parsedJson)
infraAccPortGrp_infraRsL2IfPol_dict = findAllinfraAccPortGrpwithinfraRsL2IfPol(parsedJson)
test = {}
for infraAccPortGrp, infraRsAttEntP in infraAccPortGrp_infraRsAttEntP_dict.iteritems():
    test[infraAccPortGrp]={}
    test[infraAccPortGrp]["infraRsAttEntP"]= infraAccPortGrp_infraRsAttEntP_dict[infraAccPortGrp]
    test[infraAccPortGrp]["infraRsL2IfPol"] = infraAccPortGrp_infraRsL2IfPol_dict[infraAccPortGrp]
#print test

test2 = findAllfvAEPgwithDomain(parsedJson)
#print(test2)
"""


"""
for k,v in test2.iteritems():
    if len(v) >1 :
        print str(k) + "    " + str(v)

"""
"""
for k,v in test.iteritems():
    if "LOCAL" in v["infraRsL2IfPol"]:
        print str(k) + "    "+str(v)

"""

"""
fvAEPgHaveTwoMoreDoms = {}
for k,v in fvAEPgDomDict.iteritems():
    if len(v) >= 2:
        fvAEPgHaveTwoMoreDoms[k] = v
print fvAEPgHaveTwoMoreDoms


"""

#print(fvAEPgDomDict)

#print(findAllinfraAccPortGrpwithinfraRsAttEntP(parsedJson))
#print( findAllinfraAccPortGrpwithinfraRsL2IfPol(parsedJson) )