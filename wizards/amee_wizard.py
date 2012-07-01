from osv import osv, fields
import httplib
import string
import base64
import urllib2
import urllib
import urlparse

import ast
import simplejson

class wizard_amee(osv.osv_memory):
    _name = 'amee.wizard'
    _columns = {
                 
            "gas_quant": fields.integer('Gas'),
            "iron_quant": fields.integer('Iron'),
            "material_quant": fields.integer('Material'),
            "pig_quant": fields.integer('Pig'),
            "steel_quant": fields.integer('Steel'),
            'result_co2e': fields.float('CO2e', readonly=True),
            'result_ch4': fields.float('CH4', readonly=True),
            'result_co2': fields.float('CO2', readonly=True),
            'product_id': fields.many2one('product.product', 'Product', required=True, readonly=1),
    }
    
    
    _defaults = {
                 'gas_quant': 100,
                 'iron_quant': 100,
                 'material_quant': 100,
                 'pig_quant': 100,
                 'steel_quant': 100
    }
    
    
    def query_amee(self, cr, uid, ids, context=None):
        
        data = self.read(cr, uid, ids, context=context)[0]
        
        print data
        print ""
        
        print 'product'
        product_id = data['product_id'][0]
        p    = self.pool.get('product.product')
        p   = p.browse(cr, uid, product_id)
        
        print p['name']
        material = p['name']
        
        
        amee_config = self.get_amee_config(cr, uid)
        
        material = urllib.urlencode({'material':material})
        print material
        
        server      = 'api-stage.amee.com'
        endpoint    = "/3.6/categories/iron_and_steel/calculation"
        query = "?"
        query += material
        query += "&values.gasQuantity=" + str(data['gas_quant']) + "&units.gasQuantity=kg&"
        query += "values.ironQuantity=" + str(data['iron_quant']) + "&units.ironQuantity=kg&"
        query += "values.materialQuantity=" + str(data['material_quant']) + "&units.materialQuantity=kg&"
        query += "values.pigQuantity=" + str(data['pig_quant']) + "&units.pigQuantity=kg&"
        query += "values.steelQuantity=" + str(data['steel_quant']) + "&units.steelQuantity=kg"        
        
        url = "https://" + server + endpoint + query
        
        user    = "sam1"
        pwd     = "v57ty37f"
        
        user    = amee_config.api_key
        pwd     = amee_config.password
        auth    = 'Basic ' + string.strip(base64.encodestring(user + ':' + pwd))

        
        
        
        
        
        
        headers = {"Accept":"application/json", "Authorization":auth}
        request = urllib2.Request(url)
 
        # post form data
        # request.add_data(urllib.urlencode(data))
 
        for key,value in headers.items():
            request.add_header(key,value)
 
        response = urllib2.urlopen(request)
 
        print 'http call: '
        print response.info().headers
        
        data = response.read()        
        print ""
        print data
        print ""
        
        #convert here        
        json = simplejson.loads(data)  
        print json
        print ""
        
        
        data = json['output']
        array = data['amounts']
        print array
        
        for i in range(len(array)):
            print array[i]
            res = array[i]
            type = "result_" + str.lower(res['type'])
            value = res['value']
            self.write(cr, uid, ids, {type:value}, context=None)
            
        
    
    def get_amee_config(self, cr, uid):
        amee    = self.pool.get('amee.config')
        ids     = amee.search(cr, uid, [])
        for id in ids:
            print id
        amee_config = amee.browse(cr, uid, id)
        if amee_config:
            print "AMEE API KEY" + amee_config.api_key
            print "AMEE URL" + amee_config.url
            print "PASSWORD " + amee_config.password
            return amee_config
        else:
            print "COULDNT LOAD AMEE CONFIG"
            return None
   
    def default_get(self, cr, uid, fields, context=None):
        """ To get default values for the object.
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param fields: List of fields for which we want default values
        @param context: A standard dictionary
        @return: A dictionary which of fields with values.
        """
        if context is None:
            context = {}
        record_id = context and context.get('active_id', False) or False

        res = super(wizard_amee, self).default_get(cr, uid, fields, context=context)
        product_id = self.pool.get('product.product').browse(cr, uid, record_id, context=context).id
        if 'product_id' in fields:
            res.update({'product_id':product_id})
        return res 
        

    
    def onchange_product_id(self, cr, uid, ids, prod_id):
        """ On Change of Product ID getting the value of related UoM.
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param ids: List of IDs selected 
         @param prod_id: Changed ID of Product 
         @return: A dictionary which gives the UoM of the changed Product 
        """
        product = self.pool.get('product.product').browse(cr, uid, prod_id)
        return {'value': {'uom_id': product.uom_id.id}}
    



wizard_amee()    