## Apuração - 1º Turno: Eleições Prefeituras RJ e SP 2024

Ao ser executado, o script acima realizar uma consulta nos arquivos JSON do TSE que contém informações das apurações de 1º turno para a prefeitura dos municípios do Rio de Janeiro e São Paulo. A cada execução, uma série de informações é capturada e salva em um banco de dados SQLite3, que posteriormente pode ser utilizado para análise de dados em formato de linha do tempo.

Recomenda-se que seja criado um agendamento de execução do script para execução em no máximo a cada 1 minuto, para que a análise de linha do tempo seja a mais apurada possível.

O próprio script cria o banco de dados em sua primeira execução e, nas execuções seguintes apenas o alimenta com as informações obtidas do JSON do TSE.

>script do banco de dados:
~~~~sql
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
~~~~
>query para visualizar a classificação direto no banco de dados
~~~~sql
select
	case municipio
		when 71072 then 'São Paulo'
		when 60011 then 'Rio de Janeiro'
	end as municipio,
	numero || '-' || candidato as candidato,
	cast(votos_validos as integer) as votos_validos,
	hora
from
	candidatos
where
	hora = (select max(hora) from candidatos)
order by
	municipio, votos_validos desc
~~~~
