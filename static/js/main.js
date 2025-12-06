/**
 * SIA-R Dashboard - Main JavaScript
 * Shared utilities and functions
 */

// ============================================================================
// Authentication Utilities
// ============================================================================

/**
 * Get auth token from localStorage
 */
function getToken() {
    return localStorage.getItem('auth_token') || '';
}

/**
 * Store auth token
 */
function setToken(token) {
    localStorage.setItem('auth_token', token);
}

/**
 * Clear auth token
 */
function clearToken() {
    localStorage.removeItem('auth_token');
}

/**
 * Check if user is authenticated
 */
function isAuthenticated() {
    return !!getToken();
}

/**
 * Redirect to login if not authenticated
 */
function redirectIfNotAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/login';
    }
}

// ============================================================================
// API Call Helpers
// ============================================================================

/**
 * Make authenticated API call
 */
async function apiCall(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken()
        }
    };

    const finalOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {})
        }
    };

    try {
        const response = await fetch(endpoint, finalOptions);
        
        if (response.status === 401) {
            clearToken();
            window.location.href = '/login';
            return null;
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

/**
 * Make GET request
 */
async function apiGet(endpoint) {
    return apiCall(endpoint, { method: 'GET' });
}

/**
 * Make POST request
 */
async function apiPost(endpoint, data) {
    return apiCall(endpoint, {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

/**
 * Make PUT request
 */
async function apiPut(endpoint, data) {
    return apiCall(endpoint, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
}

/**
 * Make DELETE request
 */
async function apiDelete(endpoint) {
    return apiCall(endpoint, { method: 'DELETE' });
}

// ============================================================================
// UI Utilities
// ============================================================================

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive">
            <div class="toast-header bg-${type}">
                <strong class="me-auto">${type.toUpperCase()}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    // Add toast to body
    const container = document.getElementById('toast-container') || createToastContainer();
    container.insertAdjacentHTML('beforeend', toastHtml);
    
    // Show toast
    const toastEl = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
    
    // Remove after it hides
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

/**
 * Create toast container if it doesn't exist
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

/**
 * Show success message
 */
function showSuccess(message) {
    showToast(message, 'success');
}

/**
 * Show error message
 */
function showError(message) {
    showToast(message, 'danger');
}

/**
 * Show warning message
 */
function showWarning(message) {
    showToast(message, 'warning');
}

/**
 * Show info message
 */
function showInfo(message) {
    showToast(message, 'info');
}

/**
 * Show confirmation dialog
 */
async function showConfirm(message) {
    return confirm(message);
}

/**
 * Format date
 */
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toLocaleDateString();
}

/**
 * Format datetime
 */
function formatDateTime(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toLocaleString();
}

/**
 * Format time difference
 */
function formatTimeAgo(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    const seconds = Math.floor((new Date() - date) / 1000);
    let interval = seconds / 31536000;

    if (interval > 1) return Math.floor(interval) + " años atrás";
    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + " meses atrás";
    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + " días atrás";
    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + " horas atrás";
    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + " minutos atrás";
    return Math.floor(seconds) + " segundos atrás";
}

// ============================================================================
// Data Formatting Utilities
// ============================================================================

/**
 * Get badge color based on status
 */
function getStatusBadge(status) {
    const statusMap = {
        'success': 'success',
        'completed': 'success',
        'failed': 'danger',
        'error': 'danger',
        'pending': 'warning',
        'processing': 'info',
        'draft': 'secondary',
        'published': 'success',
        'unpublished': 'secondary'
    };
    return statusMap[status] || 'secondary';
}

/**
 * Get badge color based on quality score
 */
function getQualityBadge(score) {
    if (score >= 0.85) return 'success';
    if (score >= 0.70) return 'info';
    if (score >= 0.50) return 'warning';
    return 'danger';
}

/**
 * Get badge color based on risk score
 */
function getRiskBadge(score) {
    if (score <= 0.25) return 'success';
    if (score <= 0.50) return 'info';
    if (score <= 0.75) return 'warning';
    return 'danger';
}

/**
 * Format percentage
 */
function formatPercent(value) {
    return (value * 100).toFixed(1) + '%';
}

/**
 * Format number with thousands separator
 */
function formatNumber(num) {
    return new Intl.NumberFormat('es-ES').format(num);
}

// ============================================================================
// Dark Mode Management
// ============================================================================

/**
 * Initialize dark mode
 */
function initDarkMode() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    const theme = savedTheme || (prefersDark ? 'dark' : 'light');
    setTheme(theme);
}

/**
 * Set theme
 */
function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('theme', theme);
    
    // Update theme icon
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        if (theme === 'dark') {
            themeIcon.className = 'bi bi-sun-fill';
        } else {
            themeIcon.className = 'bi bi-moon-stars';
        }
    }
}

/**
 * Toggle dark mode
 */
function toggleDarkMode() {
    const current = document.documentElement.getAttribute('data-bs-theme') || 'light';
    const newTheme = current === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

// ============================================================================
// Data Validation
// ============================================================================

/**
 * Validate email
 */
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Validate URL
 */
function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

/**
 * Validate password strength
 */
function getPasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z\d]/.test(password)) strength++;
    
    return strength;
}

// ============================================================================
// Loading State Management
// ============================================================================

/**
 * Disable button with loading state
 */
function disableButton(btnSelector, loadingText = 'Cargando...') {
    const btn = document.querySelector(btnSelector);
    if (!btn) return;
    
    btn.disabled = true;
    btn.dataset.originalText = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>' + loadingText;
}

/**
 * Enable button and restore original text
 */
function enableButton(btnSelector) {
    const btn = document.querySelector(btnSelector);
    if (!btn) return;
    
    btn.disabled = false;
    btn.innerHTML = btn.dataset.originalText || 'Enviar';
}

// ============================================================================
// Table Utilities
// ============================================================================

/**
 * Create table row
 */
function createTableRow(data, columns) {
    const row = document.createElement('tr');
    columns.forEach(col => {
        const cell = document.createElement('td');
        cell.textContent = data[col] || '-';
        row.appendChild(cell);
    });
    return row;
}

/**
 * Sort table by column
 */
function sortTable(tableId, columnIndex) {
    const table = document.getElementById(tableId);
    let rows = Array.from(table.querySelectorAll('tbody tr'));
    let isAscending = table.dataset.sortAsc !== 'true';
    
    rows.sort((a, b) => {
        const aValue = a.children[columnIndex].textContent;
        const bValue = b.children[columnIndex].textContent;
        
        if (!isNaN(aValue) && !isNaN(bValue)) {
            return isAscending ? aValue - bValue : bValue - aValue;
        }
        
        return isAscending ? 
            aValue.localeCompare(bValue) : 
            bValue.localeCompare(aValue);
    });
    
    table.dataset.sortAsc = isAscending;
    rows.forEach(row => table.querySelector('tbody').appendChild(row));
}

// ============================================================================
// Pagination Utilities
// ============================================================================

/**
 * Create pagination
 */
function createPagination(currentPage, totalPages, onPageChange) {
    const paginationEl = document.getElementById('pagination');
    if (!paginationEl) return;
    
    paginationEl.innerHTML = '';
    
    // Previous button
    const prevLi = document.createElement('li');
    prevLi.className = 'page-item' + (currentPage === 1 ? ' disabled' : '');
    prevLi.innerHTML = `
        <a class="page-link" href="#" onclick="${'currentPage > 1 ? onPageChange(' + (currentPage - 1) + ') : null'}; return false;">
            Anterior
        </a>
    `;
    paginationEl.appendChild(prevLi);
    
    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
            const li = document.createElement('li');
            li.className = 'page-item' + (i === currentPage ? ' active' : '');
            li.innerHTML = `<a class="page-link" href="#" onclick="onPageChange(${i}); return false;">${i}</a>`;
            paginationEl.appendChild(li);
        }
    }
    
    // Next button
    const nextLi = document.createElement('li');
    nextLi.className = 'page-item' + (currentPage === totalPages ? ' disabled' : '');
    nextLi.innerHTML = `
        <a class="page-link" href="#" onclick="${'currentPage < totalPages ? onPageChange(' + (currentPage + 1) + ') : null'}; return false;">
            Siguiente
        </a>
    `;
    paginationEl.appendChild(nextLi);
}

// ============================================================================
// Export Utilities
// ============================================================================

/**
 * Export data to CSV
 */
function exportToCSV(filename, data) {
    const csv = convertToCSV(data);
    const link = document.createElement('a');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv));
    link.setAttribute('download', filename);
    link.click();
}

/**
 * Convert array of objects to CSV
 */
function convertToCSV(data) {
    if (!data || data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const csv = [headers.join(',')];
    
    data.forEach(row => {
        const values = headers.map(header => {
            const value = row[header];
            // Escape quotes and wrap in quotes if contains comma
            if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                return '"' + value.replace(/"/g, '""') + '"';
            }
            return value;
        });
        csv.push(values.join(','));
    });
    
    return csv.join('\n');
}

/**
 * Export data to JSON
 */
function exportToJSON(filename, data) {
    const json = JSON.stringify(data, null, 2);
    const link = document.createElement('a');
    link.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(json));
    link.setAttribute('download', filename);
    link.click();
}

// ============================================================================
// Initialization
// ============================================================================

/**
 * Load trends from backend and render grid
 */
async function loadTrends() {
    try {
        const resp = await fetch('/api/ui/trends', { headers: { 'Authorization': 'Bearer ' + getToken() } });
        const data = await resp.json();

        const container = document.getElementById('trends-grid');
        if (!container) return;

        container.innerHTML = '';

        if (!data || !data.trends || data.trends.length === 0) {
            container.innerHTML = '<div class="text-center text-muted w-100 py-4">No se encontraron tendencias</div>';
            return;
        }

        data.trends.forEach(tr => {
            const card = document.createElement('div');
            card.className = 'trend-card';

            // create inner structure
            const inner = document.createElement('div');
            inner.className = 'trend-card-inner';

            const header = document.createElement('div');
            header.className = 'trend-header';
            header.innerHTML = `<h6 class="mb-1">${escapeHtml(tr.title)}</h6><small class="text-muted">${tr.source} · ${tr.category}</small>`;

            const summary = document.createElement('p');
            summary.className = 'trend-summary text-truncate';
            summary.textContent = tr.summary || '';

            const meta = document.createElement('div');
            meta.className = 'trend-meta d-flex justify-content-between align-items-center';

            const scoreDiv = document.createElement('div');
            scoreDiv.innerHTML = `<span class="badge bg-primary">Score ${tr.score}</span>`;

            const actionDiv = document.createElement('div');
            const btn = document.createElement('button');
            btn.className = 'btn btn-sm btn-outline-success';
            btn.textContent = 'Seleccionar';
            // attach full trend payload to onclick using encodeURIComponent to be safe
            // Attach click handler safely with closure to avoid string-escaping issues
            btn.addEventListener('click', function () {
                selectTrendJson(JSON.stringify(tr));
            });

            actionDiv.appendChild(btn);
            meta.appendChild(scoreDiv);
            meta.appendChild(actionDiv);

            inner.appendChild(header);
            inner.appendChild(summary);
            inner.appendChild(meta);
            card.appendChild(inner);

            container.appendChild(card);
        });

    } catch (err) {
        console.error('Error loading trends', err);
        showToast('No se pudieron cargar las tendencias', 'danger');
    }
}

/**
 * Select a trend (placeholder action)
 */
/**
 * Select trend from JSON payload (string) - save and redirect to pipeline
 */
function selectTrendJson(jsonPayload) {
    try {
        const trend = typeof jsonPayload === 'string' ? JSON.parse(jsonPayload) : jsonPayload;
        // Save to localStorage for pipeline prefill
        localStorage.setItem('selected_trend', JSON.stringify(trend));
        showToast(`Tendencia seleccionada: ${trend.title}`, 'success');
        // Small delay to allow the toast to render, then navigate to pipeline page
        console.log('Selected trend saved, redirecting to /pipeline/run');
        setTimeout(function() {
            try {
                window.location.assign('/pipeline/run');
            } catch (err) {
                // Fallback
                window.location.href = '/pipeline/run';
            }
        }, 200);
    } catch (err) {
        console.error('Error selecting trend', err);
        showToast('No se pudo seleccionar la tendencia', 'danger');
    }
}

/**
 * Escapes HTML to avoid injection in inserted strings
 */
function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe.replace(/[&<>"']/g, function(m) {
        return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#039;"})[m];
    });
}

function escapeJs(s) {
    if (!s) return '';
    return s.replace(/'/g, "\\'").replace(/"/g, '\\"');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dark mode
    initDarkMode();
    
    // Redirect if not authenticated (except on login page)
    if (!window.location.pathname.includes('/login')) {
        redirectIfNotAuth();
    }
    
    // Initialize Bootstrap tooltips and popovers
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// ============================================================================
// Error Handling
// ============================================================================

/**
 * Handle API errors
 */
function handleApiError(error, defaultMessage = 'Ocurrió un error') {
    console.error('Error:', error);
    
    if (error.response) {
        const message = error.response.data?.error || error.response.data?.message || defaultMessage;
        showError(message);
    } else if (error.message) {
        showError(error.message);
    } else {
        showError(defaultMessage);
    }
}

/**
 * Global error handler
 */
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    showError('Ocurrió un error inesperado');
});

/**
 * Global unhandled promise rejection handler
 */
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showError('Ocurrió un error inesperado');
});
