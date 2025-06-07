// Форматирование чисел в денежный формат
function formatMoney(amount) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB'
    }).format(amount);
}

// Форматирование даты
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(date);
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Форматирование всех сумм на странице
    document.querySelectorAll('.badge').forEach(badge => {
        const amount = parseFloat(badge.textContent);
        if (!isNaN(amount)) {
            badge.textContent = formatMoney(amount);
        }
    });

    // Форматирование всех дат на странице
    document.querySelectorAll('.text-muted').forEach(element => {
        if (element.textContent.match(/^\d{4}-\d{2}-\d{2}$/)) {
            element.textContent = formatDate(element.textContent);
        }
    });
}); 