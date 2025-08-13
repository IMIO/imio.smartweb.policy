# -*- coding: utf-8 -*-

from imio.smartweb.common.utils import get_vocabulary
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from z3c.form.interfaces import IFormLayer
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import alsoProvides


def remove_unused_contents(portal):
    api.content.delete(portal.news)
    api.content.delete(portal.events)
    api.content.delete(portal.Members)


def clear_manager_portlets(folder, manager_name):
    manager = getUtility(IPortletManager, name=manager_name, context=folder)
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)
    for portlet in assignments:
        del assignments[portlet]


def add_iam_folder(context, lang):
    i_am_folder = api.content.create(
        container=context,
        type="imio.smartweb.Folder",
        title=translate(_("I am"), target_language=lang),
    )
    api.content.transition(i_am_folder, "publish")

    root_url = context.absolute_url()
    i_am_vocabulary = get_vocabulary("imio.smartweb.vocabulary.IAm")
    for term in i_am_vocabulary:
        link = api.content.create(
            container=i_am_folder,
            type="Link",
            title=translate(_(term.title), target_language=lang),
        )
        link.remoteUrl = f"{root_url}/@@search?iam={term.token}"
        api.content.transition(link, "publish")


def add_ifind_folder(context, lang):
    i_find_folder = api.content.create(
        container=context,
        type="imio.smartweb.Folder",
        title=translate(_("I find"), target_language=lang),
    )
    api.content.transition(i_find_folder, "publish")
    collection = api.content.create(
        container=i_find_folder,
        type="Collection",
        title=translate(
            _("Procedures and practical informations"), target_language=lang
        ),
    )
    collection.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["imio.smartweb.Procedure"],
        }
    ]
    api.content.transition(collection, "publish")
    request = getRequest()
    alsoProvides(request, IFormLayer)
    request.form = {
        "cid": "page-category",
        "faceted.page-category.index": "taxonomy_procedure_category",
        "faceted.page-category.vocabulary": "collective.taxonomy.procedure_category",
    }
    handler = getMultiAdapter((collection, request), name="faceted_update_criterion")
    handler.edit(**request.form)


def add_navigation_links(context, lang=None):
    if lang is None:
        lang = api.portal.get_current_language()[:2]
    add_iam_folder(context, lang)
    add_ifind_folder(context, lang)


def get_gdpr_html_content(commune):
    if commune is None:
        commune = "[nom du pouvoir local]"
    gdpr_html_content = f"""
    <h1>Déclaration relative à la protection des données à caractère personnel</h1>
    <p>Ces mentions légales concernent le site internet public de {commune}</p>
    <h2>I. Introduction</h2>
    <p>{commune} est attaché au respect de la vie privée.</p>
    <p>Notre politique en matière de protection des personnes physiques à l'égard du traitement des données à caractère se fonde sur le Règlement (UE) 2016/679 du Parlement européen et du Conseil du 27 avril 2016 (aussi connu sous l’acronyme RGPD).</p>
    <h2>II. À quelles fins recueillons-nous, traitons-nous et conservons-nous vos données à caractère personnel?</h2>
    <p>Le présent site ne recueille aucune information personnelle (même pas pour les statistiques de fréquentation, car nous utilisons l'outil Plausible, conforme au RGPD européen).</p>
    <p>Les seules données à caractère personnel vous concernant sont recueillies dans l'e-guichet de {commune}, afin de permettre le traitement de vos démarches.</p>
    <p>Ces données sont traitées conformément à la politique décrite dans le règlement RGPD susmentionné.</p>
    <p>Elles ne sont traitées que par le personnel de {commune} et d'iMio, et des sous-traitants éventuels, aux seules fins décrites ci-dessus et afin d'améliorer le service.</p>
    <h2>III. Qui est le «responsable du traitement des données»?</h2>
    <p>Le responsable du traitement des données est le DPO de {commune}. Si vous avez des questions concernant le traitement de vos données à caractère personnel, vous pouvez les envoyer à [adresse électronique du DPO du pouvoir local]</p>
    <h2>IV. À qui vos données sont-elles communiquées?</h2>
    <p>Les données recueillies à votre sujet sont traitées de manière confidentielle et utilisées seulement par les agents de {commune}, iMio et ses sous-traitants éventuels.</p>
    <p>Aucune donnée à caractère personnel n'est transmise à des tiers ne faisant pas partie des destinataires mentionnés ou ne relevant pas du cadre juridique indiqué, sans préjudice de leur éventuelle transmission aux organes chargés d'une mission de contrôle ou d'inspection en application du droit belge, tel qu'un juge d'instruction.</p>
    <p>Ni {commune}, ni iMio ni ses sous-traitants ne divulguent de données à caractère personnel à des tiers à des fins de marketing direct.</p>
    <h2>V. Combien de temps vos données sont-elles conservées?</h2>
    <p>Pour les besoins du traitement des services, vos données sont conservées aussi longtemps que vous êtes inscrit dans l'e-guichet. Elles peuvent être supprimées, sauf si une enquête est en cours (les données seront alors conservées pendant le temps nécessaire à la conclusion de l’enquête), sur simple base d’une demande de votre part.</p>
    <h2>VI. Comment consulter vos données, en vérifier l'exactitude et, au besoin, les corriger?</h2>
    <p>Vous avez le droit de demander à tout moment une copie de vos données à caractère personnel pour vérifier l'exactitude des informations qui sont conservées et/ou pour les corriger ou les mettre à jour. Vous pouvez aussi demander que vos données à caractère personnel soient totalement effacées si aucune demande de votre part n'est en cours de traitement.</p>
    <p>Pour garantir le respect de votre vie privée et assurer votre sécurité, nous prendrons les mesures nécessaires pour vérifier votre identité avant de vous permettre de consulter, et éventuellement de corriger, des données.</p>
    <p>Veuillez envoyer vos demandes à [adresse électronique du DPO du pouvoir local].</p>
    <h2>VII. Quels sont les moyens que nous mettons en œuvre pour éviter tout abus ou accès non autorisé?</h2>
    <p>{commune} a mis en place un certain nombre de procédures (matérielles, électroniques et administratives), qu'il réévalue et actualise régulièrement, afin de protéger ces données contre tout accès non autorisé, d’en assurer la sécurité et de garantir l’utilisation correcte des informations recueillies en vue de réaliser le traitement concerné.</p>
    <p>Vos données sont conservées sur le serveur d'iMio avant d'être traitées.</p>
    <p>Les sous-traitants extérieurs ont signé un contrat avec {commune} et iMio en vertu duquel il sont légalement tenus de respecter la législation applicable en matière de protection et de traitement des données à caractère personnel, et plus précisément le Règlement (UE) 2016/679 du Parlement européen et du Conseil du 27 avril 2016 (aussi connu sous l’acronyme RGPD).</p>
    <p>Le personnel de {commune} et d'iMio qui a accès à des informations permettant d'identifier des personnes est tenu de protéger ces informations conformément à la présente déclaration relative à la protection des données à caractère personnel, et notamment en s'abstenant d'utiliser ces informations à des fins autres que la prestation des services qu'il est censé assurer.</p>
    <h2>VIII. À qui adresser des questions ou des plaintes?</h2>
    <p>Pour consulter, supprimer (dans certains cas) ou corriger les informations à caractère personnel vous concernant, veuillez contacter: le responsable du traitement des données via [adresse électronique du DPO du pouvoir local]</p>
    <p>En cas de litige, les plaintes peuvent être adressées au Délégué à la Protection des Données de l’administration communale ou au l’Autorité Locale Belge en charge de l’application de la protection des données.</p>
    """
    return gdpr_html_content


def get_cookie_policy_content():
    cookie_policy_html = """
    <h1>Politique d'utilisation des cookies</h1>
    <p>Les cookies sont des petits fichiers enregistrés sur votre appareil lorsque vous visitez un site internet. Les cookies contiennent des informations qui permettent d'identifier les utilisateurs et de retenir leurs préférences. Les cookies disposent généralement d'une date d'expiration.</p>
    <h2>Utilisation des cookies</h2>
    <p>Ce site web utilise des cookies de deux types :</p>
    <ul>
        <li>cookies essentiels</li>
        <li>cookies fonctionnels</li>
    </ul>
    <p>Les cookies essentiels sont requis pour une utilisation normale de ce site internet et ne peuvent dès lors pas être désactivés. Ces cookies permettent de répartir la charge sur nos serveurs (technique du load balancing), d'authentifier les utilisateurs et d'enregistrer leurs préférences en matière de cookies.</p>
    <h2>Cookies essentiels</h2>
    <p>Les cookies essentiels sont nécessaires au bon fonctionnement de ce site internet et ne peuvent donc pas être bloqués.</p>
    <ul>
        <li><strong>cc_cookie_accept</strong><br>Ce cookie enregistre les préférences de l'utilisateur quant au traitement des cookies. Sa validité est de deux ans.</li>
        <li><strong>serverid</strong><br>Ce cookie permet l'application d'une technique de load balancing sur nos serveurs. Il expire à la fermeture du navigateur.</li>
        <li><strong>__ac</strong><br>Ce cookie authentifie les utilisateurs du site. Il expire à la fermeture du navigateur.</li>
    </ul>
    <h2>Cookies fonctionnels</h2>
    <p>Les cookies fonctionnels sont employés pour retenir vos préférences en matière de langue sur un site multilingue. D'autres cookies fonctionnels peuvent également être enregistrés par des tiers lorsque le gestionnaire du site intègre des contenus externes comme des vidéos.</p>
    <p>Refuser ces cookies bloquera l'affichage de ces contenus externes.</p>
    <h3>I18N_LANGUAGE</h3>
    <p>Ce cookie enregistre les préférences de langue de l'utilisateur. Il expire à la fermeture du navigateur.</p>
    <h3>Cookies issus de YouTube</h3>
    <p>Nous utilisons YouTube pour encapsuler des vidéos sur le site. YouTube suit les actions des utilisateurs au moyen de cookies pour fournir des statistiques et des produits publicitaires.</p>
    <ul>
        <li>1P_JAR (1 mois)</li>
        <li>ANID (9 mois)</li>
        <li>APISID (2 ans)</li>
        <li>CONSENT (10 ans)</li>
        <li>COMPASS (3 jours)</li>
        <li>HSID (2 ans)</li>
        <li>NID (6 mois)</li>
        <li>SAPISID (2 ans)</li>
        <li>SID (2 ans)</li>
        <li>SIDCC (1 an)</li>
        <li>SSID (2 ans)</li>
        <li>__Secure-3PAPISID (2 ans)</li>
        <li>__Secure-3PSID (2 ans)</li>
        <li>__Secure-3PSIDCC (1 an)</li>
    </ul>
    <h2>Gestion et suppression des cookies</h2>
    <p>Tous les navigateurs offrent la possibilité de retrouver et de supprimer les cookies installés sur une machine. Ces fonctionnalités sont disponibles dans les préférences du navigateur au sein d'une section généralement intitulée Vie privée ou Sécurité.</p>
    <p>Vous avez par ailleurs la possibilité de supprimer automatiquement les cookies en utilisant la navigation privée de votre navigateur.</p>
    <p>Pour supprimer rapidement les cookies, certains navigateurs (Firefox, Chrome, Edge, Internet Explorer) proposent un raccourci clavier par l'appui simultané sur les touches CTRL/CMD, MAJ et DELETE.</p>
    """
    return cookie_policy_html
