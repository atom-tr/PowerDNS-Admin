from flask_migrate import Migrate

from .base import db
from .user import User
from .role import Role
from .account import Account
from .account_user import AccountUser
from .server import Server
from .history import History
from .api_key import ApiKey
from .api_key_account import ApiKeyAccount
from .setting import Setting
from .domain import Domain
from .domain_info import DomainInfo
from .domain_setting import DomainSetting
from .domain_user import DomainUser
from .domain_template import DomainTemplate
from .domain_template_record import DomainTemplateRecord
from .record import Record
from .record_entry import RecordEntry
from .url_redirect import URLRecord


def init_app(app):
    db.init_app(app)
    _migrate = Migrate(app, db)  # lgtm [py/unused-local-variable]

import os
from sqlalchemy import true
from sqlalchemy import event

from flask import current_app
from .setting import Setting

NGINX_REDIRECT = """
server {{
      listen 80;
      server_name {};
      return 301 {}$request_uri;
}}
"""

def get_domain_name(domain_id):
    return Domain.query.filter_by(id=domain_id).first().name

@event.listens_for(URLRecord, 'after_insert')   
def create_nginx_config(mapper, connection, target):
    """
    Create a nginx conf in /var/www/html/pdns/powerdnsadmin/nginx.redirect/{domain_name}.conf
    for each URLRecord
    """
    folder = Setting().get('url_redirect_nginx_conf_dir')
    # Check if /var/www/html/pdns/powerdnsadmin/nginx.redirect is exists
    if not os.path.exists(folder):
        current_app.logger.error('{} does not exists'.format(folder))
    # create the conf file
    with open('{}/{}.conf'.format(folder,target._name), 'w') as f:
        f.write(NGINX_REDIRECT.format(target._name, target.url))
        f.close()
    
    # Create A record for this target
    rc = {"rrsets": [{"changetype": "REPLACE", "type": "A", "name": target.name, "ttl": "60", "records": [{"content": Setting().get('url_redirect_ip'), "disabled": False}]}]}
    r = Record(name=target.name,
                type='A',
                status='Active',
                ttl=60,
                data=Setting().get('url_redirect_ip'),
                comment_data=target.comment)
    result = r.add(get_domain_name(target.domain_id), rc)
    if result['status'] != 'ok':
        current_app.logger.error(result)
    
@event.listens_for(URLRecord, 'after_update')
def update_nginx_config(mapper, connection, target):
    """
    Update a nginx conf in folder nginx.redirect/{domain_name}.conf
    for each URLRecord
    """
    # Check if folder nginx.redirect is exists
    folder = Setting().get('url_redirect_nginx_conf_dir')
    if not os.path.exists(folder):
        current_app.logger.error('{} does not exists'.format(folder))
    # create the conf file
    with open('{}/{}.conf'.format(folder, target._name), 'w') as f:
        f.write(NGINX_REDIRECT.format(target._name, target.url))
        f.close()
        
@event.listens_for(URLRecord, 'before_delete')
def del_nginx_config(mapper, connection, target):
    """
    Delete redirect config file
    """
    folder = Setting().get('url_redirect_nginx_conf_dir')
    try:
        if os.path.exists(folder):
            os.remove('{}/{}.conf'.format(folder,target._name))
        else:
            current_app.logger.error('{}/{}.conf does not exists'.format(folder,target._name))
        rc = Record(name=target.name,
                    type='A',
                    status='Active',
                    ttl=60,
                    data=Setting().get('url_redirect_ip'),
                    comment_data=target.comment)
        rc.delete(get_domain_name(target.domain_id))
    except Exception as e:
        current_app.logger.error(e)