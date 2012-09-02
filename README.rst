Introduction
============

This product implements kerberos/GSS-API (see RFC 4178) Pluggable Authentication Service plugin for Plone.

Kerberos is the preferred SSO method for intranet setups because it is secure, robust, and it performs well. It also offers improved usability (most of the logins are transparent to users) and robust interoperatibility between different platforms (Windows, MacOS X, Linux, BSDs, etc) and different browsers (Chrome, Internet Explorer, Firefox).

KerberosPAS implements the kerberos authentication at application server by using kerberos_ and the kerberos 5 libraries (most commonly either MIT or Heimdal). The other available products most commonly offload that task to a web server and use a REMOTE_USER environment variable to communicate the authenticated user. Downsides to that approach are the insecurity between web and application servers and decreased selection of usable web server products.

This product does not check whether the authenticated users exist in ZODB. Correct plugin order will cause authenticating non-existing users fail. A plugin-registry genericsetup profile is included, and will attempt to provide a starting point for setting the PAS plugin up. Your mileage may vary.

For performance reasons the extraction is cached using Zope session, otherwise negotiation would happen at every page load.

.. _kerberos: http://pypi.python.org/pypi/kerberos/

Configuring Kerberos
====================

Below are some basic notes for those who are not familiar with setting up Kerberos and GSS-API authentication.

A working kerberos realm should be set up. Your Plone server and the workstations should be joined to the realm. For resources on accomplishing that please see for instance:

- https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/html/Managing_Smart_Cards/Configuring_a_Kerberos_5_Server.html
- http://www.centos.org/docs/5/html/Deployment_Guide-en-US/ch-kerberos.html
- http://www.freebsd.org/doc/handbook/kerberos5.html
- http://tldp.org/HOWTO/Kerberos-Infrastructure-HOWTO/

Please take the commonly stated requirement of having working DNS and using FQDNs **seriously** or you will at later phase run into problems.

The Plone server will require krb5-libs and krb5-workstation packages.

You will need a service principal for your Plone server. It should have the form HTTP/fqdn@YOURREALM and you create it like::

 addprinc -randkey HTTP/plone.localdomain@LOCALDOMAIN

After that you save it into your Plone server's /etc/krb5.keytab by::

 ktadd HTTP/plone.localdomain@LOCALDOMAIN

After that you configure your browser for the GSS-API authentication. Internet Explorer requires that the site is in trusted sites list, and the browser has "Use integrated windows authentication" enabled. Firefox requires that you go to about:config and add your domain name to network.negotiate-auth.trusted-uris. You can either use fqdn or the dnsdomainname, I used ``.localdomain`` for development.

**Plone will run the process as a separate user that has minimal access rights. You will have to add this user, typically called ``plone``, read access rights to the file /etc/krb5.keytab**

Debugging
=========

The following environment variables will make Firefox print out extensive debug log: ::

 export NSPR_LOG_MODULES=negotiateauth:5
 export NSPR_LOG_FILE=/tmp/moz.log

The following environment variable will make krb5-libs print out trace log: ::

 export KRB5_TRACE=/tmp/krb.log

 
