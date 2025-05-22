/**
 * Theme management for DMS
 * Handles dark/light mode switching and persistence
 *
 * IMPORTANT: This is the main theme management file for the application.
 * It should be the only file handling theme switching.
 */

// Configuration
const config = {
    // Storage keys
    storageKeys: {
        theme: 'dms_theme'
    },

    // CSS classes
    classes: {
        darkMode: 'dark-mode',
        lightMode: 'light-mode',
        themeReady: 'theme-system-ready',
        themeTransition: 'theme-transition'
    },

    // Selectors for theme elements
    selectors: {
        darkIcons: '.dark-icon',
        lightIcons: '.light-icon',
        darkTexts: '.dark-mode-text',
        lightTexts: '.light-mode-text',
        themeToggles: '.theme-toggle, #themeToggle, #sidebarThemeToggle'
    },

    // Debug mode
    debug: false
};

/**
 * Helper function for logging theme-related messages
 * @param {string} message - The message to log
 * @param {string} type - The type of log (info, warning, error)
 */
function logTheme(message, type = 'info') {
    if (!config.debug) return;

    const prefix = '[Theme]';
    switch (type) {
        case 'error':
            console.error(`${prefix} ${message}`);
            break;
        case 'warning':
            console.warn(`${prefix} ${message}`);
            break;
        default:
            console.log(`${prefix} ${message}`);
    }
}

/**
 * Updates UI elements based on the current theme
 * @param {boolean} isDarkMode - Whether dark mode is active
 */
function updateThemeUI(isDarkMode) {
    try {
        // Get all theme-related elements
        const darkIcons = document.querySelectorAll(config.selectors.darkIcons);
        const lightIcons = document.querySelectorAll(config.selectors.lightIcons);
        const darkTexts = document.querySelectorAll(config.selectors.darkTexts);
        const lightTexts = document.querySelectorAll(config.selectors.lightTexts);

        // Set display property based on theme
        const updateElements = (elements, display) => {
            elements.forEach(el => { el.style.display = display; });
        };

        if (isDarkMode) {
            // Dark mode UI updates
            updateElements(darkIcons, 'none');
            updateElements(lightIcons, 'block');
            updateElements(darkTexts, 'none');
            updateElements(lightTexts, 'block');
        } else {
            // Light mode UI updates
            updateElements(darkIcons, 'block');
            updateElements(lightIcons, 'none');
            updateElements(darkTexts, 'block');
            updateElements(lightTexts, 'none');
        }
    } catch (error) {
        logTheme(`Error updating theme UI: ${error.message}`, 'error');
    }
}

/**
 * Sets the theme class on HTML and body elements
 * @param {boolean} isDarkMode - Whether to apply dark mode
 */
function setThemeClass(isDarkMode) {
    try {
        // Add transition class for smooth theme changes
        document.documentElement.classList.add(config.classes.themeTransition);

        if (isDarkMode) {
            document.documentElement.classList.add(config.classes.darkMode);
            document.body.classList.add(config.classes.darkMode);
            document.documentElement.classList.remove(config.classes.lightMode);
            document.body.classList.remove(config.classes.lightMode);
        } else {
            document.documentElement.classList.remove(config.classes.darkMode);
            document.body.classList.remove(config.classes.darkMode);
            document.documentElement.classList.add(config.classes.lightMode);
            document.body.classList.add(config.classes.lightMode);
        }

        // Remove transition class after theme change is complete
        setTimeout(() => {
            document.documentElement.classList.remove(config.classes.themeTransition);
        }, 300);
    } catch (error) {
        logTheme(`Error setting theme class: ${error.message}`, 'error');
    }
}

/**
 * Toggle between light and dark themes
 * This is the main function that handles theme toggling
 */
function toggleTheme() {
    logTheme('Theme toggle called');

    try {
        // Check if dark mode is currently active
        const isDarkMode = document.documentElement.classList.contains(config.classes.darkMode);
        const newMode = !isDarkMode;

        // Set the theme in localStorage
        localStorage.setItem(config.storageKeys.theme, newMode ? 'dark' : 'light');

        // Update theme classes and UI
        setThemeClass(newMode);
        updateThemeUI(newMode);

        // Log the theme change
        logTheme(`Switched to ${newMode ? 'dark' : 'light'} mode`);

        // Dispatch a custom event that other scripts can listen for
        document.dispatchEvent(new CustomEvent('themeChanged', {
            detail: { isDarkMode: newMode }
        }));

        // Add ripple effect to theme toggle buttons
        addRippleEffect();
    } catch (error) {
        logTheme(`Error toggling theme: ${error.message}`, 'error');
    }
}

/**
 * Add ripple effect to theme toggle buttons
 */
function addRippleEffect() {
    try {
        const themeToggles = document.querySelectorAll(config.selectors.themeToggles);
        themeToggles.forEach(toggle => {
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            toggle.appendChild(ripple);

            // Set ripple position
            const rect = toggle.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height) * 2;
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${rect.width / 2 - size / 2}px`;
            ripple.style.top = `${rect.height / 2 - size / 2}px`;

            // Remove ripple after animation completes
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    } catch (error) {
        logTheme(`Error adding ripple effect: ${error.message}`, 'error');
    }
}

/**
 * Apply the saved theme or system preference
 */
function applyTheme() {
    try {
        // Make sure document is ready
        if (!document.documentElement || !document.body) {
            logTheme('Document not fully loaded, deferring theme application', 'warning');
            return;
        }

        // Determine which theme to apply
        const savedTheme = localStorage.getItem(config.storageKeys.theme);
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const shouldApplyDark = savedTheme === 'dark' || (savedTheme === null && prefersDark);

        logTheme(`Applying theme: saved=${savedTheme}, prefersDark=${prefersDark}, applying=${shouldApplyDark ? 'dark' : 'light'}`);

        // Update theme classes and UI
        setThemeClass(shouldApplyDark);
        updateThemeUI(shouldApplyDark);

    } catch (error) {
        logTheme(`Error applying theme: ${error.message}`, 'error');
    }
}

/**
 * Initialize theme functionality
 */
function initTheme() {
    logTheme('Initializing theme system');

    try {
        // Apply theme immediately
        applyTheme();

        // Set up all theme toggle buttons
        const themeToggles = document.querySelectorAll(config.selectors.themeToggles);
        logTheme(`Found ${themeToggles.length} theme toggle buttons`);

        themeToggles.forEach((toggle, index) => {
            // Remove any existing event listeners by cloning and replacing
            const newToggle = toggle.cloneNode(true);
            if (toggle.parentNode) {
                toggle.parentNode.replaceChild(newToggle, toggle);

                // Add the event listener to the new element
                newToggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation(); // Prevent event bubbling
                    toggleTheme();
                    return false;
                });

                // Make sure toggle only shows the icon (no text)
                const textNodes = Array.from(newToggle.childNodes)
                    .filter(node => node.nodeType === Node.TEXT_NODE);

                // Remove all text nodes to ensure only icon is displayed
                textNodes.forEach(node => node.remove());

                // Ensure toggle has proper icon classes
                if (!newToggle.querySelector('i.bi')) {
                    // If no Bootstrap icon exists, add one
                    const darkIcon = document.createElement('i');
                    darkIcon.className = 'bi bi-moon-fill dark-icon';

                    const lightIcon = document.createElement('i');
                    lightIcon.className = 'bi bi-sun-fill light-icon';

                    newToggle.appendChild(darkIcon);
                    newToggle.appendChild(lightIcon);

                    // Set initial visibility based on current theme
                    const isDarkMode = document.documentElement.classList.contains(config.classes.darkMode);
                    darkIcon.style.display = isDarkMode ? 'none' : 'block';
                    lightIcon.style.display = isDarkMode ? 'block' : 'none';
                }

                logTheme(`Set up theme toggle button ${index + 1}`);
            }
        });

        // Listen for system preference changes
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        if (mediaQuery.addEventListener) {
            mediaQuery.addEventListener('change', () => {
                logTheme('System preference changed');
                if (localStorage.getItem(config.storageKeys.theme) === 'auto') {
                    applyTheme();
                }
            });
        }

        // Add a class to indicate theme system is ready
        document.documentElement.classList.add(config.classes.themeReady);

    } catch (error) {
        logTheme(`Error initializing theme: ${error.message}`, 'error');
    }
}

// Make toggleTheme available globally
window.toggleTheme = toggleTheme;

// Check if another theme system is already running
if (window.themeSystemInitialized) {
    logTheme('Another theme system is already running. This may cause conflicts.', 'warning');
} else {
    window.themeSystemInitialized = true;
}

// Initialize theme when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    logTheme('DOM content loaded, initializing theme system');
    initTheme();
});

// Apply theme immediately to prevent flash of wrong theme
if (document.readyState === 'loading') {
    logTheme('Document still loading, waiting for DOMContentLoaded');
    document.addEventListener('DOMContentLoaded', applyTheme);
} else {
    logTheme('Document already loaded, applying theme immediately');
    applyTheme();
}

// Log that this script has loaded
logTheme('Theme script loaded');
