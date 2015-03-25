from flask import Flask
from flask import render_template, redirect#jsonify
app = Flask(__name__)
from operator import itemgetter
from distutils.version import LooseVersion
import plistlib
import os

#set this to the base of your munki repo:
repo_base = '/Users/Shared/repo/'
# ad override the catalog to parse below:
catalog_to_parse = 'all'

# yup, stolen whole-heartedly from http://stackoverflow.com/a/22878816/743638
def get_key_watcher():
    keys_seen = set()
    def key_not_seen(unfiltered_prod_dict):
        key = unfiltered_prod_dict['distinct_name']
        if key in keys_seen:
            return False  # key is not new
        else:
            keys_seen.add(key)
            return True  # key seen for the first time
    return key_not_seen

try:
    products = plistlib.readPlist(os.path.join(repo_base, 'catalogs/all'))
    prodlist = []
    for prod_dict in products:
        if not prod_dict.get('installer_type') == 'apple_update_metadata':
            if not prod_dict.get('installer_type') == 'nopkg':
                joined_path = os.path.join(repo_base,'icons', prod_dict.get('name')) + '.png'
                this_prod_dict = {}
                try_keys = [('Name', 'display_name'), ('distinct_name', 'name')]
                for item in try_keys:
                    try:
                        this_prod_dict[item[0]] = prod_dict.get(item[1])
                    except Exception:
                        this_prod_dict[item[0]] = 'No %s found' % item[0]
                try:
                    this_prod_dict['version'] = LooseVersion(prod_dict.get('version'))
                except Exception:
                    this_prod_dict['description'] = 'No description found'
                try:
                    this_prod_dict['description'] = (prod_dict.get('description'))[:130] + '...'
                except Exception:
                    this_prod_dict['description'] = 'No description found'
                try:
                    this_prod_dict['link'] = (os.path.join('static/pkgs', prod_dict.get('installer_item_location'))).replace(' ', '%20')
                except Exception:
                    this_prod_dict['link'] = 'No link!'

                if prod_dict.get('installer_type') == 'profile':
                    this_prod_dict['icon_url'] = 'static/mobileconfig.png'
                elif prod_dict.get('icon_name'):
                    this_prod_dict['icon_url'] = (os.path.join('static/icons/', prod_dict.get('icon_name'))).replace(' ', '%20')
                elif os.path.exists(joined_path):
                    this_prod_dict['icon_url'] = (os.path.join('static/icons', prod_dict.get('name') + '.png')).replace(' ', '%20')
                else:
                    this_prod_dict['icon_url'] = 'static/package.png'
                prodlist.append(this_prod_dict)
    listbyvers = sorted(prodlist, key=itemgetter('version'), reverse=True)
    filtered = filter(get_key_watcher(), listbyvers)
    sprodlist = sorted(filtered, key=itemgetter('Name'))

except Exception, e:
    print e

@app.route('/')
def index():
    return render_template('moscargo.html', example_prods=sprodlist)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
