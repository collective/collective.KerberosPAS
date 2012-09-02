Introduction
============

This product implements kerberos/GSS-API (see RFC 4178) Pluggable Authentication Service plugin for Plone.

Kerberos is the preferred SSO method for intranets because it is extremely secure, robust, and performs well. It also improves the usability for end-users because they don't have to use their username/password combination after logging into workstations. Kerberos is also supported on virtually any platform (Windows, MacOS X, Linux, BSDs, etc) and by most of the web browsers (Chrome, Internet Explorer, Firefox) - and it interoperates between platforms quite well.

Most of the other available products use web server provided kerberos authentication with the combination of REMOTE_USER environment value. As the interaction between front-end web server and the application server is essentially non-protected that is not generally a good idea. Also, that limits the web server products that can be used to those that have a kerberos authentication module available. This module implements the GSS-API authentication on the application server.

This product does not check whether the authenticated users exist in ZODB. Correct plugin order will cause authenticating non-existing users fail. For performance reasons the extraction is cached using Zope session, otherwise negotiation would happen at every page load. 

Prerequisities
==============

Below are gathered some basic pointers for those who are not familiar with setting up Kerberos and GSS-API authentication.

A working kerberos realm should be already set up. Your Plone server and the workstations should be joined to the realm. For resources on accomplishing that please see for instance:
- https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/html/Managing_Smart_Cards/Configuring_a_Kerberos_5_Server.html
- http://www.centos.org/docs/5/html/Deployment_Guide-en-US/ch-kerberos.html
- http://www.freebsd.org/doc/handbook/kerberos5.html
- http://tldp.org/HOWTO/Kerberos-Infrastructure-HOWTO/

Please take the requirement of having working DNS and using FQDNs *seriously* or you will at later phase run into problems.

The Plone server will require krb5-libs and krb5-workstation packages.

You will need a service principal for your Plone server. You create it like::

 addprinc -randkey HTTP/plone.localdomain@LOCALDOMAIN

After that you save it into the plone server's /etc/krb5.keytab by::

 ktadd HTTP/plone.localdomain@LOCALDOMAIN

After that you configure your browser. Internet Explorer requires that the site is in trusted sites list, and the browser has "Use integrated windows authentication" enabled. Firefox requires that you go to about:config and add your domain name to network.negotiate-auth.trusted-uris.

**Plone will run the process as a separate user that has minimal access rights. You will have to add this user, typically called "plone" read access rights to the file /etc/krb5.keytab**

Debugging
=========

The following environment variables will make Firefox print out extensive debug log: ::

 export NSPR_LOG_MODULES=negotiateauth:5
 export NSPR_LOG_FILE=/tmp/moz.log

The following environment variable will make krb5-libs print out trace log: ::

 export KRB5_TRACE=/tmp/krb.log

 
