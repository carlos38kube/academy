import json

SRC = 'docker-leccion-compose.html'
src = open(SRC, encoding='utf-8').read()

head = src[:src.index('<main>') + len('<main>')]
tail = src[src.index('<div class="bottombar">'):]
a = tail.index('  const mc0 =')
b = tail.index('  actionBtn.addEventListener')

GENERIC_JS = """  const EX = __EX__;
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

LESSONS = {
  'contenedores': {
    'num': 1, 'title': 'Qué es un contenedor',
    'done': 'Ya sabes qué es un contenedor y en qué se diferencia de una imagen y de una VM.',
    'ex': [
      {'t': 'mc', 'q': '¿Cuál es la diferencia entre una imagen y un contenedor?',
       'opts': ['Son lo mismo', 'La imagen es la plantilla y el contenedor es una instancia en ejecución', 'El contenedor es la plantilla y la imagen es la instancia', 'La imagen solo existe en Docker Hub'],
       'c': 1, 'ok': 'La imagen es la plantilla; el contenedor es una instancia en ejecución.'},
      {'t': 'fill', 'q': 'Completa el comando para listar los contenedores en ejecución.',
       'code': 'docker ___', 'a': ['ps', 'container ls', 'container ps'],
       'ok': 'El comando es docker ps.'},
      {'t': 'mc', 'q': '¿Qué diferencia a un contenedor de una máquina virtual?',
       'opts': ['Incluye un sistema operativo completo', 'Comparte el kernel del host y es más ligero', 'Necesita un hipervisor', 'Solo funciona en Windows'],
       'c': 1, 'ok': 'Un contenedor comparte el kernel del host, por eso es más ligero que una VM.'},
      {'t': 'write', 'q': 'Escribe el comando para ejecutar un contenedor de nginx en segundo plano.',
       'k': ['docker', 'run', '-d', 'nginx'],
       'ok': 'docker run -d nginx ejecuta el contenedor en segundo plano.'},
    ],
  },
}

def body(L, n):
    out = ['\n  <div class="lesson-label">Docker desde cero · Lección %d</div>\n' % L['num']]
    for i, e in enumerate(L['ex']):
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

''' % L['done'])
    return '\n'.join(out)

for name, L in LESSONS.items():
    h = head.replace('Lección: Docker Compose', 'Lección: ' + L['title'])
    ex = [{k: v for k, v in e.items() if k in ('t', 'a', 'k', 'ok')} for e in L['ex']]
    js = GENERIC_JS.replace('__EX__', json.dumps(ex, ensure_ascii=False))
    html = h + body(L, name) + tail[:a] + js + tail[b:]
    fn = 'docker-leccion-%s.html' % name
    open(fn, 'w', encoding='utf-8').write(html)
    print('creado', fn)
