# NoApplAI Frontend

Single-page application built with vanilla JavaScript and Tailwind CSS.

## 🚀 Running the Frontend

### **Option 1: Simple HTTP Server (Recommended)**
```bash
# From the project root
cd frontend

# Python 3
python -m http.server 3000

# Or Python 2
python -m SimpleHTTPServer 3000
```

Access at: http://localhost:3000/full_page_integrated.html

### **Option 2: VS Code Live Server**
1. Install "Live Server" extension in VS Code
2. Right-click `full_page_integrated.html`
3. Select "Open with Live Server"

### **Option 3: Direct File Access**
Open `full_page_integrated.html` directly in your browser.

**Note**: Some features may require a local server for API calls to work correctly.

---

## 🔗 API Configuration

The frontend expects the backend API at:
```
http://localhost:8000
```

To change this, update the `API_BASE_URL` in `full_page_integrated.html`.

---

## 📱 Features

- **Authentication**: Login/Register/Logout
- **Program Browser**: Search and filter university programs
- **Application Dashboard**: Track all applications in one place
- **Document Upload**: Manage required documents
- **Notifications**: Real-time application updates
- **Responsive Design**: Works on mobile, tablet, and desktop

---

## 🎨 Technology Stack

- **Vanilla JavaScript**: No framework dependencies
- **Tailwind CSS**: Utility-first CSS framework (via CDN)
- **Client-side Routing**: Custom navigation system
- **JWT Authentication**: Token-based auth with localStorage
- **Fetch API**: For backend communication

---

## 🐛 Troubleshooting

### API Connection Issues
- Ensure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify Docker containers are running: `docker compose ps`

### Login Not Working
- Clear browser localStorage: `localStorage.clear()` in console
- Check backend logs: `docker compose logs backend`
- Verify test credentials in main README

### Styling Issues
- Check internet connection (Tailwind loaded via CDN)
- Clear browser cache
- Try hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
