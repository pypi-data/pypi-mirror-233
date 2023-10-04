import hashlib, yaml, requests, os, copy, re, json
import vytools.utils as utils
import vytools.printer
import vytools.uploads as uploads
from vytools.config import ITEMS
import cerberus
import mimetypes
from pathlib import Path

SCHEMA = utils.BASE_SCHEMA.copy()

phile_schema = {
  'type':'list',
  'schema': {
    'type': 'dict',
    'schema': {
      'path': {'type': 'string', 'maxlength': 1024},
      'name': {'type': 'string', 'maxlength': 128},
      'hash': {'type': 'string', 'maxlength': 32},
      'compose': {'type': 'boolean', 'required': False},
      'publish': {'type': 'boolean'}
    }
  }
}

SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['bundle']},
  'nodule':{
    'type': 'dict',
    'schema': {
      'name': {'type': 'string', 'maxlength': 128, 'required':False},
      'levl':{'type': 'integer', 'allowed': [1, 2, 3, 4], 'required':False},
      'prvt':{'type': 'dict', 'required':False},
      'pblc':{'type': 'dict', 'required':False}
    }
  },
  'cmpse':{'type': 'dict'},
  'bundles': {'type': 'list', 'schema': {'type': 'string'}},
  'philes':phile_schema
})

VALIDATE = cerberus.Validator(SCHEMA)

def cmpsedump(data):
  return yaml.dump(data).encode('utf-8')

def cmpsehash(data):
  md5 = hashlib.md5()
  md5.update(cmpsedump(data))
  return md5.hexdigest()

def fhash(pth):
  md5 = hashlib.md5()
  BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
  try:
    with open(pth, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
  except Exception as exc:
    vytools.printer.print_fail('Failed to get hash for {}: {}'.format(pth,exc))
  return md5.hexdigest()

def parse_philes(pth, phile, publish):
  philespl = phile.split(':')
  if len(philespl) < 2:
    vytools.printer.print_fail('File reference "{p}" should have a : separating the local and container paths'.format(p=phile))
    return None
  d = os.path.dirname(pth)
  path = philespl[0]
  name = philespl[1]
  fpath = os.path.join(d,path)
  if os.path.isfile(fpath):
    return [{'name':name,'hash':fhash(fpath),'path':fpath,'publish':publish}]
  elif os.path.isdir(fpath):
    philes = []
    exclude = set(['.git','.hg','.pycache','node_modules'])
    for root, dirs, files in os.walk(fpath, topdown=True):
      dirs[:] = [d for d in dirs if d not in exclude]
      for file in files:
        if not any([file.endswith(ext) for ext in ['.bundle.yml','.bundle.yaml','.vydir']]):
          p = os.path.join(root, file)
          n = p.replace(fpath,name if name != '/' else '').replace('\\','/') # no forward slashes!
          philes.append({'name':n,'hash':fhash(p),'path':p,'publish':publish})
    return philes
  else:
    vytools.printer.print_fail('No file or directory found at "{p}"'.format(p=fpath))

def parse(name, pth, items):
  item = {
    'name':name,
    'thingtype':'bundle',
    'cmpse':{},
    'nodule':{},
    'philes':[],
    'bundles':[],
    'depends_on':[],
    'path':pth,
    'loaded':True
  }

  try:
    with open(pth,'r') as r:
      content = yaml.safe_load(r.read())
      xvy = content.get('x-vy',{})
      if 'x-vy' in content: del content['x-vy']
      item['nodule'] = xvy.get('nodule',{})
      pblc = xvy.get('public',[])
      if pblc is not None:
        for pblic_phile in pblc:
          philes = parse_philes(pth, pblic_phile, True)
          if philes is None:
            vytools.printer.print_fail('Failed to parse file referenced as "{e}" in bundle "{n}"'.format(n=name, e=pblic_phile))
            return False
          item['philes'] += philes
      if 'public' in xvy: del xvy['public']

      item['bundles'] = xvy.get('bundles',[])
      if 'bundles' in xvy: del xvy['bundles']

      item['cmpse'] = copy.deepcopy(content)
      for servicename,service in item['cmpse'].get('services',{}).items():
        if 'volumes' in service and service['volumes'] is not None:
          volumes = []
          for volume in service.get('volumes',[]):
            if volume.startswith('$JOBPATH/'):
              volumes.append(volume)
            else:
              vol = parse_philes(pth, volume, False)
              if vol is None:
                vytools.printer.print_fail('Failed to parse file referenced as "{e}" in bundle "{n}"'.format(n=name, e=volume))
                return False
              item['philes'] += vol
              volumes += [vv['hash']+':'+vv['name']+':ro' for vv in vol]
          service['volumes'] = volumes
      # print('---------\n', json.dumps(item,indent=2))
      item['philes'].append({'name':'/_.yml','path':'_.yml', 'publish':False, 'hash':cmpsehash(item['cmpse']),'compose':True})

  except Exception as exc:
    vytools.printer.print_fail('Failed to parse bundle "{n}" at "{p}": {e}'.format(n=name, p=pth, e=exc))
    return False

  return utils._add_item(item, items, VALIDATE)

def find_all(items, contextpaths=None):
  success = utils.search_all(r'(.+)\.bundle\.y[a]*ml', parse, items, contextpaths=contextpaths)
  for (type_name, item) in items.items():
    if type_name.startswith('bundle:'):
      (typ, name) = type_name.split(':',1)
      item['depends_on'] = []
      successi = True
      for e in item['bundles']:
        if e.startswith('bundle:') and e in items:
          item['depends_on'].append(e)
        else:
          successi = False
          vytools.printer.print_fail('bundle "{n}" has an unknown reference to {t}'.format(n=name, t=e))
      success &= successi
      item['loaded'] &= successi
      utils._check_self_dependency(type_name, item)
  return success

def onsuccess(item, url, headers, result):
  refresh = result.get('refresh',[])
  success = True
  for hash in refresh:
    for phile in item.get('philes',[]):
      if phile['hash'] == hash:
        headers2 = copy.deepcopy(headers)
        headers2['Content-Type'] = 'application/binary'
        headers2['phile_id'] = refresh[hash]
        headers2['hash'] = hash
        if phile.get('compose',False):
          headers2['mimetype_guess'] = 'application/json'
          res = requests.post(url+'/update_phile', data=cmpsedump(item['cmpse']), headers=headers2).json()
        else:
          headers2['mimetype_guess'],enc = mimetypes.guess_type(phile['path'])
          res = requests.post(url+'/update_phile', data=Path(phile['path']).read_bytes(), headers=headers2).json()

        if not res.get('processed',False):
          success = False
          vytools.printer.print_fail('  - Failed to update phile "{}": {}'.format(phile['path'],res))
        else:
          vytools.printer.print_success('  - Uploaded updated phile "{}"'.format(phile['path']))
        break # there may be multiple phile references to this phile. Only need to update one
  res = requests.post(url+'/clean_philes', json={}, headers=headers)
  return success
  
def upload(lst, url, uname, token, check_first, update_list, items=None):
  if items is None: items = ITEMS
  return uploads.upload('bundle', lst, url, uname, token, check_first, update_list, onsuccess, items=items)

def extract_philes(bundle_name, items=None, visited_bundles=[]):
  if items is None: items = ITEMS
  if not bundle_name or not bundle_name.startswith('bundle:') or bundle_name not in items: return []
  bundle = items[bundle_name]
  philes = {}
  for ph in bundle.get('philes',[]):
    if ph['publish']:
      philes[ph['name']] = ph['path']
  for bu in bundle.get('bundles',[]):
    if bu in visited_bundles: return
    visited_bundles.append(bu)
    philes__ = extract_philes(bu, items, visited_bundles)
    for name,pth in philes__.items(): philes[name] = pth
  return philes

def mimetype(pth):
  extensions_map = {
      '': {'fmt':'binary','mime':'application/octet-stream'},
      '.manifest': {'fmt':'text','mime':'text/cache-manifest'},
      '.html': {'fmt':'text','mime':'text/html'},
      '.png': {'fmt':'binary','mime':'image/png'},
      '.ico': {'fmt':'binary','mime':'image/ico'},
      '.jpg': {'fmt':'binary','mime':'image/jpg'},
      '.svg': {'fmt':'text','mime':'image/svg+xml'},
      '.css': {'fmt':'text','mime':'text/css'},
      '.js': {'fmt':'text','mime':'application/x-javascript'},
      '.wasm': {'fmt':'text','mime':'application/wasm'},
      '.json': {'fmt':'text','mime':'application/json'},
      '.xml': {'fmt':'text','mime':'application/xml'},
  }
  return extensions_map.get('.'+pth.rsplit('.',1)[-1],{})

def rspnse__(self,pth):
    val = mimetype(pth)
    content = bytes(Path(pth).read_text(), "utf8") if val.get('fmt','text')=='text' else Path(pth).read_bytes()
    self.send_response(200)
    self.send_header("Cache-control", 'public, must-revalidate, max-age=300')
    self.send_header("ETag", '"'+fhash(pth)+'"')
    self.send_header("Content-type", val.get('mime','text/html'))
    self.end_headers()
    self.wfile.write(content)

def server(bundle_name, items=None, ip='localhost', port=8080):
  if items is None: items = ITEMS
  if vytools.utils.exists([bundle_name], items):
    import http.server # Our http server handler for http requests
    import socketserver # Establish the TCP Socket connections

    print('The following files will be served insecurely at http://{}:{}'.format(ip,port))
    philes = extract_philes(bundle_name,items)
    for name,pth in philes.items():
      print('  - {} at http://{}:{}{}'.format(pth,ip,port,name))
    input('Press any key to continue')

    class BundleHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
      def do_GET(self):
        if self.path in philes:
          rspnse__(self,philes[self.path])
        else:
          print(' -- Cant find',self.path)
    Handler = BundleHttpRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
      httpd.serve_forever()