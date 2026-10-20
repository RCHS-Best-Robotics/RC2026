// TICKER (paste below the title code in app.js)

(() => {
    const viewport = document.querySelector('.ticker-viewport');
    const track = viewport.querySelector('.ticker-track');
    const lightbox = document.querySelector('.lightbox');
    const lightboxBody = lightbox.querySelector('.lightbox-body');
    const originals = [...track.children];

    const AUTO = 0.5;   // px per frame
    const STEP = 336;   // card width + margin, update if the css changes
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

    let x = 0, setW = 0, glide = 0;
    let dragging = false, hovering = false, captured = false, moved = 0, lastX = 0;

    // clone the cards until the track is long enough to loop
    function build() {
        track.querySelectorAll('[data-clone]').forEach(n => n.remove());
        setW = track.scrollWidth;
        if (!setW) return;
        while (track.scrollWidth < viewport.offsetWidth + setW) {
            originals.forEach(n => {
                const c = n.cloneNode(true);
                c.dataset.clone = '';
                c.setAttribute('aria-hidden', 'true');
                track.append(c);
            });
        }
    }

    function frame() {
        if (setW) {
            if (!dragging) {
                const step = glide * 0.12;
                glide -= step;
                x += step + (hovering || reduce ? 0 : AUTO);
            }
            x = ((x % setW) + setW) % setW;
            track.style.transform = `translate3d(${-x}px, 0, 0)`;
        }
        requestAnimationFrame(frame);
    }

    viewport.addEventListener('pointerdown', e => {
        dragging = true; captured = false; moved = 0; lastX = e.clientX;
        viewport.classList.add('grabbing');
    });
    viewport.addEventListener('pointermove', e => {
        if (!dragging) return;
        const dx = e.clientX - lastX;
        lastX = e.clientX;
        moved += Math.abs(dx);
        x -= dx;
        // capture only on a real drag so plain clicks still reach the card
        if (!captured && moved > 5) { viewport.setPointerCapture(e.pointerId); captured = true; }
    });
    const endDrag = () => { dragging = false; viewport.classList.remove('grabbing'); };
    viewport.addEventListener('pointerup', endDrag);
    viewport.addEventListener('pointercancel', endDrag);

    viewport.addEventListener('mouseenter', () => hovering = true);
    viewport.addEventListener('mouseleave', () => hovering = false);

    document.querySelectorAll('.tick-btn').forEach(btn =>
        btn.addEventListener('click', () => { glide += Number(btn.dataset.dir) * STEP; })
    );

    track.addEventListener('click', e => {
        const tick = e.target.closest('.tick');
        if (!tick || moved > 5) return;
        lightboxBody.innerHTML = tick.innerHTML;
        lightbox.showModal();
    });
    lightbox.addEventListener('click', () => lightbox.close());

    build();
    window.addEventListener('resize', build);
    requestAnimationFrame(frame);
})();