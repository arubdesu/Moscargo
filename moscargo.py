from flask import Flask
from flask import render_template, redirect
app = Flask(__name__)
from operator import itemgetter
import plistlib
import os

#set this to your munki repo's 'all' catalog path
catalog_to_parse = '/Users/Shared/repo/catalogs/all'

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
    products = plistlib.readPlist(catalog_to_parse)
    prodlist = []
    name_vers_dict = {}
    for prod_dict in products:
        if not prod_dict.get('installer_type') == 'apple_update_metadata':
            joined_path = ('static/icons/' + prod_dict.get('name') + '.png')
            this_prod_dict = {
                            'Name': prod_dict.get('display_name'),
                            'distinct_name': prod_dict.get('name'),
                            'description': (prod_dict.get('description'))[:130] + '...',
                            'link': ('static/pkgs/' + prod_dict.get('installer_item_location')).replace(' ', '%20'),
                            'version': prod_dict.get('version'),
                            }
            if prod_dict.get('installer_type') == 'profile':
                this_prod_dict['icon_url'] = 'static/mobileconfig.png'
            elif prod_dict.get('icon_name'):
                this_prod_dict['icon_url'] = os.path.join('static/icons/', prod_dict.get('icon_name'))
            elif os.path.exists(joined_path):
                this_prod_dict['icon_url'] = joined_path.replace(' ', '%20')
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
