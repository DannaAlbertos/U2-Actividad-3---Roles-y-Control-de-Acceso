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

 ¿Cómo ayudan variables, alias y fragmentos a preparar pruebas repetibles? Incluye una operación propia que los utilice. Las variables, alias y fragmentos en GraphQL permiten estructurar pruebas automatizadas eficientes, limpias y mantenibles. Las variables desacoplan los datos dinámicos de la estructura de la consulta, permitiendo reejecutar un mismo test con múltiples escenarios de entrada sin modificar el cuerpo de la petición. Por su parte, los alias permiten solicitar el mismo campo varias veces con argumentos distintos dentro de una sola consulta, lo que facilita comparar múltiples entidades o estados de forma simultánea. Finalmente, los fragmentos agrupan selecciones de campos reutilizables para garantizar que las aserciones de prueba siempre verifiquen una estructura de datos estandarizada a lo largo de toda la suite de pruebas. 

Operación propia :  

fragment UserDetails on User { 

  id 

  username 

  status 

  role 

} 


query TestUserComparison($userIdA: ID!, $userIdB: ID!) { 

  primaryUser: user(id: $userIdA) { 

    ...UserDetails 

  } 

  secondaryUser: user(id: $userIdB) { 

    ...UserDetails 

  } 

} 


¿Qué valida un enum o un input de GraphQL y qué reglas deben seguir validándose en Python? Explica también por qué [ID!]! acepta []. 

GraphQL (Enum/Input): Valida tipos de datos, presencia de campos obligatorios y pertenencia a un conjunto de valores estáticos a nivel sintáctico y de esquema antes de llegar al resolver. 

Python: Valida la lógica de negocio, restricciones relacionales (ej. unicidad en base de datos, permisos, rangos dinámicos o dependencias entre múltiples campos). 

[ID!]! acepta []: La notación ! externa exige que la lista exista , mientras que la ! interna exige que ningún elemento dentro sea null. Una lista vacía [] cumple ambas reglas: no es null y no tiene elementos nulos dentro. 


¿Qué diferencia hay entre atomicidad e idempotencia? ¿Por qué enviar varias mutaciones en una petición no garantiza un rollback conjunto?  La atomicidad garantiza que un grupo de operaciones se ejecute como un bloque único de "todo o nada" , mientras que la idempotencia asegura que ejecutar la misma operación varias veces genere exactamente el mismo resultado final sin efectos secundarios acumulativos. Enviar varias mutaciones en una sola petición GraphQL no garantiza un rollback conjunto porque la especificación solo exige que se ejecuten secuencialmente, pero no define una transacción global; por lo tanto, cada mutación puede confirmar sus cambios en la base de datos de forma independiente y, si una falla a la mitad, las anteriores ya habrán guardado sus datos permanentemente.

 
Referencias

Kosinski, M. (2025, noviembre 26). Autenticación frente a autorización: ¿cuál es la diferencia? Ibm.com. https://www.ibm.com/mx-es/think/topics/authentication-vs-authorization 

GraphQL Foundation. (s. f.). Queries and mutations. GraphQL. Recuperado el 17 de octubre de 2026, de https://graphql.org/learn/queries/ 

Apollo GraphQL. (s. f.). Using nullability in GraphQL. Apollo GraphQL Blog. Recuperado el 17 de octubre de 2026, de https://www.apollographql.com/blog/using-nullability-in-graphql/ 

Hasura. (s. f.). Multiple mutations in a request. Hasura GraphQL Engine Documentation. Recuperado el 17 de octubre de 2026, de https://hasura.io/docs/latest/mutations/postgres/multiple-mutations/

