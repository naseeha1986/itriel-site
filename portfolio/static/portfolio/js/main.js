(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.add("js");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ---- Header gets a light shadow and shrinks once you scroll ---- */
  var header = document.getElementById("site-header");
  var fab = document.querySelector(".fab"), foot = document.querySelector(".site-footer");
  function liftFab() {            // never cover the footer: rise above it when it scrolls into view
    if (!fab || !foot) return;
    var over = window.innerHeight - foot.getBoundingClientRect().top;
    fab.style.bottom = (over > 0 ? over + 16 : 18) + "px";
  }
  window.addEventListener("scroll", liftFab, { passive: true });
  window.addEventListener("resize", liftFab);
  liftFab();

  /* ---- Page switching: one "view" visible at a time, driven by the URL hash ----
     #accueil (or no hash) = home; #methode, #solutions, #engagement, #formules, #tarifs open that page.
     #paie / #comparatif scroll to that part of its page. Back/forward and shared links work. */
  var views = $$(".view");
  // "next page" button at the bottom of every page, built from the menu itself
  var menu = $$("#sidebar-nav .nav-link");
  views.forEach(function (v, i) {
    var nxt = menu[i + 1], wrap = document.createElement("div");
    wrap.className = "next-wrap";
    wrap.innerHTML = nxt
      ? '<a class="next-btn" href="#' + nxt.getAttribute("data-view") + '">' + nxt.textContent.trim() + ' <span aria-hidden="true">→</span></a>'
      : '<a class="next-btn" href="#' + menu[0].getAttribute("data-view") + '"><span aria-hidden="true">↑</span> ' + menu[0].textContent.trim() + '</a>';
    v.appendChild(wrap);
  });
  // gentle reveal-on-scroll for the main blocks
  var rv = $$(".hero-txt,.intro .rich,.band,.steps li,.svc,.disc,.eng-top,.why,.advs li,.plan,.cmp,.reco,.tar,.team,.team-box,.note");
  rv.forEach(function (el) { el.classList.add("rv"); });
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.08 });
    rv.forEach(function (el, i) { el.style.transitionDelay = (i % 3) * 80 + "ms"; io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add("in"); }); }
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
  window.addEventListener("hashchange", function () { route(); liftFab(); });
  route();
  liftFab();
  window.addEventListener("load", liftFab);
  if ("ResizeObserver" in window) new ResizeObserver(liftFab).observe(document.body);

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
