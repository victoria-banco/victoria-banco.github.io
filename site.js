// Scroll progress
  const progressBar = document.querySelector('.scroll-progress');
  function updateProgress() {
    const scrolled = window.scrollY;
    const total = document.documentElement.scrollHeight - window.innerHeight;
    if (total > 0) progressBar.style.width = (scrolled / total * 100) + '%';
  }
  window.addEventListener('scroll', updateProgress, { passive: true });

  // Nav: dark at the top, hides on scroll down, returns cream on scroll up
  const navEl = document.querySelector('nav');
  let lastY = window.scrollY;
  let navTicking = false;

  function updateNav() {
    const y = Math.max(0, window.scrollY);
    const atTop = y < 40;
    const menuOpen = document.querySelector('.nav-overlay')?.classList.contains('open');

    navEl.classList.toggle('at-top', atTop);
    navEl.classList.toggle('scrolled', y > 60);

    if (menuOpen || atTop) {
      navEl.classList.remove('nav-hidden');
    } else if (y > lastY + 6 && y > 120) {
      navEl.classList.add('nav-hidden');      // scrolling down
    } else if (y < lastY - 6) {
      navEl.classList.remove('nav-hidden');   // scrolling up
    }

    lastY = y;
    navTicking = false;
  }

  window.addEventListener('scroll', () => {
    if (!navTicking) { navTicking = true; requestAnimationFrame(updateNav); }
  }, { passive: true });
  updateNav();

  // Mobile menu
  const hamburger = document.querySelector('.hamburger');
  const overlay   = document.querySelector('.nav-overlay');

  function openMenu()  { hamburger.classList.add('open'); overlay.classList.add('open'); document.body.style.overflow = 'hidden'; }
  function closeMenu() { hamburger.classList.remove('open'); overlay.classList.remove('open'); document.body.style.overflow = ''; }

  hamburger.addEventListener('click', () => hamburger.classList.contains('open') ? closeMenu() : openMenu());
  overlay.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));

  // Scroll reveal
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.07, rootMargin: '0px 0px -32px 0px' });
  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  // Custom cursor (desktop only)
  const ring = document.querySelector('.cursor-ring');
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches && ring) {
    let mx = 0, my = 0, rx = 0, ry = 0;
    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; ring.classList.add('active'); });
    document.addEventListener('mouseleave', () => ring.classList.remove('active'));
    document.querySelectorAll('a, button, .case-study, .service-item, .consult-card').forEach(el => {
      el.addEventListener('mouseenter', () => ring.classList.add('hovering'));
      el.addEventListener('mouseleave', () => ring.classList.remove('hovering'));
    });
    (function animate() {
      rx += (mx - rx) * 0.11; ry += (my - ry) * 0.11;
      ring.style.left = rx + 'px'; ring.style.top = ry + 'px';
      requestAnimationFrame(animate);
    })();
  }

  // Footer year
  document.getElementById('footerYear').textContent = new Date().getFullYear();
  document.querySelectorAll('.cs-year').forEach(el => el.textContent = new Date().getFullYear());

  // Spam protection: honeypot (in markup) + time gate + content checks + double-submit guard
  const formLoadTime = Date.now();
  let formSubmitted = false;
  document.getElementById('formTimestamp').value = formLoadTime;
  document.getElementById('contactForm').addEventListener('submit', function(e) {
    // Block bots that submit instantly (under 4 seconds)
    if (Date.now() - formLoadTime < 4000) { e.preventDefault(); return false; }

    // Block double submissions
    if (formSubmitted) { e.preventDefault(); return false; }

    const msg = document.getElementById('message').value.trim();
    const name = document.getElementById('name').value.trim();

    // Require a real message (min 25 chars) and a real name (min 2 chars)
    if (msg.length < 25) {
      e.preventDefault();
      alert('Please tell me a little more about your project (a few sentences helps me respond properly).');
      return false;
    }
    if (name.length < 2) { e.preventDefault(); return false; }

    // Block messages that are mostly links or contain classic spam patterns
    const linkCount = (msg.match(/https?:\/\/|www\./gi) || []).length;
    const spamPatterns = /\b(seo ranking|guest post|backlinks?|link building|web traffic|increase sales guaranteed|crypto investment|earn \$|make money fast|viagra|casino)\b/i;
    if (linkCount > 2 || spamPatterns.test(msg)) {
      e.preventDefault();
      alert('Your message could not be sent. Please remove promotional links and try again.');
      return false;
    }

    formSubmitted = true;
  });

  // Cookie consent
  function acceptCookies() {
    localStorage.setItem('vs_cookie_consent', '1');
    document.getElementById('cookieBanner').classList.add('hidden');
  }
  function openPrivacy(e) { e.preventDefault(); document.getElementById('privacyOverlay').classList.add('open'); document.body.style.overflow = 'hidden'; }
  function closePrivacy() { document.getElementById('privacyOverlay').classList.remove('open'); document.body.style.overflow = ''; }
  document.getElementById('privacyOverlay').addEventListener('click', function(e) { if (e.target === this) closePrivacy(); });
  if (localStorage.getItem('vs_cookie_consent')) document.getElementById('cookieBanner').classList.add('hidden');

  // Smooth anchor scroll
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const target = document.querySelector(link.getAttribute('href'));
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  });

// Showcase video: only fetch and play once it is actually on screen
(function () {
  const v = document.getElementById('showcaseVideo');
  if (!v) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        if (v.preload !== 'auto') { v.preload = 'auto'; v.load(); }
        v.play().catch(() => {});
      } else { v.pause(); }
    });
  }, { rootMargin: '200px 0px', threshold: 0.15 });
  io.observe(v);
})();
