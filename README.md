# miPrimerRepo

Repositorio con un programa experto sencillo para jugar gato (tic-tac-toe) en
la consola.

## Juego del gato experto

El archivo `gato_experto.py` contiene un asistente que aprende las jugadas
correctas. Si la IA no conoce qué movimiento realizar en una posición,
solicitará ayuda al jugador y guardará la respuesta en el archivo
`conocimiento_gato.json` para futuras partidas.

### Requisitos

- Python 3.9 o superior.

### Ejecución

```bash
python gato_experto.py
```

El jugador controla las `X` y mueve indicando números del 1 al 9 (de izquierda
a derecha y de arriba abajo). La IA utiliza su base de conocimiento para evitar
perder y aprende nuevos movimientos cuando es necesario.
