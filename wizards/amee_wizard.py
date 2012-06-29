from osv import osv, fields
import httplib
import string
import base64
import urllib2

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
        amee_config = self._get_amee_config( cr, uid)
        
        data = self.read(cr, uid, ids, context=context)[0]
        
        server      = 'api-stage.amee.com'
        endpoint    = "/3.6/categories/iron_and_steel/calculation"
        query = ""
        query += "?material=Steel&"
        query += "values.gasQuantity=" + str(data['gas_quant']) + "&units.gasQuantity=kg&"
        query += "values.ironQuantity=" + str(data['iron_quant']) + "&units.ironQuantity=kg&"
        query += "values.materialQuantity=" + str(data['material_quant']) + "&units.materialQuantity=kg&"
        query += "values.pigQuantity=" + str(data['pig_quant']) + "&units.pigQuantity=kg&"
        query += "values.steelQuantity=" + str(data['steel_quant']) + "&units.steelQuantity=kg"        
        
        
        
        user    = "sam1"
        pwd     = "v57ty37f"
        auth    = 'Basic ' + string.strip(base64.encodestring(user + ':' + pwd))
        
        conn = httplib.HTTPConnection(server)
        header = {  
                    "Accept" : "application/json",
                    "Authorization" : auth
                  }
        
        
        conn.request("GET", endpoint+query, None, header)
        response = conn.getresponse()
        
        
        
        
#        authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm()
#        authinfo.add_password(None, server, 'testuser', 'test-user-pass')
#        page = 'HTTP://'+SERVER+'/cgi-bin/tools/orders_waiting.py'
#        handler = urllib2.HTTPBasicAuthHandler(authinfo)
#        myopener = urllib2.build_opener(handler)
#        opened = urllib2.install_opener(myopener)
#        output = urllib2.urlopen(page)
        
        #response = urllib.urlopen('https://sam1:v57ty37f@api-stage.amee.com/3.6/categories/iron_and_steel/calculation' + query)
        
        print 'http call: '
        print conn
        print response.status, response.reason
        
        
        print "we are querying amee now for " + str(data['product_id'])
        print 'query: ' + endpoint + query
        print "data%%%%%%%%%%%%%%%%%%%%%%%%%%%%%:" 
        print data
        return { 'result_co2e':334 }
    
    def get_amee_params(self, product):
        return ["param1", "param2", "param3"]

    
    def _build_param_fields(self, context):
        print "build param fields"
        print context
        view_code = {}
        params = self.get_amee_params(context)
        for i in range(14):
            current     = "field" + str(i)
            current2     = """<field name="%s" modifiers="{}"/>""" %(current)
            
            if i < len(params):
                val         = params[i]                
                view_code[current2] = """<field name="%s" string="%s" />"""  % (current, val) 
                print val
            else:
                view_code[current2] = ""
        return view_code
                 
        
    
#    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
#        param_fields    = self._build_param_fields(context)
#        print param_fields
#        res             = super(wizard_amee, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
#      
#        print res['arch']
#        for k in param_fields.keys():
#            print k
#            if k in res['arch']:
#                print "replacing " + k
#                res['arch'] = res['arch'].replace(k, param_fields[k])
#        return res
    
    def _get_amee_config(self, cr, uid):
        amee    = self.pool.get('amee.config')
        ids     = amee.search(cr, uid, [])
        for id in ids:
            print id
        amee_config = amee.browse(cr, uid, id)
        if amee_config:
            print "AMEE API KEY" + amee_config.api_key
            print "AMEE URL" + amee_config.url
            print "PASSWORD " + amee_config.password
            return amee_config.api_key
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