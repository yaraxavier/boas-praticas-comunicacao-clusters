"""Formulário de avaliação do modelo; não detecta controles automaticamente."""
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
CATALOG=ROOT/'docs/checklist-modelo.json'
FORM=ROOT/'evidence/checklist-avaliacao.json'
def main():
    action=sys.argv[1] if len(sys.argv)>1 else 'help'
    catalog=json.loads(CATALOG.read_text())
    if action=='init':
        if FORM.exists(): raise SystemExit('Formulário já existe; nenhum dado foi sobrescrito.')
        FORM.parent.mkdir(exist_ok=True)
        FORM.write_text(json.dumps({'model_version':'4.0','environment':'PREENCHER',
            'checks':[dict(id=item['id'],status='pendente',evidence='',justification='',owner='',checked_at='')
                      for item in catalog]},ensure_ascii=False,indent=2))
        print('Formulário criado em evidence/checklist-avaliacao.json')
    elif action=='report':
        form=json.loads(FORM.read_text()); checks=form['checks']; ids=[x['id'] for x in checks]
        if len(ids)!=len(set(ids)) or set(ids)!={x['id'] for x in catalog}:
            raise SystemExit('IDs ausentes, repetidos ou desconhecidos; revisar formulário.')
        index={x['id']:x for x in catalog}; counts={}; critical=[]; invalid=[]
        for check in checks:
            status=check['status']; cid=check['id']
            if status not in ('conforme','nao_conforme','pendente','nao_aplicavel'):
                invalid.append(cid+': situação desconhecida'); continue
            if status!='pendente' and (not check.get('owner') or not check.get('checked_at')):
                invalid.append(cid+': faltam responsável/data')
            if status in ('conforme','nao_conforme'):
                evidence=check.get('evidence','')
                path=(ROOT/evidence).resolve()
                if not evidence or not path.is_relative_to(ROOT.resolve()) or not path.is_file():
                    invalid.append(cid+': evidência local inexistente ou fora do pacote')
            if status=='nao_aplicavel' and not check.get('justification'):
                invalid.append(cid+': falta justificativa de não aplicação')
            if status=='nao_conforme' and not check.get('justification'):
                invalid.append(cid+': falta descrição do gap e próxima ação')
            counts[status]=counts.get(status,0)+1
            if index[cid]['priority']=='P0' and status not in ('conforme','nao_aplicavel'): critical.append(cid)
        result={'counts':counts,'p0_unresolved':critical,'invalid_records':invalid,
            'interpretation':'Registro documental; conformidade depende da revisão humana das evidências. Nenhum ambiente é certificado por este relatório.'}
        print(json.dumps(result,ensure_ascii=False,indent=2))
        if invalid or critical: raise SystemExit(1)
    else:
        print('Uso: python3 scripts/checklist.py init | report')
if __name__=='__main__': main()
