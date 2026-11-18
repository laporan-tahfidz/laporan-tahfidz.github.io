# Super Admin Authentication System

## Overview
This system implements a secure super admin authentication mechanism using WhatsApp OTP (One-Time Password) verification.

## Features
- WhatsApp OTP-based authentication
- Session management
- Protected routes
- Secure token handling
- Support for predefined admin numbers

## Supported Admin Numbers
Only the following Indonesian numbers are allowed for super admin access:
- 081545143654
- 082274180206

## How It Works

### Frontend (SvelteKit)
1. The `/super` route is now public and does not require authentication
2. The system still supports token-based functionality for enhanced features
3. Login page at `/super-login` accepts WhatsApp number and sends OTP
4. After OTP verification, a token is stored in localStorage
5. User can access enhanced features with the token

### Backend (PHP)
1. `send-otp.php` generates a 6-digit OTP and sends it via WhatsApp using Sidobe API
2. `verify-otp.php` validates the entered OTP and generates a secure token
3. `verify-token.php` verifies the stored token for protected routes
4. Sessions are used to store OTP codes and tokens temporarily

## Files Structure
```
src/
├── routes/
│   ├── super-login/
│   │   └── +page.svelte
│   ├── super/
│   │   ├── +page.svelte
│   │   └── +page.js
│   └── +page.svelte
└── lib/
    └── utils.js

static/
├── send-otp.php
├── verify-otp.php
├── verify-token.php
├── init-session.php
├── config.php
└── library/
    └── rb-sqlite.php (if using database)
```

## Security Measures
- OTP codes expire after 5 minutes
- Secure token generation using `random_bytes(32)`
- Proper session handling
- Input validation
- CORS headers for API requests

## Dependencies
- SvelteKit 5
- Tailwind CSS
- Sidobe WhatsApp API