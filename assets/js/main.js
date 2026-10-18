/* Beltway Demolition — site behaviour.
   Plain ES2019, no dependencies. Every enhancement is optional: the site is
   fully readable and navigable with JavaScript disabled. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------- sticky header --- */
  var header = document.querySelector('.site-header');
  if (header) {
    var publishHeight = function () {
      document.documentElement.style.setProperty(
        '--masthead-h', header.offsetHeight + 'px');
    };
    var setStuck = function () {
      header.classList.toggle('is-stuck', window.scrollY > 24);
      publishHeight();
    };
    setStuck();
    window.addEventListener('scroll', setStuck, { passive: true });
    window.addEventListener('resize', publishHeight);
  }

  /* ------------------------------------------------------- mobile nav --- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    var closeNav = function () {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    };
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeNav();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeNav();
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1000) closeNav();
    });
  }


  /* ------------------------------------------------ reveal on scroll --- */
  var revealables = document.querySelectorAll('[data-reveal]');
  if (revealables.length) {
    if (reduceMotion || !('IntersectionObserver' in window)) {
      revealables.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      var revealer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var delay = parseInt(entry.target.getAttribute('data-reveal'), 10) || 0;
          setTimeout(function () { entry.target.classList.add('is-in'); }, delay);
          revealer.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -10% 0px', threshold: 0 });
      revealables.forEach(function (el) { revealer.observe(el); });
    }
  }

  /* --------------------------------------------------- counting stats --- */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    var runCount = function (el) {
      var target = parseFloat(el.getAttribute('data-count'));
      var decimals = (el.getAttribute('data-count').split('.')[1] || '').length;
      var fmt = function (v) {
        return v.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      };
      if (reduceMotion) { el.textContent = fmt(target); return; }
      var duration = 1400;
      var start = null;
      var step = function (now) {
        if (start === null) start = now;
        var p = Math.min((now - start) / duration, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = fmt(target * eased);
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };

    if (!('IntersectionObserver' in window)) {
      counters.forEach(runCount);
    } else {
      var counterObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          runCount(entry.target);
          counterObs.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -15% 0px', threshold: 0 });
      counters.forEach(function (el) { counterObs.observe(el); });
    }
  }

  /* ------------------------------------------------------ contact form --- */
  /* Posts to the Formspree endpoint in the form's action attribute
     (set FORM_ENDPOINT in _build/config.py and rebuild). Without JS the form
     still submits normally. While the endpoint is unset, visitors are told
     to call or email instead, so no lead is silently lost. */
  var form = document.querySelector('[data-contact-form]');
  if (form) {
    var status = form.querySelector('.form-status');
    var say = function (msg) {
      if (!status) return;
      status.textContent = msg;
      status.classList.add('is-visible');
    };
    var fallback = 'please call ' + (form.getAttribute('data-phone') || '') +
                   ' or email ' + (form.getAttribute('data-email') || '') + '.';
    form.addEventListener('submit', function (e) {
      var action = form.getAttribute('action') || '';
      if (!form.reportValidity()) { e.preventDefault(); return; }
      if (!/^https?:\/\//.test(action)) {
        e.preventDefault();
        say('Online requests are not switched on yet \u2014 ' + fallback);
        return;
      }
      if (!window.fetch || !window.FormData) return; /* plain POST */
      e.preventDefault();
      var btn = form.querySelector('[type="submit"]');
      if (btn) btn.disabled = true;
      say('Sending\u2026');
      fetch(action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          form.reset();
          say('Thanks \u2014 your request has been sent. We will be in touch shortly.');
        })
        .catch(function () {
          say('Sorry, that did not go through \u2014 ' + fallback);
        })
        .then(function () { if (btn) btn.disabled = false; });
    });
  }

  /* ------------------------------------------------------ current year --- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
