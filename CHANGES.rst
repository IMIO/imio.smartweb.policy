Changelog
=========


1.2.7 (2025-01-29)
------------------

- Update Python classifiers to be compatible with Python 3.12
  [remdub]

- Migrate to Plone 6.0.14
  [boulch]

- GHA tests on Python 3.8 3.9 and 3.10
  [remdub]


1.2.6 (2024-06-13)
------------------

- WEB-3763 : Fix Anysurfer controlpanel permission for fresh Smartweb installs
  See upgrade step 1029_to_1030
  [laulaz]


1.2.5 (2024-05-30)
------------------

- WEB-4107 : Use resourceRegistries ETag in caching configurations
  [laulaz]


1.2.4 (2024-02-02)
------------------

- Make content types translatable (with `plone.translatable` behavior) in
  multilingual profile.
  [laulaz]


1.2.3 (2024-01-16)
------------------

- WEB-4046 : Add "Skip to content" viewlet in portal top
  [laulaz]


1.2.2 (2023-11-21)
------------------

- Improve collective autoscaling compression quality
  Also fix missing autoscaling settings for new instances
  [laulaz]


1.2.1 (2023-10-29)
------------------

- Restore removed behaviors on Collection type
  [laulaz]


1.2 (2023-10-25)
----------------

- WEB-3985 : Add orientation behavior on Collection type
  [boulch, laulaz]


1.1.6 (2023-10-13)
------------------

- WEB-3803 : Monkey patch imio/collective.pivot post_install method to create an imio.smartweb.Folder to store defaults collective.pivot.Family contents
  [boulch]


1.1.5 (2023-10-09)
------------------

- Remove deprecated overrides because we removed picture managing out of Tiny
  [boulch]


1.1.4 (2023-05-22)
------------------

- Migrate to Plone 6.0.4
  [boulch]

- Migrate to Plone 6.0.2
  [boulch]

- WEB-3763 : Add new permission to manage configlets in control panel
  [boulch]


1.1.3 (2023-02-17)
------------------

- WEB-3820 : Added collective.geotransform but we don't deploy it automaticaly
  [boulch]

- WEB-3833 : Hide plone.app.multilingual in control panel installable products
  [boulch]


1.1.2 (2023-01-25)
------------------

- By default authorize_local_message and show_local_message in messagesviewlet must be True in smartweb
  [boulch]


1.1.1 (2023-01-12)
------------------

- Fix missing Plone icons (plone.staticresources)
  [laulaz]

- Install and configure autopublishing (with 15 min tick subscriber)
  [laulaz]

- Multilingual: add setup profile with content / default page migration to LRF
  and navigation links creation, fix selector viewlet
  [laulaz]

- Remove obsolete TinyMCE override
  [laulaz]


1.1 (2022-12-23)
----------------

- Update to Plone 6.0.0 final
  [boulch]

- WEB-3798 : Update caching profile (add lastModified to etags)
  [sverbois, remdub, boulch]


1.0.10 (2022-10-28)
-------------------

- Remove unneeded caching patches for 304 NOT MODIFIED requests
  Those are not needed anymore with the new cache configuration
  [laulaz]


1.0.9 (2022-10-05)
------------------

- WEB-3733 : Restrict permissions for "site admin" in control panel. Some options are only available for manager
  [boulch]

- Change s-maxage for new Varnish strategy based on grace
  [sverbois]


1.0.8 (2022-09-01)
------------------

- WEB-3731 : Automatically publish GDPR article
  [boulch]


1.0.7 (2022-06-07)
------------------

- Adapt SolR config to use tika for file indexing
  [mpeeters]

- Move/adapt ban_physicalpath method into imio.smartweb.common
  [boulch, laulaz]


1.0.6 (2022-05-02)
------------------

- Remove collective.z3cform.select2. We don't use full product anymore
  [boulch]


1.0.5 (2022-04-25)
------------------

- Uninstall collective.z3cform.select2, not needed anymore for faceted
  [laulaz]

- Hide unwanted upgrades from site-creation and quickinstaller
  [boulch]

- Add missing viewlet + reorder viewlets
  [boulch]


1.0.4 (2022-03-28)
------------------

- Add etags userid and roles in caching configuration
  [sverbois, boulch]

- Adapt ban_for_message to cover multi varnish servers and add http to correctly ban
  [boulch]

- Allow some Python modules in RestrictedPython (code moved from smartweb.core)
  This is useful for collective.themefragments fragments
  [boulch]

1.0.3 (2022-03-24)
------------------

- add logger to get some informations about BAN with Varnish
  [boulch]

- Fix collective autoscaling default values
  [boulch]


1.0.2 (2022-03-08)
------------------

- Add/install select2 widget for faceted
  [boulch]

- Fix BAN request when we change a message
  [boulch, laulaz]


1.0.1 (2022-03-08)
------------------

- Add missing zcml include of collective.autoscaling
  [laulaz]

- Fix faceted criteria update when installing from code (without browser request)
  [laulaz]


1.0 (2022-02-22)
----------------

- Install and set collective autoscaling with some default values
  [boulch]


1.0a17 (2022-02-11)
-------------------

- Send BAN request after a messageviewlet creation / modification / removal
  [laulaz]


1.0a16 (2022-02-10)
-------------------

- Add imio.prometheus dependency to get metrics view.
  [bsuttor]


1.0a15 (2022-02-04)
-------------------

- Activate plone.app.caching.moderateCaching.lastModified
  [sverbois, laulaz]

- Use auto-checkout for collective.z3cform.select2 (Plone 6)
  [laulaz]


1.0a14 (2022-02-03)
-------------------

- Add collective.z3cform.select2 as a dependency
  [boulch]


1.0a13 (2022-02-03)
-------------------

- Upgrade step : Reload portal types to add imio.smartweb.listing behavior on links
  [boulch]

- Patch ALL caching operations to add Cache-Control header even when
  intercepting a 304 NOT MODIFIED
  [laulaz]

- Update buildout to use Plone 6.0.0a3 packages versions
  [boulch]


1.0a12 (2022-01-31)
-------------------

- Patch terse caching operation to add Cache-Control header even when
  intercepting a 304 NOT MODIFIED
  [laulaz]

- Fix client caching value in terseCaching (was different in upgrade step)
  [laulaz]


1.0a11 (2022-01-27)
-------------------

- Fix Plone translations override
  [laulaz]


1.0a10 (2022-01-19)
-------------------

- Update buildout to use Plone 6.0.0a2 released version
  [laulaz]

- Get some missing upgrades steps from plone6 dev to plone6 released
  [boulch]

- Load/register caching configuration + move upgrades steps in an upgrades folder.
  [boulch]

- Remove client caching in terseCaching
  [sverbois]


1.0a9 (2022-01-13)
------------------

- Restore Plone colophon viewlet in footer
  [laulaz]


1.0a8 (2021-12-16)
------------------

- Add caching configuration
  [sverbois]


1.0a7 (2021-11-26)
------------------

- Restore Default workflow on Link type
  [laulaz]

- Change 'en-un-click' to ifind folder and add iam folder with some links + upgrade steps.
  [boulch]


1.0a6 (2021-11-24)
------------------

- Add upgrade to restrict collections views (will always be faceted layouts)
  [laulaz]


1.0a5 (2021-11-16)
------------------

- Add cropping support on File content type
  [laulaz]


1.0a4 (2021-11-05)
------------------

- Add `collective.solr` dependency & Activate SolR search by default
  [mpeeters]

- Add pas.plugins.imio profile dependency
  [laulaz]

- Hide plone.keywords for non editors
  [laulaz]

- Add topics & page category on File content type
  [laulaz]

- Allow only listing_view on collections
  [laulaz]

- Make Collections globally addable
  [laulaz]

- TinyMCE config is now made in imio.smartweb.common
  [laulaz]

- Simplify TinyMCE config & force paste as text
  [laulaz]

- Allow PortalPage content as default view
  [laulaz]

- Display Collection in navigation by default
  [laulaz]

- Move localmessages viewlet from default abovecontent to portalheader viewlet manager
  [boulch]

- Rename dependency : collective.bigbang to collective.bigbang
  [boulch]

- Manage grouping/order/visibility of subsite/minisite header/footer viewlets
  [laulaz]

- Allow only useful image scales in TinyMCE text fields
  [laulaz]

- Move code to imio.smartweb.common
  [laulaz]

- Remove collective.pivot out of metadata (undo auto-install)
  [boulch]


1.0a3 (2021-06-29)
------------------

- Add imio.gdpr
  [boulch]

- Add collective.messagesviewlet
  [boulch]

- Add pas.plugins.imio.
  [bsuttor]

- Add collective.bigbang.
  [bsuttor]


1.0a2 (2021-04-22)
------------------

- WEBMIGP5-12: Override TinyMCE Formats inline items
  [laulaz]

- WEBMIGP5-14: Change images behaviors
  [laulaz]

- WEBMIGP5-13: Change files behaviors
  [laulaz]

- Add configuration for TinyMCE toolbars / menus
  [laulaz]

- Add basic demo profile with content creation & improve install profile
  [laulaz]

- Fix navigation links translations
  [laulaz]

- Change header viewlets default order
  [laulaz]

- Migrate & improve buildout for Plone 6
  [boulch]

- Add uninstall profile
  [boulch]

- Fix tests for Plone 6
  [boulch]


1.0a1 (2021-04-19)
------------------

- Initial release.
  [boulch]
