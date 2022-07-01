
from .base import db
# from .domain import Domain as _Domain
# from .record import Record

class URLRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    content = db.Column(db.String(255), index=True)
    comment = db.Column(db.String(255), index=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'))
    disabled = db.Column(db.Boolean, default=False)
    
    def __init__(self, id=None, name=None, content=None, comment='', domain_id=None, disabled=False, rr=None) -> None:
        self.id = id
        self.domain_id = domain_id
        self.name =  rr['name'] if rr else name
        self.content = rr['records'][0]['content'] if rr else content
        self.comment = rr['comments'][0]['content'] if rr and 'comments' in rr else comment
        self.disabled = rr['records'][0]['disabled'] if rr else disabled
        super().__init__()
    
    @property
    def serialize(self):
        return {
            'name': self.name,
            'type': 'URL',
            'ttl': 300,
            'records': [{
                'content': self.content, 
                'disabled': self.disabled
            }],
            'comments': [{'content': self.comment, 'account': ''}]
        }
    @property
    def _name(self):
        return self.name if self.name[-1] != '.' else self.name[:-1]
    
    # @property
    # def domain_name(self):
    #     return _Domain.query.filter_by(id=self.domain_id).first().name
    @property
    def url(self):
        return self.content if 'http' in self.content else 'https://' + self.content
    

  