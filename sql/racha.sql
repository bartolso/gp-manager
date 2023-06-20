SET @streak := 0, @prev_day := NULL, @prev_player := NULL;

UPDATE gpdb.gp
SET racha = (
  SELECT racha
  FROM (
    SELECT
      CASE
        WHEN @prev_day IS NULL OR @prev_player <> jugador_id THEN @streak := 1
        WHEN DATEDIFF(dia, @prev_day) = 1 THEN @streak := @streak + 1
        ELSE @streak := 1
      END AS racha,
      @prev_day := dia,
      @prev_player := jugador_id,
      gp_id -- Assuming "id" is the primary key of your table
    FROM gpdb.gp
    ORDER BY jugador_id, dia, gp_id
  ) AS subquery
  WHERE gpdb.gp.gp_id = subquery.gp_id
);
