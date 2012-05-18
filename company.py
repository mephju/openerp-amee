
from osv import osv, fields


class ResCompany(osv.osv):

    _inherit = 'res.company'
    _columns = {
        'ups_license_key':fields.char('UPS License Key', size=100),
        'ups_user_id':fields.char('UPS User Name', size=100),
        'ups_password':fields.char('UPS User Password', size=100),
        'ups_shipper_no':fields.char('UPS Shipper Number', size=100),
        'ups_test': fields.boolean('Is Test ?'),
        'ups_weight_uom': fields.many2one('product.uom', 'UPS UOM for Weights'),
        'ups_length_uom': fields.many2one('product.uom', 'UPS UOM for Lengths'),
        'api_key': fields.char('AMEE API Key', size=50),
        "url": fields.char('AMEE Webservice URL', size=100)
    }

    
        
ResCompany()

