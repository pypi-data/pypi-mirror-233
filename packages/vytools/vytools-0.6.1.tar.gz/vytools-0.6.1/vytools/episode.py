
import vytools.utils
import vytools.compose
import vytools.definition
import vytools.object
import vytools.composerun
from vytools.config import ITEMS
import json, os, copy, io, re, itertools, datetime
import cerberus
PERMUTATION_DELIMITER = '@'
SCHEMA = vytools.utils.BASE_SCHEMA.copy()

INHERIT_ITEMS = {
  'tags':{'type':'list', 'required': False, 'schema': {'type': 'string', 'maxlength':64}},
  'expectation':{'type':'boolean', 'required': False},
}

SCHEMA.update(INHERIT_ITEMS)
SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['episode']},
  'compose':{'type':'string', 'maxlength': 64},
  'returncode':{'type':'integer', 'required':False},
  'object_mods':{'type': 'dict', 'required': False},
  "permutations":{'type': 'dict', 'required': False, 'schema': {
    'labels':{'type': 'dict', 'required': False},
    'groups':{'type': 'list', 'required': False, 'schema':{
      'type':'list', 'schema':{
        'type':'list', 'schema':{
          'type':'string','maxlength':128
        }
      }
    }}
  }},
  'results':{'type': 'dict', 'required': False},
  'passed':{'type':'boolean', 'required': False},
  'anchors':{'type': 'dict', 'required': False, 'keysrules': {'type': 'string', 'regex': vytools.compose.KEYSRULES}},
  'repos':{'type':'list', 'required': False, 'schema':{'type':'string','maxlength':1024}},
  'stage_repos':{'type':'list', 'required': False, 'schema':{'type':'string','maxlength':1024}}
})
VALIDATE = cerberus.Validator(SCHEMA)

class FlatObj:
    def __init__(self, l):
        self._x = l

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, FlatObj):
            return "##<{}>##".format(json.dumps(o._x))
        
def parse(name, pth, items):
  item = {
    'name':name,
    'thingtype':'episode',
    'path':pth,
    'loaded':True
  }
  type_name = 'episode:' + name
  item['depends_on'] = []
  try:
    content = json.load(io.open(pth, 'r', encoding='utf-8-sig'))
    if 'anchors' not in content: content['anchors'] = {}
      
    for sc in SCHEMA:
      if sc in content: # and sc not in ['repos']: TODO I want this sometimes so I took the filter out. Hopefully I don't have to put it back in
        item[sc] = content[sc]

    if vytools.utils._check_add(item['compose'], 'compose', item, items, type_name):
      for anchor_key, anchor_val in content['anchors'].items():
        if anchor_val.startswith('object:'):
          vytools.utils._check_add(anchor_val, 'object', item, items, type_name)
      
      vytools.utils._check_self_dependency(type_name, item)
      # object_mods can come from:
      #  1. the argument passed in here (command-line) 
      #  2. from the episode file "permutations" field
      #  3. from the episode file "object_mods" field
      # The order here is the priority. That is, "permutations" overrides anything in the
      # "object_mods" and the command-line argument overrides both of those. The command-line needs to be deep merged with the results of this function
      # If you save the episode, then the command-line arguments are put into the permutations field
      object_mods_3 = copy.deepcopy(item['object_mods']) if 'object_mods' in item else {}
      permutations = {}
      if 'permutations' in item and 'groups' in item['permutations'] and len(item['permutations']['groups']) > 0:
        for perma in item['permutations']['groups']:
          for permb in list(itertools.product(*perma)):
            suffx = ''
            objp = {}
            for labl in permb:
              suffx += PERMUTATION_DELIMITER+labl
              deepmerge(objp, item['permutations']['labels'][labl])
            permutations[suffx] = copy.deepcopy(object_mods_3)
            deepmerge(permutations[suffx], objp)
      else:
        permutations[''] = object_mods_3

      added = vytools.utils._add_item(item, items, VALIDATE)
      item['__permutations'] = permutations
      return added
    else:
      return False
  except Exception as exc:
    vytools.printer.print_fail('Failed to parse episode "{n}" at "{p}": {e}'.format(n=name, p=pth, e=exc))
    return False

def deepmerge(a, b, path=None): # merge b into a (b prioritized over a)
    if path is None: path = []
    for key in b:
        if key in a and isinstance(a[key], dict) and isinstance(b[key], dict):
          deepmerge(a[key], b[key], path + [str(key)])
        else:
            a[key] = copy.deepcopy(b[key])

def find_all(items, contextpaths=None):
  return vytools.utils.search_all(r'(.+)\.episode\.json', parse, items, contextpaths=contextpaths)

def get_anchors(episode, anchor_dict=None):
  if anchor_dict is None: anchor_dict = {}
  anchors = episode.get('anchors',{})
  anchors.update(anchor_dict)
  return anchors

def build(type_name, built, items=None, anchors=None, compose=None, build_level=0, object_mods=None, eppath=None):
  if items is None: items = ITEMS
  if not vytools.utils.ok_dependency_loading('build', type_name, items):
    return False

  item = items[type_name]
  extracted_anchors = get_anchors(item, anchors)
  rootcompose = compose if compose is not None  else item['compose']
  return vytools.compose.build(rootcompose, items=items, anchors=extracted_anchors, built=built, 
                        build_level=build_level, object_mods=object_mods, eppath=eppath)

def get_episode_id(episode):
  return None if '..' in episode['name'] else episode['name'].lower()

def get_episode(episode_name, items=None):
  if items is None: items = ITEMS
  if episode_name not in items:
    vytools.utils.missing_item(episode_name, items)
    return None
  return items[episode_name]

def get_episode_permutations(episode_name, items=None, jobpath=None):
  ep = get_episode(episode_name, items=items)
  pths = {}
  if ep:
    for suffx in ep['__permutations']:
      epid = get_episode_id(ep)+suffx.lower()
      eppath = vytools.composerun.runpath(epid, jobpath=jobpath)
      artpath = vytools.compose.artifact_paths(ep.get('compose',None), items, eppath=eppath)
      pths[suffx] = {'artifact_paths':artpath, 'episode_path':eppath, 'name':ep['name']+suffx, 'suffix':suffx, 'id':epid, 'object_mods':ep['__permutations'][suffx]}
  return pths

def run(type_name, items=None, anchors=None, clean=False, save=False, object_mods=None, jobpath=None, compose=None, persist=False, permutations=None):
  if items is None: items = ITEMS
  if type_name not in items:
    vytools.utils.missing_item(type_name, items)
    return False
  episode = items[type_name]
  if not vytools.utils.ok_dependency_loading('run', type_name, items):
    return False
  extracted_anchors = get_anchors(episode, anchors)
  
  resultsout = {}
  KEEP = ['repos','stage_repos','returncode','compose','object_mods','anchors']
  for suffix,subep in get_episode_permutations(type_name, items=items, jobpath=jobpath).items():
    if type(permutations) is list and suffix not in permutations: continue
    objmod = copy.deepcopy(subep['object_mods'])
    if object_mods is not None:
      deepmerge(objmod, object_mods)

    eppath = vytools.composerun.runpath(subep['id'], jobpath=jobpath)
    if subep['id'] is None or eppath is None: return False
    rootcompose = episode['compose'] if compose is None else compose
    results = vytools.composerun.run(subep['id'], rootcompose, anchors=extracted_anchors, 
      items=items, clean=clean, object_mods=objmod, jobpath=jobpath, persist=persist,
      dont_track=vytools.utils.get_repo_from_path(episode['path'], items.get('info:repository_path_list',None)))

    for x in INHERIT_ITEMS:
      if results and x in episode: results[x] = episode[x]
    if results and eppath and os.path.exists(eppath):
      results_copy = {k:results[k] for k in KEEP if k in results}
      with open(os.path.join(eppath, subep['name']+'.episode_.json'),'w') as w2:
        w2.write(json.dumps(results_copy, sort_keys=True, indent=2))
    resultsout[subep['name']] = results

  if resultsout and save and 'path' in episode:
    new_episode = {k:episode[k] for k in ['anchors','compose','object_mods','results'] if k in episode}
    if 'results' not in new_episode: new_episode['results'] = {}
    for perm,v in resultsout.items():
      resultsobj = {}
      for k in ['returncode','repos','stage_repos','timestamp']:
        if k in v:
          resultsobj[k] = v[k]
      new_episode['results'][perm] = resultsobj
    perm = {'labels':{},'groups':[]} if 'permutations' not in episode else copy.deepcopy(episode['permutations'])
    if object_mods:
      x = '{date:%Y-%m-%d_%H:%M:%S}'.format( date=datetime.datetime.now() )
      perm['labels'][x] = object_mods
      for g in perm['groups']: g.append([x])

    new_episode['permutations'] = {
      'labels': {k:FlatObj(v) for k,v in perm['labels'].items()},
      'groups': [FlatObj(v) for v in perm['groups']]
    }

    # TODO: what should I do to update the episode object loaded in vytools.ITEMS
    with open(episode['path'],'w') as w2:
      x = json.dumps(new_episode, indent=2, sort_keys=True, cls=CustomJSONEncoder)
      x = x.replace('"##<', "").replace('>##"', "").replace('\\"','"')
      w2.write(x)

  return resultsout

