# Importing Base Class 
from modules.src.base_class import BaseClass
from modules.src.id_generator_class import IDGenerator
from modules.src.slugify_class import SlugifyClass

class UserClass(BaseClass):
    def __init__(self,name=None,username=None,password=None,account_type=None,is_active=False):
        self._id = IDGenerator().generateNewId('users')
        self._name = name
        self._username = username
        self._password = password
        self.account_type = account_type
        self.is_active = is_active
        self._slug = SlugifyClass(self._name).generateSlug()

        BaseClass.__init__(self)

    def getUserRecords(self):
        print()
        print('{0} User Record'.format(self._name))
        print('--------------------------------------------')
        print('o-- User ID:{0}\n o-- Full Name:{1}\n o-- Username:{2}\n o-- Created At:{3} \n o-- Updated At:{4} \n o-- Slug:{5}'.format(self._id,self._name,self._username,self.created_at,self.updated_at,self._slug))


    
