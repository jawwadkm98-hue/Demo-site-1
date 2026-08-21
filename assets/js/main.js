/* Beltway Demo — site behaviour.
   Plain ES2019, no dependencies. Every enhancement is optional: the site is
   fully readable and navigable with JavaScript disabled. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------- sticky header --- */
  var header = document.querySelector('.site-header');
  if (header) {
    var setStuck = function () {
      header.classList.toggle('is-stuck', window.scrollY > 24);
    };
    setStuck();
    window.addEventListener('scroll', setStuck, { passive: true });
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
      if (window.innerWidth > 1100) closeNav();
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
      if (reduceMotion) { el.textContent = target.toFixed(decimals); return; }
      var duration = 1400;
      var start = null;
      var step = function (now) {
        if (start === null) start = now;
        var p = Math.min((now - start) / duration, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = (target * eased).toFixed(decimals);
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
  /* No backend yet — the form validates locally and confirms. Wire the
     submit handler to a real endpoint when one exists. */
  var form = document.querySelector('[data-contact-form]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var status = form.querySelector('.form-status');
      if (status) {
        status.textContent =
          'Thanks — your enquiry has been captured. This demo form is not yet ' +
          'connected to a mail service, so nothing was sent.';
        status.classList.add('is-visible');
      }
      form.reset();
    });
  }

  /* ------------------------------------------------------ current year --- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
