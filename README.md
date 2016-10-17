barkingiguana.chage
===================

Manage account expiration attributes using the `chage` module, provided by
this role.

Requirements
------------

The `chage` command needs to be installed and configured on the hosts being
targetted by your playbook.

Example Playbook
----------------

    # playbook.yml
    - hosts: servers
      roles:
        your-role

    # roles/your-role/tasks/main.yml
    tasks:
      - name: Set password expiry
        chage:
          user: "{{ item }}"
          password_maximum_days: 90
          password_warn_days: 76
        with_items:
          - craig
          - charlotte

    # roles/your-role/meta/main.yml
    dependencies:
      - barkingiguana.chage

License
-------

MIT
