from osv import osv, fields



class test(osv.osv):
    _name       = 'test.test'
    _columns    = { 
                   'name' : fields.text('Details')
                   }
    

test()
