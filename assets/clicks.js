(function () {
    const path = location.pathname;
    const parts = path.split('/').filter(Boolean);
    const toolsIndex = parts.indexOf('tools');
    let id = null;

    if (path === '/' || path.endsWith('/index.html')) {
        id = 'home';
    } else if (toolsIndex !== -1 && parts[toolsIndex + 1]) {
        id = parts[toolsIndex + 1];
    }

    if (id) {
        return; // Disable click tracking for now
        // const payload = JSON.stringify({ id });
        // if (navigator.sendBeacon) {
        //     navigator.sendBeacon('/api/clicks', new Blob([payload], { type: 'application/json' }));
        // } else {
        //     fetch('/api/clicks', {
        //         method: 'POST',
        //         headers: { 'Content-Type': 'application/json' },
        //         body: payload,
        //         keepalive: true
        //     });
        // }
    }

    if (toolsIndex !== -1 && parts[toolsIndex + 1] && !path.endsWith('/app.html')) {
        const basePath = `/${parts.slice(0, toolsIndex + 2).join('/')}/`;
        const appUrl = `${basePath}app.html`;
        document.querySelectorAll('a[href]').forEach((link) => {
            const href = link.getAttribute('href');
            if (!href || /^(https?:)?\/\//i.test(href) || href.startsWith('mailto:') || href.startsWith('#')) {
                return;
            }
            if (href === 'app.html' || href === './app.html' || href === 'app') {
                link.setAttribute('href', appUrl);
            }
        });
        document.querySelectorAll('iframe[src]').forEach((frame) => {
            const src = frame.getAttribute('src');
            if (src === 'app.html' || src === './app.html' || src === 'app') {
                frame.setAttribute('src', appUrl);
            }
        });
    }

    if (!path.endsWith('/app.html') || toolsIndex === -1) {
        return;
    }

    if (document.querySelector('.tool-doc-link')) {
        return;
    }

    const docLink = document.createElement('a');
    docLink.href = path.replace(/app\.html$/, 'index.html');
    docLink.className = 'tool-doc-link';
    docLink.textContent = '\u8bf4\u660e';
    docLink.setAttribute('aria-label', '\u67e5\u770b\u5de5\u5177\u8bf4\u660e');
    docLink.style.cssText = [
        'position:fixed',
        'top:18px',
        'right:18px',
        'padding:8px 14px',
        'border-radius:999px',
        'font-size:13px',
        'font-weight:600',
        'color:#0f172a',
        'background:rgba(255,255,255,0.92)',
        'text-decoration:none',
        'box-shadow:0 10px 30px rgba(0,0,0,0.2)',
        'backdrop-filter:blur(6px)',
        'z-index:9999'
    ].join(';');
    docLink.addEventListener('mouseenter', () => {
        docLink.style.transform = 'translateY(-1px)';
        docLink.style.boxShadow = '0 12px 30px rgba(0,0,0,0.25)';
    });
    docLink.addEventListener('mouseleave', () => {
        docLink.style.transform = 'translateY(0)';
        docLink.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)';
    });

    document.body.appendChild(docLink);
})();
