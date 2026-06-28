/* CampusConnect — Main JavaScript */

document.addEventListener('DOMContentLoaded', function () {

  /* =====================================================
     1. AUTO-DISMISS TOASTS
     ===================================================== */
  const toastEls = document.querySelectorAll('.toast');
  toastEls.forEach(function (el) {
    setTimeout(function () {
      const bsToast = bootstrap.Toast.getOrCreateInstance(el);
      bsToast.hide();
    }, 5000);
  });

  /* =====================================================
     2. DEADLINE COUNTDOWN LABELS
     ===================================================== */
  document.querySelectorAll('[data-deadline]').forEach(function (el) {
    const dl   = new Date(el.dataset.deadline);
    const now  = new Date();
    const diff = Math.ceil((dl - now) / (1000 * 60 * 60 * 24));
    if (diff < 0) {
      el.style.color = '#ef4444';
      el.title = 'Deadline passed';
    } else if (diff === 0) {
      el.style.color = '#ef4444';
      el.textContent = 'Today!';
    } else if (diff <= 3) {
      el.style.color = '#f97316';
      el.textContent += ` (${diff}d left)`;
    } else if (diff <= 7) {
      el.style.color = '#f59e0b';
      el.textContent += ` (${diff}d left)`;
    }
  });

  /* =====================================================
     3. RESUME SECTION SCORE BARS (animate on scroll)
     ===================================================== */
  const fills = document.querySelectorAll('.section-score-fill');
  if (fills.length) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.width =
            entry.target.getAttribute('data-width') || entry.target.style.width;
        }
      });
    });
    fills.forEach(function (el) {
      el.setAttribute('data-width', el.style.width);
      el.style.width = '0';
      setTimeout(() => observer.observe(el), 100);
    });
  }

  /* =====================================================
     4. SKILLS INPUT (profile edit)
     ===================================================== */
  const skillInput = document.querySelector('input[name="skills_input"]');
  if (skillInput) {
    skillInput.addEventListener('input', function () {
      this.style.borderColor = this.value ? 'var(--cc-primary)' : '';
    });
  }

  /* =====================================================
     5. SCROLL-TRIGGER ENGINE
        Watches [data-scroll] and [data-scroll-group]
        elements and adds .is-visible when they enter
        the viewport.
     ===================================================== */
  const scrollObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          // Fire counter animation if element has counters
          entry.target.querySelectorAll('[data-count]').forEach(animateCounter);
          scrollObserver.unobserve(entry.target); // animate once
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll('[data-scroll], [data-scroll-group]').forEach(function (el) {
    scrollObserver.observe(el);
  });

  /* =====================================================
     6. ANIMATED NUMBER COUNTER
     ===================================================== */
  function animateCounter(el) {
    const target   = parseFloat(el.dataset.count);
    const suffix   = el.dataset.suffix || '';
    const duration = 1800;
    const start    = performance.now();

    function update(now) {
      const elapsed  = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // Ease-out cubic
      const eased    = 1 - Math.pow(1 - progress, 3);
      const value    = Math.round(eased * target);
      el.textContent = value + suffix;
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  }

  // Also fire immediately for any counters already visible
  document.querySelectorAll('[data-count]').forEach(function (el) {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight) animateCounter(el);
  });

  /* =====================================================
     7. TYPEWRITER EFFECT (hero headline)
     ===================================================== */
  const typeEl = document.getElementById('typewriter-text');
  if (typeEl) {
    const words   = typeEl.dataset.words ? typeEl.dataset.words.split('|') : [];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function type() {
      const current = words[wordIndex] || '';
      if (isDeleting) {
        typeEl.textContent = current.slice(0, charIndex--);
      } else {
        typeEl.textContent = current.slice(0, charIndex++);
      }

      let delay = isDeleting ? 60 : 110;

      if (!isDeleting && charIndex > current.length) {
        delay = 1600;
        isDeleting = true;
      } else if (isDeleting && charIndex < 0) {
        isDeleting = false;
        wordIndex  = (wordIndex + 1) % words.length;
        charIndex  = 0;
        delay      = 400;
      }
      setTimeout(type, delay);
    }

    setTimeout(type, 800);
  }

  /* =====================================================
     8. HERO PARTICLE CANVAS
     ===================================================== */
  const canvas = document.getElementById('hero-particles');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let W, H, particles = [];

    function resize() {
      W = canvas.width  = canvas.offsetWidth;
      H = canvas.height = canvas.offsetHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    const PARTICLE_COUNT = 38;
    const COLOR = 'rgba(141,85,36,';

    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x:  Math.random() * (W || 1200),
        y:  Math.random() * (H || 700),
        r:  Math.random() * 2.2 + 0.5,
        vx: (Math.random() - 0.5) * 0.35,
        vy: (Math.random() - 0.5) * 0.35,
        a:  Math.random() * 0.5 + 0.15,
      });
    }

    function drawParticles() {
      ctx.clearRect(0, 0, W, H);
      particles.forEach(function (p) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = COLOR + p.a + ')';
        ctx.fill();

        // Connect nearby particles
        particles.forEach(function (q) {
          const dx = p.x - q.x, dy = p.y - q.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 110) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(q.x, q.y);
            ctx.strokeStyle = COLOR + (0.06 * (1 - dist / 110)) + ')';
            ctx.lineWidth = 0.7;
            ctx.stroke();
          }
        });

        // Move
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > W) p.vx *= -1;
        if (p.y < 0 || p.y > H) p.vy *= -1;
      });
      requestAnimationFrame(drawParticles);
    }
    drawParticles();
  }

  /* =====================================================
     9. NAVBAR — shrink on scroll
     ===================================================== */
  const navbar = document.querySelector('.cc-navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 60) {
        navbar.style.padding    = '0.4rem 0';
        navbar.style.boxShadow  = '0 4px 24px rgba(141,85,36,0.10)';
      } else {
        navbar.style.padding    = '';
        navbar.style.boxShadow  = '';
      }
    }, { passive: true });
  }

  /* =====================================================
     10. SMOOTH REVEAL for hero content on page load
     ===================================================== */
  const heroContent = document.querySelector('.hero-reveal');
  if (heroContent) {
    setTimeout(function () {
      heroContent.style.opacity   = '1';
      heroContent.style.transform = 'translateY(0)';
    }, 80);
  }

});
