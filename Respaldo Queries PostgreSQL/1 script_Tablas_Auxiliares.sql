-- Organismo
-- UnidadCompra
-- licibot_tipo_competidor
INSERT INTO licibot_tipo_competidor (id, nom_tipo_comp) VALUES(0, 'Sin Información');
INSERT INTO licibot_tipo_competidor (id, nom_tipo_comp) VALUES(1, 'Competidor Directo');
INSERT INTO licibot_tipo_competidor (id, nom_tipo_comp) VALUES(2, 'Competidor Indirecto');
INSERT INTO licibot_tipo_competidor (id, nom_tipo_comp) VALUES(3, 'Otro');

-- Proveedor
-- Categoria
-- licibot_tipo_licitacion
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('NAN', 'Sin Información');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('L1', 'Licitación Pública Menor a 100 UTM (L1)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('LE', 'Licitación Pública Entre 100 y 1000 UTM (LE)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('LP', 'Licitación Pública Mayor 1000 UTM (LP)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('LQ', 'Licitación Pública entre a 2000 y 5000 UTM');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('LR', 'Licitación Pública Mayor a 5000 (LR)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('LS', 'Licitación Pública Servicios personales especializados (LS)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('A1', 'Licitación Privada por Licitación Pública anterior sin oferentes (A1)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('B1', 'Licitación Privada por Remanente de Contrato anterior (B1)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('E1', 'Licitación Privada por Convenios con Personas Jurídicas Extranjeras fuera del Territorio Nacional (E1)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('F1', 'Licitación Privada por Servicios de Naturaleza Confidencial (F1)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('J1', 'Licitación Privada por otras causales, excluidas de la ley de Compras (J1)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('CO', 'Licitación Privada entre 100 y 1000 UTM');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('B2', 'Licitación Privada Mayor a 1000 UTM');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('A2', 'Trato Directo por Producto de Licitación Privada anterior sin oferentes o desierta (A2)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('D1', 'Trato Directo por Proveedor Único (D1)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('E2', 'Licitación Privada Menor a 100 UTM');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('C2', 'Trato Directo (Cotización) (C2)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('C1', 'Compra Directa (Orden de compra) (C1)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('F2', 'Trato Directo (Cotización) (F2)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('F3', 'Compra Directa (Orden de compra) (F3)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('G2', 'Directo (Cotización) (G2)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('G1', 'Compra Directa (Orden de compra) (G1)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('R1', 'Orden de Compra menor a 3 UTM (R1)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('CA', 'Orden de Compra sin Resolución (CA)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('SE', 'Orden de Compra proveniente de adquisición sin emisión automática de OC (SE)');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('R2', 'Orden de Compra menor a 3 UTM');
INSERT INTO licibot_tipo_licitacion (id_tipo_licitacion, nom_tipo_licitacion) VALUES('COT', 'Compra Ágil');

-- licibot_unidad_monetaria
INSERT INTO licibot_unidad_monetaria (id_unidad_monetaria, nom_unidad_monetaria) VALUES('NaN', 'Sin Información');
INSERT INTO licibot_unidad_monetaria (id_unidad_monetaria, nom_unidad_monetaria) VALUES('CLP', 'Peso Chileno');
INSERT INTO licibot_unidad_monetaria (id_unidad_monetaria, nom_unidad_monetaria) VALUES('CLF', 'Unidad de Fomento');
INSERT INTO licibot_unidad_monetaria (id_unidad_monetaria, nom_unidad_monetaria) VALUES('USD', 'Dólar Americano');
INSERT INTO licibot_unidad_monetaria (id_unidad_monetaria, nom_unidad_monetaria) VALUES('UTM', 'Unidad Tributaria Mensual');
INSERT INTO licibot_unidad_monetaria (id_unidad_monetaria, nom_unidad_monetaria) VALUES('EUR', 'Euro');

-- licibot_monto_estimado
INSERT INTO licibot_monto_estimado (id, nom_monto_estimado) VALUES(0, 'Sin Información');
INSERT INTO licibot_monto_estimado (id, nom_monto_estimado) VALUES(1, 'Presupuesto Disponible');
INSERT INTO licibot_monto_estimado (id, nom_monto_estimado) VALUES(2, 'Precio Referencial');

-- licibot_modalidad_pago
INSERT INTO licibot_modalidad_pago (id, nom_modalidad_pago) VALUES(0, 'Sin Información');
INSERT INTO licibot_modalidad_pago (id, nom_modalidad_pago) VALUES(1, 'Pago a 30 días');
INSERT INTO licibot_modalidad_pago (id, nom_modalidad_pago) VALUES(2, 'Pago a 30, 60 y 90 días');
INSERT INTO licibot_modalidad_pago (id, nom_modalidad_pago) VALUES(3, 'Pago al día');
INSERT INTO licibot_modalidad_pago (id, nom_modalidad_pago) VALUES(4, 'Pago Anual');
INSERT INTO licibot_modalidad_pago (id, nom_modalidad_pago) VALUES(5, 'Pago Bimensual');
INSERT INTO licibot_modalidad_pago (id, nom_modalidad_pago) VALUES(6, 'Pago Contra Entrega Conforme');
INSERT INTO licibot_modalidad_pago (id, nom_modalidad_pago) VALUES(7, 'Pagos Mensuales');
INSERT INTO licibot_modalidad_pago (id, nom_modalidad_pago) VALUES(8, 'Pago Por Estado de Avance');
INSERT INTO licibot_modalidad_pago (id, nom_modalidad_pago) VALUES(9, 'Pago Trimestral');
INSERT INTO licibot_modalidad_pago (id, nom_modalidad_pago) VALUES(10, 'Pago a 60 días');

-- licibot_unidad_tiempo_contrato
INSERT INTO licibot_unidad_tiempo_contrato (id, nom_uni_tiempo_con) VALUES(0, 'Sin Información');
INSERT INTO licibot_unidad_tiempo_contrato (id, nom_uni_tiempo_con) VALUES(1, 'Horas');
INSERT INTO licibot_unidad_tiempo_contrato (id, nom_uni_tiempo_con) VALUES(2, 'Días');
INSERT INTO licibot_unidad_tiempo_contrato (id, nom_uni_tiempo_con) VALUES(3, 'Semanas');
INSERT INTO licibot_unidad_tiempo_contrato (id, nom_uni_tiempo_con) VALUES(4, 'Meses');
INSERT INTO licibot_unidad_tiempo_contrato (id, nom_uni_tiempo_con) VALUES(5, 'Años');

-- licibot_unidad_tiempo_evaluacion
INSERT INTO licibot_unidad_tiempo_evaluacion (id, nom_uni_tiempo_ev) VALUES(0, 'Sin Información');
INSERT INTO licibot_unidad_tiempo_evaluacion (id, nom_uni_tiempo_ev) VALUES(1, 'Horas');
INSERT INTO licibot_unidad_tiempo_evaluacion (id, nom_uni_tiempo_ev) VALUES(2, 'Días');
INSERT INTO licibot_unidad_tiempo_evaluacion (id, nom_uni_tiempo_ev) VALUES(3, 'Semanas');
INSERT INTO licibot_unidad_tiempo_evaluacion (id, nom_uni_tiempo_ev) VALUES(4, 'Meses');
INSERT INTO licibot_unidad_tiempo_evaluacion (id, nom_uni_tiempo_ev) VALUES(5, 'Años');

-- licibot_tipo_acto_administrativo
INSERT INTO licibot_tipo_acto_administrativo (id, nom_acto_admin) VALUES(0, 'Sin Información');
INSERT INTO licibot_tipo_acto_administrativo (id, nom_acto_admin) VALUES(1, 'Autorización');
INSERT INTO licibot_tipo_acto_administrativo (id, nom_acto_admin) VALUES(2, 'Resolución');
INSERT INTO licibot_tipo_acto_administrativo (id, nom_acto_admin) VALUES(3, 'Acuerdo');
INSERT INTO licibot_tipo_acto_administrativo (id, nom_acto_admin) VALUES(4, 'Decreto');
INSERT INTO licibot_tipo_acto_administrativo (id, nom_acto_admin) VALUES(5, 'Otros');

-- Adjudicacion
-- Licitacion
-- ProductoServicio
-- Item