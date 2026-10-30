/* Progreso del alumno en jivops.com
   - En el índice: barra "12/30" en cada curso, ✓ en las lecciones hechas y enlace al certificado.
   - En cuenta.html: lista de cursos empezados dentro de <div id="jv-progreso"></div>. */
(function () {
  var API = "https://api.jivops.com";
  var token = localStorage.getItem("jivops_token");
  if (!token) return;

  var css = document.createElement("style");
  css.textContent =
    ".jv-p { display:flex; align-items:center; gap:8px; margin-left:auto; margin-right:12px; font-size:12px; color:#7c8aab; white-space:nowrap; }" +
    ".jv-p .jv-b { width:70px; height:6px; background:#0b1120; border:1px solid #23304a; border-radius:3px; overflow:hidden; }" +
    ".jv-p .jv-b i { display:block; height:100%; background:#4ade80; }" +
    ".jv-p.jv-ok { color:#4ade80; }" +
    "a.jv-hecha::after { content:' \\2713'; color:#4ade80; font-weight:700; }" +
    "a.jv-certlink { color:#e6b34d !important; font-weight:600; }" +
    "#jv-progreso .jv-fila { padding:14px 0; border-bottom:1px solid #23304a; }" +
    "#jv-progreso .jv-fila:last-child { border-bottom:0; }" +
    "#jv-progreso .jv-cab { display:flex; justify-content:space-between; gap:12px; font-size:15px; margin-bottom:8px; }" +
    "#jv-progreso .jv-cab span { color:#7c8aab; white-space:nowrap; }" +
    "#jv-progreso .jv-b2 { height:8px; background:#0b1120; border:1px solid #23304a; border-radius:4px; overflow:hidden; }" +
    "#jv-progreso .jv-b2 i { display:block; height:100%; background:#4ade80; }" +
    "#jv-progreso a { display:inline-block; margin-top:8px; color:#e6b34d; font-size:14px; }" +
    "#jv-progreso .jv-vacio { color:#7c8aab; }";
  document.head.appendChild(css);

  function slugDe(href) {
    var m = (href || "").match(/cursos\.jivops\.com\/([a-z0-9-]+)-leccion-(\d+)\.html/);
    return m ? { slug: m[1], n: parseInt(m[2], 10) } : null;
  }
  function urlCert(c) {
    return c.certificate ? "certificado.html?id=" + encodeURIComponent(c.certificate)
                         : "certificado.html?curso=" + encodeURIComponent(c.slug);
  }

  fetch(API + "/progreso", { headers: { "Authorization": "Bearer " + token } })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (p) {
      if (!p) return;
      var cursos = {};
      p.courses.forEach(function (c) { cursos[c.slug] = c; });

      // Índice: cada bloque .adv-course
      document.querySelectorAll(".adv-course").forEach(function (bloque) {
        var links = bloque.querySelectorAll(".adv-lessons a");
        var slug = null;
        links.forEach(function (a) {
          var s = slugDe(a.getAttribute("href"));
          if (!s) return;
          slug = s.slug;
          var c = cursos[s.slug];
          if (c && c.lessons.indexOf(s.n) >= 0) a.classList.add("jv-hecha");
        });
        var c = slug && cursos[slug];
        var tit = bloque.querySelector(".adv-course-title");
        if (!c || !tit || c.done === 0) return;
        var pct = Math.round(c.done * 100 / c.total);
        var info = document.createElement("span");
        info.className = "jv-p" + (c.done >= c.total ? " jv-ok" : "");
        var barra = document.createElement("span");
        barra.className = "jv-b";
        var relleno = document.createElement("i");
        relleno.style.width = pct + "%";
        barra.appendChild(relleno);
        info.appendChild(barra);
        info.appendChild(document.createTextNode(c.done + "/" + c.total));
        var flecha = tit.querySelector(".arrow");
        tit.insertBefore(info, flecha || null);
        if (c.done >= c.total) {
          var lista = bloque.querySelector(".adv-lessons");
          var a = document.createElement("a");
          a.className = "jv-certlink";
          a.href = urlCert(c);
          a.textContent = c.certificate ? "🎓 Ver mi certificado" : "🎓 Obtener certificado";
          if (lista) lista.insertBefore(a, lista.firstChild);
        }
      });

      // Cuenta: lista de cursos empezados
      var caja = document.getElementById("jv-progreso");
      if (caja) {
        caja.innerHTML = "";
        var empezados = p.courses.filter(function (c) { return c.done > 0; })
          .sort(function (a, b) { return (b.done / b.total) - (a.done / a.total); });
        if (!empezados.length) {
          var v = document.createElement("p");
          v.className = "jv-vacio";
          v.textContent = "Todavía no has completado ninguna lección.";
          caja.appendChild(v);
        }
        empezados.forEach(function (c) {
          var fila = document.createElement("div");
          fila.className = "jv-fila";
          var cab = document.createElement("div");
          cab.className = "jv-cab";
          var t = document.createElement("strong");
          t.textContent = c.title;
          var n = document.createElement("span");
          n.textContent = c.done + "/" + c.total + " lecciones";
          cab.appendChild(t); cab.appendChild(n);
          var b = document.createElement("div");
          b.className = "jv-b2";
          var i = document.createElement("i");
          i.style.width = Math.round(c.done * 100 / c.total) + "%";
          b.appendChild(i);
          fila.appendChild(cab); fila.appendChild(b);
          if (c.done >= c.total) {
            var a = document.createElement("a");
            a.href = urlCert(c);
            a.textContent = c.certificate ? "🎓 Ver mi certificado" : "🎓 Obtener certificado";
            fila.appendChild(a);
          }
          caja.appendChild(fila);
        });
      }
    })
    .catch(function () {});
})();
