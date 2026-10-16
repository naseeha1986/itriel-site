(function ($) {
  "use strict";
  document.documentElement.classList.add("js");
  var root = document.documentElement;

  /* ---- Theme toggle (persisted + system preference) ---- */
  function setTheme(t, save) {
    root.setAttribute("data-theme", t); root.setAttribute("data-bs-theme", t);
    $("#theme-toggle").attr("aria-pressed", t === "dark");
    if (save) { try { localStorage.setItem("theme", t); } catch (e) {} }
  }
  setTheme(root.getAttribute("data-theme") || "light", false);
  $("#theme-toggle").on("click", function () {
    setTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark", true);
  });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function (e) {
    var saved = null; try { saved = localStorage.getItem("theme"); } catch (x) {}
    if (!saved) setTheme(e.matches ? "dark" : "light", false);
  });

  /* ---- Sticky glass header ---- */
  var $h = $("#site-header");
  $(window).on("scroll", function () { $h.toggleClass("scrolled", window.scrollY > 30); }).trigger("scroll");

  /* ---- Close offcanvas on link click ---- */
  $("#sidebar-nav .nav-link").on("click", function () {
    var el = document.getElementById("sidebar-nav"), oc = bootstrap.Offcanvas.getInstance(el);
    if (oc) oc.hide();
  });

  /* ---- Reveal on scroll ---- */
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    items.forEach(function (el, i) { el.style.transitionDelay = (i % 4) * 70 + "ms"; io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add("in"); }); }

  /* ---- Typed headline (text is in the HTML for no-JS / screen readers) ---- */
  var t = document.getElementById("typed");
  if (t && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var full = t.dataset.typed, i = 0;
    t.setAttribute("aria-label", full); t.textContent = ""; t.classList.add("typing");
    (function tick() {
      t.textContent = full.slice(0, ++i);
      if (i < full.length) setTimeout(tick, 70); else setTimeout(function () { t.classList.remove("typing"); }, 1800);
    })();
  }

  /* ---- Toast ---- */
  function toast(msg, err) {
    var el = document.getElementById("toast");
    el.classList.toggle("err", !!err); el.querySelector(".toast-body").textContent = msg;
    bootstrap.Toast.getOrCreateInstance(el, { delay: 4500 }).show();
  }

  /* ---- AJAX contact form ---- */
  $("#contact-form").on("submit", function (ev) {
    ev.preventDefault();
    var $f = $(this), $b = $f.find("button[type=submit]");
    $f.find(".form-control").removeClass("is-invalid");
    var data = {}; $f.serializeArray().forEach(function (x) { data[x.name] = x.value; });
    $b.prop("disabled", true).text("Envoi…");
    fetch("/contact/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": data.csrfmiddlewaretoken },
      body: JSON.stringify(data)
    }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (res.ok) { $f[0].reset(); toast("Message envoyé. Merci, nous revenons vers vous rapidement."); }
        else {
          $.each(res.j.errors || {}, function (k, m) { $f.find("[name=" + k + "]").addClass("is-invalid").next(".invalid-feedback").text(m); });
          toast("Veuillez corriger les champs signalés.", true);
        }
      })
      .catch(function () { toast("Erreur réseau. Réessayez.", true); })
      .finally(function () { $b.prop("disabled", false).text("Envoyer"); });
  });
})(jQuery);
