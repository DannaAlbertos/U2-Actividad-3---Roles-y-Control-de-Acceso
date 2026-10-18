# Actividad 5

## Fundamentos de arquitectura    
### Actividad 5 – Configuración de servicios 


### Estudiantes: 
- Albertos Sosa Danna Pamela  
- Cetzal Cetzal Astrit Airan 
- Díaz Anduze Giovana Ruby 
- Alemán Venus Getsemaní 
  
### Docente: Gimer Almicar Cervera Evia 
  
- 4°A



#### Mérida, Yucatán a 17 de octubre de 2026  


### E03

![E03](Actividad05\img\E03.1.png)
![E03](Actividad05\img\E03.png)
![E03](Actividad05\img\E03.2.png)
![E03](Actividad05\img\E03.3.png)

### Caso E06. Entradas inválidas (Previsualización)

| Variante | Entrada (`input`) | Mensaje devuelto | Estado en Base de Datos |
| :--- | :--- | :--- | :--- |
| **Propuesta sobre ADMINISTRADOR** | `roleId: 1`, `permissionIds: ["1", "2"]` | `"No se pueden modificar los permisos del rol ADMINISTRADOR"` | Sin cambios (Validación Fail-Fast previa a ejecución) |
| **Permisos repetidos** | `roleId: 5`, `permissionIds: ["1", "1"]` | `"La lista de permisos contiene IDs duplicados"` | Sin cambios (Rechazo inmediato sin alterar BD) |
| **Permiso inexistente** | `roleId: 3`, `permissionIds: ["9999"]` | `"Uno o más permisos deseados no existen o están inactivos"` | Sin cambios (Rechazo previo a BD) |
| **Rol inexistente** | `roleId: "9999"`, `permissionIds: ["1", "2"]` | `"El rol no existe o está inactivo"` | Sin cambios (Rechazo previo a BD) |


 ````Evidencias en la carpeta img````


Preguntas:

Que diferencia hay entre autenticación, autorización y configuración de permisos? ¿Porqué actorCompanyUserId no comprueba identidad? 

La autenticación verifica la identidad de un usuario y por su parte la autorización proporciona al usuario el nivel adecuado de acceso a los recursos de un sistema. El primero se basa en credenciales como las contraseñas o escaneos de huella dactilares, que los usuarios presentan para demostrar que son quienes dicen ser.  Mientras que el segundo es por licencias del usuario donde se describe lo que cada uno puede hacer dentro de un recurso o red. La configuración de permisos por su lado es decidir qué acciones tiene un rol (como en el sistema con administrador, capturista etc.).  

Hablando respecto a actorCompanyUserId este no comprueba identidad porque es solo un dato de entrada que un cliente envía en la petición. Es que como es un identificador solo permite sabes que está dentro de la base de datos.  
 

 
Referencias

Kosinski, M. (2025, noviembre 26). Autenticación frente a autorización: ¿cuál es la diferencia? Ibm.com. https://www.ibm.com/mx-es/think/topics/authentication-vs-authorization 

