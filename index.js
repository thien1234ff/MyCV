/* ==========================================================================
   PRESENTATION SLIDE NAVIGATION SYSTEM
   ========================================================================== */

const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;
let currentSlideIndex = 0;
let isTransitioning = false;
const transitionCooldown = 800; // Cooldown in ms between slide changes

// DOM Elements
const prevBtn = document.getElementById('prev-slide');
const nextBtn = document.getElementById('next-slide');
const currentSlideNum = document.getElementById('current-slide-num');
const totalSlidesNum = document.getElementById('total-slides-num');
const currentSlideTitle = document.getElementById('current-slide-title');
const progressBar = document.getElementById('progression-bar');
const dotsNav = document.getElementById('pagination-dots-nav');
const menuToggle = document.getElementById('menu-toggle');
const slideMap = document.getElementById('slide-map');
const slideMapLinks = document.getElementById('slide-map-links');

// Setup indicators
if (totalSlidesNum) totalSlidesNum.textContent = totalSlides;

// Slide Titles Map
const slideTitles = [
  "Overview",
  "Dashboard Summary",
  "About Me",
  "Education & Honors",
  "Academic Achievements",
  "Leadership & Activities",
  "Projects Portfolio",
  "Research Publications",
  "Technical Skills",
  "Contact"
];

// Initialize Slides
function initSlides() {
  // Generate Dots
  if (dotsNav) {
    dotsNav.innerHTML = '';
    slides.forEach((slide, idx) => {
      const dot = document.createElement('div');
      dot.className = `dot-item ${idx === 0 ? 'active' : ''}`;
      dot.setAttribute('data-index', idx);
      
      const label = document.createElement('span');
      label.className = 'dot-label';
      label.textContent = slideTitles[idx] || `Slide ${idx + 1}`;
      dot.appendChild(label);
      
      dot.addEventListener('click', () => goToSlide(idx));
      dotsNav.appendChild(dot);
    });
  }

  // Generate Menu Map Links
  if (slideMapLinks) {
    slideMapLinks.innerHTML = '';
    slides.forEach((slide, idx) => {
      const li = document.createElement('li');
      li.className = `slide-map-item ${idx === 0 ? 'active' : ''}`;
      li.setAttribute('data-map-index', idx);
      
      const button = document.createElement('button');
      button.textContent = `${idx + 1}. ${slideTitles[idx] || `Slide ${idx + 1}`}`;
      button.addEventListener('click', () => {
        goToSlide(idx);
        toggleMenu(false);
      });
      
      li.appendChild(button);
      slideMapLinks.appendChild(li);
    });
  }

  updateControls();
}

// Go to specific slide index
function goToSlide(index) {
  if (index < 0 || index >= totalSlides || index === currentSlideIndex) return;
  
  // Verify screen width
  const isMobile = window.innerWidth <= 768;

  if (isMobile) {
    // Standard vertical scroll flow on mobile
    currentSlideIndex = index;
    slides[index].scrollIntoView({ behavior: 'smooth' });
    updateActiveStates(index);
    updateControls();
  } else {
    // Presentation slide transitions on desktop
    isTransitioning = true;
    
    // Remove active classes
    slides.forEach(slide => {
      slide.classList.remove('active-slide');
    });

    currentSlideIndex = index;
    const targetSlide = slides[index];
    
    // Trigger active slide class
    targetSlide.classList.add('active-slide');

    updateActiveStates(index);
    updateControls();

    // Trigger stats counter if on Slide 2
    if (index === 1) {
      setTimeout(animateStats, 300);
    }

    setTimeout(() => {
      isTransitioning = false;
    }, transitionCooldown);
  }
}

// Update Active Dot and Menu links states
function updateActiveStates(activeIndex) {
  // Update dots
  const dots = document.querySelectorAll('.dot-item');
  dots.forEach((dot, idx) => {
    if (idx === activeIndex) {
      dot.classList.add('active');
    } else {
      dot.classList.remove('active');
    }
  });

  // Update map list
  const mapItems = document.querySelectorAll('.slide-map-item');
  mapItems.forEach((item, idx) => {
    if (idx === activeIndex) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });
}

// Update Control Buttons, progress fills, and titles
function updateControls() {
  if (currentSlideNum) currentSlideNum.textContent = currentSlideIndex + 1;
  if (currentSlideTitle) currentSlideTitle.textContent = slideTitles[currentSlideIndex] || "Overview";
  
  // Calculate progress
  const progressPercent = ((currentSlideIndex + 1) / totalSlides) * 100;
  if (progressBar) progressBar.style.width = `${progressPercent}%`;

  // Disable/enable arrows
  if (prevBtn) prevBtn.disabled = currentSlideIndex === 0;
  if (nextBtn) nextBtn.disabled = currentSlideIndex === totalSlides - 1;
}

// Keyboard controls handler
document.addEventListener('keydown', (e) => {
  if (isTransitioning || (window.innerWidth <= 768)) return;
  
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
    e.preventDefault();
    if (currentSlideIndex < totalSlides - 1) {
      goToSlide(currentSlideIndex + 1);
    }
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
    e.preventDefault();
    if (currentSlideIndex > 0) {
      goToSlide(currentSlideIndex - 1);
    }
  }
});

// Wheel scroll controls handler (Desktop only)
window.addEventListener('wheel', (e) => {
  if (isTransitioning || (window.innerWidth <= 768)) return;
  
  // Threshold to avoid super light scrolls triggering slides
  if (Math.abs(e.deltaY) < 30) return;

  if (e.deltaY > 0) {
    if (currentSlideIndex < totalSlides - 1) {
      goToSlide(currentSlideIndex + 1);
    }
  } else {
    if (currentSlideIndex > 0) {
      goToSlide(currentSlideIndex - 1);
    }
  }
}, { passive: true });

// Swipe gesture controls handler
let touchStartX = 0;
let touchStartY = 0;

window.addEventListener('touchstart', (e) => {
  touchStartX = e.changedTouches[0].clientX;
  touchStartY = e.changedTouches[0].clientY;
}, { passive: true });

window.addEventListener('touchend', (e) => {
  if (isTransitioning || (window.innerWidth <= 768)) return;
  
  const touchEndX = e.changedTouches[0].clientX;
  const touchEndY = e.changedTouches[0].clientY;
  
  const diffX = touchStartX - touchEndX;
  const diffY = touchStartY - touchEndY;

  // Verify if horizontal swipe is dominant and large enough
  if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 60) {
    if (diffX > 0) {
      // Swipe Left -> Next Slide
      if (currentSlideIndex < totalSlides - 1) goToSlide(currentSlideIndex + 1);
    } else {
      // Swipe Right -> Prev Slide
      if (currentSlideIndex > 0) goToSlide(currentSlideIndex - 1);
    }
  }
}, { passive: true });

// Mobile Scroll Listener to update active index based on visible slide section
window.addEventListener('scroll', () => {
  if (window.innerWidth > 768) return;
  
  const scrollPosition = window.scrollY + (window.innerHeight / 2);
  
  slides.forEach((slide, idx) => {
    const slideTop = slide.offsetTop;
    const slideBottom = slideTop + slide.offsetHeight;
    
    if (scrollPosition >= slideTop && scrollPosition < slideBottom) {
      if (currentSlideIndex !== idx) {
        currentSlideIndex = idx;
        updateActiveStates(idx);
        updateControls();
        // Animate stats if entering slide 2
        if (idx === 1) {
          animateStats();
        }
      }
    }
  });
});

// Arrow Button Listeners
if (prevBtn) prevBtn.addEventListener('click', () => goToSlide(currentSlideIndex - 1));
if (nextBtn) nextBtn.addEventListener('click', () => goToSlide(currentSlideIndex + 1));


/* ==========================================================================
   NAVIGATION MENU (SLIDE MAP) DROPDOWN
   ========================================================================== */

function toggleMenu(forceState) {
  const toggleState = typeof forceState === 'boolean' ? forceState : !menuToggle.classList.contains('active');
  
  if (toggleState) {
    menuToggle.classList.add('active');
    slideMap.classList.add('active');
  } else {
    menuToggle.classList.remove('active');
    slideMap.classList.remove('active');
  }
}

if (menuToggle) menuToggle.addEventListener('click', () => toggleMenu());


/* ==========================================================================
   STATS NUMBERS COUNTING UP ANIMATION
   ========================================================================== */

let statsAnimated = false;

function animateStats() {
  const statNumbers = document.querySelectorAll('.stat-num');
  
  statNumbers.forEach(elem => {
    const targetVal = parseFloat(elem.getAttribute('data-val'));
    const decimals = parseInt(elem.getAttribute('data-decimals') || '0');
    
    let currentVal = 0;
    const duration = 1500; // Total count duration in ms
    const increment = targetVal / (duration / 16); // ~60fps
    
    const countInterval = setInterval(() => {
      currentVal += increment;
      if (currentVal >= targetVal) {
        currentVal = targetVal;
        clearInterval(countInterval);
      }
      elem.textContent = currentVal.toFixed(decimals);
    }, 16);
  });
  
  statsAnimated = true;
}


/* ==========================================================================
   PROJECTS FILTER CARDS
   ========================================================================== */

const filterTabs = document.querySelectorAll('.filter-tab');
const projectCards = document.querySelectorAll('.project-card');

filterTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    // Update active tab style
    filterTabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    
    const filter = tab.getAttribute('data-filter');
    
    projectCards.forEach(card => {
      const categories = card.getAttribute('data-categories');
      
      // Animate filter transitions using transform scaling
      card.style.opacity = '0';
      card.style.transform = 'scale(0.95) translateY(10px)';
      
      setTimeout(() => {
        if (filter === 'all' || categories.split(' ').includes(filter)) {
          card.classList.remove('hidden');
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'scale(1) translateY(0)';
          }, 50);
        } else {
          card.classList.add('hidden');
        }
      }, 300);
    });
  });
});


/* ==========================================================================
   LIGHT / DARK THEME TOGGLE
   ========================================================================== */

const themeToggle = document.getElementById('theme-toggle');
const htmlElement = document.documentElement;

// Read saved theme
const savedTheme = localStorage.getItem('theme') || 'dark';
htmlElement.setAttribute('data-theme', savedTheme);

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const currentTheme = htmlElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    htmlElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update dynamic particle colors
    if (typeof updateParticleTheme === 'function') {
      updateParticleTheme(newTheme);
    }
  });
}


/* ==========================================================================
   CERTIFICATES FULL SCREEN MODAL VIEWER
   ========================================================================== */

const certModal = document.getElementById('cert-modal');
const certModalImg = document.getElementById('cert-modal-img');
const certModalCaption = document.getElementById('cert-modal-caption');
const certModalClose = document.getElementById('cert-modal-close');

function openCertModal(imagePath, captionText) {
  if (!certModal || !certModalImg || !certModalCaption) return;
  
  certModalImg.src = imagePath;
  certModalCaption.textContent = captionText;
  certModal.classList.add('active');
}

if (certModalClose) {
  certModalClose.addEventListener('click', () => {
    certModal.classList.remove('active');
  });
}

if (certModal) {
  certModal.addEventListener('click', (e) => {
    if (e.target === certModal) {
      certModal.classList.remove('active');
    }
  });
}


/* ==========================================================================
   LIGHTWEIGHT DYNAMIC PARTICLES CANVAS
   ========================================================================== */

const canvas = document.getElementById('particle-canvas');
let ctx = null;
let particles = [];
let particleColor = 'rgba(0, 180, 216, 0.2)';
let lineColor = 'rgba(0, 180, 216, 0.08)';

if (canvas) {
  ctx = canvas.getContext('2d');
  
  // Set dimensions
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);
  
  // Initialize particles
  const particleCount = Math.min(60, Math.floor((canvas.width * canvas.height) / 25000));
  initParticles(particleCount);
  
  // Start loop
  requestAnimationFrame(animateParticles);
}

function resizeCanvas() {
  if (!canvas) return;
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

function updateParticleTheme(theme) {
  if (theme === 'light') {
    particleColor = 'rgba(0, 119, 182, 0.18)';
    lineColor = 'rgba(0, 119, 182, 0.06)';
  } else {
    particleColor = 'rgba(0, 180, 216, 0.2)';
    lineColor = 'rgba(0, 180, 216, 0.08)';
  }
  
  particles.forEach(p => {
    p.color = particleColor;
  });
}

// Set initial theme color
updateParticleTheme(savedTheme);

class Particle {
  constructor(w, h) {
    this.x = Math.random() * w;
    this.y = Math.random() * h;
    this.vx = (Math.random() - 0.5) * 0.4;
    this.vy = (Math.random() - 0.5) * 0.4;
    this.radius = Math.random() * 2.5 + 1;
    this.color = particleColor;
  }
  
  draw() {
    if (!ctx) return;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.fill();
  }
  
  update(w, h) {
    this.x += this.vx;
    this.y += this.vy;
    
    // Bounds boundary wrap
    if (this.x < 0) this.x = w;
    if (this.x > w) this.x = 0;
    if (this.y < 0) this.y = h;
    if (this.y > h) this.y = 0;
  }
}

function initParticles(count) {
  particles = [];
  for (let i = 0; i < count; i++) {
    particles.push(new Particle(canvas.width, canvas.height));
  }
}

function animateParticles() {
  if (!canvas || !ctx) return;
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  const w = canvas.width;
  const h = canvas.height;
  
  // Update & Draw
  particles.forEach(p => {
    p.update(w, h);
    p.draw();
  });
  
  // Draw Connections
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      
      if (dist < 120) {
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.strokeStyle = lineColor;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }
  
  requestAnimationFrame(animateParticles);
}


/* ==========================================================================
   INITIALIZE CORE CONTROLS
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initSlides();
  
  // Trigger initial animations
  setTimeout(() => {
    // Add animations to landing hero elements if needed
  }, 100);
});
