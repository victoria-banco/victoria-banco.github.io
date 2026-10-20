/* victoriaswart.com — no cookies, no tracking, no third-party requests. */
(function () {
  'use strict';
  var ls = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* Language dropdown */
  var sw = document.querySelector('.lang-switch');
  if (sw) {
    var btn = sw.querySelector('.lang-current');
    var shut = function () { sw.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); };
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      btn.setAttribute('aria-expanded', String(sw.classList.toggle('open')));
    });
    document.addEventListener('click', function (e) { if (!sw.contains(e.target)) shut(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') shut(); });
  }

  /* Mobile menu */
  var toggle = document.querySelector('.menu-toggle');
  var panel  = document.getElementById('mobile-nav');
  if (toggle && panel) {
    var closeBtn = panel.querySelector('.mobile-close');
    var open = function (on) {
      panel.hidden = !on;
      toggle.setAttribute('aria-expanded', String(on));
      document.body.style.overflow = on ? 'hidden' : '';
      if (on && closeBtn) closeBtn.focus(); else toggle.focus();
    };
    toggle.addEventListener('click', function () { open(panel.hidden); });
    if (closeBtn) closeBtn.addEventListener('click', function () { open(false); });
    panel.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { open(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.hidden) open(false);
    });
  }

  /* Contact form: topic preset from ?topic=, ref capture, async submit */
  var form = document.getElementById('contactForm');
  if (form) {
    var params = new URLSearchParams(location.search);
    var topic  = (params.get('topic') || '').replace(/[^a-z]/gi, '').slice(0, 20);
    var sel    = form.querySelector('#f-topic');
    if (topic && sel && sel.querySelector('option[value="' + topic + '"]')) sel.value = topic;

    var ref = (params.get('ref') || '').replace(/[^a-z0-9-]/gi, '').slice(0, 40);
    var refField = form.querySelector('#refField');
    if (refField) refField.value = ref || ls.get('vs_ref') || '';
    if (ref) ls.set('vs_ref', ref);

    var status = document.getElementById('formStatus');
    var loaded = Date.now();
    form.addEventListener('submit', function (e) {
      if (Date.now() - loaded < 3000) { e.preventDefault(); return; }   // bot gate
      if (!window.fetch) return;                                        // plain POST fallback
      e.preventDefault();
      var btn = form.querySelector('button[type=submit]');
      if (btn) btn.disabled = true;
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('bad status');
          form.reset();
          status.textContent = status.dataset.ok;
          status.dataset.state = 'ok';
        })
        .catch(function () {
          status.textContent = status.dataset.err;
          status.dataset.state = 'err';
        })
        .then(function () { if (btn) btn.disabled = false; });
    });
  }

  /* Scroll reveal */
  (function () {
    var items = document.querySelectorAll('.reveal');
    if (!items.length) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    // If anything goes wrong, show everything rather than leave a blank page.
    var failsafe = setTimeout(function () {
      items.forEach(function (el) { el.classList.add('in'); });
    }, 2500);
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); clearTimeout(failsafe); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  })();

  /* Language suggestion: browser setting only, never an IP lookup */
  (function () {
    var ROUTES = window.__routes;
    var NATIVE = { de: 'Deutsch', it: 'Italiano', es: 'Español', en: 'English' };
    var COPY = {
      de: { p: 'Diese Seite gibt es auch auf Deutsch.', y: 'Auf Deutsch ansehen' },
      it: { p: 'Questa pagina è disponibile anche in italiano.', y: 'Vedi in italiano' },
      es: { p: 'Esta página también está disponible en español.', y: 'Ver en español' },
      en: { p: 'This page is also available in English.', y: 'View in English' }
    };
    if (!ROUTES) return;
    var here  = document.body.dataset.lang;
    var route = document.body.dataset.route;
    if (ls.get('vs_lang_choice')) return;

    var prefs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
    var target = null;
    for (var i = 0; i < prefs.length; i++) {
      var base = String(prefs[i]).toLowerCase().split('-')[0];
      if (base === here) return;
      if (COPY[base] && ROUTES[route] && ROUTES[route][base]) { target = base; break; }
    }
    if (!target) return;

    var bar = document.createElement('div');
    bar.className = 'lang-offer';
    bar.setAttribute('role', 'dialog');
    bar.lang = target;
    var p = document.createElement('p'); p.textContent = COPY[target].p;
    var a = document.createElement('a'); a.textContent = COPY[target].y; a.href = ROUTES[route][target];
    var b = document.createElement('button'); b.type = 'button'; b.textContent = 'Stay in ' + NATIVE[here]; b.lang = here;
    a.addEventListener('click', function () { ls.set('vs_lang_choice', target); });
    b.addEventListener('click', function () { ls.set('vs_lang_choice', here); bar.classList.remove('show'); });
    bar.appendChild(p); bar.appendChild(a); bar.appendChild(b);
    document.body.appendChild(bar);
    setTimeout(function () { bar.classList.add('show'); }, 1000);
  })();
})();
