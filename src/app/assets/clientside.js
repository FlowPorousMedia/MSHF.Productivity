// assets/clientside.js

document.addEventListener('DOMContentLoaded', function() {
    initializeSidebarResize();
});

function initializeSidebarResize() {
    const sidebar = document.getElementById('sidebar');
    const resizeHandle = document.getElementById('sidebar-resize-handle');
    
    if (!sidebar || !resizeHandle) {
        setTimeout(initializeSidebarResize, 100);
        return;
    }
    
    let isResizing = false;
    let startX = 0;
    let startWidth = 0;
    
    function handleMove(e) {
        if (!isResizing) return;
        
        const clientX = e.clientX || (e.touches && e.touches[0].clientX);
        if (!clientX) return;
        
        // Вычисляем разницу от начальной точки
        const widthDiff = clientX - startX;
        const newWidth = startWidth + widthDiff;
        
        const minWidth = 260;
        const maxWidth = window.innerWidth * 0.75;
        
        if (newWidth >= minWidth && newWidth <= maxWidth) {
            sidebar.style.width = newWidth + 'px';
        }
    }
    
    function stopResize() {
        isResizing = false;
        resizeHandle.style.backgroundColor = 'rgba(0,0,0,0.1)';
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
        
        document.removeEventListener('mousemove', handleMove);
        document.removeEventListener('touchmove', handleMove);
        document.removeEventListener('mouseup', stopResize);
        document.removeEventListener('touchend', stopResize);
    }
    
    function startResize(e) {
        isResizing = true;
        startX = e.clientX || (e.touches && e.touches[0].clientX);
        startWidth = parseInt(document.defaultView.getComputedStyle(sidebar).width, 10);
        
        resizeHandle.style.backgroundColor = 'rgba(0,0,0,0.3)';
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
        
        document.addEventListener('mousemove', handleMove);
        document.addEventListener('touchmove', handleMove);
        document.addEventListener('mouseup', stopResize);
        document.addEventListener('touchend', stopResize);
        
        e.preventDefault();
    }
    
    resizeHandle.addEventListener('mousedown', startResize);
    resizeHandle.addEventListener('touchstart', startResize);
}