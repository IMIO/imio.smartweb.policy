Changelog
=========


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
