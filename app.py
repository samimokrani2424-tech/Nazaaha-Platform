<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة نزاهة | جامعة قسنطينة 3</title>
    
    <!-- React & ReactDOM -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    
    <!-- Babel for JSX -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap" rel="stylesheet">
    
    <style>
        body { font-family: 'Tajawal', sans-serif; background-color: #f3f4f6; }
        .rtl { direction: rtl; }
        .ltr { direction: ltr; }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #f1f1f1; }
        ::-webkit-scrollbar-thumb { background: #c1c1c1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #a8a8a8; }

        .glass-panel {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .animate-fade-in { animation: fadeIn 0.5s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useRef } = React;

        // --- Icons Component (Using SVG directly to avoid dependency issues) ---
        const Icons = {
            Book: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>,
            Upload: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>,
            Brain: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>,
            Settings: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>,
            LogOut: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>,
            GraduationCap: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>,
            LayoutDashboard: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>,
            CheckCircle: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>,
            Search: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>,
            Download: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>,
            Shield: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>,
            Coins: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 16V8"/><path d="M8 12h8"/></svg>
        };

        // --- Data Models ---
        const UNIVERSITIES = {
            "Faculté de Médecine": ["Médecine", "Pharmacie", "Médecine Dentaire"],
            "Faculté d'Architecture et d'Urbanisme": ["Architecture", "Urbanisme", "Gestion des Villes"],
            "Faculté des Arts et de la Culture": ["Arts Plastiques", "Arts Dramatiques", "Cinéma"],
            "Faculté de Génie des Procédés": ["Génie Chimique", "Génie Pharmaceutique"],
            "Faculté des Sciences Politiques": ["Sciences Politiques", "Relations Internationales"],
            "Faculté des NTIC": ["Informatique (GL)", "Informatique (SI)", "Réseaux et Télécom"],
            "Institut de Gestion des Techniques Urbaines": ["Génie Urbain", "Gestion de la ville"]
        };

        const LEVELS = ["Licence 1", "Licence 2", "Licence 3", "Master 1", "Master 2", "Doctorat"];

        const TRANSLATIONS = {
            ar: {
                title: "منصة نزاهة الأكاديمية",
                tagline: "بوابتك نحو التميز الأكاديمي - جامعة قسنطينة 3",
                login: "تسجيل الدخول",
                signup: "إنشاء حساب",
                email: "البريد الإلكتروني",
                password: "كلمة المرور",
                dashboard: "لوحة القيادة",
                library: "المكتبة الرقمية",
                upload: "مركز النشر",
                quiz: "تحدي المعرفة",
                settings: "الإعدادات",
                points: "نقاط المعرفة",
                buy: "شراء",
                owned: "مملوك",
                ai_check: "التحقق الذكي",
                upload_text: "ارفع ملفاتك وسيقوم الذكاء الاصطناعي بتقييمها",
                welcome: "مرحباً،",
                logout: "خروج",
                price: "السعر",
                quality: "الجودة العلمية",
                generated_quiz: "سؤال من كتابك",
                submit: "تحقق من الإجابة",
                correct: "إجابة صحيحة!",
                wrong: "إجابة خاطئة",
                download: "تحميل وقراءة",
                search: "بحث في المكتبة..."
            },
            fr: {
                title: "Plateforme Académique Nazaha",
                tagline: "Votre portail vers l'excellence - Université Constantine 3",
                login: "Connexion",
                signup: "Inscription",
                email: "Email",
                password: "Mot de passe",
                dashboard: "Tableau de bord",
                library: "Bibliothèque",
                upload: "Centre de Publication",
                quiz: "Quiz de Connaissance",
                settings: "Paramètres",
                points: "Points de Savoir",
                buy: "Acheter",
                owned: "Acquis",
                ai_check: "Vérification IA",
                upload_text: "Téléchargez vos fichiers, l'IA les évaluera",
                welcome: "Bienvenue, ",
                logout: "Déconnexion",
                price: "Prix",
                quality: "Qualité",
                generated_quiz: "Question générée",
                submit: "Vérifier",
                correct: "Correct!",
                wrong: "Faux",
                download: "Télécharger",
                search: "Rechercher..."
            },
            en: {
                title: "Nazaha Academic Platform",
                tagline: "Your gateway to excellence - Constantine 3 University",
                login: "Login",
                signup: "Sign Up",
                email: "Email",
                password: "Password",
                dashboard: "Dashboard",
                library: "Library",
                upload: "Upload Center",
                quiz: "Knowledge Quiz",
                settings: "Settings",
                points: "Knowledge Points",
                buy: "Buy",
                owned: "Owned",
                ai_check: "AI Check",
                upload_text: "Upload files, AI will evaluate them",
                welcome: "Welcome, ",
                logout: "Logout",
                price: "Price",
                quality: "Quality",
                generated_quiz: "Generated Question",
                submit: "Verify Answer",
                correct: "Correct!",
                wrong: "Wrong",
                download: "Download",
                search: "Search..."
            }
        };

        // --- Mock Data Initialization ---
        const INITIAL_BOOKS = [
            { id: 1, title: "Introduction à l'Architecture", author: "Dr. Amine", faculty: "Faculté d'Architecture et d'Urbanisme", price: 45, downloads: 120, quality: 85, type: "PDF", category: "Architecture" },
            { id: 2, title: "Algorithmique Avancée", author: "Prof. Sara", faculty: "Faculté des NTIC", price: 60, downloads: 45, quality: 92, type: "PDF", category: "Informatique" },
            { id: 3, "title": "Anatomie Humaine", "author": "Faculté Méd", "faculty": "Faculté de Médecine", "price": 75, "downloads": 300, "quality": 98, "type": "PDF", "category": "Médecine" }
        ];

        // --- Main App Component ---
        const App = () => {
            // State
            const [view, setView] = useState('login');
            const [lang, setLang] = useState('ar');
            const [user, setUser] = useState(null);
            const [books, setBooks] = useState([]);
            const [sidebarOpen, setSidebarOpen] = useState(true);
            const [notification, setNotification] = useState(null);

            // Auth Forms
            const [loginData, setLoginData] = useState({ email: '', password: '' });
            const [signupData, setSignupData] = useState({ name: '', email: '', password: '', faculty: '', specialty: '', level: '' });
            const [isRegistering, setIsRegistering] = useState(false);

            // Helper: Translate
            const t = (k) => TRANSLATIONS[lang][k] || k;
            const dir = lang === 'ar' ? 'rtl' : 'ltr';

            // Initialize
            useEffect(() => {
                // Load from localStorage
                const storedUser = localStorage.getItem('nazaha_user');
                const storedBooks = localStorage.getItem('nazaha_books');
                
                if (storedUser) {
                    setUser(JSON.parse(storedUser));
                    setView('dashboard');
                }
                if (storedBooks) {
                    setBooks(JSON.parse(storedBooks));
                } else {
                    setBooks(INITIAL_BOOKS);
                    localStorage.setItem('nazaha_books', JSON.stringify(INITIAL_BOOKS));
                }
            }, []);

            // Notification Handler
            const notify = (msg, type = 'success') => {
                setNotification({ msg, type });
                setTimeout(() => setNotification(null), 3000);
            };

            // Logic: AI Analysis Simulation (The "Smart" Logic ported to JS)
            const analyzeFile = (file) => {
                return new Promise((resolve) => {
                    setTimeout(() => {
                        // Simulate AI Logic based on file size and name length
                        const sizeScore = file.size > 10000 ? 30 : 10;
                        const nameScore = file.name.length > 10 ? 20 : 5;
                        const randomFactor = Math.floor(Math.random() * 40);
                        
                        const totalScore = Math.min(100, sizeScore + nameScore + randomFactor + 20); // Base 20
                        const isAcademic = totalScore > 50;
                        const price = Math.floor(totalScore * 0.8);
                        
                        resolve({ score: totalScore, price, isAcademic });
                    }, 2500);
                });
            };

            // Actions
            const handleLogin = (e) => {
                e.preventDefault();
                // Simple mock auth
                const users = JSON.parse(localStorage.getItem('nazaha_users_db') || '[]');
                const found = users.find(u => u.email === loginData.email && u.password === loginData.password);
                
                if (found) {
                    setUser(found);
                    localStorage.setItem('nazaha_user', JSON.stringify(found));
                    setView('dashboard');
                    notify(t('welcome') + found.name);
                } else {
                    notify("Invalid credentials", 'error');
                }
            };

            const handleSignup = (e) => {
                e.preventDefault();
                if(!signupData.name || !signupData.email) return notify("Please fill all fields", "error");
                
                const newUser = { ...signupData, points: 150, library: [], uploads: [] };
                const users = JSON.parse(localStorage.getItem('nazaha_users_db') || '[]');
                
                if(users.find(u => u.email === newUser.email)) return notify("Email exists", "error");
                
                users.push(newUser);
                localStorage.setItem('nazaha_users_db', JSON.stringify(users));
                notify("Account created! Please login.");
                setIsRegistering(false);
            };

            const handleLogout = () => {
                localStorage.removeItem('nazaha_user');
                setUser(null);
                setView('login');
            };

            const handlePurchase = (book) => {
                const dynamicPrice = book.price + Math.floor(book.downloads * 0.2);
                
                if (user.points >= dynamicPrice) {
                    const updatedUser = { 
                        ...user, 
                        points: user.points - dynamicPrice,
                        library: [...user.library, book]
                    };
                    
                    const updatedBooks = books.map(b => 
                        b.id === book.id ? {...b, downloads: b.downloads + 1} : b
                    );

                    setUser(updatedUser);
                    setBooks(updatedBooks);
                    localStorage.setItem('nazaha_user', JSON.stringify(updatedUser));
                    localStorage.setItem('nazaha_books', JSON.stringify(updatedBooks));
                    
                    // Update DB for persistence
                    const users = JSON.parse(localStorage.getItem('nazaha_users_db') || '[]');
                    const userIdx = users.findIndex(u => u.email === user.email);
                    if(userIdx >= 0) {
                        users[userIdx] = updatedUser;
                        localStorage.setItem('nazaha_users_db', JSON.stringify(users));
                    }

                    notify(`Successfully bought ${book.title}`);
                } else {
                    notify("Insufficient points!", "error");
                }
            };

            // --- Components ---

            const Sidebar = () => (
                <div className={`fixed inset-y-0 ${lang === 'ar' ? 'right-0' : 'left-0'} w-64 bg-gray-900 text-white transform transition-transform duration-300 ease-in-out z-30 ${sidebarOpen ? 'translate-x-0' : (lang === 'ar' ? 'translate-x-full' : '-translate-x-full')} lg:translate-x-0 lg:static lg:inset-0 flex flex-col`}>
                    <div className="h-20 flex items-center justify-center border-b border-gray-800 gap-2">
                        <Icons.GraduationCap />
                        <h1 className="text-xl font-bold">Nazaha LMS</h1>
                    </div>
                    
                    <div className="p-4 flex items-center gap-3 border-b border-gray-800">
                        <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-lg font-bold">
                            {user?.name[0].toUpperCase()}
                        </div>
                        <div>
                            <p className="font-medium text-sm">{user?.name}</p>
                            <p className="text-xs text-gray-400">{user?.faculty}</p>
                        </div>
                    </div>

                    <nav className="flex-1 p-4 space-y-2">
                        {[
                            { id: 'dashboard', icon: <Icons.LayoutDashboard />, label: t('dashboard') },
                            { id: 'library', icon: <Icons.Book />, label: t('library') },
                            { id: 'upload', icon: <Icons.Upload />, label: t('upload') },
                            { id: 'quiz', icon: <Icons.Brain />, label: t('quiz') },
                            { id: 'settings', icon: <Icons.Settings />, label: t('settings') }
                        ].map(item => (
                            <button 
                                key={item.id}
                                onClick={() => setView(item.id)}
                                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${view === item.id ? 'bg-blue-600 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'}`}
                            >
                                {item.icon}
                                <span>{item.label}</span>
                            </button>
                        ))}
                    </nav>

                    <div className="p-4 border-t border-gray-800">
                        <button onClick={handleLogout} className="w-full flex items-center gap-2 text-red-400 hover:text-red-300 transition">
                            <Icons.LogOut />
                            <span>{t('logout')}</span>
                        </button>
                    </div>
                </div>
            );

            const AuthView = () => (
                <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-gray-900 p-4" dir={dir}>
                    <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
                        <div className="p-8 text-center bg-blue-50">
                            <h1 className="text-3xl font-bold text-blue-900 mb-2">{t('title')}</h1>
                            <p className="text-gray-600">{t('tagline')}</p>
                            <div className="flex justify-center gap-2 mt-4">
                                {['ar', 'fr', 'en'].map(l => (
                                    <button key={l} onClick={() => setLang(l)} className={`px-3 py-1 rounded text-sm ${lang === l ? 'bg-blue-600 text-white' : 'bg-white border'}`}>{l.toUpperCase()}</button>
                                ))}
                            </div>
                        </div>

                        <div className="p-8">
                            <div className="flex mb-6 border-b">
                                <button onClick={() => setIsRegistering(false)} className={`flex-1 pb-3 text-center font-medium ${!isRegistering ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-400'}`}>{t('login')}</button>
                                <button onClick={() => setIsRegistering(true)} className={`flex-1 pb-3 text-center font-medium ${isRegistering ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-400'}`}>{t('signup')}</button>
                            </div>

                            {isRegistering ? (
                                <form onSubmit={handleSignup} className="space-y-4">
                                    <input required placeholder="Nom Complet" className="w-full p-3 border rounded-lg" value={signupData.name} onChange={e => setSignupData({...signupData, name: e.target.value})} />
                                    <input required type="email" placeholder="Email Univ" className="w-full p-3 border rounded-lg" value={signupData.email} onChange={e => setSignupData({...signupData, email: e.target.value})} />
                                    <input required type="password" placeholder="Password" className="w-full p-3 border rounded-lg" value={signupData.password} onChange={e => setSignupData({...signupData, password: e.target.value})} />
                                    
                                    <select className="w-full p-3 border rounded-lg" value={signupData.faculty} onChange={e => setSignupData({...signupData, faculty: e.target.value})}>
                                        <option value="">Choisir Faculté...</option>
                                        {Object.keys(UNIVERSITIES).map(f => <option key={f} value={f}>{f}</option>)}
                                    </select>
                                    
                                    <button type="submit" className="w-full bg-blue-600 text-white p-3 rounded-lg font-bold hover:bg-blue-700 transition">{t('signup')}</button>
                                </form>
                            ) : (
                                <form onSubmit={handleLogin} className="space-y-4">
                                    <input required type="email" placeholder={t('email')} className="w-full p-3 border rounded-lg" value={loginData.email} onChange={e => setLoginData({...loginData, email: e.target.value})} />
                                    <input required type="password" placeholder={t('password')} className="w-full p-3 border rounded-lg" value={loginData.password} onChange={e => setLoginData({...loginData, password: e.target.value})} />
                                    <button type="submit" className="w-full bg-blue-600 text-white p-3 rounded-lg font-bold hover:bg-blue-700 transition">{t('login')}</button>
                                </form>
                            )}
                        </div>
                    </div>
                </div>
            );

            const Dashboard = () => (
                <div className="space-y-6 animate-fade-in">
                    <header className="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-800">{t('dashboard')}</h2>
                            <p className="text-gray-500">Welcome back, student!</p>
                        </div>
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2 bg-yellow-50 px-4 py-2 rounded-full text-yellow-700 font-bold border border-yellow-200">
                                <Icons.Coins />
                                <span>{user.points} {t('points')}</span>
                            </div>
                        </div>
                    </header>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="bg-white p-6 rounded-xl shadow-sm border-r-4 border-blue-500">
                            <h3 className="text-gray-500 text-sm font-medium uppercase">My Library</h3>
                            <p className="text-3xl font-bold text-gray-800 mt-2">{user.library.length}</p>
                        </div>
                        <div className="bg-white p-6 rounded-xl shadow-sm border-r-4 border-green-500">
                            <h3 className="text-gray-500 text-sm font-medium uppercase">Uploads</h3>
                            <p className="text-3xl font-bold text-gray-800 mt-2">{user.uploads.length}</p>
                        </div>
                        <div className="bg-white p-6 rounded-xl shadow-sm border-r-4 border-purple-500">
                            <h3 className="text-gray-500 text-sm font-medium uppercase">Level</h3>
                            <p className="text-xl font-bold text-gray-800 mt-2">{user.level || "Master 1"}</p>
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-xl shadow-sm">
                        <h3 className="text-xl font-bold mb-4">Recent Books</h3>
                        {user.library.length === 0 ? (
                            <div className="text-center py-10 text-gray-500 bg-gray-50 rounded-lg border-2 border-dashed">
                                <p>You haven't bought any books yet.</p>
                                <button onClick={() => setView('library')} className="mt-2 text-blue-600 hover:underline">Go to Library</button>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                {user.library.map(book => (
                                    <div key={book.id} className="border rounded-lg p-4 hover:shadow-md transition">
                                        <div className="h-12 w-12 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center mb-3 text-xl font-bold">PDF</div>
                                        <h4 className="font-bold text-gray-800 truncate">{book.title}</h4>
                                        <button className="mt-3 w-full flex items-center justify-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-800 py-2 rounded-lg text-sm font-medium transition">
                                            <Icons.Download /> {t('download')}
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            );

            const Library = () => {
                const [filter, setFilter] = useState('');
                const filteredBooks = books.filter(b => b.title.toLowerCase().includes(filter.toLowerCase()));

                return (
                    <div className="space-y-6 animate-fade-in">
                        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                            <h2 className="text-2xl font-bold">{t('library')}</h2>
                            <div className="relative w-full md:w-64">
                                <input 
                                    type="text" 
                                    placeholder={t('search')} 
                                    className="w-full pl-10 pr-4 py-2 rounded-lg border focus:ring-2 focus:ring-blue-500 outline-none"
                                    value={filter}
                                    onChange={e => setFilter(e.target.value)}
                                />
                                <span className="absolute left-3 top-2.5 text-gray-400"><Icons.Search /></span>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            {filteredBooks.map(book => {
                                const isOwned = user.library.find(l => l.id === book.id);
                                const dynPrice = Math.floor(book.price + (book.downloads * 0.2));
                                
                                return (
                                    <div key={book.id} className="bg-white rounded-xl shadow-sm overflow-hidden border hover:shadow-lg transition duration-300 flex flex-col h-full">
                                        <div className="h-32 bg-gradient-to-r from-blue-500 to-indigo-600 p-4 flex items-end">
                                            <h3 className="text-white font-bold text-lg leading-tight">{book.title}</h3>
                                        </div>
                                        <div className="p-5 flex-1 flex flex-col">
                                            <div className="flex justify-between items-start mb-4">
                                                <span className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded font-medium">{book.category || 'General'}</span>
                                                <div className="flex items-center text-xs text-gray-500 gap-1">
                                                    <Icons.Download /> {book.downloads}
                                                </div>
                                            </div>
                                            <p className="text-sm text-gray-600 mb-4 line-clamp-2">{book.author} - {book.faculty}</p>
                                            
                                            <div className="mt-auto pt-4 border-t flex justify-between items-center">
                                                {isOwned ? (
                                                    <span className="text-green-600 font-bold flex items-center gap-1">
                                                        <Icons.CheckCircle /> {t('owned')}
                                                    </span>
                                                ) : (
                                                    <>
                                                        <span className="font-bold text-lg text-gray-800">{dynPrice} <span className="text-xs text-gray-500">XP</span></span>
                                                        <button 
                                                            onClick={() => handlePurchase(book)}
                                                            className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-blue-700 transition"
                                                        >
                                                            {t('buy')}
                                                        </button>
                                                    </>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                );
            };

            const Upload = () => {
                const [file, setFile] = useState(null);
                const [analyzing, setAnalyzing] = useState(false);
                const [result, setResult] = useState(null);
                const [title, setTitle] = useState("");

                const processFile = async () => {
                    if(!file || !title) return notify("Please select file and title", "error");
                    setAnalyzing(true);
                    const res = await analyzeFile(file);
                    setResult(res);
                    setAnalyzing(false);
                };

                const confirmUpload = () => {
                    const newBook = {
                        id: Date.now(),
                        title: title,
                        author: user.name,
                        faculty: user.faculty,
                        price: result.price,
                        downloads: 0,
                        quality: result.score,
                        category: user.specialty,
                        type: 'PDF'
                    };
                    
                    const updatedBooks = [...books, newBook];
                    setBooks(updatedBooks);
                    localStorage.setItem('nazaha_books', JSON.stringify(updatedBooks));
                    
                    const updatedUser = { ...user, points: user.points + 20, uploads: [...user.uploads, newBook] };
                    setUser(updatedUser);
                    localStorage.setItem('nazaha_user', JSON.stringify(updatedUser));
                    
                    notify("Book published successfully! +20 XP");
                    setResult(null);
                    setFile(null);
                    setTitle("");
                };

                return (
                    <div className="max-w-3xl mx-auto bg-white p-8 rounded-2xl shadow-sm animate-fade-in">
                        <div className="text-center mb-8">
                            <div className="inline-flex p-4 bg-blue-50 rounded-full text-blue-600 mb-4">
                                <Icons.Upload />
                            </div>
                            <h2 className="text-2xl font-bold text-gray-800">{t('upload')}</h2>
                            <p className="text-gray-500 mt-2">{t('upload_text')}</p>
                        </div>

                        {!result ? (
                            <div className="space-y-6">
                                <input 
                                    type="text" 
                                    placeholder="Book Title" 
                                    className="w-full p-4 border rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                                    value={title}
                                    onChange={e => setTitle(e.target.value)}
                                />
                                <div className="border-2 border-dashed border-gray-300 rounded-xl p-10 text-center hover:bg-gray-50 transition cursor-pointer relative">
                                    <input 
                                        type="file" 
                                        accept="application/pdf"
                                        className="absolute inset-0 opacity-0 cursor-pointer"
                                        onChange={e => setFile(e.target.files[0])}
                                    />
                                    <p className="text-gray-600 font-medium">{file ? file.name : "Drop PDF here or click to browse"}</p>
                                </div>
                                <button 
                                    onClick={processFile} 
                                    disabled={analyzing}
                                    className={`w-full py-4 rounded-xl font-bold text-lg text-white transition ${analyzing ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'}`}
                                >
                                    {analyzing ? "Analyzing with AI..." : "Analyze & Evaluate"}
                                </button>
                            </div>
                        ) : (
                            <div className="animate-fade-in">
                                <div className={`p-6 rounded-xl mb-6 border ${result.isAcademic ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                                    <h3 className={`font-bold text-lg mb-2 ${result.isAcademic ? 'text-green-800' : 'text-red-800'}`}>
                                        {result.isAcademic ? "✅ Academic Content Approved" : "❌ Low Quality Content"}
                                    </h3>
                                    <div className="flex gap-4 mt-4">
                                        <div className="bg-white px-4 py-2 rounded shadow-sm">
                                            <span className="text-gray-500 text-xs uppercase block">Quality Score</span>
                                            <span className="font-bold text-xl">{result.score}%</span>
                                        </div>
                                        <div className="bg-white px-4 py-2 rounded shadow-sm">
                                            <span className="text-gray-500 text-xs uppercase block">Market Price</span>
                                            <span className="font-bold text-xl text-blue-600">{result.price} XP</span>
                                        </div>
                                    </div>
                                </div>
                                
                                {result.isAcademic && (
                                    <button onClick={confirmUpload} className="w-full bg-green-600 text-white py-3 rounded-xl font-bold hover:bg-green-700 shadow-lg hover:shadow-xl transition">
                                        Publish to Library (+20 XP)
                                    </button>
                                )}
                                <button onClick={() => setResult(null)} className="w-full mt-3 text-gray-500 hover:text-gray-700">Cancel</button>
                            </div>
                        )}
                    </div>
                );
            };

            const Quiz = () => {
                const [question, setQuestion] = useState(null);
                
                const generateQ = () => {
                    if(user.library.length === 0) return notify("Buy books first", "error");
                    const randomBook = user.library[Math.floor(Math.random() * user.library.length)];
                    
                    // Simulate Question Generation
                    setTimeout(() => {
                        setQuestion({
                            text: `In the context of ${randomBook.title}, what is the primary methodology discussed in Chapter 1?`,
                            options: ["Quantitative Analysis", "Qualitative Survey", "Mixed Methods", "Case Study"],
                            correct: 0
                        });
                    }, 1500);
                };

                return (
                    <div className="max-w-2xl mx-auto">
                        <h2 className="text-2xl font-bold mb-6">{t('quiz')}</h2>
                        
                        {!question ? (
                            <div className="bg-white p-10 rounded-2xl text-center shadow-sm">
                                <div className="w-20 h-20 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
                                    <Icons.Brain />
                                </div>
                                <h3 className="text-xl font-bold mb-2">Ready to test your knowledge?</h3>
                                <p className="text-gray-500 mb-6">AI will generate questions based on the books you own.</p>
                                <button onClick={generateQ} className="bg-purple-600 text-white px-8 py-3 rounded-full font-bold hover:bg-purple-700 transition">
                                    Generate Quiz
                                </button>
                            </div>
                        ) : (
                            <div className="bg-white p-8 rounded-2xl shadow-lg animate-fade-in border-t-4 border-purple-500">
                                <span className="text-xs font-bold text-purple-600 uppercase tracking-wider">AI Generated Question</span>
                                <h3 className="text-xl font-bold mt-2 mb-6">{question.text}</h3>
                                <div className="space-y-3">
                                    {question.options.map((opt, i) => (
                                        <button 
                                            key={i} 
                                            onClick={() => {
                                                if(i === question.correct) {
                                                    notify("Correct! +10 XP");
                                                    const u = {...user, points: user.points + 10};
                                                    setUser(u);
                                                    localStorage.setItem('nazaha_user', JSON.stringify(u));
                                                    setQuestion(null);
                                                } else {
                                                    notify("Wrong answer", "error");
                                                }
                                            }}
                                            className="w-full text-left p-4 rounded-xl border hover:border-purple-500 hover:bg-purple-50 transition"
                                        >
                                            {opt}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                );
            };

            // --- Main Render ---
            if (!user) return <AuthView />;

            return (
                <div className={`flex min-h-screen bg-gray-50 ${dir}`} dir={dir}>
                    {/* Mobile Menu Button */}
                    <button 
                        className="fixed top-4 right-4 z-50 lg:hidden bg-white p-2 rounded shadow"
                        onClick={() => setSidebarOpen(!sidebarOpen)}
                    >
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
                    </button>

                    <Sidebar />

                    <main className="flex-1 p-4 lg:p-8 overflow-y-auto h-screen">
                        {notification && (
                            <div className={`fixed top-4 left-1/2 transform -translate-x-1/2 px-6 py-3 rounded-full shadow-lg z-50 text-white font-bold animate-fade-in ${notification.type === 'error' ? 'bg-red-500' : 'bg-green-600'}`}>
                                {notification.msg}
                            </div>
                        )}
                        
                        {view === 'dashboard' && <Dashboard />}
                        {view === 'library' && <Library />}
                        {view === 'upload' && <Upload />}
                        {view === 'quiz' && <Quiz />}
                        {view === 'settings' && (
                            <div className="max-w-md bg-white p-6 rounded-xl shadow-sm">
                                <h2 className="text-xl font-bold mb-4">{t('settings')}</h2>
                                <div className="space-y-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Language</label>
                                        <div className="flex gap-2">
                                            {['ar', 'fr', 'en'].map(l => (
                                                <button key={l} onClick={() => setLang(l)} className={`px-4 py-2 rounded-lg border ${lang === l ? 'bg-blue-600 text-white border-blue-600' : 'hover:bg-gray-50'}`}>{l.toUpperCase()}</button>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </main>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>

