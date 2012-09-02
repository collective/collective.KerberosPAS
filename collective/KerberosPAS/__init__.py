# -*- extra stuff goes here -*-

from KerberosAuthHelper import KerberosAuthHelper
from KerberosAuthHelper import addKerberosAuthHelper
from Products.PluggableAuthService import registerMultiPlugin
from AccessControl.Permissions import manage_users as ManageUsers

registerMultiPlugin(KerberosAuthHelper.meta_type)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    context.registerClass( KerberosAuthHelper
                         , permission=ManageUsers
                         , constructors=(
                            KerberosAuthHelper.manage_addKerberosAuthHelperForm,
                            addKerberosAuthHelper, )
                         , visibility=None
                         , icon='KerberosAuthHelper.png'
                         )

