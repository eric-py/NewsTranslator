document.addEventListener('DOMContentLoaded', function() {
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

    function updateDarkModeIcon(isDark) {
        const darkModeToggle = document.getElementById('darkModeToggle');
        if (darkModeToggle) {
            const moonIcon = darkModeToggle.querySelector('.moon-icon');
            const sunIcon = darkModeToggle.querySelector('.sun-icon');
            
            if (isDark) {
                moonIcon.classList.add('hidden');
                sunIcon.classList.remove('hidden');
                darkModeText.textContent = 'حالت روز';
            } else {
                moonIcon.classList.remove('hidden');
                sunIcon.classList.add('hidden');
                darkModeText.textContent = 'حالت شب';
            }
        }
    }

    function toggleDarkMode() {
        const isDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
        updateDarkModeIcon(isDark);
    }

    // تنظیم وضعیت اولیه حالت شب و آیکون
    const isDarkModeEnabled = localStorage.getItem('darkMode') === 'enabled';
    if (isDarkModeEnabled) {
        document.documentElement.classList.add('dark');
    }
    updateDarkModeIcon(isDarkModeEnabled);

    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleDarkMode);
    }

    const saveButton = document.getElementById('saveButton');
    if (saveButton) {
        const saveButtonText = saveButton.querySelector('span');
        const saveButtonIcon = saveButton.querySelector('svg');

        saveButton.addEventListener('click', function() {
            const isSaved = saveButton.getAttribute('data-saved') === 'true';

            if (isSaved) {
                saveButtonText.textContent = 'ذخیره';
                saveButtonIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />';
                saveButtonIcon.setAttribute('fill', 'none');
                saveButtonIcon.setAttribute('stroke', 'currentColor');
                saveButton.setAttribute('data-saved', 'false');
            } else {
                saveButtonText.textContent = 'ذخیره شده';
                saveButtonIcon.innerHTML = '<path fill-rule="evenodd" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />';
                saveButtonIcon.setAttribute('fill', 'currentColor');
                saveButtonIcon.setAttribute('stroke', 'none');
                saveButton.setAttribute('data-saved', 'true');
            }
        });
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

    console.log('All scripts loaded successfully');

    if (window.Telegram && window.Telegram.WebApp) {
        const colorScheme = window.Telegram.WebApp.colorScheme;
        const html = document.documentElement;
        if (colorScheme === 'dark') {
            html.classList.add('dark');
        } else {
            html.classList.remove('dark');
        }
        updateDarkModeIcon(colorScheme === 'dark');
    }
});