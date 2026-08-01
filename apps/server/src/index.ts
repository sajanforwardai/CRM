import express from 'express';
import cors from 'express-cors';
import { initDb } from './db/index.js';
import authRouter from './routes/auth.js';
import { errorHandler, authMiddleware } from './middleware/index.js';

const app = express();
const PORT = process.env.PORT || 4000;

// Middleware
app.use(cors());
app.use(express.json());

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Routes
app.use('/api/auth', authRouter);

// Protected route example
app.get('/api/me', authMiddleware, (req, res) => {
  res.json({ user: req.user });
});

// Error handling
app.use(errorHandler);

// Start server
async function start() {
  try {
    await initDb();
    console.log('✓ Database initialized');

    app.listen(PORT, () => {
      console.log(`✓ Server running on http://localhost:${PORT}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

start();
