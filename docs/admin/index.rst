Base Administrator's Manual
===========================

The Constellation Base module includes very few module level settings,
but does include some nifty features that can make the entire suite
easier to use.


<All Users> Group
-----------------

Since almost all permissions within the Constellation Suite are group
based, its sometimes useful to have a group that contains all users.
The :code:`<All Users>` Group is an internally generated group that
automatically contains all users.  This group does not require any
configuration to use and cannot be deleted.  This group can be very
useful if you draw your users from an external source and your global
container group isn't visible to Django.


Group Manager
-------------

In rare cases where you cannot do proper group membership management
with either Django's internal tools or an external authentication
source, you can use the built in group manager.  This system allows
you to input a comma seperated list of usernames that will be added to
the group for which the list exists.  This interface can only be
accessed by users that have the Staff permission level and is not
linked to by any internal URL.  To access this interface, navigate to
:code:`/manage/groups` and fill out the form.  Updating group
membership is always an overwrite operation, there is no option to
edit in place, so keep this in mind if you need to make changes to
your group access list.

This mechanism is implemented as a means to solve a very specific
problem, so unless you have the same problem, you probably don't need
to use it.  The problem was as follows: in the early days of the
Constellation Platform, one of the primary customers was a University
department.  All of the users were in an MS AD server and LDAP
authentication was possible to this server.  Where things went awry
was trying to get a list of all users belonging to subgroups within
the department.  This would have required an Oracle PeopleSoft
installation to have some degree of global write access to the LDAP
servers.  As this was deemed unnacceptable, it was necessary to
determine group membership by some other means.

Since the LDAP module for Django overwrites a users's groups on login,
this feature adds a signal handler that gets called on login by any
user and checks to see if they have an entry in the group list.  If
such an entry exists, they will be appended to that group.  It is
possible that a particularly speedy user might see a 403 by logging in
and navigating to a page that required a group permission before the
signal handler completed, but this is exceedingly unlikely.
