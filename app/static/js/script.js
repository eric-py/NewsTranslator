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

            const userId = window.Telegram.WebApp.initDataUnsafe.user.id;
            
            fetch('/toggle_save_news', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    user_id: userId,
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
        
        fetch(`/check_save_status?user_id=${userId}&news_id=${newsId}`)
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

    function shareContent(event) {
        event.preventDefault();
        event.stopPropagation();
        if (navigator.share) {
            navigator.share({
                title: 'عنوان خبر',
                text: 'متن خلاصه خبر برای اشتراک‌گذاری',
                url: window.location.href
            }).then(() => {
                console.log('موفقیت در اشتراک‌گذاری');
            }).catch((error) => {
                console.log('خطا در اشتراک‌گذاری:', error);
            });
        } else {
            alert('متاسفانه مرورگر شما از قابلیت اشتراک‌گذاری پشتیبانی نمی‌کند.');
        }
    }

    const shareButtons = document.querySelectorAll('#shareButton, #shareButtonBottom');
    shareButtons.forEach(button => {
        if (button) {
            button.addEventListener('click', shareContent);
        }
    });
});