
from osv import osv, fields
from lxml import etree
from dns.rdatatype import NULL


class product(osv.osv):
    _inherit = "product.product"
    
    _columns = {
                "url": fields.char('AasdfdasfL', size=100)
    }
    
    replace_text = '<separator string="AMEE"/>'
    
    def fetch_amee_data(self):
        result = {
                  'a': 10,
                  'b': 20,
                  'c': 30
        }
        
        return result
    
    def _fetch_api_key(self, cr, uid):
        amee = self.pool.get('amee.config')
        
        ids = amee.search(cr, uid, [])
        
        for id in ids:
            print id
        amee_object = amee.browse(cr, uid, id)
        
        if amee_object:
            print "AMEE API KEY" + amee_object.api_key
            print "AMEE URL" + amee_object.url
            print "PASSWORD " + amee_object.password
            return amee_object.api_key
        else:
            print "COULDNT LOAD AMEE CONFIG"
            return None

        
    
    def generate_lwc_epi_view(self, cr, uid):
        print "dynamically generating view for LWC-EPI"
        ameeValues          = self.fetch_amee_data()
        amee_api_key        = self._fetch_api_key(cr, uid)
        
        view_code = '''<group colspan="3" col="2" string="EPI DATA">'''
        
        if amee_api_key:
            view_code += """<label string="%s"/> <label string="%s"/> """ %("apikey", amee_api_key)
        
       
        for key in ameeValues.keys():
            print key
            value = ameeValues[key]
            
            view_code += """<label string="%s"/> <label string="%s"/> """ %(key, value)
            
            
            print view_code
            
        view_code += '''</group>'''
        return view_code
    
    
    
    
    
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        self._fetch_api_key(cr, uid)
        
        res = super(product, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        if self.replace_text in res['arch']:
            res['arch'] = res['arch'].replace(
                                              self.replace_text, 
                                              str(self.generate_lwc_epi_view(cr, uid))
                                              )
        return res

    
        
    
product()












