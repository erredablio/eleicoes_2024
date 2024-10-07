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