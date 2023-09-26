INSERT INTO public.licibot_modalidad_pago (nom_modalidad_pago,create_uid,create_date,write_uid,write_date) VALUES
	 ('Sin Información',NULL,NULL,NULL,NULL),
	 ('Pago a 30 días',NULL,NULL,NULL,NULL),
	 ('Pago a 30, 60 y 90 días',NULL,NULL,NULL,NULL),
	 ('Pago al día',NULL,NULL,NULL,NULL),
	 ('Pago Anual',NULL,NULL,NULL,NULL),
	 ('Pago Bimensual',NULL,NULL,NULL,NULL),
	 ('Pago Contra Entrega Conforme',NULL,NULL,NULL,NULL),
	 ('Pagos Mensuales',NULL,NULL,NULL,NULL),
	 ('Pago Por Estado de Avance',NULL,NULL,NULL,NULL),
	 ('Pago Trimestral',NULL,NULL,NULL,NULL);
INSERT INTO public.licibot_modalidad_pago (nom_modalidad_pago,create_uid,create_date,write_uid,write_date) VALUES
	 ('Pago a 60 días',NULL,NULL,NULL,NULL);
INSERT INTO public.licibot_monto_estimado (nom_monto_estimado,create_uid,create_date,write_uid,write_date) VALUES
	 ('Sin Información',NULL,NULL,NULL,NULL),
	 ('Presupuesto Disponible',NULL,NULL,NULL,NULL),
	 ('Precio Referencial',NULL,NULL,NULL,NULL);
INSERT INTO public.licibot_tipo_acto_administrativo (nom_acto_admin,create_uid,create_date,write_uid,write_date) VALUES
	 ('Sin Información',NULL,NULL,NULL,NULL),
	 ('Autorización',NULL,NULL,NULL,NULL),
	 ('Resolución',NULL,NULL,NULL,NULL),
	 ('Acuerdo',NULL,NULL,NULL,NULL),
	 ('Decreto',NULL,NULL,NULL,NULL),
	 ('Otros',NULL,NULL,NULL,NULL);
INSERT INTO public.licibot_tipo_competidor (nom_tipo_comp,create_uid,create_date,write_uid,write_date) VALUES
	 ('Sin Información',NULL,NULL,NULL,NULL),
	 ('Competidor Directo',NULL,NULL,NULL,NULL),
	 ('Competidor Indirecto',NULL,NULL,NULL,NULL),
	 ('Otro',NULL,NULL,NULL,NULL);
INSERT INTO public.licibot_tipo_licitacion (id_tipo_licitacion,nom_tipo_licitacion,create_uid,create_date,write_uid,write_date) VALUES
	 ('NAN','Sin Información',NULL,NULL,NULL,NULL),
	 ('L1','Licitación Pública Menor a 100 UTM (L1)',NULL,NULL,NULL,NULL),
	 ('LE','Licitación Pública Entre 100 y 1000 UTM (LE)',NULL,NULL,NULL,NULL),
	 ('LP','Licitación Pública Mayor 1000 UTM (LP)',NULL,NULL,NULL,NULL),
	 ('LQ','Licitación Pública entre a 2000 y 5000 UTM',NULL,NULL,NULL,NULL),
	 ('LR','Licitación Pública Mayor a 5000 (LR)',NULL,NULL,NULL,NULL),
	 ('LS','Licitación Pública Servicios personales especializados (LS)',NULL,NULL,NULL,NULL),
	 ('A1','Licitación Privada por Licitación Pública anterior sin oferentes (A1)',NULL,NULL,NULL,NULL),
	 ('B1','Licitación Privada por Remanente de Contrato anterior (B1)',NULL,NULL,NULL,NULL),
	 ('E1','Licitación Privada por Convenios con Personas Jurídicas Extranjeras fuera del Territorio Nacional (E1)',NULL,NULL,NULL,NULL);
INSERT INTO public.licibot_tipo_licitacion (id_tipo_licitacion,nom_tipo_licitacion,create_uid,create_date,write_uid,write_date) VALUES
	 ('F1','Licitación Privada por Servicios de Naturaleza Confidencial (F1)',NULL,NULL,NULL,NULL),
	 ('J1','Licitación Privada por otras causales, excluidas de la ley de Compras (J1)',NULL,NULL,NULL,NULL),
	 ('CO','Licitación Privada entre 100 y 1000 UTM',NULL,NULL,NULL,NULL),
	 ('B2','Licitación Privada Mayor a 1000 UTM',NULL,NULL,NULL,NULL),
	 ('A2','Trato Directo por Producto de Licitación Privada anterior sin oferentes o desierta (A2)',NULL,NULL,NULL,NULL),
	 ('D1','Trato Directo por Proveedor Único (D1)',NULL,NULL,NULL,NULL),
	 ('E2','Licitación Privada Menor a 100 UTM',NULL,NULL,NULL,NULL),
	 ('C2','Trato Directo (Cotización) (C2)',NULL,NULL,NULL,NULL),
	 ('C1','Compra Directa (Orden de compra) (C1)',NULL,NULL,NULL,NULL),
	 ('F2','Trato Directo (Cotización) (F2)',NULL,NULL,NULL,NULL);
INSERT INTO public.licibot_tipo_licitacion (id_tipo_licitacion,nom_tipo_licitacion,create_uid,create_date,write_uid,write_date) VALUES
	 ('F3','Compra Directa (Orden de compra) (F3)',NULL,NULL,NULL,NULL),
	 ('G2','Directo (Cotización) (G2)',NULL,NULL,NULL,NULL),
	 ('G1','Compra Directa (Orden de compra) (G1)',NULL,NULL,NULL,NULL),
	 ('R1','Orden de Compra menor a 3 UTM (R1)',NULL,NULL,NULL,NULL),
	 ('CA','Orden de Compra sin Resolución (CA)',NULL,NULL,NULL,NULL),
	 ('SE','Orden de Compra proveniente de adquisición sin emisión automática de OC (SE)',NULL,NULL,NULL,NULL),
	 ('R2','Orden de Compra menor a 3 UTM',NULL,NULL,NULL,NULL),
	 ('COT','Compra Ágil',NULL,NULL,NULL,NULL);
INSERT INTO public.licibot_unidad_monetaria (id_unidad_monetaria,nom_unidad_monetaria,create_uid,create_date,write_uid,write_date) VALUES
	 ('NaN','Sin Información',NULL,NULL,NULL,NULL),
	 ('CLP','Peso Chileno',NULL,NULL,NULL,NULL),
	 ('CLF','Unidad de Fomento',NULL,NULL,NULL,NULL),
	 ('USD','Dólar Americano',NULL,NULL,NULL,NULL),
	 ('UTM','Unidad Tributaria Mensual',NULL,NULL,NULL,NULL),
	 ('EUR','Euro',NULL,NULL,NULL,NULL);
INSERT INTO public.licibot_unidad_tiempo_contrato (nom_uni_tiempo_con,create_uid,create_date,write_uid,write_date) VALUES
	 ('Sin Información',NULL,NULL,NULL,NULL),
	 ('Horas',NULL,NULL,NULL,NULL),
	 ('Días',NULL,NULL,NULL,NULL),
	 ('Semanas',NULL,NULL,NULL,NULL),
	 ('Meses',NULL,NULL,NULL,NULL),
	 ('Años',NULL,NULL,NULL,NULL);
INSERT INTO public.licibot_unidad_tiempo_evaluacion (nom_uni_tiempo_ev,create_uid,create_date,write_uid,write_date) VALUES
	 ('Sin Información',NULL,NULL,NULL,NULL),
	 ('Horas',NULL,NULL,NULL,NULL),
	 ('Días',NULL,NULL,NULL,NULL),
	 ('Semanas',NULL,NULL,NULL,NULL),
	 ('Meses',NULL,NULL,NULL,NULL),
	 ('Años',NULL,NULL,NULL,NULL);
