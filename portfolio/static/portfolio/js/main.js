(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.add("js");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ---- Header gets a light shadow and shrinks once you scroll ---- */
  var header = document.getElementById("site-header");
  function onScroll() { header.classList.toggle("scrolled", window.scrollY > 30); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---- Page switching: one "view" visible at a time, driven by the URL hash ----
     #accueil (or no hash) = home; #methode, #solutions, #engagement, #formules, #tarifs open that page.
     #paie / #comparatif scroll to that part of its page. Back/forward and shared links work. */
  var views = $$(".view");
  var navLinks = $$("#sidebar-nav .nav-link");
  var navEl = document.getElementById("sidebar-nav");
  var main = document.getElementById("main");
  var current = null;

  function route() {
    var id = ""; try { id = decodeURIComponent(location.hash.slice(1)); } catch (e) {}
    var target = id ? document.getElementById(id) : null;
    if (id && target && !target.closest(".view")) return;            // e.g. the skip link (#main)
    var view = (target && target.closest(".view")) || views[0];       // unknown hash -> home
    var changed = view !== current;
    if (changed) {
      views.forEach(function (v) { v.classList.toggle("active", v === view); });
      current = view;
      var name = view.getAttribute("data-view");
      navLinks.forEach(function (l) {
        var on = l.getAttribute("data-view") === name;
        l.classList.toggle("active", on);
        if (on) l.setAttribute("aria-current", "page"); else l.removeAttribute("aria-current");
      });
      window.scrollTo({ top: 0, behavior: "instant" });
      if (main) main.focus({ preventScroll: true });
    }
    if (target && target !== view.querySelector("section")) {
      target.scrollIntoView({ behavior: reduceMotion || changed ? "instant" : "smooth", block: "start" });
    } else if (!changed) {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    }
  }
  window.addEventListener("hashchange", route);
  route();

  navLinks.forEach(function (l) {
    l.addEventListener("click", function () {
      var oc = window.bootstrap && bootstrap.Offcanvas.getInstance(navEl);
      if (oc && navEl.classList.contains("show")) oc.hide();
    });
  });
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href^="#"]');
    if (a && a.getAttribute("href") === location.hash) { ev.preventDefault(); route(); }
  });
})();
