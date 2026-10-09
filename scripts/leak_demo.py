"""Ensaio local de exposição por log; só marcadores, nunca credenciais reais."""
import json
SAMPLE={'event':'login','status':'ok','cpf':'CPF_FICTICIO_NAO_REAL',
        'health':'DADO_SAUDE_FICTICIO','token':'TOKEN_FICTICIO_INVALIDO'}
MARKERS=('CPF_FICTICIO_NAO_REAL','DADO_SAUDE_FICTICIO','TOKEN_FICTICIO_INVALIDO')

def operational_log(record):
    # Esta função trata exclusivamente os eventos controlados da demonstração.
    return {'event':record['event'] if record.get('event') in ('login','read_secret') else 'unknown',
            'status':record['status'] if record.get('status') in ('ok','denied') else 'invalid'}

def exposed(serialized):
    return any(marker in serialized for marker in MARKERS)

def evaluate():
    before=json.dumps(SAMPLE)
    after=json.dumps(operational_log(SAMPLE))
    return {'scenario':'S01-log-exposure','baseline_exposes_marker':exposed(before),
        'controlled_log_exposes_marker':exposed(after),
        'result':'PASS' if exposed(before) and not exposed(after) else 'FAIL',
        'limitation':'Verifica só o exemplo de campos/eventos controlados; não detecta toda informação sensível em qualquer log.'}

if __name__=='__main__':
    result=evaluate();print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['result']=='PASS' else 1)
