
from osv import osv, fields



class amee(osv.osv):
    _name = 'amee.config'
    _columns = { 
            
            'api_key': fields.char('AMEE API Key', size=50, required=True),
            "password": fields.char("AMEE API Password", size=50, required=True),
            "url": fields.char('AMEE Webservice URL', size=100, required=True)
                   }
    



amee()


