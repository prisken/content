// Content Creator Pro - Main JavaScript

// Global variables
let currentUser = null;
let apiBaseUrl = '/api';
let currentLanguage = 'en';

// Translation dictionary
const translations = {
    en: {
        // Navigation
        'dashboard': 'Dashboard',
        'generator': 'Generator',
        'library': 'Library',
        'settings': 'Settings',
        'account': 'Account',
        'logout': 'Logout',
        'english': 'English',
        'chinese': '中文',
        
        // Common
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        'cancel': 'Cancel',
        'save': 'Save',
        'edit': 'Edit',
        'delete': 'Delete',
        'close': 'Close',
        'submit': 'Submit',
        'back': 'Back',
        'next': 'Next',
        'previous': 'Previous',
        'continue': 'Continue',
        'finish': 'Finish',
        
        // Home page
        'hero_title': 'Create Engaging Content with',
        'hero_subtitle': 'AI Power',
        'hero_description': 'Generate professional social media posts, blog articles, and more with our AI-powered platform. Choose from 18 content directions and create content that resonates with your audience.',
        'start_creating': 'Start Creating',
        'learn_more': 'Learn More',
        'quick_start': 'Quick Start',
        'quick_start_desc': 'Get started in minutes with our intuitive content generator',
        'content_directions': '18 Content Directions',
        'platforms': '6 Platforms',
        'ai_powered': 'AI-Powered',
        'regional_adaptation': 'Regional Adaptation',
        'why_choose': 'Why Choose Content Creator Pro?',
        'why_choose_desc': 'Everything you need to create engaging content',
        'ai_generation': 'AI-Powered Generation',
        'ai_generation_desc': 'Advanced AI models create high-quality, engaging content tailored to your needs.',
        'regional_adaptation_title': 'Regional Adaptation',
        'regional_adaptation_desc': 'Content automatically adapts to your region with cultural sensitivity and local relevance.',
        'multi_platform': 'Multi-Platform Support',
        'multi_platform_desc': 'Create content for LinkedIn, Facebook, Instagram, Twitter, YouTube, and blogs.',
        'content_directions_title': 'Content Directions',
        'content_directions_desc': 'Choose from 18 specialized content directions',
        'business_finance': 'Business & Finance',
        'technology': 'Technology',
        'health_wellness': 'Health & Wellness',
        'education': 'Education',
        'entertainment': 'Entertainment',
        'travel_tourism': 'Travel & Tourism',
        'food_cooking': 'Food & Cooking',
        'fashion_beauty': 'Fashion & Beauty',
        'view_all_directions': 'View All Directions',
        'ready_to_create': 'Ready to Create Amazing Content?',
        'ready_to_create_desc': 'Join thousands of creators who are already using Content Creator Pro to generate engaging content.',
        'get_started_now': 'Get Started Now',
        
        // Generator page
        'content_generator': 'Content Generator',
        'step_1': 'Step 1',
        'step_2': 'Step 2',
        'step_3': 'Step 3',
        'step_4': 'Step 4',
        'step_5': 'Step 5',
        'step_3_5': 'Step 3.5',
        'choose_direction': 'Choose Your Content Direction',
        'choose_direction_desc': 'Select the primary focus for your content',
        'choose_platform': 'Choose Your Platform',
        'choose_platform_desc': 'Select where you\'ll share your content',
        'what_inspires': 'What Inspires You?',
        'what_inspires_desc': 'Tell us what\'s driving your content creation',
        'select_topics': 'Select Topics',
        'select_topics_desc': 'Choose specific topics based on your focus and sources',
        'generate_content': 'Generate Content',
        'generate_content_desc': 'Create your content with AI',
        'linkedin': 'LinkedIn',
        'facebook': 'Facebook',
        'instagram': 'Instagram',
        'twitter': 'Twitter',
        'youtube_shorts': 'YouTube Shorts',
        'blog_article': 'Blog Article',
        'professional': 'Professional',
        'casual': 'Casual',
        'inspirational': 'Inspirational',
        'educational': 'Educational',
        'entertaining': 'Entertaining',
        'books': 'Books',
        'podcasts': 'Podcasts',
        'videos': 'Videos',
        'research_papers': 'Research Papers',
        'news_articles': 'News Articles',
        'social_media': 'Social Media',
        'personal_experience': 'Personal Experience',
        'industry_trends': 'Industry Trends',
        'customer_feedback': 'Customer Feedback',
        'market_research': 'Market Research',
        'competitor_analysis': 'Competitor Analysis',
        'expert_interviews': 'Expert Interviews',
        'case_studies': 'Case Studies',
        'data_analytics': 'Data Analytics',
        'trending_topics': 'Trending Topics',
        'seasonal_events': 'Seasonal Events',
        'refresh_topics': 'Refresh Topics',
        'generate': 'Generate',
        'regenerate': 'Regenerate',
        'copy_content': 'Copy Content',
        'download_content': 'Download Content',
        'share_content': 'Share Content',
        'content_preview': 'Content Preview',
        'translation_controls': 'Translation Controls',
        'translate_to_english': 'Translate to English',
        'translate_to_chinese': 'Translate to Chinese',
        'original_content': 'Original Content',
        'translated_content': 'Translated Content',
        
        // Dashboard page
        'welcome_back': 'Welcome back',
        'dashboard_overview': 'Dashboard Overview',
        'total_content': 'Total Content',
        'this_month': 'This Month',
        'engagement_rate': 'Engagement Rate',
        'quick_actions': 'Quick Actions',
        'create_new_content': 'Create New Content',
        'view_library': 'View Library',
        'recent_content': 'Recent Content',
        'social_media_performance': 'Social Media Performance',
        'platform_performance': 'Platform Performance',
        'top_performing': 'Top Performing',
        'needs_attention': 'Needs Attention',
        'view_all': 'View All',
        'no_content_yet': 'No content created yet',
        'start_creating_content': 'Start creating content to see your dashboard in action',
        
        // Library page
        'content_library': 'Content Library',
        'filter_content': 'Filter Content',
        'search_content': 'Search content...',
        'all_platforms': 'All Platforms',
        'all_directions': 'All Directions',
        'all_dates': 'All Dates',
        'sort_by': 'Sort by',
        'newest_first': 'Newest First',
        'oldest_first': 'Oldest First',
        'most_engaged': 'Most Engaged',
        'least_engaged': 'Least Engaged',
        'no_content_found': 'No content found',
        'try_adjusting_filters': 'Try adjusting your filters or search terms',
        'content_title': 'Content Title',
        'platform': 'Platform',
        'direction': 'Direction',
        'created_date': 'Created Date',
        'engagement': 'Engagement',
        'actions': 'Actions',
        
        // Settings page
        'settings': 'Settings',
        'profile_settings': 'Profile Settings',
        'content_preferences': 'Content Preferences',
        'social_media_integration': 'Social Media Integration',
        'subscription_management': 'Subscription Management',
        'personal_information': 'Personal Information',
        'name': 'Name',
        'email': 'Email',
        'bio': 'Bio',
        'location': 'Location',
        'website': 'Website',
        'update_profile': 'Update Profile',
        'default_direction': 'Default Direction',
        'preferred_tone': 'Preferred Tone',
        'secondary_directions': 'Secondary Directions',
        'preferred_content_types': 'Preferred Content Types',
        'favorite_sources': 'Favorite Sources',
        'save_preferences': 'Save Preferences',
        'quick_start_preferences': 'Quick Start with Preferences',
        'connect_accounts': 'Connect Accounts',
        'linkedin_account': 'LinkedIn Account',
        'facebook_account': 'Facebook Account',
        'instagram_account': 'Instagram Account',
        'twitter_account': 'Twitter Account',
        'youtube_account': 'YouTube Account',
        'connect': 'Connect',
        'disconnect': 'Disconnect',
        'current_plan': 'Current Plan',
        'plan_details': 'Plan Details',
        'upgrade_plan': 'Upgrade Plan',
        'billing_history': 'Billing History',
        'payment_method': 'Payment Method',
        
        // Auth pages
        'login': 'Login',
        'register': 'Register',
        'password': 'Password',
        'confirm_password': 'Confirm Password',
        'forgot_password': 'Forgot Password?',
        'remember_me': 'Remember Me',
        'login_successful': 'Login successful!',
        'registration_successful': 'Registration successful!',
        'login_failed': 'Login failed',
        'registration_failed': 'Registration failed',
        'logged_out_successfully': 'Logged out successfully',
        'please_log_in': 'Please log in to continue',
        'already_have_account': 'Already have an account?',
        'dont_have_account': 'Don\'t have an account?',
        'sign_in': 'Sign In',
        'sign_up': 'Sign Up',
        
        // Messages
        'content_generated_successfully': 'Content generated successfully!',
        'content_translated_successfully': 'Content translated successfully!',
        'preferences_saved_successfully': 'Preferences saved successfully!',
        'profile_updated_successfully': 'Profile updated successfully!',
        'an_error_occurred': 'An error occurred',
        'translation_failed': 'Translation failed',
        'generation_failed': 'Content generation failed',
        'please_try_again': 'Please try again',
        'content_copied_to_clipboard': 'Content copied to clipboard!',
        'content_downloaded': 'Content downloaded successfully!',
        
        // Footer
        'all_rights_reserved': 'All rights reserved.',
        'privacy_policy': 'Privacy Policy',
        'terms_of_service': 'Terms of Service',
        'support': 'Support'
    },
    zh: {
        // Navigation
        'dashboard': '仪表板',
        'generator': '生成器',
        'library': '内容库',
        'settings': '设置',
        'account': '账户',
        'logout': '退出登录',
        'english': 'English',
        'chinese': '中文',
        
        // Common
        'loading': '加载中...',
        'error': '错误',
        'success': '成功',
        'cancel': '取消',
        'save': '保存',
        'edit': '编辑',
        'delete': '删除',
        'close': '关闭',
        'submit': '提交',
        'back': '返回',
        'next': '下一步',
        'previous': '上一步',
        'continue': '继续',
        'finish': '完成',
        
        // Home page
        'hero_title': '使用',
        'hero_subtitle': 'AI 力量',
        'hero_subtitle_full': 'AI 力量创建引人入胜的内容',
        'hero_description': '使用我们的AI驱动平台生成专业的社交媒体帖子、博客文章等。从18个内容方向中选择，创建与受众产生共鸣的内容。',
        'start_creating': '开始创建',
        'learn_more': '了解更多',
        'quick_start': '快速开始',
        'quick_start_desc': '通过我们直观的内容生成器在几分钟内开始',
        'content_directions': '18个内容方向',
        'platforms': '6个平台',
        'ai_powered': 'AI驱动',
        'regional_adaptation': '区域适配',
        'why_choose': '为什么选择内容创作者专业版？',
        'why_choose_desc': '创建引人入胜内容所需的一切',
        'ai_generation': 'AI驱动生成',
        'ai_generation_desc': '先进的AI模型创建高质量、引人入胜的内容，量身定制您的需求。',
        'regional_adaptation_title': '区域适配',
        'regional_adaptation_desc': '内容自动适应您的地区，具有文化敏感性和本地相关性。',
        'multi_platform': '多平台支持',
        'multi_platform_desc': '为LinkedIn、Facebook、Instagram、Twitter、YouTube和博客创建内容。',
        'content_directions_title': '内容方向',
        'content_directions_desc': '从18个专业内容方向中选择',
        'business_finance': '商业与金融',
        'technology': '技术',
        'health_wellness': '健康与保健',
        'education': '教育',
        'entertainment': '娱乐',
        'travel_tourism': '旅游',
        'food_cooking': '美食与烹饪',
        'fashion_beauty': '时尚与美容',
        'view_all_directions': '查看所有方向',
        'ready_to_create': '准备创建精彩内容？',
        'ready_to_create_desc': '加入数千名已经在使用内容创作者专业版生成引人入胜内容的创作者。',
        'get_started_now': '立即开始',
        
        // Generator page
        'content_generator': '内容生成器',
        'step_1': '第1步',
        'step_2': '第2步',
        'step_3': '第3步',
        'step_4': '第4步',
        'step_5': '第5步',
        'step_3_5': '第3.5步',
        'choose_direction': '选择您的内容方向',
        'choose_direction_desc': '选择您内容的主要焦点',
        'choose_platform': '选择您的平台',
        'choose_platform_desc': '选择您将分享内容的平台',
        'what_inspires': '什么激励着您？',
        'what_inspires_desc': '告诉我们什么驱动着您的内容创作',
        'select_topics': '选择主题',
        'select_topics_desc': '根据您的焦点和来源选择特定主题',
        'generate_content': '生成内容',
        'generate_content_desc': '使用AI创建您的内容',
        'linkedin': '领英',
        'facebook': '脸书',
        'instagram': 'Instagram',
        'twitter': '推特',
        'youtube_shorts': 'YouTube短视频',
        'blog_article': '博客文章',
        'professional': '专业',
        'casual': '随意',
        'inspirational': '励志',
        'educational': '教育',
        'entertaining': '娱乐',
        'books': '书籍',
        'podcasts': '播客',
        'videos': '视频',
        'research_papers': '研究论文',
        'news_articles': '新闻文章',
        'social_media': '社交媒体',
        'personal_experience': '个人经验',
        'industry_trends': '行业趋势',
        'customer_feedback': '客户反馈',
        'market_research': '市场研究',
        'competitor_analysis': '竞争对手分析',
        'expert_interviews': '专家访谈',
        'case_studies': '案例研究',
        'data_analytics': '数据分析',
        'trending_topics': '热门话题',
        'seasonal_events': '季节性活动',
        'refresh_topics': '刷新主题',
        'generate': '生成',
        'regenerate': '重新生成',
        'copy_content': '复制内容',
        'download_content': '下载内容',
        'share_content': '分享内容',
        'content_preview': '内容预览',
        'translation_controls': '翻译控制',
        'translate_to_english': '翻译为英文',
        'translate_to_chinese': '翻译为中文',
        'original_content': '原始内容',
        'translated_content': '翻译内容',
        
        // Dashboard page
        'welcome_back': '欢迎回来',
        'dashboard_overview': '仪表板概览',
        'total_content': '总内容',
        'this_month': '本月',
        'engagement_rate': '参与率',
        'quick_actions': '快速操作',
        'create_new_content': '创建新内容',
        'view_library': '查看内容库',
        'recent_content': '最近内容',
        'social_media_performance': '社交媒体表现',
        'platform_performance': '平台表现',
        'top_performing': '表现最佳',
        'needs_attention': '需要关注',
        'view_all': '查看全部',
        'no_content_yet': '尚未创建内容',
        'start_creating_content': '开始创建内容以查看您的仪表板运行情况',
        
        // Library page
        'content_library': '内容库',
        'filter_content': '筛选内容',
        'search_content': '搜索内容...',
        'all_platforms': '所有平台',
        'all_directions': '所有方向',
        'all_dates': '所有日期',
        'sort_by': '排序方式',
        'newest_first': '最新优先',
        'oldest_first': '最早优先',
        'most_engaged': '参与度最高',
        'least_engaged': '参与度最低',
        'no_content_found': '未找到内容',
        'try_adjusting_filters': '尝试调整您的筛选条件或搜索词',
        'content_title': '内容标题',
        'platform': '平台',
        'direction': '方向',
        'created_date': '创建日期',
        'engagement': '参与度',
        'actions': '操作',
        
        // Settings page
        'settings': '设置',
        'profile_settings': '个人资料设置',
        'content_preferences': '内容偏好',
        'social_media_integration': '社交媒体集成',
        'subscription_management': '订阅管理',
        'personal_information': '个人信息',
        'name': '姓名',
        'email': '邮箱',
        'bio': '个人简介',
        'location': '位置',
        'website': '网站',
        'update_profile': '更新个人资料',
        'default_direction': '默认方向',
        'preferred_tone': '偏好语调',
        'secondary_directions': '次要方向',
        'preferred_content_types': '偏好内容类型',
        'favorite_sources': '收藏来源',
        'save_preferences': '保存偏好',
        'quick_start_preferences': '使用偏好快速开始',
        'connect_accounts': '连接账户',
        'linkedin_account': '领英账户',
        'facebook_account': '脸书账户',
        'instagram_account': 'Instagram账户',
        'twitter_account': '推特账户',
        'youtube_account': 'YouTube账户',
        'connect': '连接',
        'disconnect': '断开连接',
        'current_plan': '当前计划',
        'plan_details': '计划详情',
        'upgrade_plan': '升级计划',
        'billing_history': '账单历史',
        'payment_method': '支付方式',
        
        // Auth pages
        'login': '登录',
        'register': '注册',
        'password': '密码',
        'confirm_password': '确认密码',
        'forgot_password': '忘记密码？',
        'remember_me': '记住我',
        'login_successful': '登录成功！',
        'registration_successful': '注册成功！',
        'login_failed': '登录失败',
        'registration_failed': '注册失败',
        'logged_out_successfully': '退出登录成功',
        'please_log_in': '请登录以继续',
        'already_have_account': '已有账户？',
        'dont_have_account': '没有账户？',
        'sign_in': '登录',
        'sign_up': '注册',
        
        // Messages
        'content_generated_successfully': '内容生成成功！',
        'content_translated_successfully': '内容翻译成功！',
        'preferences_saved_successfully': '偏好保存成功！',
        'profile_updated_successfully': '个人资料更新成功！',
        'an_error_occurred': '发生错误',
        'translation_failed': '翻译失败',
        'generation_failed': '内容生成失败',
        'please_try_again': '请重试',
        'content_copied_to_clipboard': '内容已复制到剪贴板！',
        'content_downloaded': '内容下载成功！',
        
        // Footer
        'all_rights_reserved': '版权所有。',
        'privacy_policy': '隐私政策',
        'terms_of_service': '服务条款',
        'support': '支持'
    }
};

// Initialize application
$(document).ready(function() {
    console.log('Document ready - initializing app...');
    initializeApp();
    setupEventListeners();
    initializeLanguage();
    
    // Show debug panel in development
    if (window.location.hostname === 'localhost' || window.location.hostname.includes('vercel.app')) {
        $('#debug-translation').show();
    }
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
    console.log('Setting up event listeners...');
    
    // Logout button
    $('#logout-btn').on('click', function(e) {
        e.preventDefault();
        logout();
    });
    
    // Language selector
    console.log('Setting up language selector event listeners...');
    $('.language-option').on('click', function(e) {
        console.log('Language option clicked:', $(this).data('lang'));
        e.preventDefault();
        const lang = $(this).data('lang');
        switchLanguage(lang);
    });
    
    // Test if language options exist
    console.log('Language options found:', $('.language-option').length);
    $('.language-option').each(function() {
        console.log('Language option:', $(this).data('lang'), $(this).text());
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
    
    console.log('Event listeners setup completed');
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

// Language and Translation Functions
function initializeLanguage() {
    console.log('Initializing language system...');
    const savedLang = getLocalStorage('preferred_language', 'en');
    console.log('Saved language:', savedLang);
    currentLanguage = savedLang;
    updateLanguageDisplay(savedLang);
    translatePage(savedLang);
    console.log('Language system initialized');
}

function switchLanguage(lang) {
    console.log('Switching language to:', lang);
    // Store language preference
    setLocalStorage('preferred_language', lang);
    currentLanguage = lang;
    
    // Update UI to show current language
    updateLanguageDisplay(lang);
    
    // Translate the entire page
    translatePage(lang);
    
    // Send AJAX request to update server-side language preference
    $.ajax({
        url: `/language/${lang}`,
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        success: function(response) {
            console.log('Language switch response:', response);
            if (response.success) {
                showSuccessMessage(lang === 'en' ? 'Language switched to English' : '语言已切换为中文');
            }
        },
        error: function(xhr, status, error) {
            console.log('Language switch error:', xhr, status, error);
            // Still show success message even if server request fails
            showSuccessMessage(lang === 'en' ? 'Language switched to English' : '语言已切换为中文');
        }
    });
}

function updateLanguageDisplay(lang) {
    console.log('Updating language display for:', lang);
    const languageNames = {
        'en': 'English',
        'zh': '中文'
    };
    
    $('#current-language').text(languageNames[lang] || 'English');
    
    // Update active state in dropdown
    $('.language-option').removeClass('active');
    $(`.language-option[data-lang="${lang}"]`).addClass('active');
}

function translatePage(lang) {
    console.log('Translating page to:', lang);
    const langDict = translations[lang] || translations['en'];
    console.log('Translation dictionary keys:', Object.keys(langDict).length);
    
    // Translate all elements with data-translate attribute
    $('[data-translate]').each(function() {
        const key = $(this).data('translate');
        const translation = langDict[key];
        if (translation) {
            $(this).text(translation);
            console.log(`Translated ${key} to:`, translation);
        } else {
            console.log(`No translation found for key: ${key}`);
        }
    });
    
    // Translate placeholders
    $('[data-translate-placeholder]').each(function() {
        const key = $(this).data('translate-placeholder');
        const translation = langDict[key];
        if (translation) {
            $(this).attr('placeholder', translation);
        }
    });
    
    // Translate titles
    $('[data-translate-title]').each(function() {
        const key = $(this).data('translate-title');
        const translation = langDict[key];
        if (translation) {
            $(this).attr('title', translation);
        }
    });
    
    // Update page title
    const pageTitle = $('title').text();
    if (pageTitle.includes('Content Creator Pro')) {
        $('title').text(pageTitle.replace('Content Creator Pro', lang === 'zh' ? '内容创作者专业版' : 'Content Creator Pro'));
    }
    
    // Update HTML lang attribute
    $('html').attr('lang', lang);
    console.log('Page translation completed');
}

function translateContent(targetLang) {
    const contentPreview = $('#contentPreview');
    const originalContent = contentPreview.data('original-content');
    
    if (!originalContent) {
        showErrorMessage(translations[currentLanguage]['an_error_occurred']);
        return;
    }
    
    // Show loading state
    showLoading(contentPreview, translations[currentLanguage]['loading']);
    
    // Call translation API
    $.ajax({
        url: '/api/translate',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            content: originalContent,
            target_lang: targetLang
        }),
        success: function(response) {
            hideLoading(contentPreview);
            
            if (response.success) {
                // Update content preview
                contentPreview.html(`<pre>${response.translated_content}</pre>`);
                
                // Update language indicators
                updateContentLanguageIndicator(targetLang);
                
                // Update translation button states
                updateTranslationButtonStates(targetLang);
                
                showSuccessMessage(translations[currentLanguage]['content_translated_successfully']);
            } else {
                showErrorMessage(response.error || translations[currentLanguage]['translation_failed']);
            }
        },
        error: function(xhr) {
            hideLoading(contentPreview);
            const error = xhr.responseJSON?.error || translations[currentLanguage]['translation_failed'];
            showErrorMessage(error);
        }
    });
}

function updateContentLanguageIndicator(lang) {
    $('.content-language').hide();
    $(`.content-language.${lang}`).show();
}

function updateTranslationButtonStates(activeLang) {
    // Reset all buttons
    $('#translateEn, #translateZh').removeClass('btn-primary btn-warning').addClass('btn-outline-primary btn-outline-warning');
    
    // Highlight active button
    if (activeLang === 'en') {
        $('#translateEn').removeClass('btn-outline-primary').addClass('btn-primary');
    } else if (activeLang === 'zh') {
        $('#translateZh').removeClass('btn-outline-warning').addClass('btn-warning');
    }
}

function showTranslationControls() {
    $('#translationControls').show();
    updateContentLanguageIndicator('en'); // Default to English
    updateTranslationButtonStates('en');
}

function hideTranslationControls() {
    $('#translationControls').hide();
}

// Initialize language on page load
$(document).ready(function() {
    const savedLang = getLocalStorage('preferred_language', 'en');
    updateLanguageDisplay(savedLang);
});

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