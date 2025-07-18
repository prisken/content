// Generator JavaScript - Moved from template to avoid Jinja2 conflicts

// Global variables for generator
let selectedDirection = '';
let selectedContentType = '';
let selectedSourceType = '';
let selectedTone = '';
let selectedNewsSource = '';
let generatedContent = '';
let currentContentLanguage = 'en';

// Content generation functions
function generateLinkedInPost(directionContent, sourceInfo) {
    const source = selectedNewsSource || 'reliable sources';
    const keywords = directionContent.keywords;
    const hashtags = '\n\n#' + keywords[0].replace(/\s+/g, '') + ' #' + keywords[1].replace(/\s+/g, '') + ' #Innovation #ProfessionalDevelopment';
    
    return '🚀 **BREAKING: ' + keywords[0].toUpperCase() + '**\n\n' +
           'According to recent reports from ' + source + ', we\'re witnessing unprecedented ' + keywords[1] + ' in our industry. This isn\'t just another trend—it\'s a fundamental shift.\n\n' +
           '**Key Insights:**\n' +
           '• ' + keywords[2] + ' is accelerating faster than predicted\n' +
           '• Companies embracing ' + keywords[3] + ' are seeing 3x better results\n' +
           '• Early adopters are gaining significant competitive advantages\n\n' +
           '**What This Means for You:**\n' +
           'Whether you\'re a seasoned professional or just starting out, understanding these developments is crucial for career growth.\n\n' +
           '**The Question:**\n' +
           'How are you preparing for these changes in your field?\n' +
           'Share your thoughts below—I\'d love to hear your perspective!' + hashtags + sourceInfo;
}

function generateFacebookPost(directionContent, sourceInfo) {
    const source = selectedNewsSource || 'reliable sources';
    const keywords = directionContent.keywords;
    const hashtags = '\n\n#' + keywords[0].replace(/\s+/g, '') + ' #' + keywords[1].replace(/\s+/g, '') + ' #Community #Discussion';
    
    return 'Hey friends! 👋\n\n' +
           'I just came across some really interesting news from ' + source + ' that I had to share with you all.\n\n' +
           'Apparently, there\'s been a huge breakthrough in ' + keywords[0] + ' that\'s going to change everything we know about ' + keywords[1] + '.\n\n' +
           'I was reading about it this morning and honestly, it blew my mind! 🤯\n\n' +
           'What do you think about these new developments?\n' +
           'Are you excited about the possibilities, or do you have concerns?\n\n' +
           'Drop a comment below and let\'s chat about it!\n' +
           'I\'d love to hear your thoughts' + hashtags + sourceInfo;
}

function generateInstagramPost(directionContent, sourceInfo) {
    const source = selectedNewsSource || 'reliable sources';
    const keywords = directionContent.keywords;
    const hashtags = '\n\n#' + keywords[0].replace(/\s+/g, '') + ' #' + keywords[1].replace(/\s+/g, '') + ' #Inspiration #Innovation #Creativity #Motivation #Growth';
    
    return '✨ **INSPIRATION ALERT** ✨\n\n' +
           'Today\'s dose of motivation comes from some incredible developments in ' + keywords[0] + ' that I discovered through ' + source + '.\n\n' +
           '🌟 **The Story:**\n' +
           'When I first read about these breakthroughs in ' + keywords[1] + ', I couldn\'t help but feel inspired by the endless possibilities.\n\n' +
           'It\'s amazing how ' + keywords[2] + ' continues to evolve and push boundaries.\n\n' +
           '💭 **The Takeaway:**\n' +
           'This reminds us that innovation is everywhere—we just need to keep our eyes open and our minds ready.\n\n' +
           '🔥 **The Question:**\n' +
           'What\'s inspiring you today?\n' +
           'What recent developments have caught your attention and sparked your creativity?\n\n' +
           'Share your thoughts below! Let\'s inspire each other. 💫' + hashtags + sourceInfo;
}

function generateTwitterPost(directionContent, sourceInfo) {
    const source = selectedNewsSource || 'reliable sources';
    const keywords = directionContent.keywords;
    const hashtags = '\n\n#' + keywords[0].replace(/\s+/g, '') + ' #Innovation #Trending';
    
    return '🚨 BREAKING: Major ' + keywords[0] + ' developments reported by ' + source + '!\n\n' +
           'This changes everything in ' + keywords[1] + '. Game-changer for the industry.\n\n' +
           'Thoughts?' + hashtags + sourceInfo;
}

function generateYouTubeShorts(directionContent, sourceInfo) {
    const source = selectedNewsSource || 'reliable sources';
    const keywords = directionContent.keywords;
    
    return '[HOOK: 0-3 seconds]\n' +
           '"Hey there! You won\'t BELIEVE what just happened in ' + keywords[0] + '!"\n\n' +
           '[CONTENT: 3-40 seconds]\n' +
           'According to ' + source + ', we\'re seeing revolutionary changes in ' + keywords[1] + ' that will impact everyone.\n\n' +
           'Here\'s what you need to know and how it affects you.\n\n' +
           '[CALL TO ACTION: 40-45 seconds]\n' +
           'Don\'t forget to like, subscribe, and share your thoughts in the comments below!' + sourceInfo;
}

function generateBlogArticle(directionContent, sourceInfo) {
    const source = selectedNewsSource || 'reliable sources';
    const keywords = directionContent.keywords;
    
    return '# The Future of ' + directionContent.focus.split(',')[0].toUpperCase() + ': A Comprehensive Analysis\n\n' +
           '## Introduction\n' +
           'In today\'s rapidly evolving landscape, understanding the key trends and developments in ' + keywords[0] + ' is crucial for success. Recent reports from ' + source + ' highlight significant developments that are reshaping our industry.\n\n' +
           '## Current State of ' + keywords[1].split(' ')[0] + '\n' +
           'The landscape of ' + keywords[1] + ' has undergone remarkable transformations in recent years. According to industry experts and recent data from ' + source + ', we\'re witnessing unprecedented changes that demand our attention.\n\n' +
           '## Key Developments and Trends\n\n' +
           '### 1. ' + keywords[2].split(' ')[0] + ' Evolution\n' +
           'Recent breakthroughs in ' + keywords[2] + ' have opened new possibilities for professionals and businesses alike. These developments represent a fundamental shift in how we approach industry challenges.\n\n' +
           '### 2. Impact on ' + keywords[3].split(' ')[0] + '\n' +
           'The implications of these changes extend far beyond immediate applications. Companies that embrace ' + keywords[3] + ' are positioning themselves for long-term success in an increasingly competitive market.\n\n' +
           '### 3. Future Outlook for ' + keywords[4].split(' ')[0] + '\n' +
           'Looking ahead, the trajectory of ' + keywords[4] + ' suggests continued innovation and growth. Early adopters stand to gain significant advantages in this evolving landscape.\n\n' +
           '## What This Means for Professionals\n\n' +
           '### For Industry Leaders\n' +
           'Understanding these developments is essential for strategic decision-making and maintaining competitive advantages.\n\n' +
           '### For Emerging Professionals\n' +
           'These changes present unique opportunities for career growth and skill development in high-demand areas.\n\n' +
           '### For Businesses\n' +
           'Adapting to these trends requires proactive planning and investment in relevant technologies and methodologies.\n\n' +
           '## Actionable Insights\n\n' +
           '1. **Stay Informed**: Regularly monitor developments in ' + keywords[0] + ' through reliable sources like ' + source + '\n' +
           '2. **Embrace Change**: Be open to new approaches and methodologies in your field\n' +
           '3. **Invest in Learning**: Continuously develop skills related to emerging trends\n' +
           '4. **Network Actively**: Connect with professionals who are leading innovation in these areas\n\n' +
           '## Conclusion\n' +
           'As we navigate this dynamic landscape, staying informed and adaptable is more important than ever. The developments in ' + keywords[0] + ' represent both challenges and opportunities for those willing to embrace change and innovation.\n\n' +
           'By understanding these trends and taking proactive steps to adapt, professionals and businesses can position themselves for success in an increasingly competitive and innovative environment.' + sourceInfo;
}

function displayContent(content) {
    generatedContent = content;
    
    // Add character count and validation based on content categories
    const charCount = content.length;
    const platformLimits = {
        'linkedin': 1300,
        'facebook': 63206,
        'instagram': 2200,
        'twitter': 280,
        'youtube_shorts': null, // No character limit for scripts
        'blog': null // No character limit for blog articles
    };
    
    const limit = platformLimits[selectedContentType];
    let validationMessage = '';
    let validationClass = '';
    
    if (limit) {
        if (charCount > limit) {
            validationMessage = '⚠️ Content exceeds ' + selectedContentType + ' limit (' + charCount + '/' + limit + ' characters)';
            validationClass = 'text-danger';
        } else if (charCount > limit * 0.9) {
            validationMessage = '⚠️ Content approaching ' + selectedContentType + ' limit (' + charCount + '/' + limit + ' characters)';
            validationClass = 'text-warning';
        } else {
            validationMessage = '✅ Content within ' + selectedContentType + ' limits (' + charCount + '/' + limit + ' characters)';
            validationClass = 'text-success';
        }
    } else {
        validationMessage = '📝 Content length: ' + charCount + ' characters';
        validationClass = 'text-info';
    }
    
    const displayContent = '<div class="mb-3">' +
        '<div class="d-flex justify-content-between align-items-center mb-2">' +
        '<small class="' + validationClass + '">' + validationMessage + '</small>' +
        '<small class="text-muted">' + getPlatformSpecs() + '</small>' +
        '</div>' +
        '<pre class="mb-0">' + content + '</pre>' +
        '</div>';
    
    $('#contentPreview').html(displayContent);
    
    // Store original content for translation
    $('#contentPreview').data('original-content', content);
    
    // Show content actions and translation controls
    $('#contentActions').show();
    showTranslationControls();
}

function getPlatformSpecs() {
    const specs = {
        'linkedin': 'LinkedIn: 1,300 chars max, Professional tone, 1-2 hashtags',
        'facebook': 'Facebook: 63,206 chars max, Conversational tone, 3-5 hashtags',
        'instagram': 'Instagram: 2,200 chars max, Visual tone, 5-10 hashtags',
        'twitter': 'Twitter: 280 chars max, Concise tone, 1-2 hashtags',
        'youtube_shorts': 'YouTube Shorts: 30-45 seconds, Engaging tone',
        'blog': 'Blog: 1,500-2,500 words, Informative tone, SEO-optimized'
    };
    
    return specs[selectedContentType] || '';
}

function showTranslationControls() {
    $('#translationControls').show();
    // Set initial state to English
    currentContentLanguage = 'en';
    updateTranslationButtons();
}

function translateContent(targetLang) {
    const originalContent = $('#contentPreview').data('original-content');
    const currentLang = currentContentLanguage || 'en';
    
    if (targetLang === currentLang) {
        return; // Already in the target language
    }
    
    // Show loading state
    const button = targetLang === 'en' ? $('#translateEn') : $('#translateZh');
    const originalText = button.html();
    button.prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-1"></i> Translating...');
    
    // Call translation API
    fetch('/api/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            content: originalContent,
            target_lang: targetLang,
            source_lang: currentLang
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update content display
            $('#contentPreview').html('<pre class="mb-0">' + data.translated_content + '</pre>');
            currentContentLanguage = targetLang;
            updateTranslationButtons();
            
            // Update generated content for copy/download
            generatedContent = data.translated_content;
        } else {
            // Fallback to mock translation for demo
            const mockTranslation = getMockTranslation(originalContent, targetLang);
            $('#contentPreview').html('<pre class="mb-0">' + mockTranslation + '</pre>');
            currentContentLanguage = targetLang;
            updateTranslationButtons();
            generatedContent = mockTranslation;
        }
    })
    .catch(error => {
        console.error('Translation error:', error);
        // Fallback to mock translation
        const mockTranslation = getMockTranslation(originalContent, targetLang);
        $('#contentPreview').html('<pre class="mb-0">' + mockTranslation + '</pre>');
        currentContentLanguage = targetLang;
        updateTranslationButtons();
        generatedContent = mockTranslation;
    })
    .finally(() => {
        button.prop('disabled', false).html(originalText);
    });
}

function getMockTranslation(content, targetLang) {
    if (targetLang === 'zh') {
        // Enhanced Chinese translation for new content structure
        return content
            // LinkedIn translations
            .replace(/🚀 \*\*BREAKING: /g, '🚀 **突发：')
            .replace(/According to recent reports from /g, '根据来自')
            .replace(/we're witnessing unprecedented /g, '我们正在见证前所未有的')
            .replace(/This isn't just another trend—it's a fundamental shift/g, '这不仅仅是另一个趋势——这是一个根本性的转变')
            .replace(/Key Insights:/g, '关键见解：')
            .replace(/is accelerating faster than predicted/g, '比预期加速得更快')
            .replace(/Companies embracing /g, '采用')
            .replace(/are seeing 3x better results/g, '的公司看到了3倍更好的结果')
            .replace(/Early adopters are gaining significant competitive advantages/g, '早期采用者正在获得显著的竞争优势')
            .replace(/What This Means for You:/g, '这对您意味着什么：')
            .replace(/Whether you're a seasoned professional or just starting out/g, '无论您是经验丰富的专业人士还是刚刚起步')
            .replace(/understanding these developments is crucial for career growth/g, '了解这些发展对职业发展至关重要')
            .replace(/The Question:/g, '问题：')
            .replace(/How are you preparing for these changes in your field?/g, '您如何为所在领域的这些变化做准备？')
            .replace(/Share your thoughts below—I'd love to hear your perspective/g, '在下面分享您的想法——我很想听听您的观点')
            
            // Facebook translations
            .replace(/Hey friends! 👋/g, '朋友们好！👋')
            .replace(/I just came across some really interesting news/g, '我刚刚看到一些非常有趣的新闻')
            .replace(/that I had to share with you all/g, '必须与大家分享')
            .replace(/Apparently, there's been a huge breakthrough in /g, '显然，在')
            .replace(/that's going to change everything we know about /g, '方面有了重大突破，这将改变我们对')
            .replace(/I was reading about it this morning and honestly, it blew my mind! 🤯/g, '的一切认知。我今早读到这个消息，说实话，让我震惊了！🤯')
            .replace(/What do you think about these new developments?/g, '您对这些新发展有什么看法？')
            .replace(/Are you excited about the possibilities, or do you have concerns?/g, '您对可能性感到兴奋，还是有担忧？')
            .replace(/Drop a comment below and let's chat about it!/g, '在下面留言，让我们聊聊吧！')
            .replace(/I'd love to hear your thoughts/g, '我很想听听您的想法')
            
            // Instagram translations
            .replace(/✨ \*\*INSPIRATION ALERT\*\* ✨/g, '✨ **灵感提醒** ✨')
            .replace(/Today's dose of motivation comes from/g, '今天的动力来自于')
            .replace(/incredible developments in /g, '令人难以置信的发展')
            .replace(/that I discovered through /g, '我通过')
            .replace(/🌟 \*\*The Story:\*\*/g, '🌟 **故事：**')
            .replace(/When I first read about these breakthroughs in /g, '当我第一次读到这些突破时')
            .replace(/I couldn't help but feel inspired by the endless possibilities/g, '我不禁被无限的可能性所激励')
            .replace(/It's amazing how /g, '令人惊讶的是')
            .replace(/continues to evolve and push boundaries/g, '如何继续发展并突破界限')
            .replace(/💭 \*\*The Takeaway:\*\*/g, '💭 **要点：**')
            .replace(/This reminds us that innovation is everywhere/g, '这提醒我们创新无处不在')
            .replace(/we just need to keep our eyes open and our minds ready/g, '我们只需要保持眼睛开放，思维准备就绪')
            .replace(/🔥 \*\*The Question:\*\*/g, '🔥 **问题：**')
            .replace(/What's inspiring you today?/g, '今天什么激励着您？')
            .replace(/What recent developments have caught your attention/g, '最近哪些发展引起了您的注意')
            .replace(/and sparked your creativity?/g, '并激发了您的创造力？')
            .replace(/Share your thoughts below! Let's inspire each other. 💫/g, '在下面分享您的想法！让我们互相激励。💫')
            
            // Twitter translations
            .replace(/🚨 BREAKING: Major /g, '🚨 突发：重大')
            .replace(/developments reported by /g, '发展由')
            .replace(/This changes everything in /g, '这改变了一切')
            .replace(/Game-changer for the industry/g, '行业的游戏规则改变者')
            .replace(/Thoughts?/g, '想法？')
            
            // YouTube translations
            .replace(/Hey there! You won't BELIEVE what just happened in /g, '大家好！您不会相信刚刚在')
            .replace(/According to /g, '根据')
            .replace(/we're seeing revolutionary changes in /g, '我们正在看到革命性的变化')
            .replace(/that will impact everyone/g, '这将影响每个人')
            .replace(/Here's what you need to know and how it affects you/g, '以下是您需要了解的内容以及它如何影响您')
            .replace(/Don't forget to like, subscribe, and share your thoughts in the comments below!/g, '别忘了点赞、订阅，并在下面的评论中分享您的想法！')
            
            // Blog translations
            .replace(/# The Future of /g, '# 的未来：')
            .replace(/: A Comprehensive Analysis/g, '：综合分析')
            .replace(/## Introduction/g, '## 引言')
            .replace(/In today's rapidly evolving landscape/g, '在当今快速发展的环境中')
            .replace(/understanding the key trends and developments in /g, '了解关键趋势和发展')
            .replace(/is crucial for success/g, '对成功至关重要')
            .replace(/Recent reports from /g, '最近的报告来自')
            .replace(/highlight significant developments that are reshaping our industry/g, '强调了正在重塑我们行业的重要发展')
            .replace(/## Current State of /g, '## 当前状态')
            .replace(/The landscape of /g, '的格局')
            .replace(/has undergone remarkable transformations in recent years/g, '近年来经历了显著的转变')
            .replace(/According to industry experts and recent data from /g, '根据行业专家和来自')
            .replace(/we're witnessing unprecedented changes that demand our attention/g, '的最近数据，我们正在见证需要关注的前所未有的变化')
            .replace(/## Key Developments and Trends/g, '## 关键发展和趋势')
            .replace(/ Evolution/g, ' 演变')
            .replace(/Recent breakthroughs in /g, '最近的突破')
            .replace(/have opened new possibilities for professionals and businesses alike/g, '为专业人士和企业都开辟了新的可能性')
            .replace(/These developments represent a fundamental shift in how we approach industry challenges/g, '这些发展代表了我们在应对行业挑战方式上的根本性转变')
            .replace(/## What This Means for Professionals/g, '## 这对专业人士意味着什么')
            .replace(/### For Industry Leaders/g, '### 对于行业领导者')
            .replace(/Understanding these developments is essential for strategic decision-making and maintaining competitive advantages/g, '了解这些发展对战略决策和保持竞争优势至关重要')
            .replace(/### For Emerging Professionals/g, '### 对于新兴专业人士')
            .replace(/These changes present unique opportunities for career growth and skill development in high-demand areas/g, '这些变化为高需求领域的职业发展和技能发展提供了独特的机会')
            .replace(/### For Businesses/g, '### 对于企业')
            .replace(/Adapting to these trends requires proactive planning and investment in relevant technologies and methodologies/g, '适应这些趋势需要对相关技术和方法进行主动规划和投资')
            .replace(/## Actionable Insights/g, '## 可操作的见解')
            .replace(/## Conclusion/g, '## 结论')
            .replace(/As we navigate this dynamic landscape/g, '当我们在这个动态环境中导航时')
            .replace(/staying informed and adaptable is more important than ever/g, '保持信息灵通和适应能力比以往任何时候都更重要')
            .replace(/The developments in /g, '的发展')
            .replace(/represent both challenges and opportunities for those willing to embrace change and innovation/g, '为那些愿意拥抱变化和创新的人带来了挑战和机遇')
            .replace(/By understanding these trends and taking proactive steps to adapt/g, '通过了解这些趋势并采取主动步骤来适应')
            .replace(/professionals and businesses can position themselves for success in an increasingly competitive and innovative environment/g, '专业人士和企业可以在日益竞争和创新的环境中为成功定位');
    }
    
    return content; // Return original content for English
}

function updateTranslationButtons() {
    $('#translateEn').removeClass('btn-primary btn-warning').addClass('btn-outline-primary btn-outline-warning');
    $('#translateZh').removeClass('btn-primary btn-warning').addClass('btn-outline-primary btn-outline-warning');
    
    if (currentContentLanguage === 'en') {
        $('#translateEn').removeClass('btn-outline-primary').addClass('btn-primary');
    } else if (currentContentLanguage === 'zh') {
        $('#translateZh').removeClass('btn-outline-warning').addClass('btn-warning');
    }
}

// Export functions for use in template
window.GeneratorApp = {
    generateLinkedInPost,
    generateFacebookPost,
    generateInstagramPost,
    generateTwitterPost,
    generateYouTubeShorts,
    generateBlogArticle,
    displayContent,
    translateContent,
    updateTranslationButtons,
    showTranslationControls
};

// Step navigation functions
let currentStep = 1;
const totalSteps = 4;

function nextStep() {
    if (currentStep < totalSteps) {
        $('#step' + currentStep).hide();
        currentStep++;
        $('#step' + currentStep).show();
        updateStepButtons();
    }
}

function prevStep() {
    if (currentStep > 1) {
        $('#step' + currentStep).hide();
        currentStep--;
        $('#step' + (currentStep)).show();
        updateStepButtons();
    }
}

function updateStepButtons() {
    // Update step indicators
    $('.step-indicator').removeClass('active');
    $('.step-indicator[data-step="' + currentStep + '"]').addClass('active');
    
    // Update navigation buttons
    if (currentStep === 1) {
        $('.btn-prev').hide();
    } else {
        $('.btn-prev').show();
    }
    
    if (currentStep === totalSteps) {
        $('.btn-next').hide();
        $('#generateBtn').show();
    } else {
        $('.btn-next').show();
        $('#generateBtn').hide();
    }
}

// Content generation function
function generateContent() {
    if (!selectedDirection || !selectedContentType || !selectedTone) {
        alert('Please complete all steps before generating content.');
        return;
    }
    
    // Show loading state
    $('#generateBtn').prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-1"></i> Generating...');
    
    // Simulate content generation (replace with actual API call)
    setTimeout(() => {
        const directionContent = {
            focus: selectedDirection,
            keywords: ['Innovation', 'Technology', 'Digital Transformation', 'AI', 'Future']
        };
        
        let sourceInfo = '';
        if (selectedNewsSource) {
            sourceInfo = '\n\nSource: ' + selectedNewsSource;
        }
        
        let content = '';
        switch (selectedContentType) {
            case 'linkedin':
                content = generateLinkedInPost(directionContent, sourceInfo);
                break;
            case 'facebook':
                content = generateFacebookPost(directionContent, sourceInfo);
                break;
            case 'instagram':
                content = generateInstagramPost(directionContent, sourceInfo);
                break;
            case 'twitter':
                content = generateTwitterPost(directionContent, sourceInfo);
                break;
            case 'youtube_shorts':
                content = generateYouTubeShorts(directionContent, sourceInfo);
                break;
            case 'blog':
                content = generateBlogArticle(directionContent, sourceInfo);
                break;
            default:
                content = 'Content generation failed. Please try again.';
        }
        
        displayContent(content);
        
        // Reset button
        $('#generateBtn').prop('disabled', false).html('<i class="fas fa-magic me-1"></i> Generate Content');
    }, 2000);
}

// Content action functions
function saveContent() {
    if (generatedContent) {
        // TODO: Implement save to library functionality
        alert('Content saved to library!');
    } else {
        alert('No content to save. Please generate content first.');
    }
}

function downloadContent() {
    if (generatedContent) {
        const blob = new Blob([generatedContent], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'generated-content.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } else {
        alert('No content to download. Please generate content first.');
    }
}

function copyContent() {
    if (generatedContent) {
        navigator.clipboard.writeText(generatedContent).then(() => {
            alert('Content copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy content: ', err);
            alert('Failed to copy content. Please try again.');
        });
    } else {
        alert('No content to copy. Please generate content first.');
    }
}

// Quick start with preferences
function quickStartWithPreferences() {
    // TODO: Implement quick start with saved preferences
    alert('Quick start with preferences feature coming soon!');
}

// News sources update
function updateNewsSources() {
    const region = $('#newsRegion').val();
    if (region) {
        $('#newsSourcesContainer').show();
        
        // Mock news sources based on region
        const newsSources = {
            'north_america': ['CNN', 'BBC News', 'Reuters', 'Associated Press', 'The New York Times'],
            'europe': ['BBC News', 'Reuters', 'Associated Press', 'Euronews', 'Deutsche Welle'],
            'asia_pacific': ['BBC News', 'Reuters', 'Associated Press', 'Al Jazeera', 'South China Morning Post'],
            'latin_america': ['BBC News', 'Reuters', 'Associated Press', 'Al Jazeera', 'El País'],
            'middle_east': ['BBC News', 'Reuters', 'Associated Press', 'Al Jazeera', 'The Jerusalem Post'],
            'africa': ['BBC News', 'Reuters', 'Associated Press', 'Al Jazeera', 'AllAfrica']
        };
        
        const sources = newsSources[region] || [];
        let html = '';
        
        sources.forEach(source => {
            html += '<div class="col-md-6 mb-2">' +
                   '<div class="form-check">' +
                   '<input class="form-check-input" type="radio" name="newsSource" id="' + source.replace(/\s+/g, '') + '" value="' + source + '">' +
                   '<label class="form-check-label" for="' + source.replace(/\s+/g, '') + '">' + source + '</label>' +
                   '</div>' +
                   '</div>';
        });
        
        $('#newsSourcesGrid').html(html);
        
        // Enable next button
        $('#step3_5Next').prop('disabled', false);
    } else {
        $('#newsSourcesContainer').hide();
        $('#step3_5Next').prop('disabled', true);
    }
}

// Initialize generator on page load
$(document).ready(function() {
    console.log('Generator page loaded, initializing...');
    
    // Set up event listeners for direction cards
    $('.direction-card').on('click', function() {
        $('.direction-card').removeClass('selected');
        $(this).addClass('selected');
        
        const direction = $(this).data('direction');
        const contentType = $(this).data('content-type');
        const sourceType = $(this).data('source-type');
        const tone = $(this).data('tone');
        
        if (direction) selectedDirection = direction;
        if (contentType) selectedContentType = contentType;
        if (sourceType) selectedSourceType = sourceType;
        if (tone) selectedTone = tone;
        
        // Enable next button for current step
        const currentStepBtn = $('#step' + currentStep + 'Next');
        if (currentStepBtn.length) {
            currentStepBtn.prop('disabled', false);
        }
    });
    
    // Set up news source selection
    $(document).on('change', 'input[name="newsSource"]', function() {
        selectedNewsSource = $(this).val();
        $('#step3_5Next').prop('disabled', false);
    });
    
    console.log('Generator initialization completed');
}); 