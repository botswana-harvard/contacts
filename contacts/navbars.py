from edc_navbar import NavbarItem, site_navbars, Navbar


contacts = Navbar(name='contacts')

contacts.append_item(
    NavbarItem(
        name='contacts',
        label='BHP Contacts',
        fa_icon='fa-user-plus',
        url_name='home_url'))

site_navbars.register(contacts)
