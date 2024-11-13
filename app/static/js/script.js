document.addEventListener('DOMContentLoaded', function () {

    const darkModeToggle = document.getElementById('darkModeToggle');
    const html = document.documentElement;

    function setDarkMode(isDark) {
        if (isDark) {
            html.classList.add('dark');
            sessionStorage.setItem('darkMode', 'true');
        } else {
            html.classList.remove('dark');
            sessionStorage.setItem('darkMode', 'false');
        }
    }

    const savedDarkMode = sessionStorage.getItem('darkMode');
    if (savedDarkMode === 'true') {
        setDarkMode(true);
    } else if (savedDarkMode === 'false') {
        setDarkMode(false);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        if (window.Telegram.WebApp.colorScheme == 'dark') {
            setDarkMode(true);
        } else {
            setDarkMode(false);
        }
    }

    darkModeToggle.addEventListener('click', function() {
        const isDark = html.classList.contains('dark');
        setDarkMode(!isDark);
    });

    const searchToggle = document.getElementById('searchToggle');
    const headerTitle = document.getElementById('headerTitle');
    const searchInput = document.getElementById('searchInput');

    if (searchToggle && headerTitle && searchInput) {
        let isSearchVisible = false;
        searchToggle.addEventListener('click', toggleSearch);
        document.addEventListener('click', handleDocumentClick);

        function toggleSearch(event) {
            event.stopPropagation();
            isSearchVisible = !isSearchVisible;
            if (isSearchVisible) {
                headerTitle.classList.add('hidden');
                searchInput.classList.remove('hidden');
                searchInput.classList.remove('opacity-0', 'scale-95');
                searchInput.focus();
            } else {
                hideSearch();
            }
        }

        function hideSearch() {
            headerTitle.classList.remove('hidden');
            searchInput.classList.add('hidden', 'opacity-0', 'scale-95');
            isSearchVisible = false;
        }

        function handleDocumentClick(event) {
            if (isSearchVisible && event.target !== searchToggle && event.target !== searchInput) {
                hideSearch();
            }
        }
    }

    const saveNewsBtn = document.getElementById('saveNewsBtn');
    const saveIcon = document.getElementById('saveIcon');
    const saveText = document.getElementById('saveText');
    const newsId = document.getElementById('newsId')?.value;

    if (saveNewsBtn && newsId) {
        checkSaveStatus();

        saveNewsBtn.addEventListener('click', function() {
            if (!window.Telegram.WebApp.initDataUnsafe.user) {
                alert('لطفاً از طریق ربات تلگرام وارد شوید.');
                return;
            }
            
            fetch('/api/toggle_save_news', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    news_id: newsId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateSaveButtonUI(data.is_saved);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    function checkSaveStatus() {
        if (!window.Telegram.WebApp.initDataUnsafe.user) {
            return;
        }

        const userId = window.Telegram.WebApp.initDataUnsafe.user.id;
        
        fetch(`/api/check_save_status?news_id=${newsId}`)
        .then(response => response.json())
        .then(data => {
            updateSaveButtonUI(data.is_saved);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function updateSaveButtonUI(isSaved) {
        if (isSaved) {
            saveIcon.setAttribute('fill', 'currentColor');
            saveText.textContent = 'ذخیره شده';
        } else {
            saveIcon.setAttribute('fill', 'none');
            saveText.textContent = 'ذخیره';
        }
    }

    async function shareViaTelegram(event) {
    event.preventDefault();
    event.stopPropagation();

    if (!window.Telegram || !window.Telegram.WebApp || !window.Telegram.WebApp.initDataUnsafe.user) {
        alert('لطفاً از طریق ربات تلگرام وارد شوید.');
        return;
    }

    try {
        const newsId = document.getElementById('newsId')?.value;
        if (!newsId) {
            console.error('News ID not found');
            return;
        }

        const newsResponse = await fetch(`/api/news/${newsId}`);
        if (!newsResponse.ok) {
            throw new Error(`HTTP error! status: ${newsResponse.status}`);
        }
        const newsData = await newsResponse.json();

        const botResponse = await fetch('/api/bot_username');
        if (!botResponse.ok) {
            throw new Error(`HTTP error! status: ${botResponse.status}`);
        }
        const botData = await botResponse.json();
        const botUsername = botData.bot_username;

        if (!botUsername) {
            console.error('Bot username not found');
            return;
        }

        let shareText = `📰 ${newsData.title}\n\n`;
        shareText += `🔗 برای مطالعه کامل خبر، کلیک کنید:\n`;
        shareText += `https://t.me/${botUsername}?start=news_${newsId}`;

        const shareUrl = `https://t.me/share/url?text=${encodeURIComponent(shareText)}`;

        console.log('Share URL:', shareUrl);

        window.Telegram.WebApp.openTelegramLink(shareUrl);

    } catch (error) {
        console.error('Error sharing via Telegram:', error);
    }
}

    const shareButtons = document.querySelectorAll('#shareButton, #shareButtonBottom');
    shareButtons.forEach(button => {
        if (button) {
            button.addEventListener('click', shareViaTelegram);
        }
    });

    if (window.Telegram && window.Telegram.WebApp) {
                var userId = window.Telegram.WebApp.initDataUnsafe.user.id;
                fetch("/api/set_telegram_user_id", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({user_id: userId}),
                })
                .then(response => response.json())
    }
    
});