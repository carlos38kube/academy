import json

src = open('docker-leccion-compose.html', encoding='utf-8').read()
head = src[:src.index('<main>') + len('<main>')]
tail = src[src.index('<div class="bottombar">'):]
a = tail.index('  const mc0 =')
b = tail.index('  actionBtn.addEventListener')

JS = """  const EX = __EX__;
  function norm(s) { return s.toLowerCase().replace(/["'`]/g, '').replace(/\\s+/g, ' ').trim(); }
  const mcs = {};
  exercises.forEach((el, i) => { if (EX[i].t === 'mc') mcs[i] = setupMultipleChoice(el); });
  const checkers = EX.map((e, i) => () => {
    if (e.t === 'mc') return mcs[i].check('¡Correcto! ' + e.ok, 'No es así. ' + e.ok);
    const v = norm(document.getElementById('in-' + i).value);
    if (!v) return null;
    const c = e.t === 'fill' ? e.a.some(x => norm(x) === v) : e.k.every(x => v.includes(norm(x)));
    showFeedback(exercises[i], c, c ? '¡Correcto! ' + e.ok : 'Casi. ' + e.ok);
    return c;
  });

"""

def M(q, opts, c, ok): return {'t': 'mc', 'q': q, 'opts': opts, 'c': c, 'ok': ok}
def F(q, code, a, ok): return {'t': 'fill', 'q': q, 'code': code, 'a': a, 'ok': ok}
def W(q, k, ok): return {'t': 'write', 'q': q, 'k': k, 'ok': ok}

L = []
def add(course, name, num, title, done, ex): L.append((course, name, num, title, done, ex))

D = 'docker'
add(D, 'contenedores', 1, 'Qué es un contenedor', 'Ya sabes qué es un contenedor y en qué se diferencia de una imagen y de una VM.', [
  M('¿Cuál es la diferencia entre una imagen y un contenedor?', ['Son lo mismo', 'La imagen es la plantilla y el contenedor es una instancia en ejecución', 'El contenedor es la plantilla y la imagen es la instancia', 'La imagen solo existe en Docker Hub'], 1, 'La imagen es la plantilla; el contenedor es una instancia en ejecución.'),
  F('Completa el comando para listar los contenedores en ejecución.', 'docker ___', ['ps', 'container ls', 'container ps'], 'El comando es docker ps.'),
  M('¿Qué diferencia a un contenedor de una máquina virtual?', ['Incluye un sistema operativo completo', 'Comparte el kernel del host y es más ligero', 'Necesita un hipervisor', 'Solo funciona en Windows'], 1, 'Un contenedor comparte el kernel del host, por eso es más ligero que una VM.'),
  W('Escribe el comando para ejecutar un contenedor de nginx en segundo plano.', ['docker', 'run', '-d', 'nginx'], 'docker run -d nginx ejecuta el contenedor en segundo plano.')])
add(D, 'comandos', 2, 'Comandos básicos', 'Ya dominas run, ps y stop.', [
  M('¿Qué comando detiene un contenedor en ejecución?', ['docker halt', 'docker stop', 'docker pause-all', 'docker end'], 1, 'docker stop detiene un contenedor en ejecución.'),
  F('Completa el comando para ejecutar nginx en segundo plano.', 'docker ___ -d nginx', ['run', 'container run'], 'El comando es docker run.'),
  M('¿Qué hace docker ps -a?', ['Lista solo los contenedores en ejecución', 'Lista todos los contenedores, también los detenidos', 'Elimina los contenedores detenidos', 'Muestra las imágenes'], 1, 'docker ps -a lista todos los contenedores, también los detenidos.'),
  W('Escribe el comando para detener un contenedor llamado web.', ['docker', 'stop', 'web'], 'docker stop web detiene el contenedor llamado web.')])
add(D, 'imagenes', 3, 'Imágenes', 'Ya sabes listar, descargar y borrar imágenes.', [
  M('¿Qué comando descarga una imagen desde un registro?', ['docker get', 'docker pull', 'docker download', 'docker fetch'], 1, 'docker pull descarga una imagen.'),
  F('Completa el comando para listar las imágenes locales.', 'docker ___', ['images', 'image ls'], 'El comando es docker images.'),
  M('¿Qué hace docker rmi?', ['Elimina un contenedor', 'Elimina una imagen', 'Reinicia un contenedor', 'Renombra una imagen'], 1, 'docker rmi elimina una imagen local.'),
  W('Escribe el comando para descargar la imagen ubuntu.', ['docker', 'pull', 'ubuntu'], 'docker pull ubuntu descarga la imagen ubuntu.')])
add(D, 'dockerfile', 4, 'Dockerfile', 'Ya sabes escribir un Dockerfile básico.', [
  M('¿Qué instrucción define la imagen base de un Dockerfile?', ['BASE', 'FROM', 'IMAGE', 'START'], 1, 'FROM define la imagen base.'),
  F('Completa la instrucción para copiar un archivo a la imagen.', 'FROM node:20\n___ package.json /app/', ['COPY', 'ADD'], 'COPY copia archivos del contexto a la imagen.'),
  M('¿Qué diferencia hay entre RUN y CMD?', ['Ninguna', 'RUN se ejecuta al construir la imagen y CMD define el comando por defecto al arrancar', 'CMD se ejecuta al construir y RUN al arrancar', 'RUN solo sirve en Windows'], 1, 'RUN se ejecuta al construir; CMD es el comando por defecto al arrancar el contenedor.'),
  W('Escribe un Dockerfile mínimo: base nginx y copiar index.html a /usr/share/nginx/html/.', ['from', 'nginx', 'copy', 'index.html'], 'FROM nginx y COPY index.html /usr/share/nginx/html/.')])
add(D, 'build', 5, 'Construir imágenes', 'Ya sabes construir y etiquetar imágenes.', [
  M('¿Para qué sirve la opción -t en docker build?', ['Para probar la imagen', 'Para ponerle nombre y etiqueta a la imagen', 'Para usar TLS', 'Para acelerar el build'], 1, '-t asigna nombre y etiqueta a la imagen.'),
  F('Completa el comando para construir la imagen miapp.', 'docker build ___ miapp .', ['-t', '--tag'], 'La opción es -t.'),
  M('¿Qué indica el punto final en docker build -t miapp . ?', ['El nombre del archivo', 'El contexto de build: el directorio actual', 'La versión', 'Nada'], 1, 'El punto es el contexto de build: el directorio actual.'),
  W('Escribe el comando para construir una imagen llamada miapp:1.0 desde el directorio actual.', ['docker', 'build', '-t', 'miapp:1.0'], 'docker build -t miapp:1.0 . construye la imagen.')])
add(D, 'volumenes', 6, 'Volúmenes', 'Ya sabes persistir datos con volúmenes.', [
  M('¿Para qué sirven los volúmenes?', ['Para subir el volumen del audio', 'Para que los datos persistan aunque el contenedor se elimine', 'Para acelerar la red', 'Para comprimir imágenes'], 1, 'Los volúmenes conservan los datos aunque el contenedor se elimine.'),
  F('Completa la opción para montar el volumen datos.', 'docker run -d ___ datos:/var/lib/data nginx', ['-v', '--volume'], 'La opción es -v.'),
  M('¿Qué comando crea un volumen?', ['docker volume create', 'docker create volume', 'docker mkvol', 'docker new volume'], 0, 'docker volume create crea un volumen.'),
  W('Escribe el comando para ejecutar nginx montando el volumen datos en /data.', ['docker', 'run', '-v', 'datos:/data', 'nginx'], 'docker run -v datos:/data nginx monta el volumen.')])
add(D, 'redes', 7, 'Redes y puertos', 'Ya sabes publicar puertos y conectar contenedores.', [
  M('¿Qué significa -p 8080:80?', ['El puerto 80 del host va al 8080 del contenedor', 'El puerto 8080 del host redirige al 80 del contenedor', 'Abre ambos puertos en el firewall', 'Limita a 8080 conexiones'], 1, 'Publica el puerto 80 del contenedor en el 8080 del host.'),
  F('Completa la opción para publicar el puerto.', 'docker run -d ___ 8080:80 nginx', ['-p', '--publish'], 'La opción es -p.'),
  M('En una red creada por el usuario, ¿cómo se encuentran los contenedores entre sí?', ['Por su nombre, con el DNS interno', 'Solo por IP fija', 'No pueden comunicarse', 'Solo por el puerto 80'], 0, 'Se resuelven por nombre gracias al DNS interno de Docker.'),
  W('Escribe el comando para crear una red llamada mired.', ['docker', 'network', 'create', 'mired'], 'docker network create mired crea la red.')])

X = 'linux'
add(X, 'navegacion', 1, 'Navegación', 'Ya sabes moverte por el sistema de archivos.', [
  M('¿Qué comando muestra el directorio actual?', ['where', 'pwd', 'dir', 'path'], 1, 'pwd muestra el directorio actual.'),
  F('Completa el comando para entrar en /var/log.', '___ /var/log', ['cd'], 'cd cambia de directorio.'),
  M('¿Qué muestra ls -l?', ['Solo nombres', 'Lista detallada con permisos, tamaño y fecha', 'Archivos ocultos únicamente', 'El árbol de directorios'], 1, 'ls -l muestra una lista detallada.'),
  W('Escribe el comando para volver a tu directorio personal.', ['cd'], 'cd sin argumentos (o cd ~) vuelve al directorio personal.')])
add(X, 'archivos', 2, 'Archivos y directorios', 'Ya sabes crear, copiar, mover y borrar archivos.', [
  M('¿Qué comando crea un archivo vacío?', ['touch', 'new', 'create', 'mkfile'], 0, 'touch crea un archivo vacío.'),
  F('Completa el comando para crear directorios anidados.', 'mkdir ___ proyectos/app', ['-p'], 'mkdir -p crea también los directorios intermedios.'),
  M('¿Qué hace rm -r?', ['Renombra', 'Elimina directorios de forma recursiva', 'Restaura archivos', 'Lee archivos'], 1, 'rm -r elimina directorios recursivamente.'),
  W('Escribe el comando para copiar a.txt como b.txt.', ['cp', 'a.txt', 'b.txt'], 'cp a.txt b.txt copia el archivo.')])
add(X, 'ver-contenido', 3, 'Ver contenido', 'Ya sabes leer archivos desde la terminal.', [
  M('¿Qué comando muestra las últimas líneas de un archivo?', ['head', 'tail', 'last', 'end'], 1, 'tail muestra las últimas líneas.'),
  F('Completa la opción para seguir un log en tiempo real.', 'tail ___ /var/log/syslog', ['-f'], 'tail -f sigue el archivo en tiempo real.'),
  M('¿Para qué sirve less?', ['Para borrar líneas', 'Para leer un archivo paginado', 'Para comprimir', 'Para contar líneas'], 1, 'less permite leer archivos largos página a página.'),
  W('Escribe el comando para ver las primeras 5 líneas de log.txt usando -n.', ['head', '-n', '5', 'log.txt'], 'head -n 5 log.txt muestra las 5 primeras líneas.')])
add(X, 'permisos', 4, 'Permisos', 'Ya sabes cambiar permisos y propietarios.', [
  M('¿Qué permite chmod 755 archivo?', ['Todo a todos', 'Dueño rwx; grupo y otros r-x', 'Solo lectura para todos', 'Nada'], 1, '755 da rwx al dueño y r-x al grupo y a otros.'),
  F('Completa el comando para cambiar permisos.', '___ 644 notas.txt', ['chmod'], 'chmod cambia los permisos.'),
  M('¿Qué hace chown?', ['Cambia permisos', 'Cambia el propietario', 'Cambia el nombre', 'Cambia el shell'], 1, 'chown cambia el propietario de un archivo.'),
  W('Escribe el comando para dar permiso de ejecución a script.sh.', ['chmod', '+x', 'script.sh'], 'chmod +x script.sh da permiso de ejecución.')])
add(X, 'procesos', 5, 'Procesos', 'Ya sabes listar y terminar procesos.', [
  M('¿Qué comando muestra los procesos en tiempo real?', ['top', 'ps -x', 'proc', 'jobs -all'], 0, 'top muestra los procesos en tiempo real.'),
  F('Completa la señal para forzar la terminación del proceso.', 'kill ___ 1234', ['-9', '-kill', '-sigkill'], 'kill -9 fuerza la terminación.'),
  M('¿Qué hace ps aux?', ['Lista todos los procesos del sistema', 'Reinicia procesos', 'Muestra solo tu shell', 'Borra procesos'], 0, 'ps aux lista todos los procesos.'),
  W('Escribe un comando para buscar procesos de nginx con ps aux y grep.', ['ps', 'aux', 'grep', 'nginx'], 'ps aux | grep nginx filtra los procesos de nginx.')])
add(X, 'redireccion', 6, 'Redirección y pipes', 'Ya sabes redirigir salidas y encadenar comandos.', [
  M('¿Qué hace >> ?', ['Sobrescribe el archivo', 'Añade la salida al final del archivo', 'Lee un archivo', 'Borra el archivo'], 1, '>> añade al final sin borrar lo anterior.'),
  F('Completa el operador para guardar la salida en lista.txt.', 'ls ___ lista.txt', ['>'], '> redirige la salida a un archivo.'),
  M('¿Qué hace el símbolo | ?', ['Pasa la salida de un comando como entrada del siguiente', 'Ejecuta en segundo plano', 'Comenta la línea', 'Borra la salida'], 0, 'El pipe conecta la salida de un comando con la entrada de otro.'),
  W('Escribe el comando para guardar la salida de date en fecha.txt.', ['date', '>', 'fecha.txt'], 'date > fecha.txt guarda la salida en el archivo.')])
add(X, 'variables-entorno', 7, 'Variables de entorno', 'Ya sabes definir y leer variables de entorno.', [
  M('¿Qué hace export?', ['Exporta un archivo', 'Hace visible la variable a los procesos hijos', 'Borra la variable', 'Guarda en disco'], 1, 'export hace que la variable llegue a los procesos hijos.'),
  F('Completa el comando para exportar la variable.', '___ MI_VAR=hola', ['export'], 'export define una variable de entorno.'),
  M('¿Qué es PATH?', ['Una carpeta personal', 'La lista de directorios donde el shell busca ejecutables', 'El usuario actual', 'El nombre del host'], 1, 'PATH es la lista de directorios donde se buscan los ejecutables.'),
  W('Escribe el comando para mostrar el valor de la variable HOME.', ['echo', '$HOME'], 'echo $HOME muestra el valor de HOME.')])

LABEL = {'docker': 'Docker desde cero', 'linux': 'Terminal & Linux básico'}

def body(course, num, done, ex):
    out = ['\n  <div class="lesson-label">%s · Lección %d</div>\n' % (LABEL[course], num)]
    for i, e in enumerate(ex):
        out.append('  <div class="exercise%s" data-index="%d">' % (' active' if i == 0 else '', i))
        out.append('    <div class="prompt">%s</div>' % e['q'])
        if e['t'] == 'mc':
            out.append('    <div class="options">')
            for j, o in enumerate(e['opts']):
                out.append('      <div class="option" data-correct="%s">%s</div>' % ('true' if j == e['c'] else 'false', o))
            out.append('    </div>')
        elif e['t'] == 'fill':
            out.append('    <div class="code-block">%s</div>' % e['code'])
            out.append('    <input type="text" class="fill-input" id="in-%d" placeholder="?" autocomplete="off">' % i)
        else:
            out.append('    <textarea class="code-input" id="in-%d" placeholder="Escribe tu respuesta aquí..."></textarea>' % i)
        out.append('    <div class="feedback"></div>\n  </div>\n')
    out.append('''  <div class="complete-screen" id="complete-screen">
    <div class="glyph">✓</div>
    <h2>¡Lección completada!</h2>
    <p>%s</p>
    <div class="complete-stats">
      <div><div class="num" id="final-xp">0</div><div class="lbl">XP ganado</div></div>
      <div><div class="num" id="final-hearts">3</div><div class="lbl">Vidas restantes</div></div>
    </div>
  </div>
</main>

''' % done)
    return '\n'.join(out)

for course, name, num, title, done, ex in L:
    h = head.replace('Lección: Docker Compose', 'Lección: ' + title)
    data = [{k: v for k, v in e.items() if k in ('t', 'a', 'k', 'ok')} for e in ex]
    js = JS.replace('__EX__', json.dumps(data, ensure_ascii=False))
    fn = '%s-leccion-%s.html' % (course, name)
    open(fn, 'w', encoding='utf-8').write(h + body(course, num, done, ex) + tail[:a] + js + tail[b:])
    print('creado', fn)
