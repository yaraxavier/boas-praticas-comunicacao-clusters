#!/usr/bin/env python3
"""Gera página estática desta documentação, sem dependências externas.
Renderizador restrito ao subconjunto Markdown usado neste repositório.
"""
from pathlib import Path
import html,re,shutil
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
CHAPTERS=[('guia','Guia de leitura','docs/README.md'),('modelo','Modelo geral','docs/modelo/MODELO_GERAL.md'),('referencia','GovHub, MGI e Ipea','docs/modelo/REFERENCIA_GOVHUB.md'),('arquitetura','Arquitetura A–B','docs/poc/ARQUITETURA.md'),('decisoes','Decisões','docs/02-registro-decisoes.md'),('checklist','28 práticas','docs/01-checklist-modelo.md'),('operacao','Operação','docs/poc/OPERACAO.md'),('testes','Testes e resultados','docs/poc/TESTES_E_RESULTADOS.md'),('revisoes','Revisões','docs/poc/REVISOES.md'),('fontes','Fontes originais','docs/FONTES.md'),('publicacao','Publicação','PUBLICACAO.md'),('agentes','AGENTS.md','AGENTS.md')]
TARGETS={(ROOT/p).resolve():i for i,_,p in CHAPTERS}
ASSETS=DOCS/'assets';ASSETS.mkdir(exist_ok=True)
def url(href,source):
    if href.startswith(('https://','http://','#','mailto:')):return href
    target=(source.parent/href.split('#')[0]).resolve()
    if target in TARGETS:return '#'+TARGETS[target]
    if target.name=='README.md' and '2026-10-09-instalacao-limpa' in target.parts:return '#evidencias'
    if target.is_file() and target.is_relative_to(ROOT):
        dest=ASSETS/target.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(target,dest)
        return dest.relative_to(DOCS).as_posix()
    if target.is_dir():return '#evidencias'
    return href

def inline(s,source):
    s=html.escape(s)
    # Images use evidence cards below; plain Markdown images elsewhere get normal rendering.
    s=re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',lambda m:'<img class="full" alt="'+m[1]+'" src="'+html.escape(url(html.unescape(m[2]),source),quote=True)+'">',s)
    s=re.sub(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)',lambda m:'<a href="'+html.escape(url(html.unescape(m[2]),source),quote=True)+'">'+m[1]+'</a>',s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    return s

def render(source):
    lines=source.read_text().splitlines();out=[];i=0
    while i<len(lines):
        l=lines[i]
        if not l.strip():i+=1;continue
        if l.startswith('```'):
            language=l[3:].strip();i+=1;block=[]
            while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
            if language=='mermaid':
                out.append('<div class="architecture"><strong>Cluster A · sbd-app</strong><p>Job reader → HTTPS / NodePort 30200 → OpenBao em B</p><strong>Cluster B · sbd-bao</strong><p>OpenBao → HTTPS 6443 / TokenReview → API Kubernetes de A</p><p>PebbleDB e auditoria em volume efêmero de B. Administração via port-forward local.</p></div><details><summary>Diagrama Mermaid para GitHub</summary><pre>'+html.escape('\n'.join(block))+'</pre></details>')
            else:out.append('<pre><code>'+html.escape('\n'.join(block))+'</code></pre>')
            i+=1;continue
        if l.startswith('|'):
            table=[]
            while i<len(lines) and lines[i].startswith('|'):table.append(lines[i]);i+=1
            out.append('<div class="table"><table>')
            for j,row in enumerate(table):
                if re.fullmatch(r'[| :\-]+',row):continue
                tag='th' if j==0 else 'td'
                out.append('<tr>'+''.join('<'+tag+'>'+inline(c.strip(),source)+'</'+tag+'>' for c in row.strip('|').split('|'))+'</tr>')
            out.append('</table></div>');continue
        m=re.match(r'^(#{1,6}) (.*)',l)
        if m:
            level=min(len(m[1])+1,6);out.append(f'<h{level}>'+inline(m[2],source)+f'</h{level}>');i+=1;continue
        if re.match(r'^(- |\d+\. )',l):
            ordered=bool(re.match(r'^\d+\.',l));tag='ol' if ordered else 'ul';out.append('<'+tag+'>')
            while i<len(lines) and re.match(r'^(- |\d+\. )',lines[i]):out.append('<li>'+inline(re.sub(r'^(- |\d+\. )','',lines[i]),source)+'</li>');i+=1
            out.append('</'+tag+'>');continue
        p=[l];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|- |\d+\. )',lines[i]):p.append(lines[i]);i+=1
        out.append('<p>'+inline(' '.join(p),source)+'</p>')
    return '\n'.join(out)

def main():
    sections=[]
    for ident,title,path in CHAPTERS:sections.append('<section id="'+ident+'" aria-label="'+title+'">'+render(ROOT/path)+'</section>')
    base=ROOT/'evidence/public/2026-10-09-instalacao-limpa'
    # Pixel rectangles are presentation windows over unchanged 1920x1080 originals.
    figures=[('01-extracao-e-comandos.png',(0,620,1080,965),'Figura 1 · Extração e comando de reprodução','A pasta nova e o bloco preflight → setup → test. O print integral preserva a tentativa anterior sem o ZIP.'),('02-criacao-clusters.png',(0,380,1050,1038),'Figura 2 · Criação de A e B','Registro de criação dos dois clusters kind.'),('03-setup-e-testes.png',(0,466,1080,746),'Figura 3 · Setup concluído e dez Jobs PASS','Rodada 1791544005. A sequência exibida não contém intervenção corretiva entre setup e test.'),('04-resultado-completo.png',(0,401,1370,990),'Figura 4 · Resultado final e limitações','16 critérios true; 85 linhas de auditoria; 09/10/2026 às 08:08:55 Brasília. Limites de NodePort e teste local mantidos.')]
    cards=[]
    for name,(x0,y0,x1,y1),title,caption in figures:
        dest=ASSETS/'evidencias'/name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(base/name,dest)
        href=dest.relative_to(DOCS).as_posix();w=x1-x0;h=y1-y0
        cards.append(f'<figure><h3>{title}</h3><div class="crop" style="aspect-ratio:{w}/{h}"><img src="{href}" alt="{html.escape(caption)}" style="width:{1920/w*100:.6f}%;left:{-x0/w*100:.6f}%;top:{-y0/h*100:.6f}%"></div><figcaption>{caption} <a href="{href}">Abrir original integral</a></figcaption></figure>')
    sections.insert(9,'<section id="evidencias"><h2>Evidências da instalação limpa</h2><p>Fotos recebidas da autora e conferidas visualmente. Os enquadramentos abaixo preservam os pixels originais; somente a área exibida muda. Logs e JSON originais ainda não foram transferidos.</p>'+''.join(cards)+'<p><a href="'+url(str((base/'RESULTADO_TRANSCRITO.json').relative_to(ROOT)),ROOT/'README.md')+'">JSON transcrito</a> · <a href="'+url(str((base/'MANIFESTO.json').relative_to(ROOT)),ROOT/'README.md')+'">Manifesto dos originais</a></p></section>')
    nav=''.join('<a href="#'+i+'">'+t+'</a>' for i,t,_ in CHAPTERS[:9])+ '<a href="#evidencias">Fotos e evidências</a>'+''.join('<a href="#'+i+'">'+t+'</a>' for i,t,_ in CHAPTERS[9:])
    css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f4f6fa;color:#233147;font:17px/1.65 system-ui,sans-serif}aside{position:fixed;width:260px;height:100vh;overflow:auto;background:#15253c;color:white;padding:28px 22px}aside strong{display:block;font-size:22px;margin-bottom:25px}aside a{display:block;color:#dce6f5;padding:7px 0;text-decoration:none;font-size:14px}aside a:hover{color:#62e0c4}main{margin-left:260px;padding:45px 5%;max-width:1580px}header{padding:35px;background:#e5f3ee;border-left:6px solid #16816b;margin-bottom:35px}h1{font-size:38px;line-height:1.2;margin:12px 0}h2{font-size:29px;color:#122d47}h3{font-size:22px}section{background:white;padding:30px 38px;margin:24px 0;border:1px solid #dce3ec;border-radius:10px;scroll-margin-top:20px}a{color:#006b8b}p{max-width:100ch}code{background:#eef2f7;padding:2px 5px;overflow-wrap:anywhere}pre{background:#15253c;color:#e5eef8;padding:20px;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}pre code{background:none;padding:0}.table{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px}th,td{border:1px solid #d8e1e9;text-align:left;padding:12px;vertical-align:top}th{background:#e9f0f5}figure{margin:30px 0;border:1px solid #dce3ec;padding:18px;border-radius:8px}figure h3{margin-top:0}.crop{position:relative;overflow:hidden;background:black;width:100%}.crop img{position:absolute;max-width:none;height:auto}figcaption{font-size:14px;margin-top:12px}.full{max-width:100%}.architecture{padding:22px;background:#e5f3ee;border-left:4px solid #16816b}footer{font-size:14px;color:#526078}@media(max-width:900px){aside{position:relative;width:auto;height:auto}aside a{display:inline-block;margin-right:14px}main{margin:0;padding:18px}section{padding:20px}h1{font-size:30px}}@media print{aside{display:none}main{margin:0;padding:0}section{border:0;padding:0;break-before:page}a{color:inherit}figure{break-inside:avoid}}'''
    page='<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Boas práticas entre clusters · POC A–B</title><style>'+css+'</style><body><aside><strong>Comunicação<br>entre clusters</strong>'+nav+'</aside><main><header><span>DOCUMENTAÇÃO · POC A–B · SET–OUT 2026</span><h1>Boas práticas de segurança na comunicação entre clusters Kubernetes</h1><p>Desenvolvimento: setembro a outubro de 2026. Pesquisa, arquitetura, implementação, revisões e evidências.</p><p><strong>Instalação limpa concluída · 16 critérios aprovados · escopo de laboratório</strong></p></header>'+''.join(sections)+'</main></body></html>'
    (DOCS/'index.html').write_text(page)
    print('Documentação gerada: docs/index.html')
if __name__=='__main__':main()
