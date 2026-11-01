"""Construit la version publique (kreonpaysage.com) à partir de la page publiée dans Claude.
Usage : python3 build_public.py <page_live.html> <dossier_repo> [url_formulaire]"""
import sys,re,shutil,os
src,repo=sys.argv[1],sys.argv[2];kform=sys.argv[3] if len(sys.argv)>3 else ''
s=open(src,encoding='utf-8').read()
# 1. retirer l'enveloppe de l'hébergeur Claude
i=s.find('<body>\n<!doctype html>')
if i>=0:
  s=s[i+len('<body>\n'):]
  s=re.sub(r'\n*</body></html>\s*$','\n',s)
def rep(a,b,n=1):
  global s
  c=s.count(a)
  if c!=n: sys.exit('ancre introuvable (%d) : %r'%(c,a[:80]))
  s=s.replace(a,b)
# 2. SEO + domaine
rep('<title>KREÖN</title>','<title>KREÖN · Hydroensemencement et paysage à Alès, dans le Gard</title>\n<meta name="description" content="Hydroensemencement, préparation de terrain et arrosage automatique connecté à Alès et dans tout le Gard (90 km). Gazon dès 2,50 € HT/m², talus, prairie fleurie. Demande de devis en ligne.">\n<link rel="canonical" href="https://kreonpaysage.com/">\n<meta property="og:title" content="KREÖN · Hydroensemencement et paysage dans le Gard">\n<meta property="og:description" content="Gazon, talus anti-érosion, prairie fleurie et arrosage connecté, à Alès et 90 km autour.">\n<meta property="og:image" content="https://kreonpaysage.com/img/kreon-hero-1672.webp">\n<meta property="og:url" content="https://kreonpaysage.com/">\n<link rel="icon" href="logo-160.png">')
s=s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
# 3. envoi des formulaires vers le tableau Google quand le site tourne hors de Claude
pub='''<script>
window.KFORM=%r;
(function(){if(!(window.claude&&window.claude.use))document.documentElement.classList.add('kpub')})();
function kPost(col,data,cb){if(!window.KFORM){cb({ok:false});return}
  try{fetch(window.KFORM,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify({col:col,data:data,page:location.href})}).then(function(){cb({ok:true,id:'web-'+Date.now().toString(36),slotOk:true,web:true})},function(){cb({ok:false})})}catch(e){cb({ok:false})}}
</script>
<style>html.kpub a[href="#mon-espace"],html.kpub a[href="#equipe"],html.kpub a[href="#gestion"]{display:none!important}</style>
</head>'''%kform
rep('</head>',pub)
rep("  if(!DB||!USER){cb({ok:false});return}\n  USER.id().then(function(uid){\n    if(!uid){cb({ok:false});return}\n    var ref=DB.doc('demandes/'+uid);",
    "  if(!DB||!USER){kPost('demandes',data,cb);return}\n  USER.id().then(function(uid){\n    if(!uid){cb({ok:false});return}\n    var ref=DB.doc('demandes/'+uid);")
rep("  if(!DB||!USER){cb({ok:false});return}\n  USER.id().then(function(uid){if(!uid){cb({ok:false});return}DB.doc(col+'/'+uid).set(data)",
    "  if(!DB||!USER){kPost(col,data,cb);return}\n  USER.id().then(function(uid){if(!uid){cb({ok:false});return}DB.doc(col+'/'+uid).set(data)")
rep("document.title=(p==='home'?'KREÖN':","document.title=(p==='home'?'KREÖN · Hydroensemencement et paysage à Alès, dans le Gard':")
os.makedirs(repo,exist_ok=True)
open(os.path.join(repo,'index.html'),'w',encoding='utf-8').write(s)
print('index.html',len(s),'KFORM' if kform else 'sans formulaire (mode démo)')
