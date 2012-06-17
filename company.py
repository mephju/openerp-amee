
from osv import osv, fields


class ResCompany(osv.osv):

    _inherit = 'res.company'
    _columns = {
        'pass': fields.char('AMEE API password', size=50),
        'api_key': fields.char('AMEE API Key', size=50),
        "url": fields.char('AMEE Webservice URL', size=100)
    }

    
        
ResCompany()

