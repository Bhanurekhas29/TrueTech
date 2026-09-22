document.addEventListener("DOMContentLoaded", () => {
    // Mobile nav toggle
    const navToggle = document.getElementById("nav-toggle");
    const siteNav = document.getElementById("site-nav");
    if (navToggle && siteNav) {
        navToggle.addEventListener("click", () => {
            const isOpen = siteNav.classList.toggle("is-open");
            navToggle.setAttribute("aria-expanded", isOpen);
        });
        siteNav.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => {
                siteNav.classList.remove("is-open");
                navToggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    // Alert box — dismiss button + auto-hide after a few seconds
    document.querySelectorAll(".site-message").forEach((msg) => {
        const hide = () => {
            msg.style.transition = "opacity 0.3s ease, transform 0.3s ease";
            msg.style.opacity = "0";
            msg.style.transform = "translateY(-12px)";
            setTimeout(() => msg.remove(), 300);
        };
        const closeBtn = msg.querySelector(".site-message__close");
        if (closeBtn) closeBtn.addEventListener("click", hide);
        setTimeout(hide, 6000);
    });

    // Contact form — block non-numeric characters in the phone field as you type
    const phoneField = document.getElementById("phone");
    if (phoneField) {
        phoneField.addEventListener("input", () => {
            phoneField.value = phoneField.value.replace(/[^0-9+\-\s()]/g, "");
        });
    }

    // Header shrinks slightly once the page scrolls
    const siteHeader = document.querySelector(".site-header");
    if (siteHeader) {
        const onScroll = () => {
            siteHeader.classList.toggle("is-scrolled", window.scrollY > 20);
        };
        window.addEventListener("scroll", onScroll, { passive: true });
        onScroll();
    }

    // What We Do — tabbed service directory (with a fade/slide transition on the panel)
    const wwdTabs = document.querySelectorAll(".wwd__tab");
    if (wwdTabs.length) {
        wwdTabs.forEach((tab) => {
            tab.addEventListener("click", () => {
                if (tab.classList.contains("is-active")) return;
                const targetId = tab.getAttribute("data-wwd-target");
                const nextPanel = document.getElementById(targetId);

                wwdTabs.forEach((t) => t.classList.remove("is-active"));
                tab.classList.add("is-active");

                document.querySelectorAll(".wwd__panel").forEach((p) => p.classList.remove("is-active"));
                nextPanel.classList.add("is-active", "is-entering");
                requestAnimationFrame(() => {
                    nextPanel.classList.remove("is-entering");
                });
            });
        });
    }

    // FAQ accordion
    document.querySelectorAll(".faq-item__question").forEach((btn) => {
        btn.addEventListener("click", () => {
            const item = btn.closest(".faq-item");
            const wasOpen = item.classList.contains("is-open");
            item.parentElement.querySelectorAll(".faq-item").forEach((el) => {
                el.classList.remove("is-open");
                el.querySelector(".faq-item__icon").textContent = "add";
            });
            if (!wasOpen) {
                item.classList.add("is-open");
                item.querySelector(".faq-item__icon").textContent = "remove";
            }
        });
    });

    // Our Process — sequential highlight: node lights up, then the line
    // to the next node fills, then that node lights up, and so on, looping.
    const journeyTimeline = document.querySelector(".journey__timeline");
    if (journeyTimeline) {
        const nodes = Array.from(journeyTimeline.querySelectorAll(".journey-node"));
        const holdTime = 1000;
        const fillTime = 600;

        function runJourneyCycle() {
            nodes.forEach((node) => {
                node.classList.remove("is-active");
                const fill = node.querySelector(".journey-node__connector-fill");
                if (fill) fill.style.width = "0%";
            });

            let i = 0;
            function step() {
                if (i >= nodes.length) {
                    setTimeout(runJourneyCycle, holdTime * 2);
                    return;
                }
                nodes[i].classList.add("is-active");
                const fill = nodes[i].querySelector(".journey-node__connector-fill");
                if (fill) {
                    setTimeout(() => {
                        fill.style.width = "100%";
                        setTimeout(() => {
                            i += 1;
                            step();
                        }, fillTime);
                    }, holdTime);
                } else {
                    setTimeout(() => {
                        i += 1;
                        step();
                    }, holdTime);
                }
            }
            step();
        }

        if ("IntersectionObserver" in window) {
            const journeyObserver = new IntersectionObserver(
                (entries) => {
                    entries.forEach((entry) => {
                        if (entry.isIntersecting) {
                            runJourneyCycle();
                            journeyObserver.unobserve(entry.target);
                        }
                    });
                },
                { threshold: 0.3 }
            );
            journeyObserver.observe(journeyTimeline);
        } else {
            runJourneyCycle();
        }
    }

    // Stagger groups — tag direct children with an incrementing delay index
    document.querySelectorAll(".stagger").forEach((group) => {
        Array.from(group.children).forEach((child, i) => {
            child.style.setProperty("--stagger-index", i);
        });
    });

    // Animated counters — reads the leading numeric part of a stat value,
    // counts up to it, and keeps any suffix (%, +, text) static.
    function animateCounter(el) {
        const raw = el.textContent.trim();
        const match = raw.match(/^(\d+(?:\.\d+)?)(.*)$/);
        if (!match) return; // non-numeric (e.g. "24/7") — leave as-is

        const target = parseFloat(match[1]);
        const suffix = match[2];
        const decimals = (match[1].split(".")[1] || "").length;
        const duration = 1200;
        const start = performance.now();

        function tick(now) {
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const value = (target * eased).toFixed(decimals);
            el.textContent = `${value}${suffix}`;
            if (progress < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
    }

    // Scroll-reveal (also triggers counters and stagger groups)
    const revealEls = document.querySelectorAll(".reveal, .stagger");
    const counterEls = document.querySelectorAll("[data-counter]");

    if ("IntersectionObserver" in window && (revealEls.length || counterEls.length)) {
        const revealObserver = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        revealObserver.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.15 }
        );
        revealEls.forEach((el) => revealObserver.observe(el));

        const counterObserver = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        counterObserver.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.4 }
        );
        counterEls.forEach((el) => counterObserver.observe(el));
    } else {
        revealEls.forEach((el) => el.classList.add("is-visible"));
    }
});
