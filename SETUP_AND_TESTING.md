# Setup and Testing Guide

## ✅ Issues Fixed

### 1. Backend Connection Error
**Problem:** Frontend couldn't connect to backend (Network Error)

**Solution:**
- Changed API base URL from `http://localhost:8000/api/v1` to `/api/v1` to use Vite proxy
- This allows the frontend to connect through the Vite dev server proxy, avoiding CORS issues

**File Changed:** `frontend/src/services/api.ts`

### 2. Login Failed Error
**Problem:** Login showed "Login failed" even with correct credentials

**Solution:**
- Improved error handling in auth store to show specific error messages
- Added network error detection and better error messages
- Backend login endpoint is working correctly (tested)

**Files Changed:** 
- `frontend/src/stores/auth.ts` - Better error handling
- `frontend/src/services/api.ts` - Fixed API base URL

## 🚀 How to Start Servers

### Backend Server
```powershell
cd "C:\Users\Shubh\OneDrive\Desktop\college\semester 4\Uni_Arena\backend"
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Verify Backend is Running:**
- Open: http://localhost:8000/docs (API documentation)
- Health check: http://localhost:8000/health
- Should return: `{"status":"healthy"}`

### Frontend Server
```powershell
cd "C:\Users\Shubh\OneDrive\Desktop\college\semester 4\Uni_Arena\frontend"
npm run dev
```

**Verify Frontend is Running:**
- Open: http://localhost:5173
- Should show the Uni Arena login page

## 🔐 Login Credentials

The database has been seeded with sample data. Use these credentials:

| Role | Email | Password |
|------|-------|----------|
| **Admin** | `admin@uniarena.com` | `admin123` |
| **Organizer** | `organizer@use.edu` | `organizer123` |
| **Coach** | `coach@use.edu` | `coach123` |
| **Player** | `player1@use.edu` | `player123` |

## ✅ Testing Checklist

### 1. Backend Health Check
- [x] Backend server is running on port 8000
- [x] Health endpoint returns 200 OK
- [x] Database has seed data (10 users confirmed)

### 2. Frontend Connection
- [ ] Frontend server is running on port 5173
- [ ] Can access http://localhost:5173
- [ ] No network errors in browser console

### 3. Login Test
- [ ] Can login with `admin@uniarena.com` / `admin123`
- [ ] Redirects to dashboard after login
- [ ] No "Login failed" error

### 4. API Endpoints
- [ ] Matches endpoint: http://localhost:8000/api/v1/matches
- [ ] Tournaments endpoint: http://localhost:8000/api/v1/tournaments
- [ ] Login endpoint: http://localhost:8000/api/v1/auth/login/json

## 🐛 Troubleshooting

### If Backend Won't Start
1. Check if port 8000 is in use:
   ```powershell
   netstat -ano | findstr :8000
   ```
2. Kill processes using port 8000:
   ```powershell
   taskkill /F /PID <PID_NUMBER>
   ```
3. Restart backend server

### If Frontend Shows Network Error
1. Make sure backend is running on port 8000
2. Check browser console for specific error
3. Verify Vite proxy is working (check `vite.config.ts`)
4. Try clearing browser cache

### If Login Still Fails
1. Check browser console for error details
2. Verify credentials match exactly (case-sensitive)
3. Test login endpoint directly:
   ```powershell
   $body = '{"email":"admin@uniarena.com","password":"admin123"}'
   Invoke-WebRequest -Uri "http://localhost:8000/api/v1/auth/login/json" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
   ```

## 📝 Notes

- The frontend now uses `/api/v1` as the base URL, which goes through Vite's proxy
- The proxy forwards requests to `http://localhost:8000`
- This avoids CORS issues in development
- All sport-specific scoring logic is implemented and ready to use

## 🎯 Next Steps

1. Start both servers (backend and frontend)
2. Open http://localhost:5173 in your browser
3. Try logging in with admin credentials
4. Test the coach live score update feature with different sports
5. Verify all pages load correctly
