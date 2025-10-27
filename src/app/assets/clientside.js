// assets/clientside.js

if (!window.dash_clientside) {
    window.dash_clientside = {};
}

// Initialize resize functionality when the page loads
document.addEventListener('DOMContentLoaded', function () {
    initializeSidebarResize();
});

function initializeSidebarResize() {
    const sidebar = document.getElementById('sidebar');
    const resizeHandle = document.getElementById('sidebar-resize-handle');

    if (!sidebar || !resizeHandle) {
        // Retry after a short delay if elements aren't ready yet
        setTimeout(initializeSidebarResize, 100);
        return;
    }

    let isResizing = false;
    let startX = 0;
    let startWidth = 0;

    // Mouse down event - start resizing
    resizeHandle.addEventListener('mousedown', function (e) {
        isResizing = true;
        startX = e.clientX;
        startWidth = parseInt(document.defaultView.getComputedStyle(sidebar).width, 10);
        resizeHandle.style.backgroundColor = 'rgba(0,0,0,0.3)';
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
        e.preventDefault();
    });

    // Mouse move event - handle resizing
    document.addEventListener('mousemove', function (e) {
        if (!isResizing) return;

        const widthDiff = e.clientX - startX;
        const newWidth = startWidth + widthDiff;
        const minWidth = 260;
        const maxWidth = window.innerWidth * 0.75;

        if (newWidth >= minWidth && newWidth <= maxWidth) {
            sidebar.style.width = newWidth + 'px';
        }
    });

    // Mouse up event - stop resizing
    document.addEventListener('mouseup', function () {
        if (isResizing) {
            isResizing = false;
            resizeHandle.style.backgroundColor = 'rgba(0,0,0,0.1)';
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        }
    });

    // Touch events for mobile support
    resizeHandle.addEventListener('touchstart', function (e) {
        isResizing = true;
        const touch = e.touches[0];
        startX = touch.clientX;
        startWidth = parseInt(document.defaultView.getComputedStyle(sidebar).width, 10);
        resizeHandle.style.backgroundColor = 'rgba(0,0,0,0.3)';
        document.body.style.userSelect = 'none';
        e.preventDefault();
    });

    document.addEventListener('touchmove', function (e) {
        if (!isResizing) return;

        const touch = e.touches[0];
        const widthDiff = touch.clientX - startX;
        const newWidth = startWidth + widthDiff;
        const minWidth = 260;
        const maxWidth = window.innerWidth * 0.75;

        if (newWidth >= minWidth && newWidth <= maxWidth) {
            sidebar.style.width = newWidth + 'px';
        }

        e.preventDefault();
    });

    document.addEventListener('touchend', function () {
        if (isResizing) {
            isResizing = false;
            resizeHandle.style.backgroundColor = 'rgba(0,0,0,0.1)';
            document.body.style.userSelect = '';
        }
    });
}

// Prevent text selection while resizing
document.addEventListener('selectstart', function (e) {
    if (document.body.style.userSelect === 'none') {
        e.preventDefault();
    }
});

// Re-initialize when dynamic content loads
if (window.dash_clientside && window.dash_clientside.callbacks) {
    const originalCallbackHandler = window.dash_clientside.callbacks;
    window.dash_clientside.callbacks = function () {
        const result = originalCallbackHandler.apply(this, arguments);
        // Re-initialize resize after callbacks
        setTimeout(initializeSidebarResize, 50);
        return result;
    };
}