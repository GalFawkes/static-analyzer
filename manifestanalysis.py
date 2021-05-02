from bs4 import BeautifulSoup as bs
import yaml

'''
# decompile apk (APKTool)
- get smali files
- analyze manifest
 - Filters for services
 '''


def meta_constructor(loader, node):
    '''
    function to make yaml play nice
    '''
    value = loader.construct_mapping(node)
    return value


def analyze_permissions(soup: bs) -> list:
    '''
    Analyzes a soup file to locate app permissions
    '''
    permissions = []
    manifests = soup.find_all('manifest')  # Should be one, catching edge cases
    for manifest in manifests:
        for permission in manifest.find_all('uses-permission'):
            permissions.append(permission.get('android:name'))
    return permissions


def analyze_intents(soup: bs) -> list:
    intents = []
    manifests = soup.find_all('manifest')  # should only be one manifest
    for manifest in manifests:
        for intent_filter in manifest.find_all('intent-filter'):
            for action in intent_filter.find_all('action'):
                intents.append(action.get('android:name'))
    return intents


def analyze_services(soup: bs) -> list:
    services = []
    # manifests = soup.find_all('manifest')  # should only be one manifest
    # for manifest in manifests:
#         for permission in manifest.find_all('uses-permission'):
#             permissions.append(permission.get('android:name'))
    return services


def analyze_receivers(soup: bs) -> list:
    receivers = []
    manifests = soup.find_all('manifest')  # just in case there's >1 manifest
    for manifest in manifests:
        for receiver in manifest.find_all('receiver'):
            receivers.append(receiver.get('android:name'))
    return receivers


def analysis(path: str) -> dict:
    '''
    takes filepath and does analysis.
    '''
    dict = {}
    filepath = f'{path}/AndroidManifest.xml'
    apkt_yaml = f'{path}/apktool.yml'
    with open(filepath, encoding='utf-8') as manifest:  # using UTF-8 encoding
        soup = bs(manifest, "lxml")
        manifest = {
            'permissions': analyze_permissions(soup),
            'intents': analyze_intents(soup),
            'services': analyze_services(soup),
            'receivers': analyze_receivers(soup)
        }
        dict['manifest'] = manifest
    with open(apkt_yaml, encoding='utf-8') as apktool_info:
        yaml.add_constructor(u'tag:yaml.org,2002:brut.androlib.meta.MetaInfo',
                             meta_constructor)
        apkinfo = yaml.load(apktool_info, Loader=yaml.FullLoader)
        dict['sdkInfo'] = apkinfo['sdkInfo']
    return dict