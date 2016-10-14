barkingiguana.chage
===================

Manage account expiration attributes using the `chage` module, provided by
this role.

Requirements
------------

The `chage` command.

Example Playbook
----------------

    - hosts: servers
      tasks:
        - name: Set password expiry
          chage:
            user: "{{ item }}"
            password_maximum_days: 90
            password_warn_days: 76
          with_items:
            - craig
            - charlotte

License
-------

MIT
