# Periwiki

Una herramienta muy básica que, utilizando `Streamlit` y un archivo de Python3, te permite crear una wiki muy simple basada en documentos Markdown.

Estaba buscando una forma de hacerme una Wiki personal y encontré Wikidpad, pero no me servía para lo que quería, así que me acordé de ChatGPT y este proyecto lo he ido implementando poco a poco apoyándome en él para hacer la parte más densa del código y centrarme solo en la lógica y las correcciones.

Tengo intención de ir arreglando y mejorando este proyecto, poquito a poco, _(e intentaré mantenerlo actualizado también aquí, que a veces me disperso)_.

## Requisitos

- Tener `Python3` instalado en el ordenador y descargados las bibliotecas de `Streamlit` y `Watchdog` que aparecen en el documento `requirements.txt`.

## Creación de la Wiki

1. Para crear la Wiki, primero asegúrate de que tienes instalados todos los paquetes que necesesitarás. Para ello, descárgate este repositorio y, a través de un terminal, colocate dentro del repositorio utilizando `cd` (Mac) o el equivalente en Linux o Consola de comandos en Windows.
2. Ejecuta la siguiente línea de código: `pip install -r requirements.txt`.
3. Una vez esté todo actualizado, ejecuta el documento de Python utilizando el comando: `streamlit run periwiki.py`.
4. Si es la primera vez que lo inicias, generará en el mismo sitio la carpeta **data**, donde guardará todo el contenido que vayas generando. A partir de aquí, puedes trabajar directamente en el navegador en el que te ha abierto la Wiki.

## ¿Qué puedes hacer por ahora?
Por ahora, desde la interfaz de Streamlit, puedes:
- Puedes crear la estructura de carpetas y archivos que te apetezca.
- Incluir en cualquier parte del directorio nuevos documentos `.md` para estructurar tu wiki personal.
- Puedes visualizar los documentos, editarlos y también eliminarlos (si los eliminas accidentalmente, siempre puedes recuperarlo de la papelera).

Además, recomiendo tener creado en el mismo sitio una carpeta para otros tipos de archivos que vayas a vincular a los documentos Markdown. Yo tengo hecha esta estructura:
- data
- media
    - audio
    - images
    - video
- periwiki.py
- requirements.txt

## Cositas que quiero intentar añadir próximamente
- Un buscador de documentos y texto
- La capacidad de eliminar carpetas y directorios
- Mover y duplicar archivos dentro del directorio
