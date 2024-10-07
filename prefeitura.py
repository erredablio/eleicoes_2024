import os, requests, sqlite3
from datetime import datetime

urls = [
    'https://resultados.tse.jus.br/oficial/ele2024/619/dados/rj/rj60011-c0011-e000619-u.json', #RJ-Rio de Janeiro
    'https://resultados.tse.jus.br/oficial/ele2024/619/dados/sp/sp71072-c0011-e000619-u.json', #SP-São Paulo
]

prefeitura = []

data_hora_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
dia, hora = data_hora_atual.split()

def process_json(url):
    response = requests.get(url)
    dados = response.json()
    for cargo in dados.get('carg', []):
        for agr in cargo.get('agr', []):
            for partido in agr.get('par', []):
                for candidato in partido.get('cand', []):
                    candidato_info = (
                        dados.get('cdabr'), #código do município no TSE
                        partido.get('sg'), #nome do partido
                        candidato.get('n'), #número do partido
                        candidato.get('nm'), #nome do candidato
                        candidato.get('vap'), #votos válidos
                        candidato.get('pvap'), #percentual de votos válidos
                        dia, #dia da captura
                        hora #hora da captura
                    )
                    prefeitura.append(candidato_info)

for url in urls:
    process_json(url)

db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prefeitura2.db')

conexao = sqlite3.connect(db)
banco = conexao.cursor()

banco.execute('''
CREATE TABLE IF NOT EXISTS candidatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    municipio TEXT,
    partido TEXT,
    numero TEXT,
    candidato TEXT,
    votos_validos TEXT,
    percentual_votos_validos TEXT,
    dia TEXT,
    hora TEXT
)
''')

banco.executemany('''
INSERT INTO candidatos (
    municipio,
    partido,
    numero,
    candidato,
    votos_validos,
    percentual_votos_validos,
    dia,
    hora
) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', prefeitura)

conexao.commit()
conexao.close()

print(f"Dados salvos com sucesso em {data_hora_atual}")
