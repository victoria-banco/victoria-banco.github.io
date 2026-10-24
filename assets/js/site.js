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
    // If the observer never reports at all, show everything rather than leave
    // a blank page. Clearing this on the first intersection, as it used to,
    // removed the guard for every section further down the page.
    var observed = false;
    setTimeout(function () {
      if (observed) return;
      items.forEach(function (el) { el.classList.add('in'); });
    }, 2500);
    var io = new IntersectionObserver(function (entries) {
      observed = true;
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
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

  /* Hero media: a silent looping video that fades in over its poster.
     The poster is the LCP element and is already on screen; nothing here
     runs until the page has finished loading, so the video never competes
     with it, the fonts or the CSS for bandwidth. Every failure path ends
     the same way: the poster stays and the hero is a photograph. */
  (function () {
    var boxes = document.querySelectorAll('[data-hero-media]');
    if (!boxes.length) return;

    /* Asked for less motion, or for less data: do not fetch the video at all. */
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var conn = navigator.connection;
    if (reduce || (conn && conn.saveData)) return;

    /* The cut is chosen by the shape of the box, not by the device: the same
       page can show the 4:5 panel on a tablet held upright and the 16:9 cut
       the moment it is turned on its side.

       These two boundaries are also written as media queries in
       hero-media.njk (which poster) and base.njk (which poster to preload).
       The hero fills the viewport, so all three read the same ratio and agree
       by construction — but they only stay in step if they are changed
       together. */
    function cutFor(ratio) {
      if (ratio < 0.68) return 'mobile';
      if (ratio <= 1.20) return 'panel';
      return 'desktop';
    }

    function setUp(box) {
      var video = box.querySelector('.hero-media__video');
      if (!video || !video.canPlayType) return;
      var base = box.getAttribute('data-base') || '/assets/video/hero';
      var name = box.getAttribute('data-name') || 'hero';
      var current = null;
      var dead = false;

      function play() {
        if (dead) return;
        var p = video.play();
        /* Rejected on iOS Low Power Mode and wherever autoplay is refused.
           Not an error worth surfacing: the poster is the fallback. */
        if (p && p.catch) p.catch(function () {});
      }

      function choose() {
        if (dead) return;
        var r = video.getBoundingClientRect();
        if (!r.width || !r.height) return;
        var want = cutFor(r.width / r.height);
        if (want === current) return;
        current = want;
        box.classList.remove('is-playing');
        while (video.firstChild) video.removeChild(video.firstChild);
        /* WebM first because it is roughly a third smaller; MP4 for Safari. */
        var types = [['webm', 'video/webm'], ['mp4', 'video/mp4']];
        for (var i = 0; i < types.length; i++) {
          var s = document.createElement('source');
          s.src = base + '/' + name + '-' + want + '.' + types[i][0];
          s.type = types[i][1];
          video.appendChild(s);
        }
        video.load();
        play();
      }

      video.addEventListener('playing', function () { box.classList.add('is-playing'); });
      /* Capture: a failing <source> fires error on the child, not the video. */
      video.addEventListener('error', function () {
        dead = true;
        box.classList.remove('is-playing');
      }, true);

      /* Off screen or tab in the background: stop decoding frames. */
      if (window.IntersectionObserver) {
        new IntersectionObserver(function (entries) {
          if (entries[0].isIntersecting) play(); else video.pause();
        }).observe(box);
      }
      document.addEventListener('visibilitychange', function () {
        if (document.hidden) video.pause(); else play();
      });

      /* Only a change of category reloads anything; plain resizes do not. */
      var t;
      function recheck() { clearTimeout(t); t = setTimeout(choose, 250); }
      window.addEventListener('resize', recheck);
      window.addEventListener('orientationchange', recheck);

      choose();
    }

    function start() {
      for (var i = 0; i < boxes.length; i++) setUp(boxes[i]);
    }

    /* After load, and idle if the browser will tell us when that is. */
    function afterLoad() {
      if (window.requestIdleCallback) requestIdleCallback(start, { timeout: 2000 });
      else setTimeout(start, 200);
    }
    if (document.readyState === 'complete') afterLoad();
    else window.addEventListener('load', afterLoad);
  })();
})();
