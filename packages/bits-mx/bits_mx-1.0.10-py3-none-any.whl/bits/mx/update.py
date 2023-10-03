# -*- coding: utf-8 -*-
"""MX Update class file."""

from bits.mx.gnarwl import Gnarwl
from bits.mx.google import Google
from bits.mx.groups import Groups
from bits.mx.localmail import Localmail
from bits.mx.nicknames import Nicknames


class Update(object):
    """Update class."""

    def __init__(self, mx):
        """Initialize a class instance."""
        self.mx = mx
        self.verbose = mx.verbose

        self.auth = mx.auth

        # data
        self.all_other_accounts = None
        self.gnarwl = None
        self.google_other_accounts = None
        self.groups = None
        self.help_queues = None
        self.localmail = None
        self.nicknames = None
        self.people = None

    def all(self):
        """Update everything."""
        self.gnarwl_aliases()
        self.gnarwl_ldap()
        self.google_transport()
        self.groups_transport()
        self.localmail_aliases()
        self.nickname_aliases()

    def get_gnarwl(self):
        """Get Gnarwl data from MongoDB."""
        if self.gnarwl:
            return self.gnarwl
        if self.verbose:
            print('Getting gnarwl from MongoDB...')
        m = self.auth.mongo()
        self.gnarwl = m.get_collection_dict('gnarwl')
        return self.gnarwl

    def get_groups(self):
        """Get Groups data from Google."""
        if self.groups:
            return self.groups
        if self.verbose:
            print('Getting groups from Google...')
        g = self.auth.google()
        g.auth_service_account(g.scopes, g.subject)
        self.groups = g.directory().get_groups_dict()
        return self.groups

    def get_localmail(self):
        """Get Localmail from LDAP."""
        lm = self.auth.localmail()
        if self.localmail:
            return self.localmail
        if self.verbose:
            print('Getting localmail from MongoDB...')
        filterstr = '(&(uid=*)(shadowFlag=1))'
        self.localmail = {}
        entries = lm.get_entries(filterstr=filterstr)
        for dn in entries:
            self.localmail[dn] = lm.convert_entry_to_strings(entries[dn])
        return self.localmail

    def get_nicknames(self):
        """Get Nicknames data from MongoDB."""
        if self.nicknames:
            return self.nicknames
        if self.verbose:
            print('Getting nicknames from MongoDB...')
        m = self.auth.mongo()
        self.nicknames = m.get_collection_dict('nicknames')
        return self.nicknames

    def get_all_other_accounts(self):
        """Get All Other Accounts from MongoDB."""
        if self.all_other_accounts:
            return self.all_other_accounts
        if self.verbose:
            print('Getting other_accounts from MongoDB...')
        m = self.auth.mongo()
        self.all_other_accounts = m.get_collection_dict('other_accounts')
        return self.all_other_accounts

    def get_google_other_accounts(self):
        """Get Other Accounts from MongoDB."""
        if self.google_other_accounts:
            return self.google_other_accounts
        if self.verbose:
            print('Getting other_accounts from MongoDB...')
        m = self.auth.mongo()
        self.google_other_accounts = m.get_collection_dict('other_accounts', key='google_username')
        return self.google_other_accounts

    def get_people(self):
        """Get People from PeopleDB."""
        if self.people:
            return self.people
        if self.verbose:
            print('Getting people from PeopleDB...')
        p = self.auth.people()
        self.people = p.getPeople('username')
        return self.people

    def gnarwl_aliases(self):
        """Update Gnarwl aliases."""
        g = Gnarwl(self)
        if self.verbose:
            print('Updating gnarwl aliases...')
        # get gnarwl and nickname data
        gnarwl = self.get_gnarwl()
        self.get_nicknames()
        # check gnarwl data
        if len(gnarwl) < 3:
            print('ERROR: Not enough gnarwl entries (%s), exiting.' % (
                len(gnarwl)
            ))
        # get gnarwl autoreplies for output
        output = g.generate()
        # write file
        self.write_file(g.puppetfile, output)
        if self.verbose:
            print('Wrote gnarwl aliases to: %s\n' % (g.puppetfile))

    def gnarwl_ldap(self):
        """Update Gnarwl LDAP."""
        lu = self.auth.ldapupdate()
        if self.verbose:
            print('Updating gnarwl LDAP...')
        lu.update(['gnarwl_ldap_prod'])

    def google_transport(self):
        """Update Google transport."""
        g = Google(self)
        if self.verbose:
            print('Updating google transport...')
        # get people and other accounts
        people = self.get_people()
        google_other_accounts = self.get_google_other_accounts()
        # check people data
        if len(people) < 4000:
            print('ERROR: Not enough people entries (%s), exiting.' % (
                len(people)
            ))
        # check google_other_accounts data
        if len(google_other_accounts) < 50:
            print('ERROR: Not enough other_accounts entries (%s), exiting.' % (
                len(google_other_accounts)
            ))
        # get google transports for output
        output = g.generate()
        # write file
        self.write_file(g.puppetfile, output)
        if self.verbose:
            print('Wrote google transports to: %s\n' % (g.puppetfile))

    def groups_transport(self):
        """Update Groups transport."""
        g = Groups(self)
        if self.verbose:
            print('Updating groups transport...')
        # get groups
        groups = self.get_groups()
        # check groups data
        if len(groups) < 1000:
            print('ERROR: Not enough groups entries (%s), exiting.' % (
                len(groups)
            ))
        output = g.generate()
        # write file
        self.write_file(g.puppetfile, output)
        if self.verbose:
            print('Wrote groups transports to: %s\n' % (g.puppetfile))

    def localmail_aliases(self):
        """Update Localmail aliases."""
        lm = Localmail(self)
        if self.verbose:
            print('Updating localmail aliases...')
        # get localmail
        localmail = self.get_localmail()
        if len(localmail) < 10:
            print('ERROR: Not enough localmail entries (%s), exiting.' % (
                len(localmail)
            ))
        output = lm.generate()
        # write file
        self.write_file(lm.puppetfile, output)
        if self.verbose:
            print('Wrote groups transports to: %s\n' % (lm.puppetfile))

    def nickname_aliases(self):
        """Update Nickname aliases."""
        n = Nicknames(self)
        if self.verbose:
            print('Updating nickname aliases...')
        # get nicknames, people and other accounts
        nicknames = self.get_nicknames()
        people = self.get_people()
        all_other_accounts = self.get_all_other_accounts()
        # check nicknames data
        if len(nicknames) < 10:
            print('ERROR: Not enough nicknames entries (%s), exiting.' % (
                len(nicknames)
            ))
        # check people data
        if len(people) < 4000:
            print('ERROR: Not enough people entries (%s), exiting.' % (
                len(people)
            ))
        # check other_accounts data
        if len(all_other_accounts) < 50:
            print('ERROR: Not enough other_accounts entries (%s), exiting.' % (
                len(all_other_accounts)
            ))
        output = n.generate()
        # write file
        self.write_file(n.puppetfile, output)
        if self.verbose:
            print('Wrote nickname aliases to: %s\n' % (n.puppetfile))

    def write_file(self, filename, output):
        """Write out a single file to disk."""
        # open puppetfile
        outputfile = open(filename, 'w')
        # write output
        outputfile.write('%s\n' % (output))
        # close puppetfile
        outputfile.close()
