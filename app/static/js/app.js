// Content Creator Pro - Main JavaScript

// Global variables
let currentUser = null;
let apiBaseUrl = '/api';

// Initialize application
$(document).ready(function() {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    // Check if user is logged in
    checkAuthStatus();
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

function setupEventListeners() {
    // Logout button
    $('#logout-btn').on('click', function(e) {
        e.preventDefault();
        logout();
    });
    
    // Global error handling
    $(document).ajaxError(function(event, xhr, settings, error) {
        handleAjaxError(xhr, error);
    });
    
    // Form submissions
    $('form').on('submit', function(e) {
        const form = $(this);
        if (form.hasClass('needs-validation')) {
            if (!form[0].checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.addClass('was-validated');
        }
    });
}

// Authentication functions
function checkAuthStatus() {
    const token = localStorage.getItem('auth_token');
    if (token) {
        // Validate token with server
        $.ajax({
            url: '/auth/profile',
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            success: function(response) {
                if (response.success) {
                    currentUser = response.data;
                    updateUIForLoggedInUser();
                } else {
                    logout();
                }
            },
            error: function() {
                logout();
            }
        });
    } else {
        updateUIForLoggedOutUser();
    }
}

function login(email, password) {
    return $.ajax({
        url: '/auth/login',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            email: email,
            password: password
        }),
        success: function(response) {
            if (response.success) {
                localStorage.setItem('auth_token', response.data.token);
                currentUser = response.data.user;
                updateUIForLoggedInUser();
                showSuccessMessage('Login successful!');
                return response;
            } else {
                showErrorMessage(response.error || 'Login failed');
                throw new Error(response.error);
            }
        },
        error: function(xhr) {
            const error = xhr.responseJSON?.error || 'Login failed';
            showErrorMessage(error);
            throw new Error(error);
        }
    });
}

function register(email, name, password) {
    return $.ajax({
        url: '/auth/register',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            email: email,
            name: name,
            password: password
        }),
        success: function(response) {
            if (response.success) {
                localStorage.setItem('auth_token', response.data.token);
                currentUser = response.data.user;
                updateUIForLoggedInUser();
                showSuccessMessage('Registration successful!');
                return response;
            } else {
                showErrorMessage(response.error || 'Registration failed');
                throw new Error(response.error);
            }
        },
        error: function(xhr) {
            const error = xhr.responseJSON?.error || 'Registration failed';
            showErrorMessage(error);
            throw new Error(error);
        }
    });
}

function logout() {
    localStorage.removeItem('auth_token');
    currentUser = null;
    updateUIForLoggedOutUser();
    showInfoMessage('Logged out successfully');
    
    // Redirect to home page if not already there
    if (window.location.pathname !== '/') {
        window.location.href = '/';
    }
}

function updateUIForLoggedInUser() {
    if (currentUser) {
        $('.user-name').text(currentUser.name || currentUser.email);
        $('.auth-required').show();
        $('.auth-not-required').hide();
    }
}

function updateUIForLoggedOutUser() {
    $('.auth-required').hide();
    $('.auth-not-required').show();
}

// API utility functions
function apiRequest(url, method = 'GET', data = null, options = {}) {
    const token = localStorage.getItem('auth_token');
    const defaultOptions = {
        url: `${apiBaseUrl}${url}`,
        method: method,
        contentType: 'application/json',
        headers: {}
    };
    
    if (token) {
        defaultOptions.headers['Authorization'] = `Bearer ${token}`;
    }
    
    if (data) {
        defaultOptions.data = JSON.stringify(data);
    }
    
    const requestOptions = $.extend(true, defaultOptions, options);
    
    return $.ajax(requestOptions);
}

// Error handling
function handleAjaxError(xhr, error) {
    let errorMessage = 'An error occurred';
    
    if (xhr.status === 401) {
        errorMessage = 'Please log in to continue';
        logout();
    } else if (xhr.status === 403) {
        errorMessage = 'You do not have permission to perform this action';
    } else if (xhr.status === 404) {
        errorMessage = 'The requested resource was not found';
    } else if (xhr.status === 500) {
        errorMessage = 'Server error occurred';
    } else if (xhr.responseJSON && xhr.responseJSON.error) {
        errorMessage = xhr.responseJSON.error;
    } else if (error) {
        errorMessage = error;
    }
    
    showErrorMessage(errorMessage);
}

// Message display functions
function showSuccessMessage(message, duration = 5000) {
    showMessage(message, 'success', duration);
}

function showErrorMessage(message, duration = 5000) {
    showMessage(message, 'danger', duration);
}

function showInfoMessage(message, duration = 5000) {
    showMessage(message, 'info', duration);
}

function showWarningMessage(message, duration = 5000) {
    showMessage(message, 'warning', duration);
}

function showMessage(message, type = 'info', duration = 5000) {
    // Remove existing messages
    $('.alert-message').remove();
    
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show alert-message" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Add message to page
    $('body').prepend(alertHtml);
    
    // Auto-remove after duration
    if (duration > 0) {
        setTimeout(function() {
            $('.alert-message').fadeOut(function() {
                $(this).remove();
            });
        }, duration);
    }
    
    // Scroll to top if message is not visible
    const alert = $('.alert-message');
    if (alert.length && !isElementInViewport(alert[0])) {
        $('html, body').animate({
            scrollTop: alert.offset().top - 20
        }, 300);
    }
}

// Utility functions
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Loading states
function showLoading(element, text = 'Loading...') {
    const $element = $(element);
    $element.prop('disabled', true);
    $element.addClass('loading');
    
    const originalText = $element.text();
    $element.data('original-text', originalText);
    $element.html(`<i class="fas fa-spinner fa-spin me-1"></i>${text}`);
}

function hideLoading(element) {
    const $element = $(element);
    $element.prop('disabled', false);
    $element.removeClass('loading');
    
    const originalText = $element.data('original-text');
    if (originalText) {
        $element.text(originalText);
    }
}

// Form validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/;
    return re.test(password);
}

// Local storage utilities
function setLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
        console.error('Error saving to localStorage:', e);
    }
}

function getLocalStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (e) {
        console.error('Error reading from localStorage:', e);
        return defaultValue;
    }
}

function removeLocalStorage(key) {
    try {
        localStorage.removeItem(key);
    } catch (e) {
        console.error('Error removing from localStorage:', e);
    }
}

// Export functions for use in other modules
window.ContentCreatorApp = {
    login,
    register,
    logout,
    apiRequest,
    showSuccessMessage,
    showErrorMessage,
    showInfoMessage,
    showWarningMessage,
    showLoading,
    hideLoading,
    validateEmail,
    validatePassword,
    formatDate,
    formatFileSize,
    debounce,
    throttle,
    setLocalStorage,
    getLocalStorage,
    removeLocalStorage
}; 