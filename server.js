const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = path.join(__dirname, 'public');

// CORS headers
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, RSC, Next-Router-State-Tree, Next-Router-Prefetch');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

// Helper for Next.js App Router RSC flight requests
function isRscRequest(req) {
  return req.headers['rsc'] === '1' || req.query._rsc !== undefined;
}

// Routes mapping
const ROUTE_FILES = {
  '/': { html: 'index.html', rsc: 'index.rsc' },
  '/events': { html: 'events.html', rsc: 'events.rsc' },
  '/events/flagship-events': { html: path.join('events', 'flagship-events.html'), rsc: path.join('events', 'flagship-events.rsc') },
  '/events/standout-events': { html: path.join('events', 'standout-events.html'), rsc: path.join('events', 'standout-events.rsc') },
  '/events/main-events': { html: path.join('events', 'main-events.html'), rsc: path.join('events', 'main-events.rsc') },
  '/events/dts-and-fun-events': { html: path.join('events', 'dts-and-fun-events.html'), rsc: path.join('events', 'dts-and-fun-events.rsc') },
  '/merch': { html: 'merch.html', rsc: 'merch.rsc' },
  '/privacy': { html: 'privacy.html', rsc: 'privacy.rsc' },
  '/terms': { html: 'terms.html', rsc: 'terms.rsc' },
};

// API Endpoints
app.get('/api/events', (req, res) => {
  const filePath = path.join(PUBLIC_DIR, 'api', 'events.json');
  if (fs.existsSync(filePath)) {
    res.setHeader('Content-Type', 'application/json');
    return fs.createReadStream(filePath).pipe(res);
  }
  res.status(404).json({ success: false, error: 'Not found' });
});

app.get('/api/gallery', (req, res) => {
  const filePath = path.join(PUBLIC_DIR, 'api', 'gallery.json');
  if (fs.existsSync(filePath)) {
    res.setHeader('Content-Type', 'application/json');
    return fs.createReadStream(filePath).pipe(res);
  }
  res.json({ success: true, gallery: [] });
});

app.get('/api/seats', (req, res) => {
  res.json({ total: 1300, left: 232 });
});

app.get('/api/auth/session', (req, res) => {
  res.json({ success: false, session: null, user: null });
});

app.get('/api/auth/profile', (req, res) => {
  res.json({ success: false, profile: null });
});

app.get('/api/ambassador/code', (req, res) => {
  res.status(401).json({
    error: 'Authentication Required',
    message: 'You must log in or sign up before accessing this endpoint'
  });
});

app.post('/api/register/check-code', (req, res) => {
  res.json({ valid: false, message: 'Code not found' });
});

// Handle exact and dynamic routes
for (const [route, files] of Object.entries(ROUTE_FILES)) {
  app.get(route, (req, res, next) => {
    if (isRscRequest(req)) {
      const rscPath = path.join(PUBLIC_DIR, files.rsc);
      if (fs.existsSync(rscPath)) {
        res.setHeader('Content-Type', 'text/x-component; charset=utf-8');
        return fs.createReadStream(rscPath).pipe(res);
      }
    }
    const htmlPath = path.join(PUBLIC_DIR, files.html);
    if (fs.existsSync(htmlPath)) {
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      return fs.createReadStream(htmlPath).pipe(res);
    }
    next();
  });
}

// Special check for dynamic events routes: /events/:world
app.get('/events/:world', (req, res, next) => {
  const world = req.params.world;
  const specificHtml = path.join(PUBLIC_DIR, 'events', `${world}.html`);
  const specificRsc = path.join(PUBLIC_DIR, 'events', `${world}.rsc`);
  if (isRscRequest(req) && fs.existsSync(specificRsc)) {
    res.setHeader('Content-Type', 'text/x-component; charset=utf-8');
    return fs.createReadStream(specificRsc).pipe(res);
  }
  if (fs.existsSync(specificHtml)) {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    return fs.createReadStream(specificHtml).pipe(res);
  }
  // Fallback to events.html
  const fallbackHtml = path.join(PUBLIC_DIR, 'events.html');
  if (fs.existsSync(fallbackHtml)) {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    return fs.createReadStream(fallbackHtml).pipe(res);
  }
  next();
});

// Local ImageKit image serving (offline support)
app.use('/imagekit', express.static(path.join(PUBLIC_DIR, 'imagekit')));

// Static assets handler
app.use(express.static(PUBLIC_DIR, {
  dotfiles: 'allow',
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.js')) {
      res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
    } else if (filePath.endsWith('.css')) {
      res.setHeader('Content-Type', 'text/css; charset=utf-8');
    } else if (filePath.endsWith('.woff2')) {
      res.setHeader('Content-Type', 'font/woff2');
    } else if (filePath.endsWith('.webp')) {
      res.setHeader('Content-Type', 'image/webp');
    } else if (filePath.endsWith('.mp3')) {
      res.setHeader('Content-Type', 'audio/mpeg');
    }
  }
}));

// Fallback to index.html for any unhandled routes
app.use((req, res) => {
  const indexPath = path.join(PUBLIC_DIR, 'index.html');
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.sendFile(indexPath);
});

app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`  INNOVISION NIT ROURKELA 2026 OFFICIAL WEBSITE`);
  console.log(`  Local server is running at: http://localhost:${PORT}`);
  console.log(`=======================================================`);
});
