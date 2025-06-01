window.addEventListener("DOMContentLoaded", e => {
    function o() {
        var e = document.body.querySelector("#mainNav");
        e && (0 === window.scrollY ? e.classList.remove("navbar-shrink") : e.classList.add("navbar-shrink"))
    }

    o(), document.addEventListener("scroll", o);
    var n = document.body.querySelector("#mainNav");
    n && new bootstrap.ScrollSpy(document.body, {target: "#mainNav", offset: 74});
    const t = document.body.querySelector(".navbar-toggler");
    [].slice.call(document.querySelectorAll("#navbarResponsive .nav-link")).map(function (e) {
        e.addEventListener("click", () => {
            "none" !== window.getComputedStyle(t).display && t.click()
        })
    }), new SimpleLightbox({elements: "#portfolio a.portfolio-box"})
});