SELECT rp.id AS relacion_id,
       r.code AS rol,
       p.code AS permiso,
       rp.is_active AS relacion_activa
FROM role_permissions rp
JOIN roles r ON r.id = rp.role_id
JOIN permissions p ON p.id = rp.permission_id
WHERE r.code = 'CAPTURISTA';