
from osv import osv, fields



class amee_config(osv.osv_memory):
    _name       = 'amee.config'
    _inherit    = 'res.config'
    _columns    = { 
            'api_key': fields.char('AMEE API Key', size=50, required=True),
            "password": fields.char("AMEE API Password", size=50, required=True),
            "url": fields.char('AMEE Webservice URL', size=100, required=True)
                   }
    
    def execute(self, cr, uid, ids, context=None):
        print 'config'
        print context
        
        conf = self.browse(cr, uid, ids[0], context=context)
        
        print conf.url
        
        data = self.read(cr, uid, ids, context=context)
        wizard = self.browse(cr, uid, ids, context=context)[0]
        proxy = self.pool.get('ir.values')

        return {'type' : 'ir.actions.act_window_close'}
amee_config()



