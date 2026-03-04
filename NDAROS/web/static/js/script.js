let reveal;
let slidesData = [];

// Charger les slides depuis l'API
async function loadSlides() {
    try {
        const response = await fetch('/api/slides');
        slidesData = await response.json();
        console.log('Slides loaded:', slidesData);
    } catch (error) {
        console.error('Error loading slides:', error);
    }
}

// Initialiser Reveal.js avec config complète
function initReveal() {
    Reveal.initialize({
        width: 1920,
        height: 1080,
        margin: 0,
        padding: 0,
        minScale: 1,
        maxScale: 1,
        transition: 'slide',
        transitionSpeed: 'default',
        keyboard: false,
        touch: false,
        overview: false,
        center: true,
        embedded: false,
        controls: false,
        progress: false,
        hash: false,
    });
}

// Mettre à jour la slide depuis l'API
async function updateSlideFromAPI() {
    try {
        const response = await fetch('/api/current-slide');
        const data = await response.json();
        const currentIndex = Reveal.getState().indexh || 0;
        
        if (data.slide !== currentIndex) {
            Reveal.slide(data.slide);
        }
    } catch (error) {
        // Erreur silencieuse
    }
}

// Avancer d'une slide
async function nextSlide() {
    try {
        const response = await fetch('/api/next-slide');
        const data = await response.json();
        Reveal.slide(data.slide);
    } catch (error) {
        console.error('Error calling next-slide:', error);
    }
}

// Reculer d'une slide
async function prevSlide() {
    try {
        const response = await fetch('/api/prev-slide');
        const data = await response.json();
        Reveal.slide(data.slide);
    } catch (error) {
        console.error('Error calling prev-slide:', error);
    }
}

// Aller à une slide spécifique
async function gotoSlide(n) {
    try {
        const response = await fetch(`/api/goto-slide/${n}`);
        const data = await response.json();
        Reveal.slide(data.slide);
    } catch (error) {
        console.error(`Error calling goto-slide/${n}:`, error);
    }
}

// Empêcher de quitter le fullscreen avec Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        e.preventDefault();
    }
});

// Lancer les mises à jour périodiques
setInterval(updateSlideFromAPI, 500);

// Export pour utilisation globale
window.nextSlide = nextSlide;
window.prevSlide = prevSlide;
window.gotoSlide = gotoSlide;