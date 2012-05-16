from osv import osv, fields


class amee(osv.osv):
    _name       = 'amee'
    _columns    = { 
                   'api_key': fields.char('AMEE API Key', size=50, required=True)
                   }
    

amee()
