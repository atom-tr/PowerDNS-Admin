from .base import db


class DomainInfo(db.Model):
    __tablename__ = 'domain_info'
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'))
    # domain_name = db.Column(db.String(64), primary_key=True)
    cus_name = db.Column(db.String(64))
    cus_email = db.Column(db.String(64))
    cus_phone = db.Column(db.String(64))
    
    

    def __init__(self,domain_id=None,cus_name=None,cus_email=None, cus_phone=None):
        self.domain_id = domain_id
        self.cus_name = cus_name
        self.cus_email = cus_email
        self.cus_phone = cus_phone

    # def add(self,domain_name,cus_name,cus_email):
    #     self.domain_name = domain_name
    #     self.cus_name = cus_name
    #     self.cus_email = cus_email

    # def delete(self,domain_name,cus_name,cus_email):
    #     self.domain_name = domain_name
    #     self.cus_name = cus_name
    #     self.cus_email = cus_email