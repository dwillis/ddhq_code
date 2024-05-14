from emailnetwork.extract import *
from datetime import datetime
from email.utils import getaddresses
from mailbox import mbox
import html2text
import csv
import re

from mailbox import mboxMessage

from emailnetwork.utils import clean_subject, clean_body
from emailnetwork.emails import EmailAddress, EmailMeta, EmailBody
from emailnetwork.summary import DomainSummary
from emailnetwork.extract import extract_body, extract_meta

from emailnetwork.header import HeaderCounter

from urlextract import URLExtract
extractor = URLExtract()

reader = MBoxReader("/Volumes/LaCie2/ddhq/Takeout/Mail/All mail Including Spam and Trash.mbox")

textmaker = html2text.HTML2Text()
textmaker.ignore_links = True

urls = []

with open("dpwillis67_emails_with_body_new.csv", "w") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['name', 'email', 'subject', 'date', 'year', 'month', 'day', 'hour', 'minute', 'domain', 'body', 'party', 'disclaimer'])
    for email in reader.mbox:
        meta = extract_meta(email)
        try:
            body = extract_body(email)
            body = " ".join(body.body.split())
            body = textmaker.handle(body).replace('\u200c','').replace('  ',' ').replace('\n','')
            url_list = list(set(re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', body)))
            for url in url_list:
                if url not in urls:
                    urls.append(url)
            if "paid for by" in body.lower() or "paid for and" in body.lower():
                disclaimer = True
            else:
                disclaimer = False
            if 'actblue.com' in body:
                party = 'D'
            elif 'ngpvan.com' in body:
                party = 'D'
            elif 'winred.com' in body:
                party = 'R'
            elif 'anedot.com' in body:
                party = 'R'
            elif meta.origin_domain in ['standupforliberty.net', 'rightusa.org', 'victory.donaldtrump.com', 'rightwave.org', 'bestamericanow.com', 'ourdefenseofamerica.com', 'saveamericamajority.com', 'makingamericathegreatest.com',
            'win.donaldjtrump.com', 'nhgop.org', 'mattgaetzforflorida.com', 'greatamericaupdate.com', 'e.prolifeupdate.com', 'conservativevictory2020.net', 'updates.conservativeintel.com', 'pelosi4never.com', 'stoppingsocialistdems.com',
            'itsourgreatamerica.com', 'kamala4never.com', 'standingstrongamerica.com', 'rightsideamerica.com', 'marcorubio.com', 'campaigns.rnchq.com', 'voterickscott.com', 'hawleyformo.com', 'katforcongress.com', 'conservativesdefendingfreedom.com',
            'lauraloomerforcongress.com', 'drmillermeeks.com', 'americansfordjt.com', 'indiana.gop', 'teapartypatriots.org', 'e.deroymurdock.com', 'republicanemails.org', 'chabotforcongress.com', 'nicolemalliotakis.com', 'wisgop.org',
            'bencarson.com', 'tedcruz.org', 'deskofdonaldjtrump.com', 'ericgreitens.com', 'chuckmorsefornh.com', 'wesleyfortexas.com', 'holcombforindiana.com', 'alekskarlatosforcongress.com', 'ourbestamericanow.com', 'alert.republicantaskforce.com',
            'action4liberty.com', 'lahoodforcongress.com', 'yeslivegaforvirginia.com', 'e.conservativefwd.com', 'aadlandforcolorado.com', 'reclamingamericanfreedom.com', 'nc.gop', 'joshmandel2022.com', 'katiebrittforsenate.com',
            'doctoroz.com', 'jdforohio.org', 'newsletter.conservativedirect.com', 'robportman.com', 'nicoleforny.com', 'backingamerica.com', 'victory.kansansformarshall.com', 'email.rondesantis.com', 'philscott.org', 'janetimkenforohio.com',
            'feenstraforcongress.com', 'email.donaldtrump.com', 'garbarinoforny.com', 'trump2016.com', 'joelombardofornv.com', 'markronchetti.com', 'm.jimrenacci.com', 'gregpenceforcongress.com', 'chrischristie.com', 'tedbudd.com',
            'kleefischforwigov.com', 'nhsenaterepublicans.com', 'leahvukmir.com', 'susancollins.com', 'wesleyhuntfortexas.com', 'claudiaforcongress.com', 'houseconservatives.com', 'burchettforcongress.com', 'sheddforaz.com', 'buddfornc.com',
            'barnetteforsenate.com', 'tomcotton.com', 'mwaltzforcongress.com', 'gibbonsforohio.com', 'loomered.com', 'email.jeb2016.com', 'hungforcongress.com', 'randpaul2016.com', 'crenshawforcongress.com', 'speakerryan.com', 'letsgo-brandon.net',
            'jakeevans.org', 'colinschmitt.com', 'donaldtrump.com', 'greitens4missouri.com', 'billolsonfl.com', 'mikebraunsenate.com', 'kellyforsenate.com', 'greene2020.com', 'heidistjohnforcongress.com', 'msgop.co', 'magaactionalert.com',
            'durantforsenate.com', 'action.supportstevedaines.com', 'rondesantis.com', 'randpaul.com', 'jacksonlahmeyer.com', 'mcguireforvirginia.com', 'donaldjtrump.com', 'gopteam.gop', 'amandamakkiforcongress.com', 'melissamartz.com',
            'joekentforcongress.com', 'teamhagerty.com', 'lindseygraham.com', 'jimbanks.us', 'billcoleforwv.com', 'ciscomaniforaz.com', 'bartosforsenate.com', 'ricksantorum.com', 'dahmforsenate.com', 'mobrooks.com', 'geoffdiehl.com',
            'schellerforcongress.com', 'schmidtforkansas.com', 'iesp.conservativesgive.com', 'iesp.conservativelibertywire.com', 'baxterforcongress.com', 'greitensformo-mail.com', 'billbryantforgovernor.com', 'email.nancymace.org', 'deanhellerforgov.com',
            'briandahle.com', 'gaetz4usa.com', 'amandamakki.com', 'victoryacrossamerica.gop.com', 'millermeeks2020.com', 'kellyschulzforgovernor.com', 'fredkellerforcongress.com', 'jonesforgeorgia.com', 'tedbudd.gop', 'miketurnerforohio.com',
            'haroldearls.org', 'az.kelliward.com', 'rnchq.com', 'hartzlerforsenate.org', 'mariaelvirasalazar.com', 'jamesonellis.com', 'defenddjt.com', 'stevechabot.com', 'keepingamericagreatalerts.com', 'kleefisch4wisconsin.com', 'grassleyworks.com',
            'ultramagapatriots.org', 'tedbudd.co', 'mowersforcongress.com', 'mail.donaldjtrump.com', 'johncastorani.com', 'huntfortexas.com', 'electjimjordan.com', 'christiancollins.org', 'latinosfortrump.us', 'brycereeves.com', 'brianfitzpatrick.com',
            'email.donaldjtrump.com', 'youngkinforgovernor.com', 'ultramagapatriot.org', 'mikebraunforindiana.com', 'joearpaioformayor.com', 'dolanforohio.com', 'smileyforwashington.com', 'michaelguest.ms', 'opt.scottwalker.org', 'marshablackburn.com',
            'janicemcgeachin.com', 'carlasands.com', 'votejohngibbs.com', 'm.caitlynjenner.com', 'ruleoflawrepublicans.com', 'mikehuckabee.com', 'freedomtrainalert.com', 'dolanforsenate.com', 'dominicforct.us', 'seanspicer.com', 'trumptrainnews.com', 'email.a1warroom.com',
            'e.goppresidential.com', 'finstadforcongress.com', 'wisconsinrepublicanparty.com', 'unleashamericapac.co', 'wisconsin-republicans.com', 'info.donaldjtrump.com', 'email.nikkihaley.com', 'brandonforcongressny22.com', 'act.marcorubio.com',
            'action.supportsenatorcotton.com', 'action.tomkean.com', 'adamlaxalt.com', 'alekfororegon.com', 'alekskarlatos.com', 'allanfung.com', 'andyogles.com', 'contact.tomcotton.com', 'coachtuberville.com', 'ciscomaniforarizona.com',
            'chuckedwardsnc.com', 'cheneyforwyoming.com', 'carlosgimenezforcongress.com', 'calvertforcongress.com', 'byrondonalds.com', 'dougmastriano.emailnb.com', 'donalds4congress.com', 'dancoxforgovernor.com', 'cwherbster.com', 'dannewhouse.com',
            'davemccormickpa.com', 'davidperduega.com', 'davidschweikert.com', 'deanheller.com', 'drpaulgosar.com', 'drscottjensen.com', 'duceyforgovernor.com', 'electbergmann.com', 'eliforarizona.com', 'eliseforcongress.com', 'email-huntforcongress.com',
            'email-kellycraft.com', 'email.blakemasters.com', 'email.give2laxalt.com', 'email.give2rubio.com', 'email.glenngrothman.com', 'email.helpherschel.com', 'email.jasonforvirginia.com', 'email.johngibbsemail.com', 'email.marshablackburn.com',
            'email.miyares-for-virginia.com', 'email.saveamerica45.com', 'email.votedarinlahood.com', 'eml.scottwalker.org', 'friendsofrondesantis.com', 'georgesantos.org', 'georgesantosforcongress.org', 'glenngrothman.com', 'gophouseconservatives.com',
            'gregformontana.com', 'gregorycoll.com', 'hagemanforwyoming.com', 'heidiganahl.com', 'illinois.gop', 'info.joshmandel2022.com', 'info.standforamericapac.com', 'iowagop.org', 'jakelaturner.com', 'jakelaturnerforcongress.com', 'jaromebellforcongress.com',
            'jasonforvirginia.com', 'jennifer-ruthgreen.com', 'jerrycarlupdates.com', 'jiminhofe.com', 'joekentforcongress.com', 'johncornyn.com', 'join.lindseygraham.com', 'joshbrecheen.com', 'juanciscomani.com', 'kathybarnette.com', 'kellyforak.com',
            'kellyloeffler.com', 'kellyschulzforgovernor.com', 'attaforcongress.com', 'mariaelvira4congress.com', 'mariaelvirasalazar4congress.com', 'mattgaetz.com', 'matthewfoldi.com', 'mattmowers.com', 'mattmowersfornh.com', 'mccloskeyformissouri.com',
            'mccloskeyforsenate.com', 'chaseforva.com', 'banksforsenate.com', 'teammorrisey.com', 'steil4congress.com', 'email.claudiatenneyforcongress.com', 'despositoforcongress.com', 'tateforourstate.com', 'ne.gop', 'jenforcongress.com', 'neilforarkansas.com',
            'info.houseconservativestrust.com', 'courtneygeelsforcongress.com', 'greatergeorgia.com', 'email.doug4gov.com', 'thehousegop.org', 'g4yamerica.com', 'mikeforwisconsin.com', 'outreach.mattjacobsforcongress.com', 'nationalrepublicanpolling.com',
            'savecarolina.org', 'americanupdate.com', 'e.americandefensenews.com', 'iesp.freedomnationtoday.com', 'e.americanactionnews.com', 'freedomfirstalert.com', 'e.americanbriefing.com', 'iesp.defend-the-constitution.org', 'americasnewsletter.com',
            'email.freethinkerdaily.com', 'email.freethinkerdaily.com', 'victory.votegaryblack.com', 'wsrp.org', 'right-gop.com', 'gopwin.org', 'houseconservatives.org', 'fitzgerald4congress.com', 'outreach.tomkean.com', 'anamericaunited.org', 'electsalazar.com',
            'email.jjforcongress.com', 'mail.rocaforcongress.com', 'salazarforflorida.com', 'robortt.com', 'nickforva.com', 'victory.donaldjtrump.com', 'vivek2024.com', 'updates.hageman4wyoming.com', 'votemichelsforgov.com', 'senateconservatives.com', 'support.donaldjtrump.com',
            'salazar4florida.com', 'mariaforflorida.com', 'fallon4texas.com', 'hungcaoforva.com', 'hernforcongress.com', 'teamfeenstra.com', 'wesley4texas.com', 'walker4nc.com', 'ciscomaniforcongress-mail.com', 'greitensforsenate-mail.com', 'electroddorilas.com',
            'email.trustinthemission.com', 'billposey.com', 'nancymace.org', 'nehlsforcongress.com', 'kenpaxtontx.com', 'mogop.net', 'bricewiggins.ms', 'rocaforcongress.com', 'greitensformissouri-email.com', 'missourigop.net', 'fallon4congress.com', 'mail.chrischristie.com',
            'steilforwisconsin.com', 'act.mikeforwisconsin.com', 'russellfrysc.com', 'stopstacey.org', 'tellitlikeitispac.com', 'action.morriseyforwv.com', 'steilforcongress-email.com', 'donatetorondesantis.com', 'sg.votetimaalders.com', 'bo4nc.com', 'teamherschel.com',
            'friendsofyeslivega.com', 'spartzforcongress.com', 'teamlaxalt.com', 'team.donaldtrump.com', 'thefloridagop.com', 'yeslivega.com', 'berniemorenoforohio.com', 'email.jdvance.com', 'team-cotton.com', 'trump.winwith45.com', 'cottonemails.com', 'gopactionalert.com',
            'rightwaypress.com','thegopreport.com', 'alert.keepcongressrepublican.com', 'johndeatonforsenate.com', 'gopactionalert.com', 'goppresidential.com', 'tedcruz.org', 'contact.jenforcongress.com', 'teamjimjordan.com', 'patharriganforcongress.com', 'email.donjr.com',
            'finstadforcongress.com', 'rogersforsenate.com', 'email.nancyforalaska.com', 'wisconsin-gop.com', 'conservativesfordjt.com', 'carmengoers.org', 'davisforin.com', 'robertsonforcongress.com', 'brandonherreraforcongress.com', 'win.donjr.com', 'jjforcongress.com',
            'tombarrettforcongress.com', 'mcguireva.ccsend.com', 'yvetteherrell.com', 'conforti4congress.com', 'email.scottfitzgeraldforcongress.com', 'katforcongress.ccsend.com', 'mcguireva.com', 'paulhudsonforcongress.ccsend.com', 'rajuforcongress.com', 'electgabeevans.com',
            'teichertformaryland.com', 'nancyforalaska.com', 'castellifornc.com', 'donate.lawlerforcongress.com', 'nixonforga.com', 'paulhudsonforcongress.com', 'wesleyhunttx.com', 'baughforcongress.com', 'carolinekaneforcongress.com', 'dolanforohio.ccsend.com', 'paulgosaraz.com',
            'drewfornevada.com', 'emordforva.com', 'join.electjimjordan.com', 'contact.electjimjordan.com', 'johnduarteforcongress.com', 'lawlerforcongress.com', 'lorichavezderemerforcongress.com', 'robforpa.com', 'crouchforindiana.com', 'email.donjr.com', 'ericearly.com',
            'migop.org', 'email.chuckmorsefornh.com', 'email.georgeloganforcongress.com', 'mail.markwalkerfornc.com', 'join.djtfp24.com', 'mail.larryhogan.com', 'lorichavezderemer.com']:
                party = 'R'
            elif meta.origin_domain in ['dscc.org', 'hillaryclinton.com', 'emilyslist.org', 'democrats.org', 'betoorourke.com', 'jayinslee.com', 'elizabethwarren.com', 'e.markkelly.com', 'dccc.org', 'e.ronbegone.com', 'e.johnfetterman.com',
            'mcauliffeoffice.org', 'stantonforarizona.com', 'vanhollen.org', 'joebiden.com', 'e.cheribeasley.com', 'drraulruiz.com', 'timkaine.com', 'e.giffords.org', 'stevesisolak.com', 'primarysinema.com', 'e.staceyabrams.com', 'dflhouse.com',
            'tndp.org', 'wolfforpa.com', 'azdem.org', 'e.welchforvermont.com', 'unitedemocrats.org', 'berniesanders.com', 'leftaction.com', 'dwsforcongress.com', 'karenbass.com', 'whendemocratsturnout.com', 'jessicacisnerosforcongress.com',
            'e.morganharper.org', 'marcusforgeorgia.com', 'indems.org', 'e.alex-padilla.com', 'mondaireforcongress.com', 'marcykaptur.com', 'dlcc.org', 'e.votevets.org', 'douggansler.com', 'martinheinrich.com', 'corybooker.com', 'dga.net',
            'valdemings.com', 'ocasiocortez.com', 'michaelbennet.com', 'roycooper.com', 'edmarkey.com', 'e.adamschiff.com', 'ralphnortham.com', 'katiemcginty.com', 'mikethompsonforcongress.com', 'andrewgillum.com', 'donatetohealey.com',
            'mckaylawilkes.com', 'e.alessandrabiaggi.com', 'tomsteyer.com', 'action.rosenfornevada.com', 'staceyabrams.com', 'algreen.org', 'tinaforminnesota.com', 'maggiehassan.com', 'benraylujan.com', 'kamalaharris.org', 'rushernbaker.com',
            'kirstengillibrand.com', 'act.democrats.org', 'menendezfornj.com', 'markwarnerva.com', 'timforoh.com', 'marcolopez.com', 'kinacollins.com', 'darrigo2022.com', 'votedrbob.com', 'odessaforcongress.com', 'voteforlinda.com', 'kenrussellforfloridaemail.com',
            'wvdemocrats.com', 'e.tonyevers.com', 'dnc.org', 'warnockforgeorgia.com', 'newmexicansformichelle.com', 'richardblumenthal.com', 'jeffmerkley.com', 'fladems.com', 'johncarney.org', 'lipinskiforcongress.com', 'sarahkleehoodny.com',
            'nidaallam.com', 'marktakano.com', 'email.mikebloomberg.com', 'joesestak.com', 'susieleeforcongress.com', 'frankenforiowa.org', 'timryanforcongress.com', 'tonycardenas.com', 'ritahart.com', 'wesmoore.com', 'saragideon.com',
            'billpascrell.com', 'walzforgovernor.org', 'tomperez.com', 'saludcarbajal.com', 'unitedruraldemocrats.org', 'pattymurray.com', 'e.timryanforamerica.com', 'abigailspanberger.com', 'ginaraimondo.com', 'stevebullock.com', 'leahyforvermont.com',
            'e.gavinnewsom.com', 'bradpfaff.com', 'americanbridge.org', 'abbyfinkenauer.com', 'johndelaney.com', 'bobcasey.com', 'jbpritzkercampaign.com', 'franchot.com', 'e.tammybaldwin.com', 'jontester.com', 'e.protectvoting.org', 'replacesinema.com',
            'sherrodbrown.com', 'e.mandelabarnes.com', 'lucasformo.com', 'chrissyhoulahanforcongress.com', 'katieporter.com', 'email.jahanahayes.com', 'lucasformo.com', 'act.democrats.org', 'democraticsecretaries.org', 'sethmagaziner.com', 'e.coribush.org',
            'rashidaforcongress.com', 'josh4congress.com', 'brittanypettersen.com', 'adamforcolorado.com', 'adamschiff.com', 'andreasalinasfororegon.com', 'andybeshear.com', 'andykimforcongress.com', 'andylevinforcongress.com', 'annettetaddeo.com',
            'charliecrist.com', 'catherinecortezmasto.com', 'carrickflynnfororegon.com', 'casarforcongress.com', 'brandonpresley.com', 'dickdurbin.com', 'debbiewassermanschultz.com', 'davidtrone.com', 'dankildee.com', 'dangoldmanforny.com', 'drkimschrier.com',
            'durbinforsenate.com', 'e.charlesbooker.org', 'e.chrismurphy.com', 'e.collierfortexas.com', 'e.dangoldmanforag.com', 'e.dankildee.com', 'e.dwspac.com', 'e.elissaslotkin.org', 'e.gallegoforarizona.com', 'e.ilhanomar.com', 'e.ryanforamerica.com',
            'e.timforoh.com', 'e.timforoh.org', 'e.wesmoore.com', 'e.wileynickelforcongress.com', 'e.wisdems.org', 'electhoulahan.com', 'elissaforcongress.com', 'email.ericswalwell.com', 'email.jahanahayes.com', 'emiliasykesforcongress.com', 'filemonvelaforcongress.com',
            'floridadems.org', 'frostforcongress.com', 'garamendi.org', 'garamendiforcongress.org', 'giffords.org', 'gretchenwhitmer.com', 'gwenmooreforcongress.com', 'halaforvirginia.com', 'haleystevensforcongress.com', 'harderforcongress.com', 'hello.hickenlooper.com',
            'herringforag.com', 'hickenlooper.com', 'hillaryscholten.com', 'ilhanomar.com', 'jayinslee.com', 'jazzlewis.com', 'jenniferwexton.com', 'jessicacisneros.org', 'jessicacisnerosforcongress.com', 'jimcosta.emailnb.com', 'jimmypanetta.com', 'johnfetterman.com',
            'johnkingforgovernor.com', 'joshshapiro.org', 'kathymanningfornc.com', 'keithellison.org', 'landsmanforcongress.com', 'lashrecseaird.com', 'lisabluntrochester.com', 'mail.elizabethwarren.com', 'marcykaptur.com', 'massdems.org', 'maxinewatersforcongress.com',
            'jamesforny.com', 'ninaforphilly.com', 'tamiewilson.com', 'contact.joebiden.com', 'tammybaldwin.com', 'padems.com', 'ourrevolution.org', 'gahousedems.com', 'kennedydemocratspa.com', 'derekkilmer.com', 'brendaforvermont.com', 'newpaproject.org',
            'jared.vote', 'e.miaforsc.com', 'dejaforpa.com', 'barriertoentry.org', 'traindemocrats.org', 'quarteyforcongress.com', 'sarahforwisconsin.com', 'ourrevolution.org', 'her-time.com', 'wilmotcollins.com', 'collectivepac.org', 'ericforillinois.com',
            'upsetsetup.org', 'emilyformichigan.com', 'emergeamerica.org', 'marlinga4congress.com', 'michellefortx15.com', 'ballardformontana.com', 'tomohalleran.com', 'coribush.org', 'gabeforcongress.com', 'trudybuschvalentine.com', 'jaredforflorida.com',
            'tinafororegon.com', 'ehaszforcongress.com', 'valeriefoushee.com', 'votewillrollins.com', 'wileynickelforcongress.com', 'malcolmkenyatta.com', 'sethmoulton.com', 'e.angelaalsobrooks.com', 'tishjames.com', 'ricklarsen.org', 'unitethecountry.com',
            'maggietoulouseoliver.com', 'caraveoforcongress.com', 'votecharlesgraham.com', 'wildforcongress.com','ninaturner.com', 'torres.nyc', 'email.margaretgood.com', 'polisforcolorado.com', 'castelliforcongress.com', 'email.bobcasey.com', 'vademocrats.org',
            'ronkind.org', 'terrisewellforcongress.com', 'sarajacobsforca.com', 'lizziefletcher.com', 'ohiodems.org', 'rebekahjonescampaign.com', 'terrymcauliffe.com', 'cadem.org', 'wydenforsenate.com', 'bookerforkentucky.com', 'georgiademocrat.org', 'joshrileyforcongress.com',
            'fightforreform.org', 'mail.blueampaction.com', 'padoraforcongress.com', 'e.elizabethwarren.com', 'edwardsforhouston.com', 'dlcc.org', 'canningforcongress.com', 'mayberryforcongress.com', 'betsyrader4ohio.com', 'derekmarshallca.com', 'e.hillharper.com',
            'tamieforcongress.com', 'cedarkeyprogress.com', 'davemin.com', 'tamiewilson.org', 'e.qasimforcongress.org', 'lauraforcongress.org', 'marquitabradshaw.com', 'jobyforcongress.com', 'nikkiforcongress.com', 'quacysmithforcongress.com', 'christianforohio.com',
            'andykim.com', 'davidcanepa.com', 'davidkimforca.com', 'valhoyle.com', 'organizetexas.org', 'mail.lateefahsimon.com', 'suozziforcongress2024.com', 'canningfororegon.com', 'martydolanforcongress.com']:
                party = 'D'
            elif meta.origin_domain in ['teamkennedy.com', 'cornelwest2024.com']:
                party = 'I'
            else:
                party = None

        except:
            body = None
            party = None
            disclaimer = None
        if meta.date:
            writer.writerow([meta.sender.name, meta.sender.email, meta.subject, str(meta.date), meta.date.year, meta.date.month, meta.date.day, meta.date.hour, meta.date.minute, meta.origin_domain, body, party, disclaimer])
        else:
            writer.writerow([meta.sender.name, meta.sender.email, meta.subject, None, None, None, None, None, None, meta.origin_domain, body, party, disclaimer])

with open("email_urls.csv", "w") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['url'])
    writer.writerows(urls)
