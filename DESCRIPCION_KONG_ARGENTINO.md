# KONG ARGENTINO - Documento de Diseno de Juego

## 1. Inspiracion y contexto
KONG ARGENTINO es un homenaje al clasico Donkey Kong de los 80, reimaginado con identidad futbolera argentina y clima Mundial FIFA 2026.

El juego conserva:
- Estructura vertical de plataformas y escaleras.
- Riesgo constante por objetos que caen/ruedan.
- Progresion por niveles y aumento de dificultad.

El juego incorpora:
- Hinchada argentina como ecosistema vivo de NPCs.
- Copa del Mundo como simbolo narrativo y visual.
- Celebracion final estilo campeonato mundial.

## 2. Fantasia del jugador
El jugador controla a Mario version hincha argentino y debe rescatar a Pauline de Kong Cervecero, ascendiendo nivel a nivel mientras:
- Esquiva o rompe barriles.
- Compite por recursos con la hinchada.
- Gestiona riesgo, movilidad vertical y timing de ataque.

## 3. Objetivo principal
Llegar a Pauline en la cima del escenario para activar la secuencia de rescate.

Condicion de nivel superado:
- Contacto del jugador con Pauline.

Condicion de derrota:
- Perder todas las vidas.

## 4. Historia y tono
Kong Cervecero roba la Copa del Mundo y secuestra a Pauline. Cada nivel representa una escalada por estructuras tipo estadio con ambiente de cancha argentina: bombos, cantos, bengalas y colores celeste/blanco.

## 5. Controles
- A/D o Flechas izquierda/derecha: movimiento horizontal.
- W o Flecha arriba: saltar en suelo, subir en escalera.
- S o Flecha abajo: agacharse en suelo, bajar en escalera.
- Espacio: atacar (golpea barriles y NPCs de la hinchada).
- P: pausa.
- [ y ]: bajar/subir volumen.
- ESC: volver al menu principal.

## 6. Bucle principal de juego
1. Kong lanza barriles con frecuencia segun nivel.
2. El jugador asciende por plataformas y escaleras.
3. Se recogen items (cervezas y mates) y se manejan combates cortos.
4. NPCs de la hinchada compiten por barriles y alteran el flujo del nivel.
5. Al llegar a Pauline, se otorga bonus de nivel y se avanza.

## 7. Mecanicas generales
### 7.1 Jugador
- Movimiento horizontal con inercia suave.
- Salto con gravedad y deteccion de plataformas.
- Subida/bajada de escaleras.
- Ataque direccional con alcance corto.
- Sistema de vidas, invencibilidad temporal y respawn.

### 7.2 Barriles
- Kong los genera en forma periodica.
- Ruedan por plataformas y pueden caer entre niveles de altura.
- Otorgan puntos extra si se saltan con timing correcto.
- Se rompen con ataque o con estado de poder del jugador.

### 7.3 Items
- Cerveza: suma puntos y alimenta combo.
- Mate: otorga invencibilidad/estado de poder temporal.

### 7.4 Progresion
- Minimo recomendado: 6 niveles.
- Escalado por nivel: velocidad de barril, cadencia de lanzamiento, maximo de barriles activos y movilidad de Kong.

## 8. Sistema de NPCs de la hinchada
Todos los NPCs pertenecen a la misma hinchada (no son villanos), pero funcionan como obstaculos dinamicos porque compiten por los mismos barriles y ocupan espacio de navegacion.

Tipos de hinchas definidos por vision de producto:
- Hincha Argentina (chica con bandera).
- Hincha viejo (barba blanca y bombo).
- Hincha borrachin (estado de ebriedad alta inicial).
- Hincha random (variaciones de skin y conducta).
- Hincha con bengala (emite luz y particulas).
- Hincha gemelos (duo coordinado).
- Hincha abuela (cacerola y cuchara).

Comportamientos esperados compartidos:
- Busqueda activa de barriles cercanos.
- Competencia entre NPCs por prioridad de llegada.
- Consumo de barril al contacto.
- Aumento de borrachera por consumo.
- Transiciones de estado por borrachera: normal, tambaleo, erratico, dormido/baile.
- Reaccion a golpes del jugador y a impactos de barriles.
- Canto contextual (Argentina, Messi, copa).

## 9. Kong (antagonista)
Kong Cervecero es el antagonista principal.

Requisitos de comportamiento:
- Lanzar barriles segun dificultad del nivel.
- Reaccionar con animacion/estado de enojo al recibir golpes.
- Mantener presencia visual dominante en la parte alta del mapa.

## 10. Pauline y Copa del Mundo
Pauline debe sostener la Copa del Mundo como objetivo visual y narrativo.

Al rescate:
- Se activa una secuencia de celebracion tipo FIFA World Cup.
- Duracion objetivo de secuencia: 10 segundos.
- Luego: siguiente nivel o pantalla final de victoria.

## 11. Celebracion final
Elementos minimos:
- Abrazo jugador + Pauline.
- Levantamiento de copa.
- Fuegos artificiales y confeti.
- Canto/festejo de tribuna.
- Mensaje de campeonato y cierre epico.

## 12. Arte, musica y atmosfera
Direccion audiovisual:
- Paleta con celeste, blanco y dorado como base.
- Elementos iconicos argentinos (banderas, sol, tribuna).
- Sonido de cancha con bombos, platillos y coros.
- Efectos para golpes, barriles, borrachera, power-up y festejos.

## 13. Puntuacion y progreso
Fuentes de puntos:
- Recoleccion de cervezas.
- Barriles rotos.
- Barriles saltados.
- Golpes a hinchas.
- Bonus por combo.
- Bonus de fin de nivel.

Persistencia:
- Guardado local de high score.

## 14. Requisitos de coherencia de producto
- Nombre del jugador: Mario (fijo) o seleccionable en menu.
- Pauline con copa visible y protagonica.
- Seis niveles como baseline de campana.
- Hinchas como hinchada aliada/caotica, no como enemigos tradicionales.
- Kong claramente identificado como villano.
- Clima Mundial presente en UI, visuales y audio.

## 15. Trazabilidad con el codigo actual (estado del repositorio)
Implementado actualmente:
- Estructura de 6 niveles.
- Sistema de puntaje y high score persistente.
- Kong, Pauline, jugador, barriles e items jugables.
- Controles base, pausa y volumen.
- Secuencia de victoria final con copa, particulas y festejo.
- Hincha Argentina y Hincha Viejo con logica dedicada.

Pendiente para cerrar la vision completa:
- Agregar tipos de hincha faltantes (borrachin dedicado, random, bengala, gemelos, abuela).
- Homogeneizar IA de competencia por barriles entre toda la hinchada.
- Ajustar duracion temporal exacta de celebracion final a 10 segundos medibles.
- Integrar seleccion de personaje/nombre si se desea opcion ademas de Mario.

## 16. Roadmap tecnico recomendado
Fase 1 (gameplay):
- Introducir interfaz base de NPC de hinchada y herencia por variantes.
- Definir FSM comun: buscar -> beber -> cantar -> erratico -> recuperacion.
- Unificar sistema de objetivo de barriles y prioridad de disputa.

Fase 2 (contenido):
- Implementar los 5 tipos de hincha faltantes con visual y rasgos de IA.
- Agregar efectos especificos de bengala, cacerolazo y duo de gemelos.

Fase 3 (presentacion):
- Pulir secuencia final de 10 segundos con timeline fijo.
- Reforzar feedback sonoro contextual por estado de partido/festejo.
- Balancear dificultad de niveles 4 a 6 con metricas de muerte y tiempo.

---
Documento preparado como base funcional de desarrollo para KONG ARGENTINO.
