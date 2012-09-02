from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin,IExtractionPlugin,IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import ICredentialsResetPlugin
from App.class_init import default__class_init__ as InitializeClass
from zope.interface import Interface
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
import kerberos

def addKerberosAuthHelper( dispatcher, id, title=None, REQUEST=None ):
    """ Add a HTTP Kerberos Auth Helper to a Pluggable Auth Service.
    """
    sp = KerberosAuthHelper( id, title )
    dispatcher._setObject( sp.getId(), sp )
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect( '%s/manage_workspace'
                                      '?manage_tabs_message='
                                      'KerberosAuthHelper+added.'
                                    % dispatcher.absolute_url() )

class IKerberosAuthHelper(Interface):
  """ Marker interface.
  """

class KerberosAuthHelper(BasePlugin):
  """ This class contains the required PAS plugins for GSSAPI authentication.
  """

  meta_type = 'HTTP Kerberos Auth Helper'
  protocol = 'http'
  security = ClassSecurityInfo()

  def __init__(self, id, title=None):
   self._setId(id)
   self.title = title

  security.declarePrivate('challenge')
  def challenge(self, request, response):
   """ Challenge the user's browser for credentials.
   """
   if not request._auth:
    response.addHeader('WWW-Authenticate','Negotiate')
    response.addHeader('content-type','text/plain')
    m = "<strong>You are not authorized to access this resource.</strong>"
    response.setBody(m, is_error=1)
    response.setStatus(401, lock=True)
    return 1
   return 0

  security.declarePrivate( 'extractCredentials' )
  def extractCredentials( self, request ):
   """ Extract credentials from 'request'.
   """
   creds = {}
   authorization = request._auth
   if authorization:
    try:
     result, context = kerberos.authGSSServerInit("HTTP")
     if result != 1:
      return creds
     gssstring=''
     authstr = authorization.split(" ")[1]
     r=kerberos.authGSSServerStep(context,authstr)   
     if r == 1:
      gssstring=kerberos.authGSSServerResponse(context)
     else:
      # Something went horribly wrong, challenge again!
      self.challenge(request, request.response)
     # Return the status to user's browser - this is like an ack message
     request.response.addHeader('WWW-Authenticate','Negotiate %s' % gssstring)
     username = kerberos.authGSSServerUserName(context)
     creds['login'] = self.deriveUserName(username)
     creds['remote_host'] = request.getClientAddr()
     creds['kerberos'] = True
     # For caching
     request.SESSION.set("__login",creds['login'])
     request.SESSION.set("__remote_host",creds['remote_host'])
     request.SESSION.set("__kerberos",creds['kerberos'])
     kerberos.authGSSServerClean(context)
    except GSSError as e:
     print "GSSAPI error in extractCredentials :"+str(e)
   else:
     # Let's attempt to cache this
     login = request.SESSION.get("__login")
     remote_host = request.SESSION.get("__remote_host")
     kerbeross = request.SESSION.get("__kerberos")
     if login and remote_host and kerbeross and request.getClientAddr() == remote_host:
      creds['login'] = login
      creds['remote_host'] = remote_host
      creds['kerberos'] = kerbeross
   return creds

  def deriveUserName(self,input):
   """ If the input is like xxx@yyy, return xxx. Otherwise return the whole string.
   """
   result = ""
   if input:
    split = input.split("@")
    if len(split) == 2:
     result = split[0]
    else:
     result = input 
   return result

  security.declarePrivate('authenticateCredentials')
  def authenticateCredentials(self, credentials):
   """ If the credentials has "kerberos" set trust the username implicitly.
   """
   if 'kerberos' in credentials:
    login=credentials['login'] 
    return (login, login)
   return None

  security.declarePrivate( 'resetCredentials' )
  def resetCredentials(self, request, response):
   """ Force the browser to flush credentials
   """
   response.unauthorized()

  manage_addKerberosAuthHelperForm = PageTemplateFile(
    'www/kaAdd', globals(), __name__='manage_addKerberosAuthHelperForm' )

classImplements(KerberosAuthHelper, IKerberosAuthHelper, IChallengePlugin, ICredentialsResetPlugin, IExtractionPlugin, IAuthenticationPlugin)
InitializeClass(KerberosAuthHelper)

