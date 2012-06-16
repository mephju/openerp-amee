import wizard

class wizard_amee(wizard.interface):
    
    _amee_form = """
        <form string="Reconciliation">
          <field name='pass'/>
        </form> """
    
    
    _amee_fields = {
        'pass': {
                 'string': 'New Password', 
                 'type': 'char', 
                 'size': 64
        }
    }
    
    def _query(self,cr,uid,data,context):
        print "query is called"
        return {}

        
    
    states = {
              'init': {
                     'actions': [],
                    'result': {
                           'type': 'form',
                           'arch': _amee_form,
                           'fields': _amee_fields,
                           'state':[('query','Query'),('end','Cancel')]
                     }
              },
              'query': {
                    'actions': [_query],
                    'result': {'type': 'state', 'state':'end'}
              }
              
    }
    
    
    
wizard_amee("amee.wizard")
print "registeredd amee.query.wizard"
print "registeredd amee.query.wizard"
print "registeredd amee.query.wizard"
print "registeredd amee.query.wizard"
print "registeredd amee.query.wizard"
print "registeredd amee.query.wizard"
print "registeredd amee.query.wizard"
print "registeredd amee.query.wizard"