/* CampusConnect — Main JavaScript */

// Auto-dismiss toasts
document.addEventListener('DOMContentLoaded', function () {
  const toastEls = document.querySelectorAll('.toast');
  toastEls.forEach(function (el) {
    setTimeout(function () {
      const bsToast = bootstrap.Toast.getOrCreateInstance(el);
      bsToast.hide();
    }, 5000);
  });

  // Deadline countdown labels
  document.querySelectorAll('[data-deadline]').forEach(function (el) {
    const dl = new Date(el.dataset.deadline);
    const now = new Date();
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

  // Animate section score bars on scroll (for resume result page)
  const fills = document.querySelectorAll('.section-score-fill');
  if (fills.length) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.width = entry.target.getAttribute('data-width') || entry.target.style.width;
        }
      });
    });
    fills.forEach(function (el) {
      el.setAttribute('data-width', el.style.width);
      el.style.width = '0';
      setTimeout(() => observer.observe(el), 100);
    });
  }

  // Skills input tag cloud (profile edit)
  const skillInput = document.querySelector('input[name="skills_input"]');
  if (skillInput) {
    skillInput.addEventListener('input', function () {
      const val = this.value;
      this.style.borderColor = val ? 'var(--cc-primary)' : '';
    });
  }
});
