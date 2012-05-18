
from osv import osv, fields
from lxml import etree


class product(osv.osv):
    _inherit = "product.product"
    
    replace_text = '<separator string="AMEE"/>'


    def fetch_amee_data(self):
        result = {
                  'a': 10,
                  'b': 20,
                  'c': 30
        }
        
        return result
        
    
    def generate_lwc_epi_view(self):
        print "dynamically generating view for LWC-EPI"
        values = self.fetch_amee_data()
        
        view_code = '''<group colspan="3" col="2" string="EPI DATA">'''
        
        for key in values.keys():
            print key
            value = values[key]
            view_code += """<label string="%s"/> <label string="%s"/> """ %(key, value)
            print view_code
            
        view_code += '''</group>'''
        return view_code
    
    
    
    
    
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        res = super(product, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        if self.replace_text in res['arch']:
            res['arch'] = res['arch'].replace(
                                              self.replace_text, 
                                              str(self.generate_lwc_epi_view())
                                              )
        return res

    
        
    
product()
