UPDATE gpdb.gp AS t1
INNER JOIN (
    SELECT dia, hora, ROW_NUMBER() OVER (PARTITION BY dia ORDER BY hora) AS puesto
    FROM gpdb.gp
) AS t2
ON t1.dia = t2.dia AND t1.hora = t2.hora
SET t1.puesto = t2.puesto;
