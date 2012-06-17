from osv import osv, fields

class wizard_amee(osv.osv_memory):
    _name = 'amee.wizard'
    _columns = { 
            "field0": fields.char('field0', size=100),
            "field1": fields.char('field1', size=100),
            "field2": fields.char('field2', size=100),
            "field3": fields.char('field3', size=100),
            "field4": fields.char('field4', size=100),
            "field5": fields.char('field5', size=100),
            "field6": fields.char('field6', size=100),
            "field7": fields.char('field7', size=100),
            "field8": fields.char('field8', size=100),
            "field9": fields.char('field9', size=100),
            "field10": fields.char('field10', size=100),
            "field11": fields.char('field11', size=100),
            "field12": fields.char('field12', size=100),
            "field13": fields.char('field13', size=100),
            'product_id': fields.many2one('product.product', 'Product', required=True, readonly=1),
    }
    
    
    def query_amee(self, cr, uid, ids, context=None):
        amee_config = self._get_amee_config( cr, uid)
        print "we are querying amee now"
        print context
        return {}
    
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
                 
        
    
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        param_fields    = self._build_param_fields(context)
        print param_fields
        res             = super(wizard_amee, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
      
        print res['arch']
        for k in param_fields.keys():
            print k
            if k in res['arch']:
                print "replacing " + k
                res['arch'] = res['arch'].replace(k, param_fields[k])
        return res
    
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