Global timeoffset and Chapters tutorial
=======================================

.. include:: links.rst

This tutorial is an example of use of toc2audio version 1.0.0.

This is an actual published podcast: `Python en español #17:
Tertulia 2021-01-26 <https://podcast.jcea.es/python/17>`_. The
Markdown_ document is written in spanish, but you can hopefully
follow the details with no fuss. Charset used is UTF-8, as you
should too.

Situation:

- I listen to the podcast and write the shownotes in Markdown_
  format. I like useful shownotes, so the document is quite large,
  almost 10Kbytes::

    Participantes:
    
    - Jesús Cea, email: [jcea@jcea.es](mailto:jcea@jcea.es), twitter:
      [@jcea](https://twitter.com/jcea), <https://blog.jcea.es/>,
      <https://www.jcea.es/>. Conectando desde Madrid.
    
    - Eduardo Castro, email:
      [info@ecdesign.es](mailto:info@ecdesign.es). Conectando desde A
      Guarda.
    
    - Javier, conectando desde Madrid.
    
    - Víctor Ramírez, twitter: [@virako](https://twitter.com/virako),
      programador python y amante de vim, conectando desde Huelva.
    
    - Dani, conectando desde Málaga.
    
    - Miguel Sánchez, email:
      [msanchez@uninet.edu](msanchez@uninet.edu), conectando desde
      Canarias.
    
    - Jorge Rúa, conectando desde Vigo.
    
    Audio editado por Pablo Gómez, twitter:
    [@julebek](https://twitter.com/julebek).
    
    La música de la entrada y la salida es "Lightning Bugs", de Jason
    Shaw. Publicada en <https://audionautix.com/> con licencia
    - [Creative Commons Attribution 4.0 International
    License](https://audionautix.com/creative-commons-music).
    
    - [00:00] Haciendo tiempo hasta que entre más gente.
    
        - Raspberry Pi Pico:
          <https://www.raspberrypi.org/products/raspberry-pi-pico/>.
    
            - Jesús Cea está encantado con su rango de alimentación.
    
        - Micropython: <https://www.micropython.org/>.
    
    - [05:10] Truco: `Python -i`: Ejecuta un script y pasa a modo
      interactivo.
    
        También se puede hacer desde el propio código con
        `code.InteractiveConsole(locals=globals()).interact()`.
    
        Jesús Cea se queja de que usando la invocación desde código
        no funciona la edición de líneas. Javier da la pista correcta:
        para que funcione, basta con hacer `import readline` antes de
        lanzar el modo interactivo.
    
    - [10:25] Regresión con ipdb: <https://pypi.org/project/ipdb/>.
    
    - [11:45] Nueva versión de Pyston <https://www.pyston.org/>.
    
        - Intérprete de Python más rápido. Un 50% más rápido que
          cpython.
    
    - [15:30] Ver si dos fechas son iguales con `datetime`
      <https://docs.python.org/3/library/datetime.html>.
    
        - Trabajar siempre en UTC
          <https://es.wikipedia.org/wiki/Tiempo_universal_coordinado>,
          aunque solo tengas una zona horaria.
    
    - [19:00] Jesús Cea ha investigado cómo funcionan los POSTs HTTP
      en las protecciones CSRF <https://es.wikipedia.org/wiki/CSRF>.
    
        - Buena práctica: La respuesta al POST es una redirección a un
          GET. Patrón Post/Redirect/Get (PRG)
          <https://es.wikipedia.org/wiki/Post/Redirect/Get>.
    
        - Ventajas de usar un framework.
    
    - [23:40] ¿Optimizaciones cuando tienes grandes cantidades de
      datos?
    
        - Tema muy amplio, hacen falta detalles del problema.
    
        - Se ofrecen algunas ideas:
    
            - Map/Reduce: <https://en.wikipedia.org/wiki/Map_reduce>.
    
            - Usar generadores u otras construcciones "lazy" siempre
              que sea posible.
              <https://wiki.python.org/moin/Generators>.
    
    - [31:00] Gestión de memoria en Python.
    
        - Design of CPython’s Garbage Collector:
          <https://devguide.python.org/garbage_collector/>.
    
        - Hora de sacar la basura garbage collector - Pablo Galindo y
          Victor Terrón - PyConES 2018
          <https://www.youtube.com/watch?v=G9wOSExzs5g>.
    
    - [34:25] Tipografía para programadores:
    
        - Victor Mono: <https://rubjo.github.io/victor-mono/>.
    
        - Fira Code: <https://fonts.google.com/specimen/Fira+Code>.
    
        - Fira Code Retina:
          <https://github.com/tonsky/FiraCode/issues/872>.
    
    - [36:25] Eduardo Castro se ha currado una lista de trucos
      sencillos pero interesantes:
    
        **En estas notas solo referenciamos los puntos a los que
        dedicamos más tiempo, se habló de más cosas**.
    
        **El documento para poder seguir los comentarios de la
        grabación está en <https://demo.hedgedoc.org/s/hEZB92q40#>.**
    
        - `hash(float('inf')) -> 314159`.
    
        - [42:10] LRU Caché:
          <<https://docs.python.org/3/library/functools.html#functools.lru_cache>.
    
            - Bugs abundantes en LRU Cache y múltiples hilos:
              <https://bugs.python.org/issue?%40columns=id%2Cactivity%2Ctitle%2Ccreator%2Cassignee%2Cstatus%2Ctype&%40sort=-activity&%40filter=status&%40action=searchid&ignore=file%3Acontent&%40search_text=lru_cache+threads&submit=search&status=-1%2C1%2C2%2C3>.
    
        - Yield:
    
            - Ojo con excepciones y filtraciones de memoria.
    
            - [47:45] Uso interesante con los "context managers":
              `@contextlib.contextmanager`
              <https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager>
              y `@contextlib.asynccontextmanager`
              <https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager>.
    
        - [50:20] itertools:
          <https://docs.python.org/3/library/itertools.html>. A Jesús
          Cea no le entra en la cabeza la programación funcional.
    
    - [55:10] ¿Qué es ser Pythonico?
    
        - Aunque esté en la biblioteca estándar, no significa que sea
          pythónico:
          
            - asyncore:
              <https://docs.python.org/3/library/asyncore.html>. Está
              marcado como obsoleto desde Python 3.6.
    
            - Mover métodos funcionales en una librería separada.
    
            - Las dos jerarquías distintas que existían en Python 2.
              Esto se unificó en Python 3.
    
            - `from __future__ import ...`.
    
            - La migración a Python 3 fue un intento de simplificar el
              lenguaje. Pero Python 3 se está complicando cada vez
              más.
    
                - La complejidad fragmenta los diferentes idiomas del
                  lenguaje.
    
    - [01:07:30] Seguimos desgranando los trucos propuestos por
      Eduardo.
    
        - `collections.defaultdict()`:
          <https://docs.python.org/3/library/collections.html#collections.defaultdict>.
    
    - [01:10:20] `iter()` y `next()` admiten una parametro extra
      centinela opcional que especifica un valor que termina el
      iterador.
    
        - Utilizar objetos centinelas que no sean `None`, porque
          `None` puede ser un objeto válido.
    
    - [01:16:40] Los "slices" son objetos que se pueden crear y
      utilizar: `slice(1,100)`.
    
        - Pasar un iterador a una función abre posibilidades
          interesantes.
    
        - `Slice Objects`: <https://docs.python.org/3/c-api/slice.html>.
    
    - [01:22:50] `contextlib.suppress()`
      <https://docs.python.org/3/library/contextlib.html#contextlib.suppress>.
    
        - Hay que recordar que aunque la excepción se suprime, la
          ejecución del cuerpo se corta en ese punto.
    
    - [01:23:55] pathlib:
      <https://docs.python.org/3/library/pathlib.html>.
    
    - [01:24:20] Usos atípicos de `else`: `if`, `for`, `try`,
      `while`...
    
        - <https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops>.
    
        - <https://docs.python.org/3/tutorial/errors.html#handling-exceptions>.
    
        - Teoría unificada sobre `else` en Python.
    
    - [1:29:15] El orden de los `except ...` **IMPORTA**.
    
    - [01:31:30] Tu yo del futuro tiene que tratar con tu yo del
      pasado. "Escribe código como si el siguiente que tuviera que
      trabajar con el fuese un psicópata asesino que sabe
      donde vives".
    
        - Sistemas de control de versiones: "Annotate" -> "blame".
    
    - [01:33:05] Usos de lambda.
    
        - Módulo Operator: <https://docs.python.org/3/library/operator.html>.
    
    - [01:35:00] Algunos trucos cortos adicionales.
    
        - `collections.deque`:
          <https://docs.python.org/3/library/collections.html>.
    
        - `dateutil`: <https://pypi.org/project/python-dateutil/>.
    
        - `itertools`:
          <https://docs.python.org/3/library/itertools.html>.
    
        - `if a < x < b`:
    
                >>> import dis
                >>> dis.dis(lambda x: a < x < b)
                  1           0 LOAD_GLOBAL              0 (a)
                              2 LOAD_FAST                0 (x)
                              4 DUP_TOP
                              6 ROT_THREE
                              8 COMPARE_OP               0 (<)
                             10 JUMP_IF_FALSE_OR_POP    18
                             12 LOAD_GLOBAL              1 (b)
                             14 COMPARE_OP               0 (<)
                             16 RETURN_VALUE
                        >>   18 ROT_TWO
                             20 POP_TOP
                             22 RETURN_VALUE
    
    
        - Desempaquetado complejo:
    
                >>> a, b, (c, d), *e, f = 1, 2, (3, 4), 5, 6, 7, 8, 9
                >>> print(a,b,c,d,e,f)
                1 2 3 4 [5, 6, 7, 8] 9
    
        - Usar la variable "guión bajo" para descartar valores. Ojo
          con la internacionalización.
    
    - [01:55:30] Python cada vez tiene más "gotchas". Algunos
      ejemplos:
    
        - Operador morsa. Tratado con projilidad en tertulias
          anteriores.
    
        - Parámetros mutables.
    
        - Definir "closures" dentro de un `for` pero usarlo fuera.
    
        - Tuplas con un solo elemento. Es más evidente el constructor
          `tuple()`, pero ojo: `tuple('abc') -> ('a', 'b', 'c')`.
    
    - [02:00:14] ¡Terminamos con los trucos!
    
    - [02:00:45] Ideas para indexar y buscar el documentos:
    
        - Whoosh:
          <https://whoosh.readthedocs.io/en/latest/intro.html>.
    
        - Solr: <https://solr.apache.org/>.
    
    - [02:03:30] Deberes para el futuro: módulos `dis`
      <https://docs.python.org/3/library/dis.html> y `enum`
      <https://docs.python.org/3/library/enum.html>.
    
    - [02:03:55] Sugerencia sobre visión artificial:
      <https://www.pyimagesearch.com/>. De lo mejor que hay.
    
    - [02:05:55] regex <https://pypi.org/project/regex/> que libera el
      GIL <https://en.wikipedia.org/wiki/Global_interpreter_lock>.
    
    - [02:06:55] Acelerador y distribución de programas Python
      precompilados en binario y empaquetados en un directorio e,
      incluso, en un único fichero: Nuitka: <https://nuitka.net/>.
    
    - [02:08:05] Design of CPython’s Garbage Collector:
      <https://devguide.python.org/garbage_collector/>.
    
    - [02:08:25] Cierre.
    
    - [02:10:00] Casi se nos olvida el aviso legal para grabar y
      publicar las sesiones.
    
    - [02:12:03] Final.

  Notice the masive use of timestamps, links and formating.

- After writing the shownotes we add an intro to the audio,
  presenting the podcast, the record date and the topics we are
  going to talk about during session.

  Note that you don't know how long is going to be the intro until
  you record it **after** knowing the topics.

- The intro is 52 seconds long. So, all timestamps must be offset
  by 52 seconds. No problem, the software can apply a global
  timestamp offset when creating the shownotes page and the
  chapters in the audio files.

- We generate the audio files. For my podcast, I generate M4A_ and
  Opus_ audio files.

  No MP3_. **MP3_ MUST DIE!**

  Details of how to generate audio files are out of scope of this
  project.

- Now we check how the shownotes are showed:

  .. code-block:: console

     jcea@jcea:~$ toc2audio.py --offset 52 --show \
                               --chapters ~/docs/Tertulias/20210126.md \
                               Python-17-tertulia-20210126.m4a \
                               Python-17-tertulia-20210126.opus

  .. note::

     Note that we are applying a global timestamp offset of 52
     seconds to accomodate the length of the intro voice
     presenting the original recording. All timestamps you typed
     will be automatically adjusted.

  This invocation will display the raw HTML_ in the console. You
  can copy & paste it to your podcast platform. The program will
  also open a webbrowser displaying the shownotes as the users
  wuould see them. You can visually check the formatting and tune
  the Markdown_ document according to your taste and needs. You
  would see something similar to the main content displayed in
  `Python en español #17: Tertulia 2021-01-26`_.

  If you don't like the result, you can :code:`control+c` the
  program, update the Markdown_ file and retry again unting you
  like it.

- You will see this HTML_ code in your console:

  .. code-block:: html

    <p>Participantes:</p>
    <ul>
    <li>
    <p>Jesús Cea, email: <a href="mailto:jcea@jcea.es">jcea@jcea.es</a>, twitter:
      <a href="https://twitter.com/jcea">@jcea</a>, <a href="https://blog.jcea.es/">https://blog.jcea.es/</a>,
      <a href="https://www.jcea.es/">https://www.jcea.es/</a>. Conectando desde Madrid.</p>
    </li>
    <li>
    <p>Eduardo Castro, email:
      <a href="mailto:info@ecdesign.es">info@ecdesign.es</a>. Conectando desde A
      Guarda.</p>
    </li>
    <li>
    <p>Javier, conectando desde Madrid.</p>
    </li>
    <li>
    <p>Víctor Ramírez, twitter: <a href="https://twitter.com/virako">@virako</a>,
      programador python y amante de vim, conectando desde Huelva.</p>
    </li>
    <li>
    <p>Dani, conectando desde Málaga.</p>
    </li>
    <li>
    <p>Miguel Sánchez, email:
      <a href="msanchez@uninet.edu">msanchez@uninet.edu</a>, conectando desde
      Canarias.</p>
    </li>
    <li>
    <p>Jorge Rúa, conectando desde Vigo.</p>
    </li>
    </ul>
    <p>Audio editado por Pablo Gómez, twitter:
    <a href="https://twitter.com/julebek">@julebek</a>.</p>
    <p>La música de la entrada y la salida es "Lightning Bugs", de Jason
    Shaw. Publicada en <a href="https://audionautix.com/">https://audionautix.com/</a> con licencia
    - <a href="https://audionautix.com/creative-commons-music">Creative Commons Attribution 4.0 International
    License</a>.</p>
    <ul>
    <li>
    <p><timestamp compact="1" offset="52" ts="52"><strong>[00:52]</strong><topic> Haciendo tiempo hasta que entre más gente.</topic></timestamp></p>
    <ul>
    <li>
    <p>Raspberry Pi Pico:
      <a href="https://www.raspberrypi.org/products/raspberry-pi-pico/">https://www.raspberrypi.org/products/raspberry-pi-pico/</a>.</p>
    <ul>
    <li>Jesús Cea está encantado con su rango de alimentación.</li>
    </ul>
    </li>
    <li>
    <p>Micropython: <a href="https://www.micropython.org/">https://www.micropython.org/</a>.</p>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="362"><strong>[06:02]</strong><topic> Truco: <code>Python -i</code>: Ejecuta un script y pasa a modo
      interactivo.</topic></timestamp></p>
    <p>También se puede hacer desde el propio código con
    <code>code.InteractiveConsole(locals=globals()).interact()</code>.</p>
    <p>Jesús Cea se queja de que usando la invocación desde código
    no funciona la edición de líneas. Javier da la pista correcta:
    para que funcione, basta con hacer <code>import readline</code> antes de
    lanzar el modo interactivo.</p>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="677"><strong>[11:17]</strong><topic> Regresión con ipdb: <a href="https://pypi.org/project/ipdb/">https://pypi.org/project/ipdb/</a>.</topic></timestamp></p>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="757"><strong>[12:37]</strong><topic> Nueva versión de Pyston <a href="https://www.pyston.org/">https://www.pyston.org/</a>.</topic></timestamp></p>
    <ul>
    <li>Intérprete de Python más rápido. Un 50% más rápido que
      cpython.</li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="982"><strong>[16:22]</strong><topic> Ver si dos fechas son iguales con <code>datetime</code>
      <a href="https://docs.python.org/3/library/datetime.html">https://docs.python.org/3/library/datetime.html</a>.</topic></timestamp></p>
    <ul>
    <li>Trabajar siempre en UTC
      <a href="https://es.wikipedia.org/wiki/Tiempo_universal_coordinado">https://es.wikipedia.org/wiki/Tiempo_universal_coordinado</a>,
      aunque solo tengas una zona horaria.</li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="1192"><strong>[19:52]</strong><topic> Jesús Cea ha investigado cómo funcionan los POSTs HTTP
      en las protecciones CSRF <a href="https://es.wikipedia.org/wiki/CSRF">https://es.wikipedia.org/wiki/CSRF</a>.</topic></timestamp></p>
    <ul>
    <li>
    <p>Buena práctica: La respuesta al POST es una redirección a un
      GET. Patrón Post/Redirect/Get (PRG)
      <a href="https://es.wikipedia.org/wiki/Post/Redirect/Get">https://es.wikipedia.org/wiki/Post/Redirect/Get</a>.</p>
    </li>
    <li>
    <p>Ventajas de usar un framework.</p>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="1472"><strong>[24:32]</strong><topic> ¿Optimizaciones cuando tienes grandes cantidades de
      datos?</topic></timestamp></p>
    <ul>
    <li>
    <p>Tema muy amplio, hacen falta detalles del problema.</p>
    </li>
    <li>
    <p>Se ofrecen algunas ideas:</p>
    <ul>
    <li>
    <p>Map/Reduce: <a href="https://en.wikipedia.org/wiki/Map_reduce">https://en.wikipedia.org/wiki/Map_reduce</a>.</p>
    </li>
    <li>
    <p>Usar generadores u otras construcciones "lazy" siempre
      que sea posible.
      <a href="https://wiki.python.org/moin/Generators">https://wiki.python.org/moin/Generators</a>.</p>
    </li>
    </ul>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="1912"><strong>[31:52]</strong><topic> Gestión de memoria en Python.</topic></timestamp></p>
    <ul>
    <li>
    <p>Design of CPython’s Garbage Collector:
      <a href="https://devguide.python.org/garbage_collector/">https://devguide.python.org/garbage_collector/</a>.</p>
    </li>
    <li>
    <p>Hora de sacar la basura garbage collector - Pablo Galindo y
      Victor Terrón - PyConES 2018
      <a href="https://www.youtube.com/watch?v=G9wOSExzs5g">https://www.youtube.com/watch?v=G9wOSExzs5g</a>.</p>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="2117"><strong>[35:17]</strong><topic> Tipografía para programadores:</topic></timestamp></p>
    <ul>
    <li>
    <p>Victor Mono: <a href="https://rubjo.github.io/victor-mono/">https://rubjo.github.io/victor-mono/</a>.</p>
    </li>
    <li>
    <p>Fira Code: <a href="https://fonts.google.com/specimen/Fira+Code">https://fonts.google.com/specimen/Fira+Code</a>.</p>
    </li>
    <li>
    <p>Fira Code Retina:
      <a href="https://github.com/tonsky/FiraCode/issues/872">https://github.com/tonsky/FiraCode/issues/872</a>.</p>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="2237"><strong>[37:17]</strong><topic> Eduardo Castro se ha currado una lista de trucos
      sencillos pero interesantes:</topic></timestamp></p>
    <p><strong>En estas notas solo referenciamos los puntos a los que
    dedicamos más tiempo, se habló de más cosas</strong>.</p>
    <p><strong>El documento para poder seguir los comentarios de la
    grabación está en <a href="https://demo.hedgedoc.org/s/hEZB92q40#">https://demo.hedgedoc.org/s/hEZB92q40#</a>.</strong></p>
    <ul>
    <li>
    <p><code>hash(float('inf')) -&gt; 314159</code>.</p>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="2582"><strong>[43:02]</strong><topic> LRU Caché:
      &lt;<a href="https://docs.python.org/3/library/functools.html#functools.lru_cache">https://docs.python.org/3/library/functools.html#functools.lru_cache</a>.</topic></timestamp></p>
    <ul>
    <li>Bugs abundantes en LRU Cache y múltiples hilos:
      <a href="https://bugs.python.org/issue?%40columns=id%2Cactivity%2Ctitle%2Ccreator%2Cassignee%2Cstatus%2Ctype&amp;%40sort=-activity&amp;%40filter=status&amp;%40action=searchid&amp;ignore=file%3Acontent&amp;%40search_text=lru_cache+threads&amp;submit=search&amp;status=-1%2C1%2C2%2C3">https://bugs.python.org/issue?%40columns=id%2Cactivity%2Ctitle%2Ccreator%2Cassignee%2Cstatus%2Ctype&amp;%40sort=-activity&amp;%40filter=status&amp;%40action=searchid&amp;ignore=file%3Acontent&amp;%40search_text=lru_cache+threads&amp;submit=search&amp;status=-1%2C1%2C2%2C3</a>.</li>
    </ul>
    </li>
    <li>
    <p>Yield:</p>
    <ul>
    <li>
    <p>Ojo con excepciones y filtraciones de memoria.</p>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="2917"><strong>[48:37]</strong><topic> Uso interesante con los "context managers":
      <code>@contextlib.contextmanager</code>
      <a href="https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager">https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager</a>
      y <code>@contextlib.asynccontextmanager</code>
      <a href="https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager">https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager</a>.</topic></timestamp></p>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="3072"><strong>[51:12]</strong><topic> itertools:
      <a href="https://docs.python.org/3/library/itertools.html">https://docs.python.org/3/library/itertools.html</a>. A Jesús
      Cea no le entra en la cabeza la programación funcional.</topic></timestamp></p>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="1" offset="52" ts="3362"><strong>[56:02]</strong><topic> ¿Qué es ser Pythonico?</topic></timestamp></p>
    <ul>
    <li>
    <p>Aunque esté en la biblioteca estándar, no significa que sea
      pythónico:</p>
    <ul>
    <li>
    <p>asyncore:
      <a href="https://docs.python.org/3/library/asyncore.html">https://docs.python.org/3/library/asyncore.html</a>. Está
      marcado como obsoleto desde Python 3.6.</p>
    </li>
    <li>
    <p>Mover métodos funcionales en una librería separada.</p>
    </li>
    <li>
    <p>Las dos jerarquías distintas que existían en Python 2.
      Esto se unificó en Python 3.</p>
    </li>
    <li>
    <p><code>from __future__ import ...</code>.</p>
    </li>
    <li>
    <p>La migración a Python 3 fue un intento de simplificar el
      lenguaje. Pero Python 3 se está complicando cada vez
      más.</p>
    <ul>
    <li>La complejidad fragmenta los diferentes idiomas del
      lenguaje.</li>
    </ul>
    </li>
    </ul>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="4102"><strong>[01:08:22]</strong><topic> Seguimos desgranando los trucos propuestos por
      Eduardo.</topic></timestamp></p>
    <ul>
    <li><code>collections.defaultdict()</code>:
      <a href="https://docs.python.org/3/library/collections.html#collections.defaultdict">https://docs.python.org/3/library/collections.html#collections.defaultdict</a>.</li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="4272"><strong>[01:11:12]</strong><topic> <code>iter()</code> y <code>next()</code> admiten una parametro extra
      centinela opcional que especifica un valor que termina el
      iterador.</topic></timestamp></p>
    <ul>
    <li>Utilizar objetos centinelas que no sean <code>None</code>, porque
      <code>None</code> puede ser un objeto válido.</li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="4652"><strong>[01:17:32]</strong><topic> Los "slices" son objetos que se pueden crear y
      utilizar: <code>slice(1,100)</code>.</topic></timestamp></p>
    <ul>
    <li>
    <p>Pasar un iterador a una función abre posibilidades
      interesantes.</p>
    </li>
    <li>
    <p><code>Slice Objects</code>: <a href="https://docs.python.org/3/c-api/slice.html">https://docs.python.org/3/c-api/slice.html</a>.</p>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="5022"><strong>[01:23:42]</strong><topic> <code>contextlib.suppress()</code>
      <a href="https://docs.python.org/3/library/contextlib.html#contextlib.suppress">https://docs.python.org/3/library/contextlib.html#contextlib.suppress</a>.</topic></timestamp></p>
    <ul>
    <li>Hay que recordar que aunque la excepción se suprime, la
      ejecución del cuerpo se corta en ese punto.</li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="5087"><strong>[01:24:47]</strong><topic> pathlib:
      <a href="https://docs.python.org/3/library/pathlib.html">https://docs.python.org/3/library/pathlib.html</a>.</topic></timestamp></p>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="5112"><strong>[01:25:12]</strong><topic> Usos atípicos de <code>else</code>: <code>if</code>, <code>for</code>, <code>try</code>,
      <code>while</code>...</topic></timestamp></p>
    <ul>
    <li>
    <p><a href="https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops">https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops</a>.</p>
    </li>
    <li>
    <p><a href="https://docs.python.org/3/tutorial/errors.html#handling-exceptions">https://docs.python.org/3/tutorial/errors.html#handling-exceptions</a>.</p>
    </li>
    <li>
    <p>Teoría unificada sobre <code>else</code> en Python.</p>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="5407"><strong>[01:30:07]</strong><topic> El orden de los <code>except ...</code> <strong>IMPORTA</strong>.</topic></timestamp></p>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="5542"><strong>[01:32:22]</strong><topic> Tu yo del futuro tiene que tratar con tu yo del
      pasado. "Escribe código como si el siguiente que tuviera que
      trabajar con el fuese un psicópata asesino que sabe
      donde vives".</topic></timestamp></p>
    <ul>
    <li>Sistemas de control de versiones: "Annotate" -&gt; "blame".</li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="5637"><strong>[01:33:57]</strong><topic> Usos de lambda.</topic></timestamp></p>
    <ul>
    <li>Módulo Operator: <a href="https://docs.python.org/3/library/operator.html">https://docs.python.org/3/library/operator.html</a>.</li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="5752"><strong>[01:35:52]</strong><topic> Algunos trucos cortos adicionales.</topic></timestamp></p>
    <ul>
    <li>
    <p><code>collections.deque</code>:
      <a href="https://docs.python.org/3/library/collections.html">https://docs.python.org/3/library/collections.html</a>.</p>
    </li>
    <li>
    <p><code>dateutil</code>: <a href="https://pypi.org/project/python-dateutil/">https://pypi.org/project/python-dateutil/</a>.</p>
    </li>
    <li>
    <p><code>itertools</code>:
      <a href="https://docs.python.org/3/library/itertools.html">https://docs.python.org/3/library/itertools.html</a>.</p>
    </li>
    <li>
    <p><code>if a &lt; x &lt; b</code>:</p>
    <pre><code>&gt;&gt;&gt; import dis
    &gt;&gt;&gt; dis.dis(lambda x: a &lt; x &lt; b)
      1           0 LOAD_GLOBAL              0 (a)
                  2 LOAD_FAST                0 (x)
                  4 DUP_TOP
                  6 ROT_THREE
                  8 COMPARE_OP               0 (&lt;)
                 10 JUMP_IF_FALSE_OR_POP    18
                 12 LOAD_GLOBAL              1 (b)
                 14 COMPARE_OP               0 (&lt;)
                 16 RETURN_VALUE
            &gt;&gt;   18 ROT_TWO
                 20 POP_TOP
                 22 RETURN_VALUE
    </code></pre>
    </li>
    <li>
    <p>Desempaquetado complejo:</p>
    <pre><code>&gt;&gt;&gt; a, b, (c, d), *e, f = 1, 2, (3, 4), 5, 6, 7, 8, 9
    &gt;&gt;&gt; print(a,b,c,d,e,f)
    1 2 3 4 [5, 6, 7, 8] 9
    </code></pre>
    </li>
    <li>
    <p>Usar la variable "guión bajo" para descartar valores. Ojo
      con la internacionalización.</p>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="6982"><strong>[01:56:22]</strong><topic> Python cada vez tiene más "gotchas". Algunos
      ejemplos:</topic></timestamp></p>
    <ul>
    <li>
    <p>Operador morsa. Tratado con projilidad en tertulias
      anteriores.</p>
    </li>
    <li>
    <p>Parámetros mutables.</p>
    </li>
    <li>
    <p>Definir "closures" dentro de un <code>for</code> pero usarlo fuera.</p>
    </li>
    <li>
    <p>Tuplas con un solo elemento. Es más evidente el constructor
      <code>tuple()</code>, pero ojo: <code>tuple('abc') -&gt; ('a', 'b', 'c')</code>.</p>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="7266"><strong>[02:01:06]</strong><topic> ¡Terminamos con los trucos!</topic></timestamp></p>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="7297"><strong>[02:01:37]</strong><topic> Ideas para indexar y buscar el documentos:</topic></timestamp></p>
    <ul>
    <li>
    <p>Whoosh:
      <a href="https://whoosh.readthedocs.io/en/latest/intro.html">https://whoosh.readthedocs.io/en/latest/intro.html</a>.</p>
    </li>
    <li>
    <p>Solr: <a href="https://solr.apache.org/">https://solr.apache.org/</a>.</p>
    </li>
    </ul>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="7462"><strong>[02:04:22]</strong><topic> Deberes para el futuro: módulos <code>dis</code>
      <a href="https://docs.python.org/3/library/dis.html">https://docs.python.org/3/library/dis.html</a> y <code>enum</code>
      <a href="https://docs.python.org/3/library/enum.html">https://docs.python.org/3/library/enum.html</a>.</topic></timestamp></p>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="7487"><strong>[02:04:47]</strong><topic> Sugerencia sobre visión artificial:
      <a href="https://www.pyimagesearch.com/">https://www.pyimagesearch.com/</a>. De lo mejor que hay.</topic></timestamp></p>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="7607"><strong>[02:06:47]</strong><topic> regex <a href="https://pypi.org/project/regex/">https://pypi.org/project/regex/</a> que libera el
      GIL <a href="https://en.wikipedia.org/wiki/Global_interpreter_lock">https://en.wikipedia.org/wiki/Global_interpreter_lock</a>.</topic></timestamp></p>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="7667"><strong>[02:07:47]</strong><topic> Acelerador y distribución de programas Python
      precompilados en binario y empaquetados en un directorio e,
      incluso, en un único fichero: Nuitka: <a href="https://nuitka.net/">https://nuitka.net/</a>.</topic></timestamp></p>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="7737"><strong>[02:08:57]</strong><topic> Design of CPython’s Garbage Collector:
      <a href="https://devguide.python.org/garbage_collector/">https://devguide.python.org/garbage_collector/</a>.</topic></timestamp></p>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="7757"><strong>[02:09:17]</strong><topic> Cierre.</topic></timestamp></p>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="7852"><strong>[02:10:52]</strong><topic> Casi se nos olvida el aviso legal para grabar y
      publicar las sesiones.</topic></timestamp></p>
    </li>
    <li>
    <p><timestamp compact="0" offset="52" ts="7975"><strong>[02:12:55]</strong><topic> Final.</topic></timestamp></p>
    </li>
    </ul>
    
    We applied an offset of 52 seconds (00:52) to all timestamps
    Press ENTER to continue

  You can copy&paste this HTML_ code to your podcast platform.

  .. note::

    Notice the presence of custom :code:`<timestamp>` tags.
    Browsers will ignore them, but some other software could find
    them useful.

- After you copied the HTML_ formatted shownotes, you press
  :code:`ENTER` and toc2audio will add chapter information to the
  audio files you indicated.

- After the audio files metadata is updated, the console will
  display chapter summary:

  .. code-block::

    Chapters:
    00:00:00 - 00:00:52: ( 0m 52s): ---
    00:00:52 - 00:06:02: ( 5m 10s): Haciendo tiempo hasta que entre más gente.
    00:06:02 - 00:11:17: ( 5m 15s): Truco: Python -i: Ejecuta un script y pasa a modo interactivo.
    00:11:17 - 00:12:37: ( 1m 20s): Regresión con ipdb: https://pypi.org/project/ipdb/.
    00:12:37 - 00:16:22: ( 3m 45s): Nueva versión de Pyston https://www.pyston.org/.
    00:16:22 - 00:19:52: ( 3m 30s): Ver si dos fechas son iguales con datetime https://docs.python.org/3/library/datetime.html.
    00:19:52 - 00:24:32: ( 4m 40s): Jesús Cea ha investigado cómo funcionan los POSTs HTTP en las protecciones CSRF https://es.wikipedia.org/wiki/CSRF.
    00:24:32 - 00:31:52: ( 7m 20s): ¿Optimizaciones cuando tienes grandes cantidades de datos?
    00:31:52 - 00:35:17: ( 3m 25s): Gestión de memoria en Python.
    00:35:17 - 00:37:17: ( 2m  0s): Tipografía para programadores:
    00:37:17 - 00:43:02: ( 5m 45s): Eduardo Castro se ha currado una lista de trucos sencillos pero interesantes:
    00:43:02 - 00:48:37: ( 5m 35s): LRU Caché: <https://docs.python.org/3/library/functools.html#functools.lru_cache.
    00:48:37 - 00:51:12: ( 2m 35s): Uso interesante con los "context managers": @contextlib.contextmanager https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager y @contextlib.asynccontextmanager https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager.
    00:51:12 - 00:56:02: ( 4m 50s): itertools: https://docs.python.org/3/library/itertools.html. A Jesús Cea no le entra en la cabeza la programación funcional.
    00:56:02 - 01:08:22: (12m 20s): ¿Qué es ser Pythonico?
    01:08:22 - 01:11:12: ( 2m 50s): Seguimos desgranando los trucos propuestos por Eduardo.
    01:11:12 - 01:17:32: ( 6m 20s): iter() y next() admiten una parametro extra centinela opcional que especifica un valor que termina el iterador.
    01:17:32 - 01:23:42: ( 6m 10s): Los "slices" son objetos que se pueden crear y utilizar: slice(1,100).
    01:23:42 - 01:24:47: ( 1m  5s): contextlib.suppress() https://docs.python.org/3/library/contextlib.html#contextlib.suppress.
    01:24:47 - 01:25:12: ( 0m 25s): pathlib: https://docs.python.org/3/library/pathlib.html.
    01:25:12 - 01:30:07: ( 4m 55s): Usos atípicos de else: if, for, try, while...
    01:30:07 - 01:32:22: ( 2m 15s): El orden de los except ... IMPORTA.
    01:32:22 - 01:33:57: ( 1m 35s): Tu yo del futuro tiene que tratar con tu yo del pasado. "Escribe código como si el siguiente que tuviera que trabajar con el fuese un psicópata asesino que sabe donde vives".
    01:33:57 - 01:35:52: ( 1m 55s): Usos de lambda.
    01:35:52 - 01:56:22: (20m 30s): Algunos trucos cortos adicionales.
    01:56:22 - 02:01:06: ( 4m 44s): Python cada vez tiene más "gotchas". Algunos ejemplos:
    02:01:06 - 02:01:37: ( 0m 31s): ¡Terminamos con los trucos!
    02:01:37 - 02:04:22: ( 2m 45s): Ideas para indexar y buscar el documentos:
    02:04:22 - 02:04:47: ( 0m 25s): Deberes para el futuro: módulos dis https://docs.python.org/3/library/dis.html y enum https://docs.python.org/3/library/enum.html.
    02:04:47 - 02:06:47: ( 2m  0s): Sugerencia sobre visión artificial: https://www.pyimagesearch.com/. De lo mejor que hay.
    02:06:47 - 02:07:47: ( 1m  0s): regex https://pypi.org/project/regex/ que libera el GIL https://en.wikipedia.org/wiki/Global_interpreter_lock.
    02:07:47 - 02:08:57: ( 1m 10s): Acelerador y distribución de programas Python precompilados en binario y empaquetados en un directorio e, incluso, en un único fichero: Nuitka: https://nuitka.net/.
    02:08:57 - 02:09:17: ( 0m 20s): Design of CPython’s Garbage Collector: https://devguide.python.org/garbage_collector/.
    02:09:17 - 02:10:52: ( 1m 35s): Cierre.
    02:10:52 - 02:12:55: ( 2m  3s): Casi se nos olvida el aviso legal para grabar y publicar las sesiones.
    02:12:55 -                    : Final.

  Here you see all chapter information added to the audio file,
  start and end time of each chapter, length information and
  title.

  Note a few details:

  - Many audio file formats require the chapter information to
    cover the entire file. toc2audio will include a dummy chapter
    named :code:`---` if your first chapter doesn't start at
    :code:`00:00`. This implicit chapter will be added too if you
    apply a timestamp offset, for the very same reason.

    In this example, I wrote in the Markdown_ document that my
    first chapter starts at :code:`00:00`, but I am applying a
    global timestamp offset of 52 seconds, so my first chapter
    will start now at :code:`00:52` and toc2audio will add a dummy
    charter called :code:`---` covering from :code:`00:00` to
    :code:`00:52`, the start of my first explicit chapter.

  - The chapters list is flat (lineal), beside the hierarchical
    format of the Markdown_ document.

  - The last chapter shows no duration details. toc2audio will end
    it implicitly at the end of the audio file.

    .. note::

       A future release of toc2audio might display the actual end
       of the last chapter after analyzing the audio file.

- Congrats. Your audio file have been updated with chapter
  information.

- Now you can test your audio files using any player supporting
  chapter metadata, like `mplayer <http://www.mplayerhq.hu/>`__.
  Move around with :code:`!` and :code:`@`.

If you don't like the final result, you can edit the Markdown_
document again and repeat the entire procedure. It is fast and
toc2audio doesn't care if the audio files you are enhancing
already have chapter information. it will happily overwrite it
with the new version.

You can see the result online: `Python en español #17: Tertulia
2021-01-26`_.
